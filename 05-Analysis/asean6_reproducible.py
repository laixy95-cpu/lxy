"""Reproducible ASEAN-6 sequential-crisis diagnostic (Python 3 / Colab compatible)."""
from __future__ import annotations

import json
import logging
import platform
import random
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import pearsonr, spearmanr

SEED = 20260809
COUNTRIES = ["Indonesia", "Malaysia", "Philippines", "Singapore", "Thailand", "Vietnam"]
YEARS = list(range(2010, 2024))
STAGES = {"COVID": [2020, 2021], "Price": [2022, 2023]}

DIMENSIONS = {
    "EnergyServiceSecurity": {"TDLoss": -1, "AccessElec": 1},
    "MacroPricePressure": {"Inflation": -1},
    "LowCarbonContinuity": {
        "RenTFEC": 1, "CO2IntElec": -1, "EnergyIntensity": -1,
        "RenCap": 1, "RenElec": 1,
    },
}
PRECONDITIONS = ["GovEffect", "RegQuality", "Credit", "Internet", "GovExp", "lnGDPpc", "Diversification"]
EXPOSURES = ["covid_exposure_tourism", "covid_exposure_services", "price_exposure_fuelimports",
             "price_exposure_fossilshare", "price_exposure_gasshare"]


def setup_dirs(root: Path) -> dict[str, Path]:
    dirs = {name: root / name for name in ["data_audit", "clean_data", "tables", "figures", "logs"]}
    for p in dirs.values():
        p.mkdir(parents=True, exist_ok=True)
    return dirs


def setup_logging(path: Path) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s",
                        handlers=[logging.FileHandler(path, encoding="utf-8"), logging.StreamHandler()])


