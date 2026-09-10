"""
Documented corrections to `1 ETRI_Core data.xlsx` as supplied.

Each entry records what is wrong, the published value, and the source. Nothing is
silently patched: `apply()` returns the corrected panel and a log, and the log is
written into the run manifest.

Evidence that these are file defects rather than method defects: with CORRECTION 1
applied, every country value and the regional mean for macro-price stability in the
compound stage reproduce the manuscript exactly (Singapore -1.816, Philippines
-1.150, Thailand -1.118 vs -1.117, Malaysia -0.342, Vietnam -0.194, Indonesia
+0.016, regional -0.767). Four of six energy-service country values also reproduce
exactly; the two that do not are among the three with missing 2023 TDLoss.
"""
from __future__ import annotations

import pandas as pd

# CORRECTION 1 - Thailand CPI inflation, 2022 and 2023.
# The workbook implies -1.61% and +8.48%. World Bank FP.CPI.TOTL.ZG publishes
# 6.08% and 1.23%. Every other country-year in the column matches WDI to two
# decimals, so this is isolated to Thailand's two crisis years - the two years
# that carry the paper's headline finding.
INFLATION_FIX = {("Thailand", 2022): 6.08, ("Thailand", 2023): 1.23}

# CORRECTION 2 - cells coded 0 that denote "not published", not a measured zero.
# `isna()`-based audits do not catch these, so the original audit_core() passes.
#   RenTFEC          all six countries, 2022 and 2023   (2021 values 1.1-28.0)
#   EnergyIntensity  all six countries, 2022 and 2023   (2021 values 2.5-4.5)
#   TDLoss           Malaysia, Philippines, Vietnam, 2023
# These cannot be reconstructed from published sources here and must come from the
# author's own extract. Handled by `load_panel(zeros_as_missing=True)`.
KNOWN_MISSING = {
    "RenTFEC": [2022, 2023],
    "EnergyIntensity": [2022, 2023],
    "TDLoss": [2023],
}


def apply(panel: pd.DataFrame, inflation: bool = True) -> tuple[pd.DataFrame, list[dict]]:
    log = []
    out = panel.copy()
    if inflation:
        for (country, year), value in INFLATION_FIX.items():
            m = ((out.country == country) & (out.year == year)
                 & (out.indicator == "Inflation"))
            if m.any():
                before = float(out.loc[m, "value"].iloc[0])
                out.loc[m, "value"] = value
                log.append(dict(correction="CORRECTION 1", country=country, year=year,
                                indicator="Inflation", before=before, after=value,
                                source="World Bank WDI FP.CPI.TOTL.ZG"))
    return out, log
