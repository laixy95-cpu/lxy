# EDS manuscript workspace — ASEAN-6 sequential crises

An Obsidian vault implementing the literature→outline workflow, applied to
*"Sequential crises reorder the dominant shortfall in energy systems:
counterfactual evidence from ASEAN-6, 2010–2023"* (Wei & Lai), being prepared for
**Environment, Development and Sustainability** (Springer) after rejection at JCLP.

Open this folder as an Obsidian vault (`Open folder as vault`) — the `[[wikilinks]]`,
tags and YAML frontmatter all resolve.

## Start here

| Read | For |
|---|---|
| **[[01-Manuscript/Master-Outline]]** | The deliverable: every section, every citation, every action |
| [[03-Audit/Internal-Consistency-Audit]] | 17 findings, severity-ranked |
| [[03-Audit/Needs-Verification]] | 12 items needing secondary confirmation |
| [[03-Audit/EDS-Compliance-Checklist]] | Ordered work blocks with estimates |
| [[02-Literature/_Index]] | 42 references in priority order |
| [[04-Journal/EDS-Requirements]] | Journal specs vs current manuscript |
| **[[03-Audit/Data-Validation-Report]]** | ✅ The method reproduces; the data file is the problem |
| [[03-Audit/Code-Manuscript-Reconciliation]] | The supplied code does not implement the manuscript's method |
| [[06-Reviews/JCLP-Response-Map]] | What the JCLP reviewers asked and what the revision did |

## The workflow this implements

| Step in the original method | How it works here |
|---|---|
| Search the literature, download everything | 42 references extracted from the manuscript; enriched via web verification |
| **Have it rank priority** | Four tiers by *argumentative load*, not citation count: **P1** load-bearing (12) · **P2** supporting (13) · **P3** contextual (11) · **P0** data sources (6) |
| Put each day's exchange into Obsidian | `00-Inbox/YYYY-MM-DD.md`, one note per session |
| Daily: organise section headings, content, citations from new input | `scripts/build_vault.py` re-parses the manuscript and regenerates the citation map and index |
| **Mark what needs secondary lookup** | `03-Audit/Needs-Verification.md`, plus a `doi_status` field and a verification checklist in every literature note |
| End state: a detailed outline with all original citations and usage advice | `01-Manuscript/Master-Outline.md` |

### Two honest deviations

1. **`llmwiki` is not reachable from this environment** (egress policy blocks it,
   along with Crossref, OpenAlex and Semantic Scholar). Reference verification
   went through web search instead — so **3 of 42 DOIs are confirmed; 39 are
   reconstructed from publisher patterns and must be checked.** Every literature
   note carries its own `doi_status`. Don't treat 🔍 entries as verified.
2. **The corpus is the manuscript's own bibliography**, not a fresh field sweep.
   Building the pipeline from what you already cite makes the audit exact. A
   forward search for work published since drafting is a separate, worthwhile pass.

## Layout

```
00-Inbox/          daily capture, newest last
01-Manuscript/     source .docx, extracted text, figures, Master-Outline
02-Literature/     42 notes + _Index (priority-ordered)
03-Audit/          consistency audit, code reconciliation, verification queue, checklist
04-Journal/        target-journal specification
05-Analysis/       rebuilt pipeline (counterfactual_spec, asean6_counterfactual) + author's code
07-Results/        pipeline output: all tables + run manifest
06-Reviews/        JCLP reviewer reports + response map
scripts/           extract_docx.py, build_vault.py, verify_numbers.py
```

## Scripts

```bash
python3 scripts/extract_docx.py    # .docx -> structured text (headings, tables)
python3 scripts/build_vault.py     # regenerate literature notes + index; reports orphan citations
python3 scripts/verify_numbers.py  # recompute every regional statistic against printed values
```

`verify_numbers.py` currently reports **23/23 arithmetic checks passing**. Re-run it
after any edit to the results — it is the cheapest guard against introducing an
inconsistency while fixing the framing.
