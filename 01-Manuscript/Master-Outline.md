---
type: master-outline
manuscript: "Sequential crises reorder the dominant shortfall in energy systems: counterfactual evidence from ASEAN-6, 2010–2023"
authors: "Tie Wei; Xiao Ying Lai"
target: "Environment, Development and Sustainability (Springer, 10668)"
prior_submission: "Journal of Cleaner Production — rejected"
date: 2026-09-10
tags: [outline, eds-revision, master]
---

# Master outline — every section, every citation, every action

Legend — **P1** load-bearing · **P2** supporting · **P3** contextual · **P0** data source
🔴 blocks submission · 🟠 referee will raise it · 🟡 copy-edit · ✅ verified sound

Companion notes: [[../03-Audit/Internal-Consistency-Audit]] ·
[[../03-Audit/Needs-Verification]] · [[../03-Audit/EDS-Compliance-Checklist]] ·
[[../02-Literature/_Index]]

---

## The one-paragraph diagnosis

The measurement machinery is **sound** — 23/23 recomputation checks pass, the
decompositions reconcile exactly, and the sensitivity analysis is unusually
honest. What is weak is the **framing**: the paper's uniqueness claim is
contradicted by its own Table 4 (A1), one robustness check it promises is never
reported (A4), and its flagship policy narrative rests on a mis-attributed
Vietnamese policy (NV1). None of these require new analysis beyond one re-run.
Fix the framing and this is a defensible EDS paper. Leave it and a referee finds
A1 in the abstract on first read.

**On the JCLP rejection.** Nothing here reads as a data or execution failure. The
likely objection was *contribution*: "a descriptive deviation measure on N = 6,
where no gap exceeds its own forecast error." That objection is not answered by
more hedging — the current text hedges a great deal already. It is answered by
stating positively what the method *delivers* that composite indices cannot, and
by making the negative results (COVID null; capacity growth not crisis-driven)
into findings rather than apologies. See §Reframing at the end.

---

## Title & front matter

**Current:** "Sequential crises reorder the dominant shortfall in energy systems:
counterfactual evidence from ASEAN-6, 2010–2023"

- ✅ Good: names mechanism, method and scope; "shortfall" is honest where
  "resilience" would overclaim.
- 🟡 "reorder" implies a sequence of ≥3 states; you observe two stages and one
  transition. "shifts" is the defensible verb.
- 🔴 **A14** — placeholders live: "Affiliation to be completed", "Funding: To be
  completed", no corresponding author, no ORCID. EDS requires ORCID for the
  corresponding author.

**Action:** resolve placeholders; consider *"Sequential crises shift the dominant
shortfall in energy systems: counterfactual evidence from ASEAN-6, 2010–2023"*.

---

## Abstract — 🔴 rewrite required

**264 words; EDS allows 150–250.** Two problems, one fatal.

🔴 **A1.** "the only regional estimate whose cross-country interval excludes
zero" — false. Energy-service/COVID (−0.077, CI [−0.125, −0.029]) also excludes
zero *and* also lies below every placebo window. Replace with the claim that
**is** unique and that you have already computed: macro-price/compound has the
largest gap-to-RMSE ratio of all six cells (0.86 vs 0.65 next).

🟠 Cut ≥14 words. Candidates, in order — they cost nothing:
- "The counterfactual form is matched to each indicator's data-generating process,
  since linear extrapolation of bounded or mean-reverting series produces expected
  values outside the feasible region." → keep the first clause only (−17 words).
- "Within the low-carbon dimension, the carbon content of electricity contributed
  +0.049 and renewable capacity +0.003." → this decomposition detail is not what a
  reader needs in an abstract (−17 words).

