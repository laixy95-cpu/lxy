# Analysis code

## What is here

| File | Status | Purpose |
|---|---|---|
| `counterfactual_spec.py` | **new** | The Table 3 specification module — the component named in Data Availability and absent from the original code |
| `asean6_counterfactual.py` | **new** | Full pipeline: Eqs. (1)–(6), rolling-origin backtest, placebo windows, seven robustness variants, gap-to-RMSE |
| `validate_against_manuscript.py` | **new** | Compares output against every value printed in the manuscript |
| `make_synthetic_panel.py` | **new** | Fabricated panel for smoke-testing only — **never report its numbers** |
| `asean6_reproducible.py` | author's | Original script. Uniform linear fit on standardised dimension scores |
| `ASEAN6_Revised_Reproducible_Analysis.ipynb` | author's | Colab wrapper around the original |
| `build_colab_notebook.py`, `inspect_inputs.py` | author's | Notebook builder and input auditor |

## Run it

```bash
pip install numpy pandas scipy openpyxl

# 1. smoke test — proves the machinery works, numbers are fake
python3 make_synthetic_panel.py
python3 asean6_counterfactual.py --input-dir synthetic_inputs --output-root smoke

# 2. the real thing
python3 asean6_counterfactual.py --input-dir <dir with the six xlsx> --output-root out

# 3. do the manuscript's numbers survive?
python3 validate_against_manuscript.py --input-dir <dir with the six xlsx>
```

`--with-intervals` adds Student-t cross-country intervals. **Off by default**, because
JCLP Reviewer #2 point 6 objected to them and `Method_Decision_Log.md` says not to
produce them — see [[../03-Audit/Code-Manuscript-Reconciliation#R4]].

## What this fixes

**Table 3 is now implemented.** Counterfactuals are fitted on **raw** indicator
values over a trailing window and standardised afterwards, per Eq. (3) — logit for
`AccessElec`, pre-crisis mean on 2015–2019 for `Inflation`, log-linear for `RenCap`,
linear otherwise. The original code fits one linear trend to already-standardised
dimension scores, which §3.4 calls "inadmissible for the log and logit forms".

**The feasibility gate from the Table 3 notes is enforced** — expected access above
100%, negative capacity, implied deflation below −1% all raise. Verified: on a
series pinned at the ceiling, the logit form predicts 99.998 while the linear form
predicts 100.47 and the gate fires. That is the manuscript's own motivating example,
now reproducible rather than asserted.

**Audit A4 — the missing robustness check — is available.** `uniform_linear_specs()`
supplies the seventh variant §3.6 promises and Table 8 omits. It is also exactly what
`asean6_reproducible.py` uses as its *main* model, so reporting it reconciles the two
code bases in one row.

**Audit A5 — the gap-to-RMSE denominator — is explicit.** `RATIO_RULE` fixes it as
the mean of the two horizon RMSEs a stage spans (h=1,2 for COVID; h=3,4 for compound),
the only rule under which all six printed ratios reproduce.

**Audit A2 — the placebo window count — is settled.** `placebo_window_geometry()`
enumerates admissible windows from the year grid alone:

| min. training obs | COVID windows | Compound windows |
|---|---|---|
| 3 | 6 | 4 |
| **4** | **5** | **3** |
| 5 | 4 | 2 |
| 6 | 3 | 1 |

§3.6's "five and three, floors 0.167 and 0.250" is reproduced by, and only by, a
four-observation minimum — so §3.6 is internally consistent and is the default here.
§4.6 and Table 9's "three windows for each stage, floor 0.250" is produced by **no**
rule. **Keep §3.6; correct §4.6 and Table 9.** Every window is now reported by name,
which fixes A3.

**Eq. (6) reconciliation is asserted, not assumed.** `decomposition_audit.csv` carries
the residual; the smoke test returns 2.8e-17.

## Conventions you should know about

- **Trailing-window rule.** At origin *o* a spec trains on `[o − window_len + 1, o]`,
  clipped at 2010. At *o* = 2019 that is 2010–2019 for the ten-year specs and
  2015–2019 for `Inflation`, reproducing the main specification exactly — and the
  same rule then defines every rolling-origin refit. The manuscript does not state
  how `Inflation`'s shorter window behaves under backtesting; this is the natural
  reading, and it is recorded in the run manifest.
- **Logit clamping.** Access shares are published as exactly 100.0, and logit(1) is
  undefined, so values are clamped into (1e−4, 1−1e−4). This materially affects the
  fitted slope for economies already at the ceiling. `T3_fit_diagnostics.csv` reports
  `clamped_points` per country-indicator — **check it**, and treat `EPS_SHARE` as a
  sensitivity parameter, not a constant.
- **Backtest horizon counts are unbalanced** by construction (h=1 has five origins,
  h=4 has two), since every evaluation year must stay inside 2010–2019. `n` is
  reported per horizon.

## Still needed

The six Excel inputs — `1 ETRI_Core data.xlsx`, `2 crisis_exposure.xlsx`,
`4 policy_response_price_cushioning.xlsx`, `6 policy_response_extended (1).xlsx`.
Only `1 ETRI_Core data.xlsx` is required by this pipeline; the policy workbooks feed
Table 7, which the original script already produces correctly.
