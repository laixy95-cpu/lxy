"""Decompose the revised results into the three changes, so each can be reviewed
independently:  D1 Thailand inflation | A18 TDLoss log-linear | 3-indicator low-carbon."""
import sys, warnings, dataclasses, json
sys.path.insert(0, "05-Analysis"); warnings.filterwarnings("ignore")
import pandas as pd, numpy as np
import asean6_counterfactual as A
from counterfactual_spec import SPECS, active_specs
import data_corrections

FULL = active_specs("full")
CORE = active_specs("core")
LIN  = {k: (dataclasses.replace(v, form="linear") if k == "TDLoss" else v)
        for k, v in FULL.items()}
LIN_CORE = {k: v for k, v in LIN.items() if k in CORE}

def cfg(specs, thai):
    panel = A.load_panel("05-Analysis/inputs")
    if thai:
        panel, _ = data_corrections.apply(panel)
    keep = list(specs)
    panel = panel[panel.indicator.isin(keep)]
    pre = panel[panel.year.between(*A.PRE)]
    rows = []
    for ind, g in pre.groupby("indicator"):
        v = g.value.dropna()
        rows.append(dict(indicator=ind, centre=float(v.mean()), scale=float(v.std(ddof=1)),
                         parameter_type="mean_sd", n_baseline=len(v),
                         direction=SPECS[ind].direction))
    params = pd.DataFrame(rows).set_index("indicator")
    gaps, _ = A.indicator_gaps(panel, params, specs, enforce=False)
    dl, _ = A.dimension_gaps(gaps)
    reg = dl.groupby(["dimension", "stage"], as_index=False).dimension_gap.mean()
    return reg.set_index(["dimension", "stage"]).dimension_gap, dl, gaps

STEPS = [
    ("0  as submitted (5 ind, TDLoss linear, no fix)", LIN,      False),
    ("1  + D1 Thailand inflation corrected",           LIN,      True),
    ("2  + A18 TDLoss log-linear",                     FULL,     True),
    ("3  + 3-indicator low-carbon  = FINAL",           CORE,     True),
]
MAN = {("EnergyServiceSecurity","COVID"):-0.077, ("EnergyServiceSecurity","Compound"):-0.103,
       ("MacroPricePressure","COVID"):0.120,     ("MacroPricePressure","Compound"):-0.767,
       ("LowCarbonContinuity","COVID"):0.035,    ("LowCarbonContinuity","Compound"):0.102}

if __name__ == "__main__":
    out = {}
    for label, specs, thai in STEPS:
        s, dl, gaps = cfg(specs, thai)
        out[label] = s
        if label.startswith("3"):
            dl.to_csv("07-Results/tables/FINAL_country_gaps.csv", index=False)
    t = pd.DataFrame(out)
    t.insert(0, "manuscript", [MAN.get(i, np.nan) for i in t.index])
    print("=" * 100)
    print("ABLATION — regional gaps after each change")
    print("=" * 100)
    print(t.round(3).to_string())
    print()
    print("per-step movement:")
    d = t.iloc[:, 1:].diff(axis=1).iloc[:, 1:]
    print(d.round(3).to_string())