**Keep** the last sentence ("Crisis preparedness in the region can concentrate on
price transmission") — a concrete, falsifiable takeaway is exactly what the JCLP
reader found missing.

---

## 1. Introduction — 🟠 restructure, this is where your 500 words are

**Cites 28 of 42 references** (P1: Fan, Guan, Jasiūnas, Monie, Nijsse, OECD/JRC,
Roege, Schmitz, Zakeri, Zhang 2026a, Zhang 2026b · P2: Crnčec, D'Orazio, Evro,
Horbach & Rammer, Jaeger-Erben, Li, Mersch, Quitzow, Tian · P3: Aleluia, Bai,
Fahim, Hu & Weng, Jindal, Kilinc-Ata, Kim, Zhong).

That is a literature review, not an introduction, and it **duplicates Section 2
almost citation-for-citation**. ¶2 ≈ §2.2, ¶4 ≈ §2.3, ¶3 ≈ §2.6.

**Action:** compress ¶2–¶4 to roughly one paragraph, keeping only the P1 anchors
(Zakeri, Guan, Nijsse, OECD/JRC, Monie, Schmitz) plus one regional cite (Bai or
Aleluia). Push the rest into Section 2, which already carries them. **This alone
clears the 7,000-word limit** and sharpens the opening.

| Beat | Keep? | Citations | Note |
|---|---|---|---|
| ¶1 two shocks in three years | ✅ keep | Zakeri 2022 (P1), Guan 2023 (P1) | Best paragraph in the paper — poses the question in four sentences |
| ¶2 existing work reports levels | 🔻 compress | 10 refs | Move to §2.2 |
| ¶3 secular trends confound levels | ✅ **keep and expand** | Nijsse 2023 (P1), OECD/JRC 2008 (P1) | **This is the paper's reason to exist.** Give it the space you take from ¶2 |
| ¶4 resilience gives the reference point | ✅ keep | Roege, Jasiūnas, Monie, Zhang 2026a, Fan, Schmitz, Zhang 2026b | Fix "Zhang et al. 2026" → **2026a** (A6) |
| ¶5 ASEAN setting | 🔻 compress | 8 refs | Keep the Singapore-importer / Indonesia-exporter contrast; move the rest to §2.3 |
| ¶6 what this study does | ✅ keep | — | Concrete and well written |
| ¶7 three contributions | ✅ keep | — | See reframing note below |
| ¶8 roadmap | ✅ keep | — | 🟡 "organized" → "organised" (A8) |

🟠 **Contribution 3 currently reads as an apology**: "Because none of the regional
gaps exceeds the corresponding forecast error … the findings are interpreted as
descriptive diagnostics rather than causal estimates." Invert it: *reporting each
gap against the forecast error of its own benchmark is a **standard the field does
not currently meet** — most composite-index work reports no benchmark uncertainty
at all (your own §2.5 says so).* Same fact, and it becomes a contribution.

---

## 2. Literature review

### 2.1 Crisis conditions and transition trajectories
P1: Zakeri · P2: Hussain, Jaeger-Erben, Quitzow. ✅ Tight, well-argued, competing-channels framing is right. No action.

### 2.2 Evidence from COVID-19 and 2022–2023
P1: Guan · P2: Crnčec, D'Orazio, Evro, Horbach & Rammer, Jaeger-Erben, Li, Mersch, Tian, Xu & Sharma.
- ✅ Good geographic honesty ("concentrates on Europe, China, India, and other OECD economies") — this is your gap, state it once here and once in §2.6 only.
- 🟠 **Quitzow et al. (2021) finds COVID *deepened* divergence; you find no measurable COVID shortfall.** Reconcile explicitly rather than citing them side by side — your dimensions are national outcomes, theirs is investment. That distinction *is* a finding.
- 🟡 Xu & Sharma cited only here — fine, but it earns nothing.
- 🔍 **NV8** Horbach & Rammer: confirm final volume/issue; DOI stem says 2025.

### 2.3 Energy transition and crisis exposure in Southeast Asia
P3: Aleluia, Bai, Fahim, Hu & Weng, Kim, Safrina & Utama, Zhong.
- 🟠 **Bai et al. (2023) is the ASEAN composite-index paper your method is defined against** and it is buried in a list of seven. A referee's first thought is "Bai already did this." Give it a dedicated sentence contrasting cross-country benchmarking with own-trajectory benchmarking, and add it as a named row or note in Table 1.
- 🟡 The Singapore/Indonesia contrast is stated here **and** in §1 **and** in §5.1, verbatim three times. Keep §5.1 (where it does analytical work), cut one of the others.

### 2.4 Policy and institutional responses
P2: Aslam · P3: Champeecharoensuk, Jindal, Kilinc-Ata, al Irsyad.
- 🔴 **A17** — "All six economies manage domestic energy prices through … subsidies, tariff caps, and price-smoothing funds" **contradicts §5.1, §5.2 and Table 7**, which all say Singapore has none. Fix to "five of the six"; Singapore passes wholesale prices through. This is not cosmetic: §5.1 explains Singapore's −1.816 *by* that absence.
- 🔍 **NV9** source the administered-pricing claim per country.
- 🟡 al Irsyad + Champeecharoensuk (EV papers) are the least load-bearing citations in the paper — first candidates if you need more words.

### 2.5 Measuring crisis-period performance — ✅ the strongest section
P1: Fan, Jasiūnas, Monie, OECD/JRC, Roege, Schmitz, Zhang 2026a, Zhang 2026b · P2: Aslam, Zhao.
- ✅ **Table 1 is the paper's best asset.** The "Benchmark / Phase covered / Principal constraint" framing states the contribution more clearly than the abstract does. Consider referencing it in the abstract.
- ✅ Zhao et al. (2025) as the explicit reason a panel regression is unavailable at N = 6 is the right defensive move — a referee *will* ask.
- 🟠 Add Bai et al. (2023) to Table 1 (see §2.3).
- 🔍 **NV7** Zhang 2026a is a *building*-systems review; attribute the four-phase framing to Monie et al. alone, or flag the scope transfer.
- 🟠 Promote Schmitz et al. (2025) from a trailing sentence — it is your strongest recent conceptual cover.

### 2.6 Research gaps
P1: Nijsse only.
- ✅ Three gaps map cleanly onto the three contributions. Well constructed.
- 🟡 Some repetition with §1¶3 and §2.2 — resolves once §1 is compressed.

---

## 3. Data and methods

### 3.1 Analytical framework
P1: Fan, Jasiūnas, Monie, Nijsse, Roege, Schmitz. ✅ Sound. Resistance-phase-only scope is properly justified.

### 3.2 Sample, periodisation, empirical sequence
P1: Zakeri · P3: Aleluia, Bai. ✅ 84 country-years, balanced, complete. Clean.
🟡 Heading says "periodisation"; §3.1's lead-in says "periodization" seven lines earlier (**A8**).

### 3.3 Outcome measurement and standardisation
P0: Ember, IRENA, UNSD, World Bank · P1: OECD/JRC.
- ✅ Fixed 2010–2019 reference distribution so crisis years cannot redefine their own benchmark — good, and worth saying more loudly.
- 🔴 **NV2** — does `RenCap` include large hydro? At Vietnam's stated 268→391 W/person the implied totals only reconcile with hydro included. If so, the indicator measures legacy stock for several countries, and §4.3's headline plus Table 3's log-linear justification are both affected. **Highest-value open question in the manuscript.**
- 🔍 **NV10** add access dates to all four sources.
- 🟡 "with their directions in the analysis code" — directions are in Table 2; say so.

### 3.4 Counterfactual specification and maintenance gaps — ✅ the methodological core
P1: Nijsse.
- ✅ **Table 3 is the contribution.** The concrete failure cases — electrification >100% for four economies, implied deflation for three — are the most persuasive lines in the paper. Do not let them get cut.
- ✅ The automated feasibility check is a genuinely good idea; give it one more sentence.
- ✅ Eqs (1)–(5) verified internally consistent.
- 🟡 **A11** — Student-t intervals disclaimed as non-inferential while using an inferential construct. Pick one.
- 🔍 **NV6** confirm Nijsse et al. supports *proportional* growth (and note it concerns solar, not hydro — see NV2).

### 3.5 Indicator decomposition and policy-function inventory
P0: IEA, IMF.
- ✅ Exact reconciliation to machine precision, retained as an audit — excellent practice.
- 🔴 **NV3** — the IMF COVID-19 tracker ended ~2021 but Table 7 codes 2022–2023. State which source covers which stage, with retrieval dates.
- ✅ The disclaimer that counts carry no scale/duration/targeting information is correct and repeated appropriately.

### 3.6 Validation design — 🔴 three defects, all fixable
P1: Tashman.
- 🔴 **A2** "Five windows … and three …" with floors "0.167 and 0.250" contradicts §4.6 and Table 9 (three windows each, floor 0.250 throughout). Also literal typo: "With&nbsp;&nbsp;windows" — the *k* is missing.
- 🔴 **A4** promises **seven** checks including "a uniform linear form replaces the assignments in Table 3"; **Table 8 reports six — the uniform-linear one is missing.** This is the check that tests your central methodological choice. Run it and report it: if results shift, that justifies your design; if not, you have defused the obvious objection.
- 🔴 **A5** the gap-to-RMSE denominator is underspecified. Printed ratios reproduce **only** as the mean of the two horizon RMSEs a stage spans (h=1,2 / h=3,4) — 6/6 under that rule, 0/6 under a single horizon. Since this ratio now carries your headline claim (A1), define it explicitly.

---

## 4. Results — ✅ arithmetic verified, zero citations (correct)

Every regional mean, interval, decomposition and leave-one-out range recomputes
exactly. See [[../scripts/verify_numbers.py]].

### 4.1 Sequential crises reordered the regional constraints
🔴 **A1 lives here too** — same false uniqueness claim. Replace with the
gap-to-RMSE formulation and add one sentence conceding the COVID/energy-service
interval also excludes zero.

### 4.2 Country gaps ✅
Means verified: price −0.767, service −0.103, low-carbon +0.102. All reconcile.

### 4.3 Cleaner electricity, not capacity growth ✅
Contributions sum exactly (+0.035, +0.102). Conditional on **NV2** — if `RenCap`
is hydro-inclusive, "capacity growth" means something different than implied.

### 4.4 National low-carbon configurations ✅
Consistent with Table 6.
🟡 Straight vs curly apostrophes ("Vietnam's", "Malaysia's") — normalise.

### 4.5 Policy inventories ✅
- ✅ "coincided with heterogeneous pressure points, but the counts do not reveal
  effectiveness" — exactly the right restraint.
- 🔍 **NV3** applies to Table 7's 2022–23 coding.

### 4.6 Robustness checks
- ✅ Reporting that omitting Vietnam **reverses the regional sign** is the single
  most credible thing in the paper. Keep it prominent; it will earn referee trust.
- 🔴 **A4** the missing seventh check.
- 🟠 **A10** Table 8's sign-match column mixes denominators (36 gaps vs 6 country
  low-carbon gaps) with no label.
