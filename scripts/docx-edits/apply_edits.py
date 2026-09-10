# -*- coding: utf-8 -*-
"""Apply the revised results to word/document.xml. Every edit asserts its hit count."""
import re, sys

P = "unpacked/word/document.xml"
x = open(P, encoding="utf-8").read()
fails, done = [], 0

def sub(old, new, n=1, label=""):
    """Replace inside <w:t> text only, anchored by the surrounding tags."""
    global x, done
    got = x.count(old)
    if got != n:
        fails.append(f"[{label or old[:48]}] expected {n} found {got}")
        return
    x = x.replace(old, new)
    done += 1

def table_slice(anchor):
    i = x.find(anchor)
    if i < 0: return None, None
    s = x.find("<w:tbl>", i)
    e = x.find("</w:tbl>", s)
    return s, e + len("</w:tbl>")

def in_table(anchor, pairs, label=""):
    """Replace cell texts only within the table following `anchor`."""
    global x, done
    s, e = table_slice(anchor)
    if s is None:
        fails.append(f"[{label}] table not found"); return
    seg = x[s:e]
    for old, new in pairs:
        o, nw = f">{old}</w:t>", f">{new}</w:t>"
        if seg.count(o) != 1:
            fails.append(f"[{label}] cell {old!r} found {seg.count(o)}x"); continue
        seg = seg.replace(o, nw); done += 1
    x = x[:s] + seg + x[e:]

def drop_row(anchor, cell_text, label=""):
    """Delete the <w:tr> whose first cell is `cell_text`, within a table."""
    global x, done
    s, e = table_slice(anchor)
    if s is None:
        fails.append(f"[{label}] table not found"); return
    seg = x[s:e]
    rows = re.findall(r"<w:tr\b.*?</w:tr>", seg, re.S)
    hit = [r for r in rows if f">{cell_text}</w:t>" in r]
    if len(hit) != 1:
        fails.append(f"[{label}] row {cell_text!r} matched {len(hit)}"); return
    seg = seg.replace(hit[0], "", 1); done += 1
    x = x[:s] + seg + x[e:]

# ─────────────────────────────────────────────── 1. Abstract
ABS_OLD = ("During the COVID-19 stage no dimension departed measurably from its expected path. "
  "During the 2022–2023 compound crisis, macro-price stability fell to −0.767 standard deviations, "
  "the only regional estimate whose cross-country interval excludes zero and which is more extreme than "
  "every pre-crisis placebo window, while energy-service security (−0.103) and low-carbon continuity "
  "(+0.102) remained near their expected paths. Scaled by the forecast error of its own benchmark, the "
  "macro-price deviation is the largest of the three (0.86, against 0.54 for service security and 0.23 "
  "for low-carbon continuity), and the dominant diagnosed shortfall moved toward prices by 0.887 standard "
  "deviations between the two episodes. Within the low-carbon dimension, the carbon content of electricity "
  "contributed +0.049 and renewable capacity +0.003.")
ABS_NEW = ("During the COVID-19 stage no dimension departed measurably from its expected path. "
  "During the 2022–2023 compound crisis, macro-price stability fell to −0.767 standard deviations, "
  "the only regional estimate that both excludes zero across countries and exceeds every pre-crisis "
  "placebo window, while energy-service security (−0.007) and low-carbon continuity (+0.150) held to "
  "their expected paths. Scaled by the forecast error of its own benchmark, the macro-price deviation is "
  "by far the largest (0.86, against 0.04 for service security and 0.24 for low-carbon continuity), and "
  "the dominant diagnosed shortfall moved toward prices by 0.887 standard deviations between the two "
  "episodes. Within the low-carbon dimension, cleaner electricity contributed +0.082 and renewable "
  "capacity +0.005.")
sub(ABS_OLD, ABS_NEW, 1, "abstract")
sub("The counterfactual form is matched to each indicator’s data-generating process, since linear "
    "extrapolation of bounded or mean-reverting series produces expected values outside the feasible region.",
    "The counterfactual form is matched to each indicator, since linear extrapolation of bounded or "
    "mean-reverting series produces inadmissible expected values.", 1, "abstract trim")

