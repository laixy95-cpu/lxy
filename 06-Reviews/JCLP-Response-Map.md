---
type: reviewer-response-map
journal_from: "Journal of Cleaner Production (rejected)"
journal_to: "Environment, Development and Sustainability"
reviewers: 3
date: 2026-09-10
tags: [reviews, jclp, eds-revision]
---

# JCLP reviewers → what the revision did

**Verdict: the revision answered them well.** Of 17 substantive points, 12 are
fully addressed, 4 partially, 1 reintroduced. The rewrite from "Energy Transition
Resilience Index" to a counterfactual deviation diagnostic is a direct, honest
response to the deepest objection (R2#1), not a cosmetic re-titling. Table 1 was
built to answer R2#2 and R4#3. Dropping every regression answers R2#5, R2#6 and
R4#4.

The rejection was "does not meet the required quality standards" — an editorial
desk decision on top of two *major revision*-shaped reports. **The current draft
is materially stronger than what they saw.**

Source: [[JCLP_Reviewers.txt]]

---

## Reviewer #1 — recommended major revision

| # | Point | Response | Status |
|---|---|---|---|
| 1 | ETRI mixes long-run development and macro conditions with crisis measurement; separate pre-crisis buffers, crisis-period governance and structural conditions; distinguish **resilience maintenance from structural improvement** | ETRI abandoned. Three outcome dimensions reported separately; buffers/exposures dropped entirely; §3.1 limits scope to the **resistance phase** | ✅ |
| 2 | Equal-weight robustness insufficient at small N | Table 8: min–max, alt trend window, two level baselines, LOCO, LOIO. **LOCO reported as sign-reversing when Vietnam is dropped** | ✅ strong |
| 3 | Non-overlap spec makes descriptive and regression analyses inconsistent | Moot — all regressions removed | ✅ |
| 4 | 2022–23 confounds post-pandemic recovery, base-period rebound, price transmission and policy; explain stage logic **in the main text** | §3.2 states the stage logic; §3.4 concedes Eq. (5) "does not identify the independent effect of either shock" | ⚠️ **partial** — acknowledged, not resolved. See below |

**R1#4 is still your most exposed flank.** The base-effect problem is real: a
2020–21 collapse mechanically inflates 2022–23 deviations measured against a
2010–19 path. You disclaim causal identification but never quantify the base
effect. **Cheapest fix:** report the 2022–23 gap against a counterfactual refitted
through 2021 as a sensitivity row. If the sign holds, the objection is closed.

---

## Reviewer #2 — the deepest report

| # | Point | Response | Status |
|---|---|---|---|
| 1 | **Conceptual**: ETRI is a static performance measure, not resilience. A decline under shock says nothing about resilience; a resilient country can still decline. Resilience is an intrinsic capacity over the whole shock–response process | Fully conceded. The paper no longer claims to measure resilience — it measures **deviation from an expected path**, names it a "maintenance gap", and §3.1 restricts to resistance. Title says "shortfall", not "resilience" | ✅ **exemplary** |
| 2 | Add a **measurement-level** comparison against existing resilience index systems | **Table 1** — approach × what the number measures × benchmark × phase × constraint. Built for this objection | ✅ |
| 3 | Non-overlap degenerates AFF to inflation alone; "without changing the conceptual meaning" cannot be sustained | Dimension is now openly single-indicator, and §3.6/§4.1 add the **gap-to-RMSE ratio** precisely so a 1-indicator and a 5-indicator dimension can be compared | ✅ clever |
| 4 | Buffer-variable mechanisms too thin | Buffers removed from the manuscript | ✅ by removal |
| 5 | N = 6 stage-level regressions have no power; policy coding cannot capture scale, duration, coverage, cost, targeting or implementation | Regressions removed. §3.5 and §4.5 state the coding limits in almost the reviewer's own words | ✅ |
| 6 | Table 6's CIs implausibly narrow; **HC1 SEs wrong for small samples** | Regressions removed — **but 95% CIs return in Table 4 and p-values in Table 9** | 🔴 **reintroduced** |

**R2#6 is the trap.** This reviewer scrutinised your interval widths and found them
anomalous. The revision removed the regressions but re-added Student-t intervals
across six country values — and your headline claim now depends on one of them
(audit **A1**). Your own `Method_Decision_Log.md` says not to output confidence
intervals. See [[../03-Audit/Code-Manuscript-Reconciliation#R4]]. **Drop the
intervals; lead with gap-to-RMSE.**

---

## Reviewer #4

| # | Point | Response | Status |
|---|---|---|---|
| 1 | Case-selection justification too brief | §2.3 expanded; import-exposure spread from Singapore to Indonesia | ✅ |
| 2 | Buffer–resilience link tautological (GovExp, lnGDPpc already part of the construct) | Buffers removed | ✅ |
| 3 | Differentiate indicators from established ETI frameworks | Table 1 + OECD/JRC contrast | ✅ |
| 4 | With six countries, downplay statistical inference to exploratory/diagnostic | Done throughout — except the reinstated intervals (R2#6) | ⚠️ |
| 5 | Methodology **overly lengthy**; shorten | §3 is still ~1,900 words across six subsections | ⚠️ **not addressed** |
| 6 | Policy mix reduced to two categories is too simplistic; explore why instruments align with different dimensions | Now **three** functions; §5.2–5.5 map instruments to diagnosed constraints | ✅ |
| 7 | Professional English editing; abstract's first sentence too long | Opening rewritten to "Crises test energy systems on three fronts at once…" — clear improvement | ✅ |

**R4#5 aligns with your EDS length problem.** You must cut ~500 words anyway
(audit **A9**). Cutting §3 answers a reviewer *and* meets the limit — but §3 is
also where your contribution lives. **Better: cut Introduction ¶2–¶4**, which
duplicate §2 citation-for-citation, and use some of the space to *tighten* §3
rather than shorten it. Then say in the cover letter that the methodology was
reorganised for concision.

---

## Still open

1. 🔴 **R2#6 / R4#4** — confidence intervals reinstated against the reviewers' advice and your own decision log.
2. ⚠️ **R1#4** — base-effect confounding acknowledged but never quantified. One sensitivity row closes it.
3. ⚠️ **R4#5** — methodology still long.
4. ⚠️ **R2#1 residual** — the paper concedes it measures resistance only, but the *title* still says "energy systems … shortfall" and §5 draws preparedness conclusions (§5.4) that reach beyond resistance. Keep §5.4's claims inside what a resistance-phase measure can support — especially given the Vietnam problem ([[../03-Audit/Needs-Verification#NV1]]).

---

## For the EDS cover letter

State the JCLP history plainly and turn it into evidence of rigour:

> An earlier version of this work was reviewed at *Journal of Cleaner Production*.
> Reviewers raised a fundamental conceptual objection — that an index-based
> measure of transition performance cannot be interpreted as resilience — together
> with concerns about statistical inference at N = 6. We accepted both. The
> present manuscript abandons the composite index, measures crisis-period
> performance as deviation from each country's own pre-crisis trajectory, reports
> the three dimensions separately rather than aggregating them, removes all
> regression analysis, and bounds every estimate by the forecast error of its own
> benchmark. Table 1 sets out the measurement-level comparison with existing
> resilience index systems that reviewers requested.

That paragraph converts a rejection into a demonstrated revision history. Do not
hide it — EDS editors respond well to authors who can show what they changed and why.
