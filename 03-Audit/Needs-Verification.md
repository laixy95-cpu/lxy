---
type: verification-queue
date: 2026-09-10
open_items: 12
tags: [audit, needs-verification, eds-revision]
---

# Needs secondary verification

The 二次查询和确认 queue. Items are ordered by how much damage they do if a
referee finds them first. ✅ = I verified it this session against live sources;
🔍 = you need to check it against the source document or your own data.

---

## 🔴 NV1 — §5.4's Vietnam evidence argues against §5.4's thesis ✅ verified

**The claim (§5.4):**
> "Its renewable capacity rose from 268 to 391 watts per capita between 2019 and
> 2020, **delivering commitments made under the 2017–2019 feed-in tariff
> programme**. What an economy builds during a crisis is largely what it financed
> and permitted before one."

**What the policy record actually shows:**

| Instrument | Issued | Eligibility window |
|---|---|---|
| Decision 11/2017/QĐ-TTg (FIT1) | 2017 | COD 1 Jun 2017 – 30 Jun 2019 |
| **Decision 13/2020/QĐ-TTg (FIT2)** | **6 Apr 2020**, effective 22 May 2020 | COD by **31 Dec 2020** |

Roughly 6 GW of Vietnam's ~9.3 GW of 2020 rooftop solar was commissioned in
**December 2020 alone**, racing the Decision 13 deadline. Decision 13 was adopted
*inside* your COVID-19 crisis stage.

**Why this matters.** Your flagship preparedness case is substantially a case of
crisis-period policy producing crisis-period deployment — the opposite of
"what an economy builds during a crisis is what it permitted before one". And this
is not a peripheral example: Vietnam is the country whose removal **reverses the
sign** of your headline regional low-carbon result (+0.102 → −0.048). A referee
with Southeast Asia expertise will know the Decision 13 story.

**The honest nuance in your favour:** Decision 13 *also* extended FIT eligibility
to FIT1 projects that missed the June 2019 COD, so part of the 2020 volume genuinely
is pre-crisis pipeline.

**Action — one of:**
1. *(strongest)* Split the 2020 addition into FIT1-extension volume vs new FIT2
   rooftop volume, and let the numbers set the claim.
2. *(safe)* Reframe §5.4 from "pre-crisis pipeline" to **"policy certainty with a
   credible deadline"** — which the evidence does support, and which still yields
   an actionable recommendation.

Do **not** leave the current mono-causal attribution.

---

## 🔴 NV2 — Does `RenCap` include large hydro? 🔍 you must check

§5.4 gives Vietnam 268 → 391 W/person. At 2019–20 populations that implies
≈25.9 GW → ≈37.9 GW of total capacity — only reconcilable if **large hydro is
included** (Vietnam's solar was ~4.9 GW in 2019 and ~16.5 GW by end-2020, on top
of ~20 GW hydro).

If hydro is in, then for several ASEAN-6 economies `RenCap` is dominated by
decades-old hydro, and the indicator is not measuring transition effort at all —
it is measuring legacy stock plus new build. That directly affects:

- Vietnam's **+0.358** and Malaysia's **−0.348** contributions (Malaysia is hydro-heavy);
- §4.3's headline that "cleaner electricity, not capacity growth" drives the result;
- the log-linear specification in Table 3, justified by *solar* deployment momentum
  (Nijsse et al. 2023) but applied to a series that may be mostly hydro.

**Action:** confirm the exact IRENA series (total renewable vs non-hydro renewable),
state it in Table 2, and if hydro is included either justify it or re-run on
non-hydro. This is the single most consequential open question about your data.

---

## 🟠 NV3 — The 2022–2023 policy inventory may have no documented source 🔍

§3.5 cites the IMF policy tracker + IEA Policies and Measures Database for
Table 7. The IMF *Policy Responses to COVID-19* tracker was **discontinued after
2021**, yet Table 7 codes 2022 and 2023 actions for all six countries.

**Action:** state which source covers which stage. If IEA + national documents
carry 2022–23 alone, say so, and give the retrieval date — a presence/absence
coding is defined by when you looked.

---

## 🟠 NV4 — Confirm §5.6's premise about ASEAN reporting 🔍

§5.6 recommends that ASEAN report each indicator against a national trajectory,
premised on "ASEAN energy cooperation **already collects the annual series this
study uses**" (cited to Bai et al. 2023; Hu and Weng 2024).

