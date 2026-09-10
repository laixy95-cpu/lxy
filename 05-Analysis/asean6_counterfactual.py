"""
ASEAN-6 counterfactual-deviation pipeline.

Produces every quantity the manuscript reports, using the indicator-specific
counterfactuals of Table 3 (see `counterfactual_spec.py`) rather than the uniform
linear fit on standardised dimension scores in `asean6_reproducible.py`.

Implements, with equation numbers as printed in the manuscript:

    Eq. (1)  standardisation on the pooled ASEAN-6 2010-2019 distribution
    Eq. (2)  dimension score as the equal-weighted mean of standardised indicators
    Eq. (3)  indicator gap, counterfactual fitted on RAW values then standardised
    Eq. (4)  dimension gap averaged over indicators and stage years
    Eq. (5)  stage reordering
    Eq. (6)  indicator contributions, which sum exactly to the dimension gap

plus the rolling-origin backtest (Tashman 2000), horizon-matched placebo windows,
the seven robustness variants of section 3.6, and the gap-to-RMSE ratios.

Two conventions the manuscript leaves underspecified are made explicit here and
recorded in the run manifest:

  * audit A5 - a stage spans two forecast horizons, and the printed ratios
    reproduce only against the MEAN of the two horizon RMSEs (6/6), never a
    single horizon (0/6). `RATIO_RULE` below fixes that as the mean.
  * audit A2/A3 - the placebo window count is contradictory in the manuscript
    (five/three at the COVID horizon, floor 0.167 vs 0.250) and Table 9 prints one
    identical window on all six rows. Windows are enumerated here from the panel
    and the minimum training length, and every window is reported by name.
"""
from __future__ import annotations

import json
import platform
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

from counterfactual_spec import (
    MIN_TRAIN, SPECS, DIMENSIONS, InfeasibleCounterfactual, Spec,
    fixed_window_specs, training_years, uniform_linear_specs,
)

COUNTRIES = ["Indonesia", "Malaysia", "Philippines", "Singapore", "Thailand", "Vietnam"]
YEARS = list(range(2010, 2024))
PRE = (2010, 2019)
ORIGIN = 2019
STAGES = {"COVID": (2020, 2021), "Compound": (2022, 2023)}
STAGE_HORIZONS = {"COVID": (1, 2), "Compound": (3, 4)}
RATIO_RULE = "mean of the rolling-origin RMSE at the two horizons the stage spans"
# Section 3.6 reports five placebo windows at the COVID horizon and three at the
# compound horizon, with p-value floors of 0.167 and 0.250. On this year grid that
# is reproduced by, and only by, a four-observation minimum training length; see
# `placebo_window_geometry`. Section 4.6 and Table 9 instead report three windows
# for each stage with a floor of 0.250, which no single rule produces. Section 3.6
# is therefore the self-consistent text and is what this default reproduces.
PLACEBO_MIN_TRAIN = 4
T_DF, T_CRIT = 5, 2.570582  # Student-t, df = 5


# ------------------------------------------------------------------ Eq. (1)
def scaling_params(panel: pd.DataFrame, method: str = "zscore") -> pd.DataFrame:
    """Fixed reference distribution: pooled ASEAN-6, 2010-2019, 60 obs/indicator."""
    pre = panel[panel.year.between(*PRE)]
    rows = []
    for ind, g in pre.groupby("indicator"):
        v = g.value.dropna()
        if method == "zscore":
            centre, scale, kind = v.mean(), v.std(ddof=1), "mean_sd"
        else:
            centre, scale, kind = v.min(), v.max() - v.min(), "min_range"
        if not scale > 0:
            raise ValueError(f"{ind}: degenerate scale parameter")
        rows.append(dict(indicator=ind, centre=float(centre), scale=float(scale),
                         parameter_type=kind, n_baseline=int(len(v)),
                         direction=SPECS[ind].direction))
    return pd.DataFrame(rows).set_index("indicator")


def _std(x, ind, params):
    p = params.loc[ind]
    return p.direction * (np.asarray(x, dtype=float) - p.centre) / p.scale


