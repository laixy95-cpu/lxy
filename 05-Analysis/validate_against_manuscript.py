"""
Compare pipeline output against the values printed in the manuscript.

Run this the moment the real inputs are available. It answers the question the
audit cannot answer without data: do the manuscript's numbers survive when the
Table 3 counterfactuals are actually implemented?

    python3 validate_against_manuscript.py --input-dir <dir with the six xlsx>

Every target below is transcribed from the submitted manuscript. TOL is deliberately
loose (0.002) because printed values are rounded to three decimals.
"""
from __future__ import annotations

import argparse
import sys

import numpy as np
import pandas as pd

from asean6_counterfactual import (
    STAGE_HORIZONS, backtest, decompose, dimension_gaps, gap_to_rmse,
    indicator_gaps, load_panel, placebo, placebo_test, regional, robustness,
    scaling_params,
)

TOL = 0.002
DIM = {"EnergyServiceSecurity": "Energy-service security",
       "MacroPricePressure": "Macro-price stability",
       "LowCarbonContinuity": "Low-carbon continuity"}

# Table 4 - regional gaps and gap-to-RMSE ratios
T4 = {  # (dimension, stage): (gap, ratio)
    ("EnergyServiceSecurity", "COVID"): (-0.077, 0.65),
    ("EnergyServiceSecurity", "Compound"): (-0.103, 0.54),
    ("MacroPricePressure", "COVID"): (+0.120, 0.14),
    ("MacroPricePressure", "Compound"): (-0.767, 0.86),
    ("LowCarbonContinuity", "COVID"): (+0.035, 0.14),
    ("LowCarbonContinuity", "Compound"): (+0.102, 0.23),
}
# Section 4.2 - country gaps, compound stage
T42 = {
    "MacroPricePressure": dict(Singapore=-1.816, Philippines=-1.150, Thailand=-1.117,
                               Malaysia=-0.342, Vietnam=-0.194, Indonesia=+0.016),
    "EnergyServiceSecurity": dict(Philippines=-0.445, Vietnam=-0.232, Singapore=-0.109,
                                  Thailand=-0.018, Malaysia=-0.002, Indonesia=+0.185),
    "LowCarbonContinuity": dict(Vietnam=+0.851, Singapore=+0.246, Indonesia=+0.145,
                                Philippines=+0.107, Malaysia=-0.507, Thailand=-0.230),
}
# Table 5 - indicator contributions to the regional low-carbon gap
T5 = {"RenTFEC": (+0.022, +0.039), "CO2IntElec": (+0.007, +0.049),
      "EnergyIntensity": (-0.030, -0.027), "RenCap": (+0.025, +0.003),
      "RenElec": (+0.011, +0.038)}
# Table 9 - rolling-origin RMSE by horizon
T9 = {"EnergyServiceSecurity": {1: 0.099, 2: 0.137, 3: 0.173, 4: 0.213},
      "MacroPricePressure": {1: 0.860, 2: 0.802, 3: 0.812, 4: 0.970},
      "LowCarbonContinuity": {1: 0.208, 2: 0.281, 3: 0.348, 4: 0.554}}
# Table 8 - regional low-carbon gap, compound stage, under each variant
T8 = {"Pre-crisis min-max scaling": +0.030, "Five-year training window": +0.170,
      "2017-2019 mean baseline": +0.296, "2019 level baseline": +0.315}
LOCO_RANGE, LOIO_RANGE = (-0.048, +0.224), (+0.066, +0.162)


class Report:
    def __init__(self):
        self.rows, self.fails = [], 0

    def check(self, label, got, want, tol=TOL):
        ok = got is not None and not np.isnan(got) and abs(got - want) <= tol
        self.fails += (not ok)
        self.rows.append((("PASS" if ok else "FAIL"), label,
                          "n/a" if got is None or np.isnan(got) else f"{got:+.4f}",
                          f"{want:+.4f}",
                          "" if ok else f"{got-want:+.4f}" if got is not None else ""))
        return ok

    def show(self, title):
        print(f"\n=== {title} ===")
        w = max(len(r[1]) for r in self.rows) if self.rows else 10
        for s, lab, got, want, d in self.rows:
            print(f"  {s:4}  {lab:<{w}}  computed={got:>9}  printed={want:>9}  {d}")
        self.rows = []


