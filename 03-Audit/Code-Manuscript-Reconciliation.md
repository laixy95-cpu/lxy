---
type: audit
severity: critical
date: 2026-09-10
code: 05-Analysis/asean6_reproducible.py
tags: [audit, reproducibility, critical, eds-revision]
---

# Code ↔ manuscript reconciliation

> **The uploaded code does not implement the method the manuscript describes, and
> its own recorded conclusion is the opposite of the manuscript's headline finding.**

The most likely explanation is benign: this is an **earlier revision**, and the
newer one was not uploaded. The manuscript's own Data Availability statement
names four artefacts — panel, analysis code, **"the counterfactual specification
module"**, and the revision log — and that module is exactly what is missing here.
But until it surfaces, nothing in Tables 3, 4 (intervals), 5, 6 or 9 can be
reproduced, and **EDS may ask.**

I could not run anything: the six Excel inputs (`1 ETRI_Core data.xlsx`,
`2 crisis_exposure.xlsx`, `4 policy_response_price_cushioning.xlsx`,
`6 policy_response_extended (1).xlsx`) were not uploaded.

---

## 🔴 R1 — The script's recorded conclusion contradicts the manuscript

`asean6_reproducible.py:356` writes this into `Results_Interpretation_CN.md`:

> 修改版结果**不支持**把 2022–2023 年的宏观价格压力称为区域首要维护短板：该维度的
> 区域平均缺口为**正**，而低碳转型连续性的**负缺口最大**。

> *"The revised results do **not** support calling macro-price pressure the
> region's primary maintenance shortfall in 2022–2023: that dimension's regional
> mean gap is **positive**, while low-carbon continuity has the **largest negative
> gap**."*

| 2022–2023 | This script | The manuscript |
|---|---|---|
| Macro-price | gap **positive**, not the shortfall | **−0.767**, the headline shortfall |
| Low-carbon | **largest negative** gap | **+0.102**, above its expected path |

These are opposite findings. The string is hardcoded, so it records what the
author concluded when this version ran — it is not a stale computed artefact.

**This must be resolved before submission.** If the manuscript's numbers come
from a later specification, that specification is the reproducibility package and
this file should not ship with it. Shipping both invites a referee to run the code
and find the opposite result.

---

## 🔴 R2 — The counterfactual in code is the one the manuscript calls inadmissible

`trend_gaps()` (line 134) is the entire counterfactual engine:

```python
slope, intercept = np.polyfit(train.year, train[dim], 1)   # linear, degree 1
```

- **Linear only.** No logit, no log-linear, no pre-crisis mean. `grep` for
  `logit|np.log|expit` returns nothing.
- **Fitted on the dimension score**, `train[dim]` — which line 122 defines as the
  mean of already-standardised indicators.
- **Not indicator-level.** There is no per-indicator counterfactual anywhere.

Manuscript §3.4, Table 3 notes:

> "Counterfactuals are fitted on **raw indicator values** and standardised
> afterwards… Fitting on standardised scores is equivalent for affine forms alone
> and is **inadmissible for the log and logit forms**."

So the code does precisely what the manuscript identifies as inadmissible — and
Table 3, the paper's central methodological contribution, has no implementation.

**This also explains audit finding A4.** §3.6 promises seven robustness checks
including "a uniform linear form replaces the assignments in Table 3", but Table 8
reports six. In this code there are no per-indicator assignments to replace: the
uniform linear form *is* the main specification. The six checks in Table 8 map
exactly onto what this script computes.

**And it explains Table 3's motivating examples.** "Linear extrapolation … yields
expected access above the physical ceiling for four economies"; "linear
extrapolation implies deflation for three economies." Those are diagnoses *of this
script*. Table 3 reads as the fix that was designed after running it.

---

## 🔴 R3 — Five reported tables have no code path

`grep` over the script returns **zero** matches for `rmse`, `placebo`, `rolling`,
`backtest`, `t.ppf`, `interval`.

