"""Step 0 - audit the supplied outcome panel and fix the provisional analysis sample.

Reads : data/raw/global_outcome_panel_2012_2024.csv
Writes: data/built/panel_analysis_sample.csv
        output/tables/panel_audit_summary.csv     (every check vs. the figure quoted in the brief)
        output/tables/panel_country_coverage.csv  (per-iso coverage and in-sample flag)
        output/tables/panel_identity_check.csv    (electricity accounting identity, first differences)
        logs/00_audit_panel.log

No imputation anywhere: rows are kept or dropped, never filled.
Run from anywhere:  python3 src/00_audit_panel.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw/global_outcome_panel_2012_2024.csv"
LOG = ROOT / "logs/00_audit_panel.log"
LOG.parent.mkdir(exist_ok=True)
LOG.write_text("")


def say(msg=""):
    print(msg)
    with LOG.open("a") as f:
        f.write(msg + "\n")


df = pd.read_csv(RAW)
assert not df.duplicated(["iso", "year"]).any(), "(iso, year) must be unique"
assert df.year.between(2012, 2024).all()

# Provisional analysis sample: outcome + exposure observed. This reproduces the brief's
# "2532 obs / 197 countries". It is provisional: the exposure column here (re_imp_chn, four
# products) is replaced by the 72-product BACI instrument at step 2, after which the sample
# is re-fixed. CHN is excluded automatically (no import-from-China series for the exporter).
S_KEYS = ["gen_twh", "co2", "re_imp_chn"]
s = df.dropna(subset=S_KEYS).copy()
c = s.drop_duplicates("iso")

# ---- per-country coverage --------------------------------------------------------------
cov = df.groupby("iso").agg(
    country=("country", "first"), subregion=("subregion", "first"),
    oecd=("oecd", "max"), bri_ever=("is_bri_ever", "max"),
    n_years=("year", "size"), n_gen=("gen_twh", "count"),
    n_co2=("co2", "count"), n_imp=("re_imp_chn", "count"), n_demand=("demand_twh", "count"),
).reset_index()
cov["in_sample"] = cov.iso.isin(c.iso)
cov["drop_reason"] = np.select(
    [cov.in_sample, cov.n_gen == 0, cov.n_imp == 0],
    ["", "no electricity generation series", "no imports-from-China series"],
    default="no co2 series")
cov.to_csv(ROOT / "output/tables/panel_country_coverage.csv", index=False)

# ---- electricity accounting identity ---------------------------------------------------
# Ember/OWID: gen = fossil + low-carbon exactly; demand = gen + net imports.
# Hence, exactly:  d(solar+wind) = d(demand) - d(netimp) - d(fossil) - d(hydro) - d(nuclear) - d(other ren)
need = ["gen_twh", "fossil_twh", "lowc_twh", "demand_twh", "solar_twh", "wind_twh", "hydro_twh", "ren_twh"]
t = s.dropna(subset=need).sort_values(["iso", "year"]).copy()
t["sw"] = t.solar_twh + t.wind_twh
t["netimp"] = t.demand_twh - t.gen_twh
t["nuclear"] = t.lowc_twh - t.ren_twh
t["oth_ren"] = t.ren_twh - (t.solar_twh + t.wind_twh + t.hydro_twh)
terms = ["sw", "demand_twh", "netimp", "fossil_twh", "hydro_twh", "nuclear", "oth_ren"]
d = t.groupby("iso")[terms].diff()
d = d[t.groupby("iso").year.diff().eq(1)]            # first differences over consecutive years only
resid = d.demand_twh - d.netimp - d.fossil_twh - d.hydro_twh - d.nuclear - d.oth_ren - d.sw
ident = pd.DataFrame({
    "term": terms,
    "mean_abs_delta_twh": [d[k].abs().mean() for k in terms],
    "share_nonzero": [(d[k].abs() > 0.01).mean() for k in terms],
})
ident.to_csv(ROOT / "output/tables/panel_identity_check.csv", index=False)

# ---- summary vs. brief -----------------------------------------------------------------
rows = [
    ("file rows", len(df), None),
    ("file iso codes", df.iso.nunique(), None),
    ("duplicate (iso,year)", int(df.duplicated(["iso", "year"]).sum()), 0),
    ("analysis-sample rows", len(s), 2532),
    ("analysis-sample countries", s.iso.nunique(), 197),
    ("  OECD", int(c.oecd.sum()), 38),
    ("  BRI-ever", int((c.is_bri_ever == 1).sum()), 148),
    ("  OECD and BRI-ever", int(((c.oecd == 1) & (c.is_bri_ever == 1)).sum()), None),
    ("  neither", int(((c.oecd == 0) & (c.is_bri_ever != 1)).sum()), 30),
    ("subregions in sample", c.subregion.nunique(), None),
    ("min countries in a subregion", int(c.subregion.value_counts().min()), None),
    ("max |gen - (fossil+lowc)| TWh", float((t.gen_twh - t.fossil_twh - t.lowc_twh).abs().max()), 0),
    ("max |identity residual| TWh", float(resid.abs().max()), 0),
    ("re_imp_chn zeros in sample", int((s.re_imp_chn == 0).sum()), None),
    ("re_imp_chn == sum of 4 products (max abs diff)",
     float((s.re_imp_chn - s[["solar", "wind", "battery", "grid_inverter"]].sum(axis=1)).abs().max()), None),
]
# Match status is computed on the raw list: a None in a DataFrame column would become NaN.
match = ["" if b is None else ("yes" if abs(v - b) < 1e-6 else "NO") for _, v, b in rows]
summ = pd.DataFrame(rows, columns=["check", "value", "brief_says"])
summ["matches_brief"] = match
summ.to_csv(ROOT / "output/tables/panel_audit_summary.csv", index=False)

# ---- coverage in estimation window -----------------------------------------------------
w = s[s.year.between(2013, 2024)]
say("== PANEL AUDIT ==")
say(summ.to_string(index=False))
say("\n== Electricity identity: first-difference magnitudes (analysis sample, TWh) ==")
say(ident.round(3).to_string(index=False))
say(f"\nwindow 2013-2024: {len(w)} rows, {w.iso.nunique()} countries (before BACI/WDI merge)")
say("\nDropped isos by reason:\n" + cov[~cov.in_sample].drop_duplicates("iso").drop_reason.value_counts().to_string())
say("\nIn-sample country-years by year:\n" + s.groupby("year").iso.nunique().to_string())

s.to_csv(ROOT / "data/built/panel_analysis_sample.csv", index=False)
say(f"\nwrote data/built/panel_analysis_sample.csv ({len(s)} rows)")