- 🔴 **A2/A3** placebo counts and the identical "2016–2018" window on all six rows.

### 4.7 Results synthesis ✅
Honest and well-judged. No action.

---

## 5. Discussion and policy implications

### 5.1 A price margin, not a supply or transition margin ✅ strongest discussion
P1: Guan, Schmitz, Zakeri · P2: Hussain, Jaeger-Erben, Li, Quitzow, Tian.
- ✅ Singapore (−1.816, no buffer, ~100% import) vs Indonesia (+0.016, administered
  prices, coal exporter) is a genuinely persuasive natural contrast.
- ✅ Conceding CPI ≠ household energy burden, citing Guan, is the right call.
- 🔴 depends on fixing **A17** in §2.4 — as written, §2.4 says Singapore *does* have
  administered pricing, which destroys this mechanism.
- 🟠 reconcile with Quitzow (see §2.2).

### 5.2 Legislate price-support triggers ✅
P1: Guan · P2: Horbach & Rammer, Jaeger-Erben.
- ✅ The non-ordering between cushioning-years and price shortfall (Thailand and
  the Philippines: 2 years, ≈ −1.1; Vietnam: 1 year, −0.194) is a real finding.
- 🔍 **NV5** verify Jaeger-Erben supports a *design-over-presence* argument; if not,
  present it as your inference.