# ------------------------------------------------------------ Eq. (3) gaps
def indicator_gaps(panel: pd.DataFrame, params: pd.DataFrame,
                   specs: dict[str, Spec] = None, origin: int = ORIGIN,
                   eval_years: list[int] = None, enforce: bool = True,
                   min_train: int = MIN_TRAIN) -> pd.DataFrame:
    """Counterfactual fitted on raw values over the trailing window, then standardised."""
    specs = specs or SPECS
    eval_years = eval_years or [y for y in YEARS if y > origin]
    rows, diag = [], []
    for country in COUNTRIES:
        for ind, spec in specs.items():
            sub = panel[(panel.country == country) & (panel.indicator == ind)]
            win = training_years(origin, spec.window_len)
            train = sub[sub.year.isin(win)].dropna(subset=["value"]).sort_values("year")
            if len(train) < min_train:
                raise InfeasibleCounterfactual(
                    f"{country}/{ind} @origin {origin}: {len(train)} training points")
            fn = spec.fit(train.year.values, train.value.values, min_train)
            pred = np.asarray(fn(eval_years), dtype=float)
            try:
                spec.check(pred)
                admissible, note = True, ""
            except InfeasibleCounterfactual as exc:
                admissible, note = False, str(exc)
                if enforce:
                    raise
            diag.append(dict(country=country, indicator=ind, form=spec.form,
                             origin=origin, train_start=win[0], train_end=win[-1],
                             n_train=len(train), clamped_points=getattr(fn, "clamped", 0),
                             admissible=admissible, note=note))
            for year, expected in zip(eval_years, pred):
                obs = sub.loc[sub.year == year, "value"]
                if obs.empty or pd.isna(obs.iloc[0]):
                    continue
                z_obs = float(_std(obs.iloc[0], ind, params))
                z_exp = float(_std(expected, ind, params))
                rows.append(dict(country=country, indicator=ind,
                                 dimension=spec.dimension, year=year,
                                 observed=float(obs.iloc[0]), expected=float(expected),
                                 z_observed=z_obs, z_expected=z_exp,
                                 gap=z_obs - z_exp))
    return pd.DataFrame(rows), pd.DataFrame(diag)


def _stage_of(year: int) -> str | None:
    for name, (a, b) in STAGES.items():
        if a <= year <= b:
            return name
    return None


# ------------------------------------------------- Eq. (4) dimension gaps
def dimension_gaps(gaps: pd.DataFrame) -> pd.DataFrame:
    g = gaps.assign(stage=gaps.year.map(_stage_of)).dropna(subset=["stage"])
    out = (g.groupby(["country", "dimension", "stage"], as_index=False)
             .gap.mean().rename(columns={"gap": "dimension_gap"}))
    wide = out.pivot(index=["country", "dimension"], columns="stage",
                     values="dimension_gap")
    # Eq. (5)
    wide["reordering"] = wide["Compound"] - wide["COVID"]
    return out, wide.reset_index()


# ------------------------------------------------- Eq. (6) decomposition
def decompose(gaps: pd.DataFrame, dimension: str = "LowCarbonContinuity") -> pd.DataFrame:
    """Indicator contributions that sum exactly to the dimension gap."""
    n = len(DIMENSIONS[dimension])
    g = gaps[gaps.dimension == dimension].assign(stage=lambda d: d.year.map(_stage_of))
    g = g.dropna(subset=["stage"])
    return (g.groupby(["country", "indicator", "stage"], as_index=False)
              .gap.mean().assign(contribution=lambda d: d.gap / n)
              .drop(columns="gap"))


def regional(dim_gaps: pd.DataFrame, intervals: bool = True) -> pd.DataFrame:
    """Unweighted country means. Student-t intervals are OPTIONAL and off by
    default in the CLI: see audit A11 and the JCLP R2#6 objection."""
    rows = []
    for (dim, stage), g in dim_gaps.groupby(["dimension", "stage"]):
        v = g.dimension_gap.values
        rec = dict(dimension=dim, stage=stage, regional_gap=float(v.mean()),
                   n_countries=len(v), sd=float(v.std(ddof=1)))
        if intervals:
            se = v.std(ddof=1) / np.sqrt(len(v))
            rec.update(ci_low=float(v.mean() - T_CRIT * se),
                       ci_high=float(v.mean() + T_CRIT * se),
                       excludes_zero=bool((v.mean() - T_CRIT * se) *
                                          (v.mean() + T_CRIT * se) > 0))
        rows.append(rec)
    return pd.DataFrame(rows)


# ------------------------------------------------------- rolling-origin
def backtest(panel: pd.DataFrame, params: pd.DataFrame,
             specs: dict[str, Spec] = None, origins=range(2014, 2019),
             horizons=(1, 2, 3, 4)) -> pd.DataFrame:
    """Tashman (2000) rolling origin; every evaluation year stays inside 2010-2019."""
    specs = specs or SPECS
    recs = []
    for origin in origins:
        ev = [origin + h for h in horizons if origin + h <= PRE[1]]
        if not ev:
            continue
        gaps, _ = indicator_gaps(panel, params, specs, origin=origin,
                                 eval_years=ev, enforce=False)
        dim = (gaps.groupby(["country", "dimension", "year"], as_index=False)
                   .gap.mean())
        dim["horizon"] = dim.year - origin
        dim["origin"] = origin
        recs.append(dim)
    allb = pd.concat(recs, ignore_index=True)
    return (allb.groupby(["dimension", "horizon"], as_index=False)
                .agg(bias=("gap", "mean"),
                     mae=("gap", lambda s: s.abs().mean()),
                     rmse=("gap", lambda s: float(np.sqrt((s ** 2).mean()))),
                     n=("gap", "size")))