def main(input_dir: str) -> int:
    panel = load_panel(input_dir)
    params = scaling_params(panel)
    gaps, diag = indicator_gaps(panel, params)
    dim_long, _ = dimension_gaps(gaps)
    reg = regional(dim_long, intervals=True)
    bt = backtest(panel, params)
    ratios = gap_to_rmse(reg, bt)
    contrib = decompose(gaps)
    rob, extras = robustness(panel)
    r = Report()

    for (d, s), (gap, ratio) in T4.items():
        row = reg[(reg.dimension == d) & (reg.stage == s)]
        r.check(f"{DIM[d]} / {s} gap",
                float(row.regional_gap.iloc[0]) if len(row) else None, gap)
        rr = ratios[(ratios.dimension == d) & (ratios.stage == s)]
        r.check(f"{DIM[d]} / {s} gap-to-RMSE",
                float(rr.ratio.iloc[0]) if len(rr) else None, ratio, tol=0.006)
    r.show("Table 4 - regional gaps and ratios")

    for d, per in T42.items():
        for c, want in per.items():
            row = dim_long[(dim_long.dimension == d) & (dim_long.stage == "Compound")
                           & (dim_long.country == c)]
            r.check(f"{DIM[d]} / {c}",
                    float(row.dimension_gap.iloc[0]) if len(row) else None, want)
    r.show("Section 4.2 - country gaps, compound stage")

    for ind, (cv, cp) in T5.items():
        for stage, want in (("COVID", cv), ("Compound", cp)):
            row = contrib[(contrib.indicator == ind) & (contrib.stage == stage)]
            r.check(f"{ind} / {stage}",
                    float(row.contribution.mean()) if len(row) else None, want)
    r.show("Table 5 - indicator contributions")

    for d, per in T9.items():
        for h, want in per.items():
            row = bt[(bt.dimension == d) & (bt.horizon == h)]
            r.check(f"{DIM[d]} h={h} RMSE",
                    float(row.rmse.iloc[0]) if len(row) else None, want)
    r.show("Table 9 - rolling-origin RMSE")

    for name, want in T8.items():
        row = rob[rob.check.str.startswith(name.split(" (")[0])]
        r.check(name, float(row.regional_lowcarbon_compound.iloc[0]) if len(row) else None, want)
    lo, hi = extras["leave_one_country_out_range"]
    r.check("LOCO min", lo, LOCO_RANGE[0]); r.check("LOCO max", hi, LOCO_RANGE[1])
    lo, hi = extras["leave_one_indicator_out_range"]
    r.check("LOIO min", lo, LOIO_RANGE[0]); r.check("LOIO max", hi, LOIO_RANGE[1])
    r.show("Table 8 - robustness variants")

    print("\n=== Claims that cannot be checked arithmetically ===")
    ez = reg[reg.excludes_zero] if "excludes_zero" in reg else pd.DataFrame()
    print(f"  Regional estimates whose cross-country interval excludes zero: {len(ez)}")
    for _, x in ez.iterrows():
        print(f"    - {DIM[x.dimension]} / {x.stage}: {x.regional_gap:+.3f} "
              f"[{x.ci_low:+.3f}, {x.ci_high:+.3f}]")
    print("  Audit A1: the manuscript claims this set has exactly one member")
    print("  (macro-price / compound). If more appear above, A1 is confirmed and the")
    print("  abstract, section 4.1, section 5 and section 6 all need restating.")

    ul = rob[rob.check.str.startswith("Uniform linear")]
    if len(ul):
        print(f"\n  Uniform linear form (the check Table 8 omits, audit A4):")
        print(f"    regional low-carbon / compound = "
              f"{float(ul.regional_lowcarbon_compound.iloc[0]):+.3f} "
              f"vs main {extras['main_lowcarbon_compound']:+.3f}")
        print(f"    Pearson r = {float(ul.pearson.iloc[0]):.3f}, "
              f"sign agreement = {float(ul.sign_agreement.iloc[0]):.1%}")
    bad = int((~diag.admissible).sum())
    print(f"\n  Country-indicator fits leaving the admissible region: {bad}")

    print(f"\n{'ALL CHECKS PASSED' if not r.fails else f'{r.fails} CHECK(S) FAILED'}")
    return 1 if r.fails else 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True)
    sys.exit(main(ap.parse_args().input_dir))