But your Table 2 sources are World Bank, UN SDG, Ember and IRENA — **not** the
ASEAN Centre for Energy. Verify that ACE actually publishes these eight
indicators. If it does not, the recommendation becomes "ASEAN should begin
collecting…", which is a different and weaker ask.

---

## 🟠 NV5 — Is Jaeger-Erben et al. (2025) carrying more than it can? 🔍

Cited five times (§1, §2.1, §2.2, §5.1, §5.2) and made to support §5.2's core
claim that instrument *design* matters more than instrument *presence*. It is a
study of **European household coping behaviour** in winter 2022/23.

**Action:** confirm it makes a policy-design argument. If it does not, §5.2's
recommendation is resting on your own inference — which is fine, but must be
stated as your inference, not as a cited finding.

---

## 🟠 NV6 — Does Nijsse et al. (2023) support the log-linear form? 🔍

Table 3 justifies the log-linear counterfactual for `RenCap` with: "Deployment
compounds once established, so growth is proportional and not additive (Nijsse
et al. 2023)." That is a specification choice defended by citation.

**Action:** verify the paper supports *proportional* growth for installed
capacity. Note the scope question: it concerns **solar**, while `RenCap` may be
mostly hydro (NV2). If so, this justification does not transfer and the
specification needs a different defence.

---

## 🟡 NV7 — Zhang et al. (2026a) is a *buildings* review used for national systems 🔍

✅ Record verified: RSER 233, 116814, published Feb 2026, article
S1364032126001139. But its scope is **building energy systems**. §1 uses it for
"recent studies formalise resilience as a four-phase process".

**Action:** either attribute the four-phase framing to Monie et al. (2025) alone
(Table 1 notes already say "Phase terminology follows Monie et al."), or state
explicitly that you are transferring a building-scale formalisation to national
systems.

---

## 🟡 NV8 — Horbach and Rammer citation details ✅ partly verified

DOI **10.1515/ger-2025-0010**, *German Economic Review* (De Gruyter). Published
title uses "Short-**Term**" (matching yours); the ZEW/SSRN working-paper version
reads "Short-**time**".

**Action:** it was ahead-of-print — check whether a final volume/issue/pages and
year now exist and replace "(advance online publication)". Note the DOI stem says
`2025`, so confirm whether the citation year should be 2025 or 2026.

---

## 🟡 NV9 — "All six countries use administered pricing" needs per-country sourcing 🔍

§2.4 makes this claim on the strength of one regional citation
(Kilinc-Ata and Proskuryakova 2024) — and it contradicts §5.1, §5.2 and Table 7
on Singapore (see audit **A17**). Source each country's mechanism individually,
or restrict the claim to five.

---

## 🟡 NV10 — Data access dates for all four indicator sources 🔍

`World Bank (2026)`, `United Nations Statistics Division (2026)`, `Ember (2024)`,
`IRENA (2024)` have **no retrieval dates**. WDI and the SDG database are revised
continuously; your own "data-revision log" implies you hit revisions.

**Action:** add "accessed DD Month YYYY" to each, and deposit the exact extract
used. Ember matters most — `CO2IntElec` (+0.049) and `RenElec` (+0.038) are your
two largest positive contributions.

---

## 🟡 NV11 — Confirm the 40 remaining DOIs 🔍

I verified 3 of 42 references against live sources this session
(Zhang 2026a, Zhang 2026b, Horbach & Rammer). Each note in [[../02-Literature/]]
carries a `doi_status` field: `web-verified` or `unverified`. The DOIs recorded
for unverified entries are **reconstructed from standard publisher patterns, not
confirmed** — check every one before submission.

---

## 🟡 NV12 — Confirm the target journal is EDS, not ESD 🔍

I have proceeded on **EDS = Environment, Development and Sustainability**
(Springer, journal 10668) — consistent with your APA-style reference list and
Springer-style "Declarations" block.

Flagging it because your reference list cites **four** papers from
*Energy for Sustainable Development* (**ESD**, Elsevier) — al Irsyad 2025,
Champeecharoensuk 2025, Jindal 2024, Kim 2025 — which is also a plausible target
and abbreviates similarly. The two journals have different formats and different
scope. Confirm before I do the formatting pass; everything in
[[EDS-Compliance-Checklist]] assumes Springer EDS.