def gap_to_rmse(reg: pd.DataFrame, bt: pd.DataFrame) -> pd.DataFrame:
    """|regional gap| / mean RMSE across the two horizons the stage spans (A5)."""
    out = []
    for _, r in reg.iterrows():
        h = STAGE_HORIZONS[r.stage]
        d = bt[(bt.dimension == r.dimension) & (bt.horizon.isin(h))]
        denom = float(d.rmse.mean())
        out.append(dict(dimension=r.dimension, stage=r.stage,
                        regional_gap=r.regional_gap, horizons=f"h={h[0]}-{h[1]}",
                        rmse_denominator=denom,
                        ratio=abs(r.regional_gap) / denom if denom else np.nan))
    return pd.DataFrame(out)


# ------------------------------------------------------------- placebo
def placebo_window_geometry(min_train: int = MIN_TRAIN) -> pd.DataFrame:
    """How many placebo windows the panel admits, as a function of the minimum
    training length. This depends only on the year grid, not on the data, so it
    settles audit A2 before the analysis is even run: the manuscript's counts
    (five/three in section 3.6, three/three in section 4.6) imply different and
    unstated minimum-training rules."""
    rows = []
    for mt in range(3, 8):
        for stage, (h1, h2) in STAGE_HORIZONS.items():
            origins = [o for o in range(PRE[0] + mt - 1, PRE[1] + 1)
                       if o + h2 <= PRE[1]]
            rows.append(dict(min_train=mt, stage=stage, n_windows=len(origins),
                             p_floor=1 / (len(origins) + 1) if origins else np.nan,
                             windows="; ".join(f"{o+h1}-{o+h2}" for o in origins)))
    return pd.DataFrame(rows)


def placebo(panel: pd.DataFrame, params: pd.DataFrame,
            specs: dict[str, Spec] = None,
            min_train: int = PLACEBO_MIN_TRAIN) -> pd.DataFrame:
    """Horizon-matched pre-crisis pseudo-stages.

    A placebo for a stage spanning horizons (h1, h2) is the window (o+h1, o+h2)
    for every origin o whose whole window lies inside the pre-crisis period and
    which still has MIN_TRAIN training observations. Each window is named, which
    is what Table 9 fails to do (audit A3).
    """
    specs = specs or SPECS
    rows = []
    for stage, (h1, h2) in STAGE_HORIZONS.items():
        for origin in range(PRE[0] + min_train - 1, PRE[1] + 1):
            ev = [origin + h1, origin + h2]
            if ev[-1] > PRE[1]:
                continue
            try:
                gaps, _ = indicator_gaps(panel, params, specs, origin=origin,
                                         eval_years=ev, enforce=False,
                                         min_train=min_train)
            except InfeasibleCounterfactual:
                continue
            dim = gaps.groupby(["country", "dimension"], as_index=False).gap.mean()
            for d, g in dim.groupby("dimension"):
                rows.append(dict(stage=stage, dimension=d, origin=origin,
                                 window=f"{ev[0]}-{ev[1]}",
                                 regional_gap=float(g.gap.mean())))
    return pd.DataFrame(rows)


def placebo_test(pl: pd.DataFrame, reg: pd.DataFrame) -> pd.DataFrame:
    """One-sided rank position of the observed gap among its placebo windows."""
    out = []
    for _, r in reg.iterrows():
        w = pl[(pl.stage == r.stage) & (pl.dimension == r.dimension)]
        k = len(w)
        if k == 0:
            continue
        if r.regional_gap < 0:
            more = int((w.regional_gap <= r.regional_gap).sum())
        else:
            more = int((w.regional_gap >= r.regional_gap).sum())
        out.append(dict(dimension=r.dimension, stage=r.stage,
                        observed=r.regional_gap, n_windows=k,
                        windows="; ".join(sorted(w.window.unique())),
                        placebo_min=float(w.regional_gap.min()),
                        placebo_max=float(w.regional_gap.max()),
                        more_extreme=more, p_value=(more + 1) / (k + 1),
                        p_floor=1 / (k + 1),
                        beyond_all_placebos=bool(more == 0)))
    return pd.DataFrame(out)


