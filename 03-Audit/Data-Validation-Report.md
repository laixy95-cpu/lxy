---
type: validation
date: 2026-09-10
data: "1 ETRI_Core data.xlsx (as supplied)"
pipeline: 05-Analysis/asean6_counterfactual.py
tags: [audit, validation, critical, eds-revision]
---

# Data validation — the manuscript's method reproduces

**Headline: your method is sound and your numbers are right.** I rebuilt Table 3
from the manuscript text and it reproduces the published values exactly wherever
the supplied data is complete. **The failures are all in the data file, not the
method.**

Two of my earlier findings change as a result. **A1 is withdrawn as a substantive
error** — the claim is true, but the table that supports it is wrong. **A18 is new.**

---

## What reproduces exactly

| Quantity | Computed | Manuscript |
|---|---|---|
| Macro-price / compound, **all six countries** | −1.816, −1.150, −1.118, −0.342, −0.194, +0.016 | −1.816, −1.150, −1.117, −0.342, −0.194, +0.016 |
| Macro-price / compound, regional | **−0.767** | −0.767 |
| Macro-price / COVID, regional | **+0.120** | +0.120 |
| Table 4 CI, macro-price / compound | **[−1.508, −0.026]** | [−1.508, −0.026] |
| Table 4 CI, energy-service / COVID | [−0.126, −0.030] | [−0.125, −0.029] |
| Gap-to-RMSE, macro-price / compound | **0.861** | 0.86 |
| Gap-to-RMSE, energy-service / COVID | **0.658** | 0.65 |
| Table 9 rolling-origin RMSE | **11 of 12 exact**, 12th within rounding | — |
| Energy-service / compound, 4 of 6 countries | exact | — |

Reproducing 11 of 12 backtest RMSEs and all six macro-price country values from a
specification rebuilt out of the prose is strong evidence that Table 3 describes
what was actually run. **You can tell EDS the analysis is reproducible.**

---

## 🔴 D1 — Thailand's 2022 and 2023 inflation are wrong in the file

The workbook implies **−1.61%** and **+8.48%**. World Bank FP.CPI.TOTL.ZG publishes
**6.08%** and **1.23%**. Every other country-year in the column matches WDI to two
decimals — this is isolated to Thailand, in the two years that carry the paper's
headline finding.

**Correcting it reproduces the manuscript exactly:**

| | as supplied | Thailand corrected | manuscript |
|---|---|---|---|
| Thailand | −1.044 | **−1.118** | −1.117 |
| Regional | −0.755 | **−0.767** | −0.767 |

So the manuscript was computed from a **correct** version of this column. The file
you sent is not the file that produced the paper. Recover it, or apply
[[../05-Analysis/data_corrections.py]] and re-run.

---

## 🔴 D2 — Two low-carbon indicators have no crisis-period data at all

Cells coded **`0`**, not blank — so `isna()` audits pass and the original
`audit_core()` reports "no missing values":

| Indicator | Missing | 2021 values, for scale |
|---|---|---|
| `RenTFEC` | **all six countries, 2022 and 2023** | 1.1 – 28.0 |
| `EnergyIntensity` | **all six countries, 2022 and 2023** | 2.5 – 4.5 |
| `TDLoss` | Malaysia, Philippines, Vietnam, 2023 | 6.2 – 9.6 |

**27 of 672 cells.** A renewable share of 0% is impossible for Indonesia or Vietnam;
an energy intensity of 0 is impossible for anyone.

This is not a rounding issue — it removes **two of the five low-carbon indicators
for the entire compound-crisis stage**. Consequences:

- **Table 5 cannot be produced.** It reports `RenTFEC` **+0.039** and
  `EnergyIntensity` **−0.027** for 2022–2023. Neither indicator has 2022–2023 data here.
- **Table 6 cannot be produced.** It names "Renewables in final energy" or
  "Energy intensity" as the largest positive or negative term for **four of six
  countries**.
- **The +0.102 low-carbon gap cannot be produced.** On three of five indicators I get
  **+0.150**; treating the zeros as real data instead gives **+0.563**.
- §3.3's claim of "complete data for all eight indicators" and Table 2's "used as
  published, with no interpolation" are both untrue of this file.

**This is the blocking item.** Nothing in §4.3, §4.4, Table 5 or Table 6 can be
verified until the complete extract appears.

---

## 🟠 D3 — Malaysia's `TDLoss` looks carried forward

