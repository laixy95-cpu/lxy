"""
Generate a SYNTHETIC ASEAN-6 panel for smoke-testing the pipeline.

The numbers are fabricated. They exist only to prove that the code executes,
that the Eq. (6) decomposition reconciles, and that the feasibility gate fires on
the series the manuscript says it should. They are NOT the study's data and must
never be reported. Replace with `1 ETRI_Core data.xlsx`.

Series are shaped to match the qualitative features Table 3 asserts:
  AccessElec       three economies already at the 100% ceiling
  Inflation        mean-reverting pre-crisis disinflation, then a 2022-23 spike
  RenCap           multiplicative growth, roughly eighteenfold across the panel
"""
from pathlib import Path

import numpy as np
import pandas as pd

COUNTRIES = ["Indonesia", "Malaysia", "Philippines", "Singapore", "Thailand", "Vietnam"]
YEARS = list(range(2010, 2024))
RNG = np.random.default_rng(20260910)

ACCESS_2010 = dict(Indonesia=94.0, Malaysia=99.3, Philippines=87.0,
                   Singapore=100.0, Thailand=99.5, Vietnam=97.6)
CAP_2010 = dict(Indonesia=25.0, Malaysia=22.0, Philippines=38.0,
                Singapore=6.0, Thailand=18.0, Vietnam=30.0)
CAP_GROWTH = dict(Indonesia=1.10, Malaysia=1.24, Philippines=1.09,
                  Singapore=1.36, Thailand=1.22, Vietnam=1.32)


def build() -> pd.DataFrame:
    rows = []
    for c in COUNTRIES:
        for y in YEARS:
            k = y - 2010
            crisis = y >= 2022
            acc = 100 - (100 - ACCESS_2010[c]) * np.exp(-0.28 * k)
            infl = 3.0 + 1.6 * np.exp(-0.18 * k) + RNG.normal(0, .35)
            if crisis:
                infl += 3.4 + RNG.normal(0, .5)          # 2022-23 price episode
            cap = CAP_2010[c] * CAP_GROWTH[c] ** k
            if c == "Vietnam" and y >= 2020:
                cap *= 1.45                               # FIT-driven level shift
            rows.append(dict(
                country=c, year=y,
                TDLoss=max(1.5, 11.0 - 0.22 * k + RNG.normal(0, .25)),
                AccessElec=min(100.0, round(acc, 2)),
                Inflation=round(infl, 3),
                RenTFEC=max(0.5, 18.0 + 0.45 * k + RNG.normal(0, .6)),
                CO2IntElec=max(50.0, 560.0 - 7.5 * k + RNG.normal(0, 9)),
                EnergyIntensity=max(1.0, 5.4 - 0.09 * k + RNG.normal(0, .09)),
                RenCap=round(cap, 2),
                RenElec=min(95.0, max(1.0, 14.0 + 0.9 * k + RNG.normal(0, .8))),
            ))
    return pd.DataFrame(rows)


if __name__ == "__main__":
    out = Path("synthetic_inputs")
    out.mkdir(exist_ok=True)
    df = build()
    with pd.ExcelWriter(out / "1 ETRI_Core data.xlsx", engine="openpyxl") as w:
        df.to_excel(w, sheet_name="ETRI_core", index=False)
    ratio = (df[df.year == 2023].RenCap.sum() / df[df.year == 2010].RenCap.sum())
    at_ceiling = (df[df.year == 2019].AccessElec >= 99.995).sum()
    print(f"rows={len(df)}  RenCap growth={ratio:.1f}x  "
          f"economies at the access ceiling in 2019={at_ceiling}")