# ---------------------------------------------------------- robustness
def _dimension_scores(panel: pd.DataFrame, params: pd.DataFrame) -> pd.DataFrame:
    """Eq. (2): equal-weighted mean of standardised indicators."""
    p = panel.copy()
    p["z"] = [float(_std(v, i, params)) for v, i in zip(p.value, p.indicator)]
    p["dimension"] = p.indicator.map({i: s.dimension for i, s in SPECS.items()})
    return (p.groupby(["country", "year", "dimension"], as_index=False)
             .z.mean().rename(columns={"z": "score"}))


def level_baseline_gaps(panel: pd.DataFrame, params: pd.DataFrame,
                        baseline: str) -> pd.DataFrame:
    """Replace the fitted path with a pre-crisis level (sections 3.6 / 4.6)."""
    sc = _dimension_scores(panel, params)
    rows = []
    for (country, dim), g in sc.groupby(["country", "dimension"]):
        if baseline == "2017-2019 mean":
            ref = g[g.year.between(2017, 2019)].score.mean()
        elif baseline == "2019 level":
            ref = g.loc[g.year == 2019, "score"].iloc[0]
        else:
            raise ValueError(baseline)
        for stage, (a, b) in STAGES.items():
            obs = g[g.year.between(a, b)].score.mean()
            rows.append(dict(country=country, dimension=dim, stage=stage,
                             dimension_gap=float(obs - ref)))
    return pd.DataFrame(rows)


