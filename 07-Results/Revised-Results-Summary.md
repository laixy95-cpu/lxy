---
type: results
date: 2026-09-10
spec: "3-indicator low-carbon; TDLoss log-linear (A18); Thailand inflation corrected (D1)"
tags: [results, eds-revision]
---

# Revised results — what changes, and what does not

Produced by `05-Analysis/asean6_counterfactual.py`. Three deliberate departures
from the submitted manuscript, each documented:

1. **Low-carbon uses the three indicators with complete 2010–2023 coverage**
   (`CO2IntElec`, `RenCap`, `RenElec`). `RenTFEC` and `EnergyIntensity` are SDG
   7.2.1 and 7.3.1, published only through 2022 — confirmed against *Tracking SDG7:
   The Energy Progress Report 2025* — so they cannot cover 2023 and a five-indicator
   dimension would average different indicator sets across the two years of the
   same stage.
2. **`TDLoss` switched to log-linear** (audit A18). The linear form reached −0.49%
   expected losses for Singapore by 2023.
3. **Thailand's 2022–2023 inflation corrected** to published WDI (audit D1).

Eq. (6) reconciles to 2.2e-16. No fit leaves the admissible region.

---

## The headline finding survives intact

| Dimension / stage | Revised | Submitted | Ratio to RMSE | Interval excludes 0 | Beyond every placebo | **Both** |
|---|---|---|---|---|---|---|
| Macro-price / compound | **−0.767** | −0.767 | **0.861** | ✅ | ✅ | **✅ unique** |
| Macro-price / COVID | +0.120 | +0.120 | 0.144 | — | — | — |
| Energy-service / COVID | −0.047 | −0.077 | 0.427 | ✅ | — | — |
| Energy-service / compound | −0.007 | −0.103 | 0.043 | — | ✅ | — |
| Low-carbon / COVID | +0.073 | +0.035 | 0.224 | — | ✅ | — |
| Low-carbon / compound | **+0.150** | +0.102 | 0.241 | — | ✅ | — |

- **Macro-price stability is unchanged to three decimals**, and remains the only
  estimate satisfying both criteria — the paper's central claim.
- **The stage reordering is unchanged**: −0.767 − 0.120 = **−0.887**, exactly as
  published.
- Vietnam still reverses the regional low-carbon sign when omitted
  (leave-one-country-out range −0.075 to +0.318).

## The argument gets *stronger*, not weaker

Energy-service security moves from −0.077/−0.103 to **−0.047/−0.007**, and
low-carbon from +0.035/+0.102 to **+0.073/+0.150**. Both move away from zero in the
direction the paper argues: supply held and decarbonisation continued, while prices
gave way. The compound-stage energy-service gap is now 0.043 of its own forecast
error — essentially indistinguishable from its expected path.

The asymmetry the paper is built on is therefore sharper: **0.861 against 0.043 and
0.241.**

## §4.3's conclusion is preserved

| Indicator | COVID | Compound | Role in 2022–2023 |
|---|---|---|---|
| Electricity carbon intensity | +0.012 | **+0.082** | Largest positive offset |
| Renewable electricity share | +0.019 | +0.063 | Positive offset |
| Renewable capacity per capita | +0.042 | **+0.005** | Negligible |
| **Net low-carbon gap** | **+0.073** | **+0.150** | Exact sum |

This replaces Table 5 and reproduces the section heading's claim — *"cleaner
electricity, not capacity growth"* — more cleanly than the five-indicator version,
since capacity contributes +0.005 against carbon intensity's +0.082.

## What needs rewriting

- **Table 5** → the three-row table above. Drop `RenTFEC` and `EnergyIntensity`.
- **Table 6** → recompute; the country configurations named "Renewables in final
  energy" and "Energy intensity" no longer exist in the dimension.
- **Table 4** → new gaps and ratios for energy-service and low-carbon.
- **Table 3** → `TDLoss` becomes log-linear; add negative losses to the feasibility
  check described in the notes.
- **Table 9** → five COVID placebo windows (floor 0.167) and three compound
  (floor 0.250), each named. See audit A2/A3.
- **§3.3 / Table 2** → state that the low-carbon dimension uses three indicators
  and why; remove the "complete data for all eight indicators" claim.
- **Abstract, §4.1, §5, §6** → update the energy-service and low-carbon figures.
  The macro-price figures and the −0.887 reordering are unchanged.
- **§4.4** → country configurations recomputed on the three-indicator basis.

## Country gaps, compound stage

See `tables/T4_dimension_gaps.csv`. Macro-price country values are unchanged from
the manuscript (Singapore −1.816 … Indonesia +0.016).