| Manuscript output | Producible here? | Why not |
|---|---|---|
| Table 3 — counterfactual form per indicator | ❌ | only one form exists |
| Table 4 — "95% CI" columns | ❌ | no interval computed anywhere |
| Table 4 / §4.1 — "(ratio to RMSE)" | ❌ | no RMSE computed anywhere |
| Table 5 — indicator contributions summing to the dimension gap | ❌ | no decomposition; LOIO is a different operation |
| Table 6 — country low-carbon configurations | ❌ | same |
| Table 9 — placebo p-values, rolling-origin bias/MAE/RMSE | ❌ | neither diagnostic exists |
| Fig. 3 — indicator decomposition | ❌ | `make_figures` emits 3 figures, none is this |
| Fig. 4 — placebo and backtest errors | ❌ | same |

**Producible:** Table 2 (direction map), Table 7 (policy functions), Table 8's six
rows, country-stage gaps, and Figs. 1–2 in substance.

---

## 🔴 R4 — The manuscript reinstates the statistics this revision removed

`Method_Decision_Log.md`, written by the script at line 363:

> 不运行 N=6 政策回归，**不输出 p 值、置信区间或显著性星号**
> *"Do not run N=6 policy regressions; **do not output p-values, confidence
> intervals, or significance stars**."*

That decision answers three reviewers directly (R2#5, R2#6, R4#4). **But Table 4
reports 95% confidence intervals and Table 9 reports p-values.**

This is the most dangerous item in the whole audit, because **audit finding A1 —
the paper's central uniqueness claim — is built entirely on those reinstated
intervals.** The claim that macro-price stability is "the only regional estimate
whose cross-country interval excludes zero" rests on a construct that:

1. three JCLP reviewers objected to at N = 6,
2. your own method decision log says not to produce, and
3. §3.4 itself disclaims ("carry no implication of sampling from a larger
   population" — audit **A11**).

**Recommendation:** drop the intervals and lead with the gap-to-RMSE ratio, which
is a genuine out-of-sample forecast-error scale rather than a sampling construct.
It is defensible at N = 6 in a way that a t-interval is not, it already gives you a
*unique* claim (0.86 vs 0.65 next), and it keeps faith with the revision decision
the reviewers asked for. This resolves A1, A11 and R4 in one move.

---

## 🟠 R5 — Dimension renamed in a way the reviewers may notice

Code: `MacroPricePressure`, with the decision log recording *why*:

> 由于缺少至少两个覆盖充分的能源价格/负担指标，Inflation 被谨慎命名为 MacroPricePressure
> *"Because fewer than two adequately-covered energy price/burden indicators are
> available, Inflation is cautiously named MacroPricePressure."*

Manuscript: **"Macro-price stability."**

Reviewer #2's point 3 was precisely that a dimension reduced to inflation alone
"can no longer reflect its original conceptual meaning." "Pressure" is the honest
label for a single-indicator construct; "stability" reads as a broader property.
Keep `pressure`, or justify the change explicitly.

---

## 🟡 R6 — Code carries variables the manuscript dropped

`PRECONDITIONS` (GovEffect, RegQuality, Credit, Internet, GovExp, lnGDPpc,
Diversification) and `EXPOSURES` (tourism, services, fuel imports, fossil share,
gas share) are computed into `Table2_PreCrisisProfiles` and `S7_ExposureConstruction`,
but appear nowhere in the manuscript.

Dropping them was the right response to Reviewer #2's tautology objection and
Reviewer #4's point 2. Just make sure the shipped package does not emit sheets the
paper never discusses — a referee will ask what they are and why they were cut.

---

## What to do

1. **Locate the version that produced the manuscript's numbers** — the
   "counterfactual specification module" your Data Availability names. Everything
   below is contingent on it.
2. **If it exists:** ship it, not this file. Re-run and confirm Tables 3–6 and 9.
   Then A4's missing uniform-linear check is free — *this script is that check*,
   so report what it gives.
3. **If it does not exist:** the manuscript currently describes a method that has
   not been run. Tables 3, 5, 6, 9 and Table 4's intervals and ratios would all
   need to be produced before submission. Tell me and I will implement Table 3's
   specification — logit for `AccessElec`, pre-crisis mean for `Inflation`,
   log-linear for `RenCap`, linear otherwise, fitted on raw values — plus the
   placebo, rolling-origin backtest and decomposition, against this script's
   structure.
4. **Either way, drop the confidence intervals** (R4) and lead with gap-to-RMSE.
5. **Upload the six Excel inputs** so any of this can actually be executed here.
