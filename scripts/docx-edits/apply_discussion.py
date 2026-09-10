# -*- coding: utf-8 -*-
import sys
P="unpacked/word/document.xml"; x=open(P,encoding="utf-8").read(); fails=[]; done=0
def sub(old,new,label):
    global x,done
    if x.count(old)!=1: fails.append(f"[{label}] x{x.count(old)}"); return
    x=x.replace(old,new); done+=1

# ── 5 opening
sub("Macro-price stability moved by −0.887 standard deviations between them, and the compound-stage "
    "shortfall of −0.767 is the only regional estimate whose cross-country interval excludes zero and "
    "which exceeds every pre-crisis placebo window.",
    "Macro-price stability moved by −0.887 standard deviations between them, and the compound-stage "
    "shortfall of −0.767 is the only regional estimate that both excludes zero across countries and "
    "exceeds every pre-crisis placebo window.","5 opening (A1)")

# ── 5.1
sub("The Philippines (−1.150) and Thailand (−1.117) sit between these poles.",
    "The Philippines (−1.150) and Thailand (−1.118) sit between these poles.","5.1 Thailand")
sub("the macro-price deviation reaches 0.86 against 0.54 for service security and 0.23 for low-carbon "
    "continuity, so the ranking holds once the three dimensions are placed on a common footing.",
    "the macro-price deviation reaches 0.86 against 0.04 for service security and 0.24 for low-carbon "
    "continuity, so the ranking holds by a wide margin once the three dimensions are placed on a common "
    "footing.","5.1 ratios")

# ── 5.3
sub("Electricity carbon intensity contributed +0.049, renewables in final energy +0.039, and the renewable "
    "electricity share +0.038, while renewable capacity per capita contributed +0.003.",
    "Electricity carbon intensity contributed +0.082 and the renewable electricity share +0.063, while "
    "renewable capacity per capita contributed +0.005.","5.3 decomposition")

# ── 5.4  (numbers + NV1: the 2020 capacity surge followed Decision 13/2020, adopted during the shock)
sub("Vietnam recorded a low-carbon gap of +0.851, the largest in the panel, and removing Vietnam reverses "
    "the sign of the regional result. Its renewable capacity rose from 268 to 391 watts per capita between "
    "2019 and 2020, delivering commitments made under the 2017–2019 feed-in tariff programme. What an "
    "economy builds during a crisis is largely what it financed and permitted before one.",
    "Vietnam recorded a low-carbon gap of +1.277, the largest in the panel, and removing Vietnam reverses "
    "the sign of the regional result. Its renewable capacity rose from 268 to 391 watts per capita between "
    "2019 and 2020. That addition combined projects that had missed the June 2019 deadline of the "
    "2017–2019 feed-in tariff with a rooftop segment created by Decision 13/2020, adopted in April 2020 "
    "and expiring that December. What an economy builds during a crisis therefore reflects both the pipeline "
    "it had already financed and the certainty of the deadline it is building against.","5.4 Vietnam (NV1)")

# ── 5.5
sub("The Philippines recorded −0.445 and Vietnam −0.232, while Indonesia recorded +0.185 and the "
    "economies already at full access recorded gaps between −0.002 and −0.109.",
    "The Philippines recorded −0.235 and Vietnam −0.068, while Indonesia recorded +0.191 and the "
    "economies already at full access recorded gaps between −0.013 and +0.068.","5.5 service")

# ── 6 Conclusion
sub("energy-service security recorded −0.077, macro-price stability +0.120, and low-carbon continuity "
    "+0.035, each smaller than the forecast error of its own benchmark.",
    "energy-service security recorded −0.047, macro-price stability +0.120, and low-carbon continuity "
    "+0.073, each smaller than the forecast error of its own benchmark.","6 covid")
sub("Macro-price stability fell to −0.767, the single regional estimate whose cross-country interval "
    "excludes zero and which is more negative than every pre-crisis placebo window, while energy-service "
    "security (−0.103) and low-carbon continuity (+0.102) stayed near their expected paths.",
    "Macro-price stability fell to −0.767, the single regional estimate that both excludes zero across "
    "countries and is more negative than every pre-crisis placebo window, while energy-service security "
    "(−0.007) and low-carbon continuity (+0.150) stayed near their expected paths.","6 compound (A1)")
sub("(0.86 for macro-price, 0.54 for service security, 0.23 for low-carbon continuity). Within the "
    "low-carbon dimension, the carbon content of electricity contributed +0.049 and renewable capacity "
    "+0.003, which places the regional position with the composition of supply and not with capacity "
    "additions beyond trend.",
    "(0.86 for macro-price, 0.04 for service security, 0.24 for low-carbon continuity). Within the "
    "low-carbon dimension, the carbon content of electricity contributed +0.082 and renewable capacity "
    "+0.005, which places the regional position with the composition of supply and not with capacity "
    "additions beyond trend.","6 ratios")

open(P,"w",encoding="utf-8").write(x)
print(f"discussion edits applied: {done}")
if fails: print("FAILED:"); [print("  ",f) for f in fails]; sys.exit(1)