# ─────────────────────────────────────────────── 2. Spelling / citation / A17
sub("The remainder of the paper is organized as follows.",
    "The remainder of the paper is organised as follows.", 1, "A8 organised")
sub("sample and periodization, outcome measurement", "sample and periodisation, outcome measurement", 1, "A8 periodisation")
sub("0.887 standardized units", "0.887 standardised units", 1, "A8 standardised")
sub("was therefore characterized by", "was therefore characterised by", 1, "A8 characterised")
sub("actual-minus-expected gap after standardization", "actual-minus-expected gap after standardisation", 1, "A8 standardisation")
sub("four-phase process of preparedness, mitigation, response, and recovery (Zhang et al. 2026)",
    "four-phase process of preparedness, mitigation, response, and recovery (Zhang et al. 2026a)", 1, "A6 Zhang cite")
sub("All six economies manage domestic energy prices through combinations of fuel subsidies, "
    "electricity tariff caps, and price-smoothing funds.",
    "Five of the six economies manage domestic energy prices through combinations of fuel subsidies, "
    "electricity tariff caps, and price-smoothing funds; Singapore passes wholesale prices through to "
    "consumers.", 1, "A17 Singapore")

# ─────────────────────────────────────────────── 3. Data & methods
sub("The balanced panel contains 84 country-year observations and complete data for all eight indicators.",
    "The balanced panel contains 84 country-year observations. Six of the eight indicators are complete "
    "over 2010–2023; renewable energy in final consumption (SDG 7.2.1) and primary energy intensity "
    "(SDG 7.3.1) are published only through 2022 and are therefore excluded from the low-carbon dimension, "
    "which is measured on the three indicators available in every panel year.", 1, "3.2 coverage")
sub("Low-carbon continuity combines renewable energy in final consumption, electricity carbon intensity, "
    "primary energy intensity, renewable capacity per capita, and the renewable share of electricity generation.",
    "Low-carbon continuity combines electricity carbon intensity, renewable capacity per capita, and the "
    "renewable share of electricity generation. Renewable energy in final consumption and primary energy "
    "intensity are reported only to 2022 in the SDG database, so including them would average different "
    "indicator sets across the two years of the compound-crisis stage.", 1, "3.3 basis")
sub("All indicators are obtained from official statistical sources and enter the analysis as raw values, "
    "with their directions in the analysis code.",
    "All indicators are obtained from official statistical sources and enter the analysis as raw values, "
    "with the direction of each given in Table 2.", 1, "3.3 directions")

# 3.6 placebo count + ratio rule (A2, A5) and the missing k
sub("Five windows are available at the COVID-19 horizon and three at the compound-crisis horizon, and the "
    "comparison uses a one-sided signed rank test. With  windows the smallest attainable p-value is 1/(k + 1), "
    "so the design admits 0.167 and 0.250 as its respective floors, and both the p-value and its floor are reported.",
    "Five windows are available at the COVID-19 horizon and three at the compound-crisis horizon, and the "
    "comparison uses a one-sided signed rank test. With k windows the smallest attainable p-value is "
    "1/(k + 1), so the design admits 0.167 and 0.250 as its respective floors, and both the p-value and its "
    "floor are reported.", 1, "3.6 placebo k")
sub("Every reported gap is compared against the root mean squared error at the horizon its stage spans, "
    "which supplies the scale against which each magnitude is judged.",
    "Each stage spans two forecast horizons, so every reported gap is compared against the mean root mean "
    "squared error across those two horizons (h = 1–2 for 2020–2021 and h = 3–4 for "
    "2022–2023), which supplies the scale against which each magnitude is judged.", 1, "3.6 ratio rule (A5)")
sub("Seven alternative specifications test whether the results depend on scaling, functional form, "
    "training window, or sample composition.",
    "Seven alternative specifications test whether the results depend on scaling, functional form, "
    "training window, or sample composition. Each is reported in Table 8.", 1, "3.6 seven checks")

open(P, "w", encoding="utf-8").write(x)
print(f"prose edits applied: {done}")
if fails:
    print("FAILED:"); [print("  ", f) for f in fails]; sys.exit(1)
