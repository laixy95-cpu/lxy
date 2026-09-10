---
type: audit
manuscript: Manuscript_EDS_Full.docx
target: "Environment, Development and Sustainability (Springer, 10668)"
date: 2026-09-10
arithmetic_checks: 23
arithmetic_passed: 23
tags: [audit, eds-revision, critical]
---

# Internal consistency audit

**Headline: the arithmetic is sound.** All 23 recomputation checks in
[[../scripts/verify_numbers.py]] reproduce the printed values — regional means,
Student-t intervals, decomposition sums, leave-one-out ranges, stage-reordering
deltas and the cross-country spread. A reviewer who recomputes your tables will
find them correct. **Every problem below is interpretive, structural, or
editorial — none is a calculation error.** That is a strong position to revise from.

Severity: 🔴 critical (blocks submission) · 🟠 major (reviewer will raise it) · 🟡 minor (copy-edit)

---

## ✅ A1 — WITHDRAWN. The claim is true; the table supporting it is wrong

I first reported the uniqueness claim as false. **Running the rebuilt pipeline on
the real data shows it is true** — see [[Data-Validation-Report#A1]].

Under §3.6's placebo design (five COVID windows — see A2) the energy-service/COVID
window **2014–2015** returns −0.1234, more extreme than the observed −0.0776. So
energy-service/COVID does not beat every placebo, and testing both criteria
together leaves exactly one estimate — macro-price/compound — as the manuscript says.

**But Table 9 as printed contradicts it**: it reports three COVID windows spanning
−0.026 to +0.044, which omits the 2014–2015 window. Against that table the claim
reads as false, and that is the table a referee will check.

**Action: keep the claim, fix Table 9** (see A2/A3). Add one clause noting the
criteria are conjunctive and that the COVID energy-service interval also excludes
zero on its own.

---

## 🔴 A18 — Table 3's `TDLoss` assignment produces negative losses for Singapore

`TDLoss` is assigned a linear trend as "Secular decline, far from bounds", but
Singapore falls 4.91% → 1.03% over 2010–2019 and the fitted path reaches
**−0.19% in 2022 and −0.49% in 2023**. The feasibility check described in the
Table 3 notes tests access, capacity and deflation — **not negative losses** — so
it does not fire.

Switching to log-linear removes the infeasibility and moves Singapore's
energy-service gap from −0.109 to **+0.068** (sign flip); regional −0.054 → −0.007.
Full table in [[Data-Validation-Report#A18]].

---

## 🔴 A17 — §2.4 contradicts both §5.1 and Table 7 on Singapore

- §2.4: "**All six economies** manage domestic energy prices through combinations
  of fuel subsidies, electricity tariff caps, and price-smoothing funds."
- §5.1: "Singapore … **with no fuel subsidy regime**."
- §5.2: price cushioning "**absent only in Singapore**."
- Table 7: Singapore price cushioning = **0**.

§2.4 is the odd one out and must be corrected — Singapore's electricity market is
liberalised with half-hourly wholesale pricing. This matters more than a wording
slip: Singapore is your largest single observation (−1.816) and §5.1 explains it
precisely *by* the absence of a buffer. Leaving §2.4 as-is destroys that mechanism.

**Fix:** "Five of the six economies manage domestic energy prices through
subsidies, tariff caps or price-smoothing funds; Singapore passes wholesale
prices through to consumers."

---

## 🟠 A2 — Methods and Results disagree on the number of placebo windows — **RESOLVED**

| | Placebo windows | p-value floor |
|---|---|---|
| §3.6 (L127) | **5** at COVID horizon, **3** at compound | "0.167 and 0.250 as its respective floors" |
| §4.6 (L232) + Table 9 | **3** for each stage | 0.250 everywhere |

**Settled by construction.** The number of admissible placebo windows depends only
on the year grid and the minimum training length, not on the data
(`placebo_window_geometry()` in [[../05-Analysis/asean6_counterfactual.py]]):

| min. training obs | COVID | Compound |
|---|---|---|
| 3 | 6 | 4 |
| **4** | **5** | **3** |
| 5 | 4 | 2 |
| 6 | 3 | 1 |

§3.6's counts and both its floors — 1/(5+1) = 0.167 and 1/(3+1) = 0.250 — are
reproduced by, and only by, a **four-observation minimum**. §4.6's "three for each
stage" is produced by **no** rule: the design cannot give three at both horizons.

**Therefore §3.6 is correct and §4.6 plus Table 9 are wrong.** Restate §4.6 as five
COVID windows (floor 0.167) and three compound windows (floor 0.250), and correct
Table 9's floor column accordingly.

Also fix the literal gap in §3.6: "With&nbsp;&nbsp;windows the smallest attainable
p-value is 1/(k + 1)" — the *k* is missing.

## 🟠 A3 — Table 9 prints the same placebo window for every row

All six placebo rows read "2016–2018", yet §4.6 states COVID placebos use a
one-year first horizon and compound placebos a three-year first horizon. Windows
at different horizons cannot all be 2016–2018, and "three windows" cannot be
represented by one label. List the actual windows per row (e.g. 2014–2015,
2015–2016, 2016–2017) and the origin each was fitted from.

---

## 🟠 A4 — A promised robustness check is never reported

§3.6: "**Seven** alternative specifications… **A uniform linear form replaces the
assignments in Table 3.**"

Table 8 reports six: min–max, 2015–2019 window, 2017–2019 mean, 2019 level,
leave-one-country-out, leave-one-indicator-out. **The uniform-linear check is
missing** — and it is the most important one in the paper, because matching the
counterfactual form to each indicator *is* your methodological contribution.
Its absence is exactly where a referee will push.

**Fix:** run it and add the row. If a uniform linear form materially changes the
result, that is a *positive* finding that justifies your design. If it does not,
you have cheaply defused the obvious objection. Either way, report it.

---

## 🟠 A5 — The gap-to-RMSE denominator is not defined reproducibly

§3.6 says each gap is compared against "the root mean squared error **at the
horizon its stage spans**" (singular). But a stage spans *two* horizons, and the
printed ratios reproduce only under the **mean of both**:

| Dimension / stage | ÷ single RMSE (h=2 / h=4) | ÷ mean of two horizons | Printed |
|---|---|---|---|
| Service / COVID | 0.56 | **0.65** | 0.65 |
| Service / compound | 0.48 | **0.53–0.54** | 0.54 |
| Price / COVID | 0.15 | **0.14** | 0.14 |
| Price / compound | 0.79 | **0.86** | 0.86 |
| Low-carbon / COVID | 0.12 | **0.14** | 0.14 |
| Low-carbon / compound | 0.18 | **0.23** | 0.23 |

Six of six reproduce under the mean; none under a single horizon. Since the
gap-to-RMSE ratio now carries your headline claim (see A1), state the convention
explicitly in §3.6: *"each stage gap is scaled by the mean rolling-origin RMSE
across the two horizons the stage spans (h = 1–2 for 2020–2021, h = 3–4 for
2022–2023)."*

---

## 🟠 A6 — Duplicate reference entry

The reference list contains the same paper twice:

- `Zhang, C., Su, Y., … (2026). A critical review and future perspectives… RSER, 233, 116814.`
- `Zhang, C., Su, Y., … (2026a). A critical review and future perspectives… RSER, 233, 116814.`

Identical authors, title, journal, volume, article number. §1 cites the
undifferentiated "Zhang et al. 2026"; §2.5 and Table 1 cite "2026a".
**Delete the unsuffixed entry and change the §1 citation to 2026a.**
Verified live: RSER, published February 2026, article 116814.

---

## 🟠 A9 — Over both EDS length limits

| | Manuscript | EDS limit |
|---|---|---|
| Abstract | **264 words** | 150–250 |
| Main text (excl. tables & refs) | **7,515 words** | ~7,000 |
| Keywords | 6 | 4–6 ✅ |

Abstract needs ≥14 words cut; body needs ~500. See
[[EDS-Compliance-Checklist]] for where to cut without losing substance.

---

## 🟠 A10 — Table 8 mixes two denominators in one column

"sign match = 100%" and "88.9%" are computed over **36** country × dimension ×
stage gaps. "50.0%" and "66.7%" are computed over **6** country low-carbon gaps
only. Same column, different bases, no label. A reader comparing 88.9% against
50.0% is comparing different things. Label each rate with its denominator.

---

## 🟡 A8 — Mixed US/UK spelling of the same words

| US form | Line | UK form used elsewhere |
|---|---|---|
| periodi**z**ation | 57 | periodi**s**ation — §3.2 heading, L64 |
| standardi**z**ed / standardi**z**ation | 136, 174 | standardi**s**ed (×7) |
| organi**z**ed | 17 | — |
| characteri**z**ed | 136 | — |

`periodization` (L57) and `periodisation` (L64) are seven lines apart. EDS follows
UK convention; unify to *-ise/-isation*. Leave cited article titles as published
(e.g. Zhang et al.'s "optimize").

---

## 🟡 A11 — Student-t intervals described as not inferential

§3.4: intervals "summarise cross-country dispersion and **carry no implication of
sampling from a larger population**." But a Student-t interval *is* a
sampling-theory construct; using one while disclaiming its basis invites the
objection. Either call them descriptive dispersion ranges (mean ± t·SE labelled
as such, no "95% CI" header in Table 4), or keep the CI and own the assumption.
The current halfway position is the weakest option.

---

## 🟡 A12 — Section 5 summary is stranded inside §5.7 Limitations

The paragraph beginning "In summary, the ASEAN-6 met two consecutive shocks…"
summarises the whole of Section 5 but sits inside the Limitations subsection.
Promote it to §5.8 (Synthesis), or move it above §5.7.

---

## 🟡 A13 — Reference-list formatting

- "**Al** Irsyad" in the reference list vs "**al** Irsyad" in §2.4 text.
- The al Irsyad entry uses "**et al.**" in the reference list — Springer requires
  full author lists in references.

---

## 🟡 A14 — Unresolved placeholders

- "¹ Affiliation to be completed by the authors."
- "Funding  To be completed by the authors."
- No corresponding author marked, no ORCID iDs.

---

## 🟡 A15 — Data availability statement understates what you have

Current: "available from the corresponding author on request." But the paper
promises a "reproducibility package" four separate times, and its entire claim to
credibility is that every magnitude is bounded by a reproducible backtest.
Deposit the panel, code and revision log (Zenodo/OSF) and cite the DOI. On-request
availability is increasingly declined at Springer and wastes your strongest asset.

---

## 🟡 A16 — Rounding note

The service/compound ratio prints 0.54; recomputing from the rounded gap (−0.103)
gives 0.534 → 0.53. It reproduces as 0.54 only from the unrounded −0.10350. State
that ratios are computed from unrounded values.