def load_inputs(input_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    core = pd.read_excel(input_dir / "1 ETRI_Core data.xlsx", sheet_name="ETRI_core")
    exposure = pd.read_excel(input_dir / "2 crisis_exposure.xlsx", sheet_name="crisis_exposure")
    p1 = pd.read_excel(input_dir / "4 policy_response_price_cushioning.xlsx")
    p2 = pd.read_excel(input_dir / "6 policy_response_extended (1).xlsx")
    policies = p1.merge(p2, on=["country", "year"], how="outer")
    return core, exposure, policies


def audit_core(core: pd.DataFrame, audit_dir: Path) -> pd.DataFrame:
    assert set(core.country) == set(COUNTRIES), f"Unexpected countries: {sorted(set(core.country))}"
    assert set(core.year.astype(int)) == set(YEARS), "Year coverage must be 2010-2023"
    assert len(core) == 84, "Expected 84 country-year observations"
    assert not core.duplicated(["country", "year"]).any(), "Duplicate country-year rows detected"
    expected = pd.MultiIndex.from_product([COUNTRIES, YEARS], names=["country", "year"])
    actual = pd.MultiIndex.from_frame(core[["country", "year"]])
    assert len(expected.difference(actual)) == 0, "Country-year grid is incomplete"
    rows = []
    for col in core.columns:
        if col in ["country", "year"]:
            continue
        miss = core.loc[core[col].isna(), ["country", "year"]]
        rows.append({"variable": col, "n_missing": len(miss), "missing_rate": len(miss) / len(core),
                     "missing_country_years": "; ".join(miss.astype(str).agg("-".join, axis=1))})
    out = pd.DataFrame(rows)
    out.to_csv(audit_dir / "missingness_audit.csv", index=False, encoding="utf-8-sig")
    return out


def direction_table() -> pd.DataFrame:
    rows = []
    for dim, mapping in DIMENSIONS.items():
        for var, sign in mapping.items():
            rows.append({"layer": "crisis-period outcome", "dimension": dim, "indicator": var,
                         "variable_name": var, "direction": "positive" if sign == 1 else "negative",
                         "multiplier": sign, "role": "dimension input", "baseline_period": "2010-2019",
                         "source": "1 ETRI_Core data.xlsx", "coverage": "ASEAN-6, 2010-2023",
                         "missing_treatment": "none; score missing if validity threshold is not met"})
    for var in PRECONDITIONS:
        rows.append({"layer": "pre-crisis condition", "dimension": "StructuralProfile", "indicator": var,
                     "variable_name": var, "direction": "descriptive", "multiplier": np.nan,
                     "role": "profile only", "baseline_period": "2017-2019 mean",
                     "source": "1 ETRI_Core data.xlsx", "coverage": "ASEAN-6, 2010-2023",
                     "missing_treatment": "none"})
    return pd.DataFrame(rows)


def scale_dimensions(core: pd.DataFrame, method: str = "zscore", omit: tuple[str, str] | None = None):
    out = core.copy()
    params = []
    dim_cols = []
    for dim, mapping0 in DIMENSIONS.items():
        mapping = dict(mapping0)
        if omit and omit[0] == dim:
            mapping.pop(omit[1], None)
        zcols = []
        for var, sign in mapping.items():
            base = core.loc[core.year.between(2010, 2019), var].dropna()
            assert len(base) > 1
            if method == "zscore":
                center, scale = base.mean(), base.std(ddof=1)
                assert scale > 0
                out[f"s_{var}"] = sign * (core[var] - center) / scale
                ptype = "mean_sd"
            else:
                center, scale = base.min(), base.max() - base.min()
                assert scale > 0
                out[f"s_{var}"] = sign * (core[var] - center) / scale
                ptype = "min_range"
            zcols.append(f"s_{var}")
            params.append({"indicator": var, "direction_multiplier": sign, "method": method,
                           "parameter_type": ptype, "center": center, "scale": scale,
                           "parameter_sample": "ASEAN-6 pooled 2010-2019", "n_baseline": len(base)})
        assert zcols, f"No indicators left in {dim}"
        valid_share = out[zcols].notna().mean(axis=1)
        out[dim] = out[zcols].mean(axis=1, skipna=True).where(valid_share >= 0.5)
        out[f"{dim}_valid_share"] = valid_share
        dim_cols.append(dim)
    return out, pd.DataFrame(params), dim_cols


def trend_gaps(scored: pd.DataFrame, dims: list[str], start: int = 2010) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rows, fits = [], []
    for country in COUNTRIES:
        for dim in dims:
            train = scored[(scored.country == country) & scored.year.between(start, 2019)][["year", dim]].dropna()
            assert len(train) >= 5, f"Insufficient pre-crisis observations: {country}, {dim}"
            slope, intercept = np.polyfit(train.year, train[dim], 1)
            fitted = intercept + slope * train.year
            ss_res = np.square(train[dim] - fitted).sum()
            ss_tot = np.square(train[dim] - train[dim].mean()).sum()
            r2 = 1 - ss_res / ss_tot if ss_tot else np.nan
            fits.append({"country": country, "dimension": dim, "trend_start": start, "trend_end": 2019,
                         "intercept": intercept, "slope": slope, "r_squared": r2, "n": len(train)})
            for year in YEARS:
                actual = scored.loc[(scored.country == country) & (scored.year == year), dim].iloc[0]
                expected = intercept + slope * year if year >= 2020 else np.nan
                rows.append({"country": country, "year": year, "dimension": dim, "actual": actual,
                             "expected": expected, "maintenance_gap": actual - expected if year >= 2020 else np.nan})
    annual = pd.DataFrame(rows)
    stage = (annual[annual.year >= 2020].assign(stage=lambda x: np.where(x.year <= 2021, "COVID", "Price"))
             .groupby(["country", "dimension", "stage"], as_index=False)
             .agg(actual_stage_mean=("actual", "mean"), expected_stage_mean=("expected", "mean"),
                  maintenance_gap=("maintenance_gap", "mean")))
    wide = stage.pivot(index=["country", "dimension"], columns="stage", values="maintenance_gap").reset_index()
    wide["Price_minus_COVID"] = wide["Price"] - wide["COVID"]
    stage = stage.merge(wide[["country", "dimension", "Price_minus_COVID"]], on=["country", "dimension"])
    return annual, stage, pd.DataFrame(fits)


def stage_baseline_sensitivity(scored: pd.DataFrame, dims: list[str]) -> pd.DataFrame:
    rows = []
    for country in COUNTRIES:
        for dim in dims:
            pre3 = scored[(scored.country == country) & scored.year.between(2017, 2019)][dim].mean()
            y2019 = scored[(scored.country == country) & (scored.year == 2019)][dim].iloc[0]
            for stage, years in STAGES.items():
                actual = scored[(scored.country == country) & scored.year.isin(years)][dim].mean()
                rows += [{"country": country, "dimension": dim, "stage": stage, "baseline": "2017-2019 mean", "gap": actual-pre3},
                         {"country": country, "dimension": dim, "stage": stage, "baseline": "2019 level", "gap": actual-y2019}]
    return pd.DataFrame(rows)


def precrisis_profiles(core: pd.DataFrame, exposure: pd.DataFrame) -> pd.DataFrame:
    merged = core.merge(exposure, on=["country", "year"], how="left")
    cols = PRECONDITIONS + EXPOSURES
    return (merged[merged.year.between(2017, 2019)].groupby("country", as_index=False)[cols].mean()
            .rename(columns={c: f"pre_{c}" for c in cols}))


def policy_matrix(policies: pd.DataFrame, stage: pd.DataFrame) -> pd.DataFrame:
    p = policies.copy()
    price_col = "final_price_cushioning_code (0/1)"
    p[price_col] = pd.to_numeric(p.get(price_col), errors="coerce").fillna(0)
    p["targeted_transfer_or_compensation"] = pd.to_numeric(p.get("targeted_transfer_or_compensation"), errors="coerce").fillna(0)
    p["transition_continuity_policy"] = pd.to_numeric(p.get("transition_continuity_policy"), errors="coerce").fillna(0)
    p["stage"] = np.where(p.year <= 2021, "COVID", "Price")
    agg = p.groupby(["country", "stage"], as_index=False).agg(
        price_cushioning=(price_col, "sum"), targeted_support=("targeted_transfer_or_compensation", "sum"),
        transition_continuity=("transition_continuity_policy", "sum"))
    short = (stage.loc[stage.groupby(["country", "stage"]).maintenance_gap.idxmin(),
                       ["country", "stage", "dimension", "maintenance_gap"]]
             .rename(columns={"dimension": "main_maintenance_gap_dimension"}))
    out = agg.merge(short, on=["country", "stage"], how="left")
    out["functional_alignment"] = "Policy functions are descriptively compared with the observed shortfall; no causal effectiveness is inferred."
    return out


def robustness(main_stage: pd.DataFrame, variants: dict[str, pd.DataFrame]) -> pd.DataFrame:
    key = ["country", "dimension", "stage"]
    base = main_stage[key + ["maintenance_gap"]].rename(columns={"maintenance_gap": "base"})
    rows = []
    for name, variant in variants.items():
        m = base.merge(variant[key + ["maintenance_gap"]].rename(columns={"maintenance_gap": "variant"}), on=key)
        ok = m[["base", "variant"]].dropna()
        pear = pearsonr(ok.base, ok.variant).statistic if len(ok) > 2 else np.nan
        spear = spearmanr(ok.base, ok.variant).statistic if len(ok) > 2 else np.nan
        sign = np.mean(np.sign(ok.base) == np.sign(ok.variant))
        base_short = m.loc[m.groupby(["country", "stage"]).base.idxmin(), key]
        var_short = m.loc[m.groupby(["country", "stage"]).variant.idxmin(), key]
        short_agree = base_short.merge(var_short, on=["country", "stage"], suffixes=("_b", "_v"))
        short_rate = np.mean(short_agree.dimension_b == short_agree.dimension_v)
        rows.append({"check": name, "pearson": pear, "spearman": spear, "gap_sign_agreement": sign,
                     "main_shortfall_agreement": short_rate,
                     "core_conclusion_retained": bool(sign >= 0.8 and short_rate >= 0.67)})
    return pd.DataFrame(rows)


def make_figures(annual: pd.DataFrame, stage: pd.DataFrame, policy: pd.DataFrame, fig_dir: Path) -> None:
    sns.set_theme(style="whitegrid", context="paper")
    palette = dict(zip(COUNTRIES, sns.color_palette("colorblind", 6)))
    dims = list(DIMENSIONS)
    fig, axes = plt.subplots(len(dims), 1, figsize=(9, 10), sharex=True)
    for ax, dim in zip(axes, dims):
        d = annual[annual.dimension == dim]
        for country in COUNTRIES:
            c = d[d.country == country]
            ax.plot(c.year, c.actual, color=palette[country], lw=1.6, label=country)
            ax.plot(c.loc[c.year >= 2020, "year"], c.loc[c.year >= 2020, "expected"],
                    color=palette[country], lw=1.2, ls="--")
        ax.axvline(2020, color="0.35", lw=.8); ax.axvline(2022, color="0.35", lw=.8)
        ax.set_title(dim); ax.set_ylabel("Pre-crisis standardized score")
    axes[-1].set_xlabel("Year")
    axes[0].legend(ncol=3, frameon=False, fontsize=8)
    fig.tight_layout()
    for ext in ["png", "pdf"]: fig.savefig(fig_dir / f"Figure2_ObservedExpected.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)

    heat = stage.pivot_table(index=["country", "dimension"], columns="stage", values="maintenance_gap").reset_index()
    heat["Reordering"] = heat["Price"] - heat["COVID"]
    mat = heat.set_index(["country", "dimension"])[["COVID", "Price", "Reordering"]]
    fig, ax = plt.subplots(figsize=(7, 9))
    vmax = np.nanmax(np.abs(mat.values))
    sns.heatmap(mat, cmap="vlag", center=0, vmin=-vmax, vmax=vmax, annot=True, fmt=".2f", ax=ax,
                cbar_kws={"label": "Maintenance gap"})
    ax.set_xlabel(""); ax.set_ylabel("")
    fig.tight_layout()
    for ext in ["png", "pdf"]: fig.savefig(fig_dir / f"Figure3_GapHeatmap.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)

    pm = policy.pivot_table(index=["country", "stage"], values=["price_cushioning", "targeted_support", "transition_continuity"], aggfunc="sum")
    fig, ax = plt.subplots(figsize=(7, 6))
    sns.heatmap(pm, cmap="Blues", annot=True, fmt=".0f", ax=ax, cbar_kws={"label": "Coded country-year occurrences"})
    ax.set_xlabel("Policy function"); ax.set_ylabel("")
    fig.tight_layout()
    for ext in ["png", "pdf"]: fig.savefig(fig_dir / f"Figure4_PolicyMatrix.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)


def write_excel(path: Path, sheets: dict[str, pd.DataFrame]) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        for name, df in sheets.items():
            df.to_excel(writer, sheet_name=name[:31], index=False)
        for ws in writer.book.worksheets:
            ws.freeze_panes = "A2"
            ws.auto_filter.ref = ws.dimensions
            ws.sheet_view.showGridLines = False
            for cell in ws[1]:
                cell.font = cell.font.copy(bold=True, color="FFFFFF")
                cell.fill = cell.fill.copy(fill_type="solid", fgColor="1F4E78")
            for col in ws.columns:
                letter = col[0].column_letter
                ws.column_dimensions[letter].width = min(max(10, max(len(str(c.value or "")) for c in col) + 2), 42)


def run(input_dir: str | Path, output_root: str | Path) -> None:
    random.seed(SEED); np.random.seed(SEED)
    input_dir, root = Path(input_dir), Path(output_root)
    dirs = setup_dirs(root)
    setup_logging(dirs["logs"] / "run.log")
    started = datetime.now(timezone.utc)
    core, exposure, policies = load_inputs(input_dir)
    missing = audit_core(core, dirs["data_audit"])
    direction = direction_table()
    scored, params, dims = scale_dimensions(core)
    annual, stage, fits = trend_gaps(scored, dims, 2010)
    _, stage_alttrend, _ = trend_gaps(scored, dims, 2015)
    scaled_mm, params_mm, _ = scale_dimensions(core, "minmax")
    _, stage_minmax, _ = trend_gaps(scaled_mm, dims, 2010)
    altbaseline = stage_baseline_sensitivity(scored, dims)

    loo_ind = []
    loo_variants = {}
    for dim, mapping in DIMENSIONS.items():
        if len(mapping) < 2: continue
        for var in mapping:
            s, _, ds = scale_dimensions(core, omit=(dim, var))
            _, st, _ = trend_gaps(s, ds)
            label = f"LOIO:{dim}:{var}"
            loo_variants[label] = st
            loo_ind.append(st.assign(omitted_dimension=dim, omitted_indicator=var))
    loo_ind_df = pd.concat(loo_ind, ignore_index=True)

    regional = stage.groupby(["dimension", "stage"], as_index=False).maintenance_gap.mean().rename(columns={"maintenance_gap": "all_country_mean"})
    loco = []
    for omitted in COUNTRIES:
        retained = stage[stage.country != omitted]
        assert omitted not in set(retained.country) and retained.country.nunique() == 5
        x = (retained.groupby(["dimension", "stage"], as_index=False).maintenance_gap.mean()
             .merge(regional, on=["dimension", "stage"]))
        x["omitted_country"] = omitted
        loco.append(x)
    loco_df = pd.concat(loco, ignore_index=True)

    profiles = precrisis_profiles(core, exposure)
    policy = policy_matrix(policies, stage)
    variants = {"Alternative trend window 2015-2019": stage_alttrend,
                "Alternative scaling pre-crisis min-max": stage_minmax, **loo_variants}
    robust = robustness(stage, variants)
    country_path = (stage.loc[stage.groupby(["country", "stage"]).maintenance_gap.idxmin(),
                              ["country", "stage", "dimension", "maintenance_gap"]]
                    .rename(columns={"dimension": "main_shortfall", "maintenance_gap": "gap"}))
    country_path["pathway_description"] = country_path.apply(
        lambda r: f"During {r.stage}, the largest observed trend-relative shortfall was {r.main_shortfall} ({r.gap:.2f}).", axis=1)

    direction.to_csv(dirs["clean_data"] / "01_indicator_direction_map.csv", index=False, encoding="utf-8-sig")
    params.to_csv(dirs["clean_data"] / "01_scaling_parameters.csv", index=False, encoding="utf-8-sig")
    scored.to_csv(dirs["clean_data"] / "scored_country_year_panel.csv", index=False, encoding="utf-8-sig")
    annual.to_csv(dirs["tables"] / "02_annual_actual_expected_gaps.csv", index=False, encoding="utf-8-sig")
    stage.to_csv(dirs["tables"] / "02_stage_maintenance_gaps.csv", index=False, encoding="utf-8-sig")
    stage[["country", "dimension", "Price_minus_COVID"]].drop_duplicates().to_csv(
        dirs["tables"] / "02_stage_reordering.csv", index=False, encoding="utf-8-sig")
    fits.to_csv(dirs["data_audit"] / "trend_fit_diagnostics.csv", index=False, encoding="utf-8-sig")

    main_sheets = {
        "Table1_Measurement": direction, "Table2_PreCrisisProfiles": profiles,
        "Table3_MaintenanceGaps": stage, "Table4_CountryPathways": country_path,
        "Table5_PolicyFunctions": policy, "Table6_RobustnessSummary": robust,
    }
    supp_sheets = {
        "S1_DataCoverage": missing, "S2_AlternativeScaling": params_mm,
        "S3_AnnualMaintenanceGaps": annual, "S4_AlternativeTrendWindows": stage_alttrend,
        "S5_LeaveOneIndicatorOut": loo_ind_df, "S6_LeaveOneCountryOut": loco_df,
        "S7_ExposureConstruction": profiles[["country"] + [f"pre_{x}" for x in EXPOSURES]],
        "S8_PolicyInventory": policies, "AlternativeBaselines": altbaseline,
    }
    write_excel(dirs["tables"] / "Revised_ASEAN6_Tables.xlsx", main_sheets)
    write_excel(dirs["tables"] / "Revised_ASEAN6_Supplementary_Tables.xlsx", supp_sheets)
    make_figures(annual, stage, policy, dirs["figures"])

    shortest = stage.groupby(["stage", "dimension"], as_index=False).maintenance_gap.mean()
    shortest = shortest.loc[shortest.groupby("stage").maintenance_gap.idxmin()]
    interp = ["# 修改版结果解释（中文）", "", "## 数据审计", "",
              "核心数据严格包含 ASEAN-6 的 2010–2023 年，共 84 条唯一 country-year 记录；核心指标无缺失。",
              "现有长期价格变量只有一般通胀率 Inflation，因此按预设规则命名为宏观价格压力（MacroPricePressure），不称为完整的能源价格与可负担性维度。",
              "", "## 核心结果", ""]
    for _, r in shortest.iterrows():
        interp.append(f"- {r.stage} 阶段的区域平均最大趋势相对短板为 {r.dimension}，平均维护缺口 {r.maintenance_gap:.3f}。")
    interp += ["", "## 对原结论的影响", "",
               "修改版结果不支持把 2022–2023 年的宏观价格压力称为区域首要维护短板：该维度的区域平均缺口为正，而低碳转型连续性的负缺口最大。鉴于价格侧只有一般通胀率，这一结果不能进一步推断能源可负担性没有恶化；它只说明现有长期数据不足以维持原来的强结论。",
               "", "所有维护缺口均为描述性的、基于危机前趋势的预期轨迹偏离，不构成因果反事实。政策编码仅表示功能出现与年份覆盖，不能识别政策规模、执行力度或效果。"]
    (root / "Results_Interpretation_CN.md").write_text("\n".join(interp), encoding="utf-8")
    (root / "Method_Decision_Log.md").write_text(
        "# 方法决策记录\n\n- 将旧 ETRI 拆为结果、危机前条件、暴露和政策响应四层。\n"
        "- 结果层仅保留 EnergyServiceSecurity、MacroPricePressure、LowCarbonContinuity。\n"
        "- 标准化参数仅由 ASEAN-6 pooled 2010–2019 样本估计。\n"
        "- 不运行 N=6 政策回归，不输出 p 值、置信区间或显著性星号。\n"
        "- 由于缺少至少两个覆盖充分的能源价格/负担指标，Inflation 被谨慎命名为 MacroPricePressure。\n",
        encoding="utf-8")
    manifest = {"started_utc": started.isoformat(), "finished_utc": datetime.now(timezone.utc).isoformat(),
                "seed": SEED, "python": platform.python_version(), "inputs": sorted(p.name for p in input_dir.iterdir()),
                "dimensions": DIMENSIONS, "no_policy_regression": True}
    (dirs["logs"] / "run_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    logging.info("Completed. Outputs: %s", root)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", default="source_snapshot")
    parser.add_argument("--output-root", default=".")
    args = parser.parse_args()
    run(args.input_dir, args.output_root)
