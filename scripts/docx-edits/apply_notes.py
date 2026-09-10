# -*- coding: utf-8 -*-
import re, sys
P="unpacked/word/document.xml"; x=open(P,encoding="utf-8").read(); fails=[]; done=0
def sub(old,new,label):
    global x,done
    if x.count(old)!=1: fails.append(f"[{label}] x{x.count(old)}"); return
    x=x.replace(old,new); done+=1

# Table 5 note: three indicators now
sub("actual-minus-expected gap after standardisation, divided by five.",
    "actual-minus-expected gap after standardisation, divided by three.","T5 note")

# Table 3 note: extend the feasibility gate to negative losses (A18)
sub("An automated feasibility check rejects any specification that produces expected access above 100 per "
    "cent, negative renewable capacity, or implied deflation below −1 per cent.",
    "An automated feasibility check rejects any specification that produces expected access above 100 per "
    "cent, negative transmission and distribution losses, negative renewable capacity, or implied deflation "
    "below −1 per cent.","T3 note (A18)")

# Table 4 note: state the ratio convention (A5)
sub("Parentheses report the absolute gap-to-RMSE ratio, which supports comparison across dimensions with "
    "different numbers of indicators.",
    "Parentheses report the absolute gap-to-RMSE ratio, computed against the mean rolling-origin RMSE across "
    "the two horizons each stage spans, which supports comparison across dimensions with different numbers "
    "of indicators.","T4 note (A5)")

# Table 8 note: name the denominator (A10)
sub("Notes: Correlations and sign-match rates compare alternative and main actual-minus-expected gaps.",
    "Notes: Correlations and sign-match rates compare alternative and main actual-minus-expected gaps across "
    "all thirty-six country-dimension-stage cells.","T8 note (A10)")

# Table 2 note: record the coverage constraint
sub("Crisis-year observations are used as published, with no interpolation or model-based imputation.",
    "Crisis-year observations are used as published, with no interpolation or model-based imputation. "
    "Renewable energy in final consumption (SDG 7.2.1) and primary energy intensity (SDG 7.3.1) are "
    "published only through 2022 and are therefore not carried into the low-carbon dimension.","T2 note")

# A6: delete the unsuffixed duplicate Zhang entry
dup=("Zhang, C., Su, Y., Wang, J., Rezgui, Y., Luo, Z., Wu, Y., Sun, C., &amp; Zhao, T. (2026). A critical "
     "review and future perspectives: How to define, assess, improve, and optimize the energy resilience for "
     "building energy systems by generalized flexible energy resources? Renewable and Sustainable Energy "
     "Reviews, 233, 116814.")
i=x.find(f">{dup}</w:t>")
if i<0: fails.append("[A6] duplicate reference not found")
else:
    s=x.rfind("<w:p ",0,i); s2=x.rfind("<w:p>",0,i); s=max(s,s2)
    e=x.find("</w:p>",i)+len("</w:p>")
    x=x[:s]+x[e:]; done+=1

# A13: Springer requires full author lists; fix the name form
sub("Al Irsyad, M. I., Firmansyah, A. I., Hasibuan, V. T. F., et al. (2025).",
    "al Irsyad, M. I., Firmansyah, A. I., Hasibuan, V. T. F., Anggono, T., Wiryono, S. K., &amp; Prasetyo, "
    "A. D. (2025).","A13 al Irsyad")

open(P,"w",encoding="utf-8").write(x)
print(f"notes/reference edits applied: {done}")
if fails: print("FAILED:"); [print("  ",f) for f in fails]; sys.exit(1)