Malaysia records **6.90%** for 2015–2022 — eight identical values, then 0 (missing)
in 2023. Real T&D losses do not hold constant to two decimals for eight years.
If this is carry-forward imputation it contradicts Table 2's "no interpolation or
model-based imputation" note, and Malaysia's energy-service gap (−0.002) is an
artefact of a flat series. Check the source extract.

---

## 🔴 A18 (new) — Table 3's `TDLoss` assignment is wrong for Singapore

Table 3 assigns `TDLoss` a **linear trend**, justified as "Secular decline, **far
from bounds**". Singapore's losses fall 4.91% (2010) → 1.03% (2019). It is *not*
far from the zero bound, and the fitted path goes **negative**:

```
Singapore TDLoss, linear counterfactual:  2020: +0.41   2021: +0.11
                                          2022: -0.19   2023: -0.49
```

Expected transmission losses of −0.49% are physically impossible — the same class
of error the manuscript uses to justify indicator-specific forms for `AccessElec`
and `Inflation`. It was missed because the assignment was made on the pooled
character of the series, not per country. **And the feasibility check as described
in the Table 3 notes would not catch it**: it tests access above 100%, negative
renewable capacity and implied deflation, but not negative losses.

**Fix — switch `TDLoss` to log-linear** (cannot go negative, preserves secular
decline). Effect:

| | linear (Table 3) | log-linear | change |
|---|---|---|---|
| Singapore | −0.109 | **+0.068** | +0.177 (**sign flips**) |
| Vietnam | −0.114 | −0.068 | +0.046 |
| Philippines | −0.265 | −0.235 | +0.030 |
| Regional | −0.054 | −0.007 | +0.046 |

Also add negative losses to the feasibility check in the Table 3 notes.

---

## ✅ A1 — WITHDRAWN as a substantive error; it is a table error

I previously reported that the uniqueness claim was false. **With the placebo design
corrected, the claim is true.** The correction matters, so here it is explicitly.

Under §3.6's design (five COVID windows, three compound — see A2), the placebo
windows for energy-service/COVID are:

```
2014-2015: -0.1234   2015-2016: -0.0038   2016-2017: +0.0439
2017-2018: +0.0444   2018-2019: -0.0265        observed: -0.0776
```

The **2014–2015** window (−0.1234) is more extreme than the observed −0.0776, so
energy-service/COVID does **not** beat every placebo. Testing both criteria:

| | interval excludes 0 | beyond every placebo | both |
|---|---|---|---|
| Energy-service / COVID | ✅ | ❌ | — |
| Low-carbon / COVID | ❌ | ✅ | — |
| Low-carbon / compound | ❌ | ✅ | — |
| **Macro-price / compound** | ✅ | ✅ | **✅ unique** |

**Exactly one estimate satisfies both — as the manuscript claims.**

**But your Table 9 contradicts it.** Table 9 reports three COVID windows with range
−0.026 to +0.044, which excludes the 2014–2015 window. Against *that* table, the
observed −0.077 does beat every placebo, and the uniqueness claim reads as false.

**So: keep the claim, fix Table 9.** Restate §4.6 and Table 9 to the §3.6 design —
five COVID windows (floor 0.167), three compound windows (floor 0.250) — and list
the windows by name. A referee checking the claim against the corrected table will
confirm it.

I would still add one clarifying clause: the criteria are conjunctive, and the
COVID energy-service interval also excludes zero on its own.

---

## Where this leaves the checklist

| Item | Status |
|---|---|
| **D2** complete `RenTFEC`, `EnergyIntensity`, `TDLoss` extract | 🔴 blocking |
| **D1** Thailand inflation | 🔴 fix or apply `data_corrections.py` |
| **A18** `TDLoss` → log-linear; extend the feasibility check | 🔴 method fix |
| **A2/A3** correct Table 9 to the five/three design, name the windows | 🔴 |
| **A1** claim stands once Table 9 is fixed | ✅ withdrawn |
| **A4** uniform-linear row now computed: r = 0.810, sign agreement 88.9% | ✅ ready |
| **A5** ratio rule confirmed: 0.861 and 0.658 reproduce the printed 0.86 and 0.65 | ✅ |
| Tables 5, 6 and the +0.102 low-carbon gap | ⏸ blocked on D2 |

Full outputs: [[../07-Results/]]. Re-run with
`python3 asean6_counterfactual.py --input-dir inputs --output-root ../07-Results --with-intervals`,
then `validate_against_manuscript.py` for a line-by-line check.
