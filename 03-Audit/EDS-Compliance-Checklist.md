---
type: checklist
target: "Environment, Development and Sustainability"
date: 2026-09-10
tags: [checklist, eds-revision]
---

# EDS submission checklist

Ordered so that each block can be finished independently. Estimates assume the
analysis code is to hand.

## Block 1 — Blocking corrections (do first; ~half a day)

- [ ] **A1** Rewrite the uniqueness claim in **4 places** — Abstract, §4.1, §5
      opening, §6. Use gap-to-RMSE (0.86 vs 0.65 next), and concede that the
      COVID energy-service interval also excludes zero.
- [ ] **A17** §2.4 "All six economies…" → "Five of the six…"; Singapore passes
      wholesale prices through. Reconcile with §5.1, §5.2, Table 7.
- [ ] **A6** Delete the duplicate `Zhang et al. (2026)`; change §1 to `2026a`.
- [ ] **A2** Reconcile placebo window counts between §3.6 and §4.6/Table 9;
      insert the missing *k* in "With&nbsp;&nbsp;windows".
- [ ] **A5** Define the gap-to-RMSE denominator as the mean of the two horizon
      RMSEs the stage spans.
- [ ] **A14** Affiliation, funding, corresponding author, ORCID.

## Block 2 — Needs a code re-run (~1 day)

- [ ] **A4** Run the uniform-linear-form robustness check and add it to Table 8.
- [ ] **A3** Replace the identical "2016–2018" placebo label with the actual
      windows and fitting origins per row.
- [ ] **NV1** Split Vietnam's 2020 capacity addition into FIT1-extension vs new
      FIT2 rooftop volume — or reframe §5.4 (see outline).
- [ ] **NV2** Confirm whether `RenCap` includes large hydro; state it in Table 2;
      re-run on non-hydro if needed.
- [ ] **A16** Report ratios from unrounded values, or to 3 dp.

## Block 3 — Sourcing and verification (~1 day)

- [ ] **NV3** Which source covers 2022–23 policy coding? Add retrieval dates.
- [ ] **NV4** Does ASEAN/ACE collect these eight series? (§5.6 premise)
- [ ] **NV5** Does Jaeger-Erben et al. support a design-over-presence argument?
- [ ] **NV6** Does Nijsse et al. support proportional growth for capacity?
- [ ] **NV7** Attribute the four-phase framing to Monie et al. alone.
- [ ] **NV8** Horbach & Rammer final volume/issue/year.
- [ ] **NV9** Per-country sourcing for administered pricing.
- [ ] **NV10** Access dates: World Bank, UNSD, Ember, IRENA, IEA, IMF.
- [ ] **NV11** Verify the remaining 39 DOIs (3 of 42 done).
- [ ] **NV12** Confirm EDS (Springer) vs ESD (Elsevier).

## Block 4 — Length and language (~half a day)

- [ ] Abstract 264 → ≤250 (two cut candidates identified in the outline).
- [ ] Main text 7,515 → ≤7,000. **Source: compress Introduction ¶2–¶4**, which
      duplicate §2.2/§2.3/§2.6 almost citation-for-citation. Secondary: the EV
      citations in §2.4; the Singapore/Indonesia contrast stated three times.
- [ ] **A8** Unify to UK spelling: `periodization`→`periodisation` (L57),
      `standardized`/`standardization` (L136, L174), `organized` (L17),
      `characterized` (L136). Leave cited titles as published.
- [ ] **A13** "Al Irsyad"/"al Irsyad"; expand "et al." in the reference list.
- [ ] **A12** Move the "In summary…" paragraph out of §5.7.
- [ ] **A10** Label Table 8's two sign-match denominators (36 vs 6).
- [ ] Normalise apostrophes in §4.4.
- [ ] Add DOIs to all references.

## Block 5 — Strategic (do alongside Block 1)

- [ ] **A15** Deposit the reproducibility package (Zenodo/OSF); cite the DOI.
- [ ] **A11** Decide: descriptive dispersion range, or own the t-interval.
- [ ] Add Bai et al. (2023) as an explicit contrast in §2.5 / Table 1.
- [ ] Reconcile with Quitzow et al. (2021) on COVID divergence.
- [ ] Reframe contribution 3 from apology to standard (see outline).
- [ ] Reframe the two null results as findings.

## Pre-submission gate
- [ ] Every number in the text matches its table (re-run `scripts/verify_numbers.py`)
- [ ] Every in-text citation appears in the reference list and vice versa
      (re-run `scripts/build_vault.py` — it reports orphans)
- [ ] Abstract ≤250 words, body ≤7,000
- [ ] No placeholders remain
- [ ] Cover letter states the JCLP history if the journal asks