### 5.3 Protect dispatch-side levers ✅
P1: Nijsse · P2: D'Orazio, Evro · P3: Kilinc-Ata, Zhong.
- ✅ Qualifying the green-recovery framing is a genuine contribution — **state it
  more assertively**, it is currently phrased as a hedge.
- 🔍 conditional on **NV2** and **NV6**.

### 5.4 Pre-crisis pipeline as a crisis instrument — 🔴 the evidence cuts the other way
P1: Monie, Roege · P3: Fahim, Jindal.
- 🔴 **NV1.** The 2019→2020 Vietnamese capacity jump is attributed to "commitments
  made under the 2017–2019 feed-in tariff programme". But **Decision 13/2020 was
  issued 6 April 2020** — inside your COVID stage — and ~6 GW of ~9.3 GW of 2020
  rooftop solar was commissioned in **December 2020** racing its deadline. So your
  flagship preparedness case is substantially crisis-period policy producing
  crisis-period deployment: the opposite of the section's thesis. And Vietnam is
  the country whose removal flips your headline sign.
- **Two ways out.** (1) Split the 2020 addition into FIT1-extension volume vs new
  FIT2 rooftop volume and let the numbers set the claim. (2) Reframe from
  "pre-crisis pipeline" to **"policy certainty with a credible deadline"** — which
  the evidence supports and which is still actionable.