def robustness(panel: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """The seven variants of section 3.6. Variant 2 - the uniform linear form - is
    the check Table 8 omits (audit A4); it is the specification that
    `asean6_reproducible.py` uses as its MAIN model, so reporting it here also
    reconciles the two code bases."""
    params = scaling_params(panel, "zscore")
    base_gaps, _ = indicator_gaps(panel, params)
    base_dim, _ = dimension_gaps(base_gaps)

    variants: dict[str, pd.DataFrame] = {}

    mm = scaling_params(panel, "minmax")
    g, _ = indicator_gaps(panel, mm)
    variants["Pre-crisis min-max scaling"] = dimension_gaps(g)[0]

    g, _ = indicator_gaps(panel, params, uniform_linear_specs(), enforce=False)
    variants["Uniform linear form (Table 3 replaced)"] = dimension_gaps(g)[0]

    g, _ = indicator_gaps(panel, params, fixed_window_specs(5))
    variants["Five-year training window"] = dimension_gaps(g)[0]

    variants["2017-2019 mean baseline"] = level_baseline_gaps(panel, params, "2017-2019 mean")
    variants["2019 level baseline"] = level_baseline_gaps(panel, params, "2019 level")

    rows = []
    key = ["country", "dimension", "stage"]
    for name, var in variants.items():
        m = (base_dim.rename(columns={"dimension_gap": "base"})
                     .merge(var.rename(columns={"dimension_gap": "variant"}), on=key)
                     .dropna(subset=["base", "variant"]))
        rows.append(dict(
            check=name, n_cells=len(m),
            pearson=float(stats.pearsonr(m.base, m.variant).statistic),
            spearman=float(stats.spearmanr(m.base, m.variant).statistic),
            sign_agreement=float(np.mean(np.sign(m.base) == np.sign(m.variant))),
            sign_agreement_basis=f"{len(m)} country x dimension x stage gaps",
            regional_lowcarbon_compound=float(
                var[(var.dimension == "LowCarbonContinuity") &
                    (var.stage == "Compound")].dimension_gap.mean()),
        ))

    # leave-one-country-out and leave-one-indicator-out on the headline quantity
    lc = base_dim[(base_dim.dimension == "LowCarbonContinuity") &
                  (base_dim.stage == "Compound")]
    loco = {c: float(lc[lc.country != c].dimension_gap.mean()) for c in COUNTRIES}
    rows.append(dict(check="Leave one country out", n_cells=len(COUNTRIES),
                     pearson=np.nan, spearman=np.nan, sign_agreement=np.nan,
                     sign_agreement_basis="range across six exclusions",
                     regional_lowcarbon_compound=np.nan))

    loio = {}
    for ind in DIMENSIONS["LowCarbonContinuity"]:
        sub = {k: v for k, v in SPECS.items() if k != ind}
        g, _ = indicator_gaps(panel[panel.indicator != ind], params, sub)
        d, _ = dimension_gaps(g)
        loio[ind] = float(d[(d.dimension == "LowCarbonContinuity") &
                            (d.stage == "Compound")].dimension_gap.mean())
    rows.append(dict(check="Leave one indicator out", n_cells=len(loio),
                     pearson=np.nan, spearman=np.nan, sign_agreement=np.nan,
                     sign_agreement_basis="range across five exclusions",
                     regional_lowcarbon_compound=np.nan))

    extras = {
        "leave_one_country_out": loco,
        "leave_one_country_out_range": [min(loco.values()), max(loco.values())],
        "sign_reversing_countries": [c for c, v in loco.items()
                                     if np.sign(v) != np.sign(lc.dimension_gap.mean())],
        "leave_one_indicator_out": loio,
        "leave_one_indicator_out_range": [min(loio.values()), max(loio.values())],
        "main_lowcarbon_compound": float(lc.dimension_gap.mean()),
    }
    return pd.DataFrame(rows), extras


# ------------------------------------------------------------------ IO
def load_panel(input_dir: Path) -> pd.DataFrame:
    """Read the ETRI core workbook into long format (country, year, indicator, value)."""
    core = pd.read_excel(Path(input_dir) / "1 ETRI_Core data.xlsx", sheet_name="ETRI_core")
    missing = [i for i in SPECS if i not in core.columns]
    if missing:
        raise KeyError(f"Core workbook is missing required indicators: {missing}")
    long = core.melt(id_vars=["country", "year"], value_vars=list(SPECS),
                     var_name="indicator", value_name="value")
    long["year"] = long.year.astype(int)
    bad = sorted(set(long.country) - set(COUNTRIES))
    if bad:
        raise ValueError(f"Unexpected countries: {bad}")
    if len(core) != 84:
        raise ValueError(f"Expected 84 country-year rows, found {len(core)}")
    return long


def run(input_dir, output_root, with_intervals: bool = False) -> dict:
    out = Path(output_root)
    (out / "tables").mkdir(parents=True, exist_ok=True)
    panel = load_panel(input_dir)
    params = scaling_params(panel)
    gaps, diag = indicator_gaps(panel, params)
    dim_long, dim_wide = dimension_gaps(gaps)
    contrib = decompose(gaps)
    reg = regional(dim_long, intervals=with_intervals)
    bt = backtest(panel, params)
    ratios = gap_to_rmse(reg, bt)
    pl = placebo(panel, params)
    pl_test = placebo_test(pl, reg)
    rob, extras = robustness(panel)

    # Eq. (6) audit: contributions must sum to the dimension gap
    chk = (contrib.groupby(["country", "stage"], as_index=False).contribution.sum()
           .merge(dim_long[dim_long.dimension == "LowCarbonContinuity"],
                  on=["country", "stage"]))
    chk["reconciliation_error"] = chk.contribution - chk.dimension_gap
    max_err = float(chk.reconciliation_error.abs().max())

    tables = {"T9_placebo_geometry": placebo_window_geometry(),
              "T2_indicator_gaps": gaps, "T3_fit_diagnostics": diag,
              "T4_dimension_gaps": dim_long, "T4_reordering": dim_wide,
              "T4_regional": reg, "T5_contributions": contrib,
              "T8_robustness": rob, "T9_backtest": bt, "T9_placebo": pl,
              "T9_placebo_test": pl_test, "gap_to_rmse": ratios,
              "decomposition_audit": chk}
    for name, df in tables.items():
        df.to_csv(out / "tables" / f"{name}.csv", index=False, encoding="utf-8-sig")

    manifest = dict(
        generated_utc=datetime.now(timezone.utc).isoformat(),
        python=platform.python_version(), origin=ORIGIN,
        specifications={k: asdict(v) for k, v in SPECS.items()},
        ratio_rule=RATIO_RULE, confidence_intervals_reported=with_intervals,
        decomposition_max_error=max_err,
        placebo_windows={f"{r.stage}/{r.dimension}": r.windows
                         for r in pl_test.itertuples()},
        robustness_extras=extras,
        inadmissible_under_uniform_linear=int((~diag.admissible).sum()),
    )
    (out / "run_manifest.json").write_text(
        json.dumps(manifest, indent=2, default=str), encoding="utf-8")
    return dict(tables=tables, manifest=manifest, extras=extras)


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input-dir", required=True)
    ap.add_argument("--output-root", default="counterfactual_output")
    ap.add_argument("--with-intervals", action="store_true",
                    help="also emit Student-t cross-country intervals (see audit A11)")
    a = ap.parse_args()
    res = run(a.input_dir, a.output_root, a.with_intervals)
    print(json.dumps(res["manifest"]["robustness_extras"], indent=2, default=str))