- ⚠️ A second timing problem: the jump is 2019→2020 (COVID stage) but is used to
  explain the **2022–2023** gap. It does so only because a 2020 level shift persists
  against a 2010–2019 counterfactual. That is legitimate — but say it, or a referee
  will read it as an error.

### 5.5 Close the remaining electrification gap ✅
P3: Aleluia, Safrina & Utama. Clean; shortfalls concentrate in the two economies
that had not completed electrification. Ring-fencing recommendation follows.

### 5.6 Monitor deviations from national trajectories ✅
P3: Bai, Hu & Weng, Kim.
- ✅ Best-supported recommendation: level baselines reproduce the main
  specification's sign in only 50.0% / 66.7% of country cells — your own evidence.
- 🔍 **NV4** verify ASEAN/ACE actually collects these eight series. Your own Table 2
  sources are World Bank/UN/Ember/IRENA, not ACE.

### 5.7 Limitations ✅ appropriately candid
🟡 **A12** the "In summary…" paragraph summarises all of Section 5 but sits inside
Limitations. Promote to §5.8 or move above §5.7.

---

## 6. Conclusion ✅ with one required fix
P1: Fan, Guan, Monie, Zakeri · P2: Hussain · P3: Hu & Weng, Kim.
- 🔴 **A1** third occurrence of the false uniqueness claim.
- ✅ Future-work list (energy-specific prices, longer post-crisis window,
  budget-level policy data, hierarchical/Bayesian pooling) is concrete and good.
- 🟡 Two very long paragraphs; split for readability.

---

## Declarations
- 🔴 **A14** affiliation, funding, corresponding author, ORCID all outstanding.
- 🟠 **A15** Data availability says "from the corresponding author on request"
  while the text promises a reproducibility package four times. **Deposit it**
  (Zenodo/OSF) and cite the DOI. Reproducibility is this paper's main asset — do
  not hide it behind an email request.
- ✅ Author contributions (CRediT) properly specified.

---

## References
- 🔴 **A6** delete the duplicate `Zhang et al. (2026)`; keep `2026a`; fix §1's cite.
- 🟡 **A13** "Al Irsyad" vs "al Irsyad"; the entry uses "et al." — Springer requires
  full author lists.
- 🔍 **NV11** 3 of 42 DOIs web-verified this session; the other 39 are reconstructed
  from publisher patterns and **must be confirmed**. See `doi_status` in each
  [[../02-Literature/_Index|literature note]].
- 🟡 Add DOIs throughout (Springer expects them).

---

## Reframing for EDS — answering the JCLP objection

Do not re-submit the same argument in a lower-impact venue. Three moves:

1. **Lead with the diagnostic failure you can demonstrate, not with the estimates.**
   Level-based baselines reproduce your main specification's country-level sign in
   only **50.0%** and **66.7%** of cells. That means *the benchmark choice determines  the
   diagnosis* — half of country classifications flip depending on a methodological
   choice most monitoring exercises make without comment. That is a
   methodological finding of consequence, it is fully supported by your own
   Table 8, and it does not depend on N = 6.

2. **Make the two null results findings, not apologies.** No measurable COVID
   shortfall in any dimension, and capacity additions tracking pre-crisis growth
   rates, are both *informative* — they bound what crisis-period policy can move
   inside a two-year window and they qualify the green-recovery literature
   (D'Orazio 2024; Evro et al. 2025). Currently both are framed defensively.

3. **Sell the reporting convention.** Gap ÷ own-benchmark forecast error is a
   transferable standard that composite indices do not meet. §2.5 already
   establishes that benchmark uncertainty "is seldom reported explicitly." Say
   plainly that any monitoring exercise should report it, and that you provide the
   procedure. EDS's audience — sustainability policy and monitoring — is a better
   fit for that argument than JCLP's.

**Fit check:** EDS publishes country/regional sustainability assessment and
policy-monitoring work, so the venue is right. Emphasise the ASEAN governance
contribution and the monitoring recommendation (§5.6) over the econometrics.
