# -*- coding: utf-8 -*-
import re, sys
P="unpacked/word/document.xml"; x=open(P,encoding="utf-8").read(); fails=[]; done=0
def sub(old,new,label,n=1):
    global x,done
    if x.count(old)!=n: fails.append(f"[{label}] x{x.count(old)}"); return
    x=x.replace(old,new); done+=1

# ── 4.1
sub("the ASEAN-6 mean gaps were −0.077 for energy-service security, +0.120 for macro-price stability, "
    "and +0.035 for low-carbon continuity. In 2022–2023, the energy-service gap declined to −0.103 "
    "and the macro-price stability gap to −0.767, while the low-carbon gap increased to +0.102.",
    "the ASEAN-6 mean gaps were −0.047 for energy-service security, +0.120 for macro-price stability, "
    "and +0.073 for low-carbon continuity. In 2022–2023, the energy-service gap narrowed to −0.007 "
    "and the macro-price stability gap fell to −0.767, while the low-carbon gap increased to +0.150.","4.1 gaps")
sub("the macro-price stability gap declined by 0.887 standardised units and the energy-service gap by 0.026, "
    "while low-carbon continuity increased by 0.067.",
    "the macro-price stability gap declined by 0.887 standardised units, while the energy-service gap "
    "narrowed by 0.040 and low-carbon continuity increased by 0.077.","4.1 reordering")
sub("The macro-price gap is the only regional estimate that combines a descriptive cross-country interval "
    "excluding zero with a value below every corresponding pre-crisis placebo window. As the macro-price "
    "stability is measured by one indicator and low-carbon continuity averages five, the cross-dimensional "
    "magnitudes are also evaluated against each dimension’s forecast error. The absolute gap-to-RMSE "
    "ratios are 0.86 for macro-price stability, 0.54 for energy-service security, and 0.23 for low-carbon "
    "continuity, confirming that macro-price stability recorded the largest relative deviation.",
    "The macro-price gap is the only regional estimate that combines a descriptive cross-country interval "
    "excluding zero with a value beyond every corresponding pre-crisis placebo window. The two criteria are "
    "conjunctive: the COVID-stage energy-service interval also excludes zero, but that gap falls inside its "
    "placebo range. As macro-price stability is measured by one indicator and low-carbon continuity averages "
    "three, the cross-dimensional magnitudes are also evaluated against each dimension’s forecast error. "
    "The absolute gap-to-RMSE ratios are 0.86 for macro-price stability, 0.04 for energy-service security, "
    "and 0.24 for low-carbon continuity, confirming that macro-price stability recorded the largest relative "
    "deviation by a wide margin.","4.1 uniqueness (A1)")

# ── 4.2
sub("Five countries recorded negative gaps: Singapore (−1.816), the Philippines (−1.150), "
    "Thailand (−1.117), Malaysia (−0.342), and Vietnam (−0.194).",
    "Five countries recorded negative gaps: Singapore (−1.816), the Philippines (−1.150), "
    "Thailand (−1.118), Malaysia (−0.342), and Vietnam (−0.194).","4.2 price")
sub("Energy-service security was below its counterfactual in five countries. The Philippines recorded the "
    "largest gap (−0.445), followed by Vietnam (−0.232), Singapore (−0.109), Thailand "
    "(−0.018), and Malaysia (−0.002). Indonesia remained above its path at +0.185. The result "
    "separates a regional mean shortfall from heterogeneous country exposure.",
    "Energy-service security was below its counterfactual in three countries. The Philippines recorded the "
    "largest gap (−0.235), followed by Vietnam (−0.068) and Thailand (−0.013), while Malaysia "
    "(+0.013), Singapore (+0.068), and Indonesia (+0.191) remained above their paths. The regional mean is "
    "therefore close to zero and masks heterogeneous country exposure.","4.2 service")
sub("Vietnam (+0.851), Singapore (+0.246), Indonesia (+0.145), and the Philippines (+0.107) remained above "
    "their expected paths. Malaysia (−0.507) and Thailand (−0.230) fell below them.",
    "Vietnam (+1.277), Singapore (+0.295), Indonesia (+0.257), and the Philippines (+0.103) remained above "
    "their expected paths. Malaysia (−0.687) and Thailand (−0.343) fell below them.","4.2 lowcarbon")

# ── 4.3
sub("The indicator decomposition explains why low-carbon continuity remained positive. During 2020–2021, "
    "renewable capacity per capita contributed +0.025 to the regional gap. Renewables in final energy (+0.022), "
    "renewable electricity (+0.011), and electricity carbon intensity (+0.007) added further offsets. Energy "
    "intensity contributed −0.030, leaving a net gap of +0.035.",
    "The indicator decomposition explains why low-carbon continuity remained positive. During 2020–2021, "
    "renewable capacity per capita contributed +0.042 to the regional gap, with renewable electricity (+0.019) "
    "and electricity carbon intensity (+0.012) adding further offsets, leaving a net gap of +0.073.","4.3 covid")
sub("The 2022–2023 composition was broader. Electricity carbon intensity (+0.049), renewables in final "
    "energy (+0.039), and renewable electricity (+0.038) supported maintenance. Renewable capacity per ",
    "The 2022–2023 composition shifted decisively toward supply mix. Electricity carbon intensity "
    "(+0.082) and renewable electricity (+0.063) supported maintenance, while renewable capacity per ","4.3 comp a")
sub("capita added only +0.003, while energy intensity was the only regional drag (−0.027). These five "
    "terms reconcile to the +0.102 low-carbon gap with zero computational error at machine precision.",
    "capita added only +0.005. These three terms reconcile to the +0.150 low-carbon gap with zero "
    "computational error at machine precision.","4.3 comp b")

# ── 4.4
sub("Vietnam's +0.851 gap was anchored by renewable capacity (+0.358), electricity carbon-intensity "
    "improvement (+0.243), and renewable electricity (+0.166), while energy intensity provided its largest "
    "drag (−0.041). Singapore also relied on renewable capacity (+0.194), with a small negative "
    "contribution from electricity carbon intensity (−0.039).",
    "Vietnam's +1.277 gap was anchored by renewable capacity (+0.596), electricity carbon-intensity "
    "improvement (+0.405), and renewable electricity (+0.276), with no negative contribution. Singapore also "
    "relied on renewable capacity (+0.324), with a small negative contribution from electricity carbon "
    "intensity (−0.065).","4.4 a")
sub("Indonesia and the Philippines recorded smaller positive gaps. Renewables in final energy provided the "
    "largest positive contribution in both countries, while energy intensity was the main negative term. "
    "Malaysia's −0.507 gap was dominated by weak renewable-capacity performance (−0.348) and "
    "additional negative contributions from energy intensity, renewable electricity, and electricity carbon "
    "intensity. Thailand faced a renewable-capacity drag (−0.197), with positive energy-intensity and "
    "carbon-intensity contributions unable to offset it.",
    "Indonesia and the Philippines recorded smaller positive gaps, with electricity carbon intensity the "
    "largest positive contribution in both. Malaysia's −0.687 gap was dominated by weak "
    "renewable-capacity performance (−0.580), with renewable electricity (−0.065) and electricity "
    "carbon intensity (−0.043) also negative. Thailand faced a renewable-capacity drag (−0.328) "
    "that a positive carbon-intensity contribution (+0.009) could not offset.","4.4 b")

# ── 4.5 and Table 7
sub("Macro-price stability was the largest shortfall in four countries during 2022–2023. Malaysia's "
    "largest shortfall was low-carbon continuity, Vietnam's was energy-service security, and Indonesia had "
    "no negative dimension gap in that stage.",
    "Macro-price stability was the largest shortfall in four countries during 2022–2023. Malaysia's "
    "largest shortfall was low-carbon continuity, and Indonesia had no negative dimension gap in that stage.","4.5")
sub(">Low-carbon continuity (−0.507)</w:t>",">Low-carbon continuity (−0.687)</w:t>","T7 Malaysia")
sub(">Macro-price stability (−1.117)</w:t>",">Macro-price stability (−1.118)</w:t>","T7 Thailand")
sub(">Energy-service security (−0.232)</w:t>",">Macro-price stability (−0.194)</w:t>","T7 Vietnam")

# ── 4.6
sub("Min–max scaling produces +0.030 and a 0.955 Pearson correlation with the main gaps. A shorter "
    "2015–2019 trend produces +0.170, with Pearson r = 0.964 and an 88.9% sign agreement across "
    "country-dimension gaps.",
    "Min–max scaling produces +0.042 and a 0.953 Pearson correlation with the main gaps. A shorter "
    "2015–2019 trend produces +0.245, with Pearson r = 0.952 and an 88.9% sign agreement across the "
    "thirty-six country-dimension-stage gaps. Replacing the indicator-specific assignments with a uniform "
    "linear form produces +0.294 at r = 0.818, and the feasibility check rejects that specification because "
    "it implies negative transmission losses and expected access above 100 per cent.","4.6 a")
sub("The 2017–2019 mean yields +0.296 and the 2019 level yields +0.315, but their country sign agreement "
    "is 50.0% and 66.7%. Country composition is consequential: leave-one-country-out estimates range from "
    "−0.048 to +0.224, with the sign reversing when Vietnam is omitted. Removing one low-carbon "
    "indicator at a time yields +0.066 to +0.162.",
    "The 2017–2019 mean yields +0.448 and the 2019 level yields +0.471, but their sign agreement falls "
    "to 55.6% and 63.9% across the same thirty-six gaps. Country composition is consequential: "
    "leave-one-country-out estimates range from −0.075 to +0.318, with the sign reversing when Vietnam "
    "is omitted. Removing one low-carbon indicator at a time yields +0.102 to +0.218.","4.6 b")
sub("Horizon-matched placebo windows were estimated for all three dimensions. COVID-19 placebos use a "
    "one-year first horizon; compound-crisis placebos use a three-year first horizon. Three windows are "
    "retained for each stage, so the rank p-value floor is 1/(3+1) = 0.250. These checks are descriptive and "
    "do not supply conventional inference.",
    "Horizon-matched placebo windows were estimated for all three dimensions. COVID-19 placebos use a "
    "one-year first horizon; compound-crisis placebos use a three-year first horizon. Five windows are "
    "available at the COVID-19 horizon and three at the compound-crisis horizon, so the rank p-value floors "
    "are 1/(5+1) = 0.167 and 1/(3+1) = 0.250. These checks are descriptive and do not supply conventional "
    "inference.","4.6 placebo (A2)")
sub("Macro-price stability has positive bias that grows from +0.435 to +0.728, while low-carbon continuity "
    "has negative bias from −0.063 to −0.214. RMSE also rises with horizon, reaching 0.970 for "
    "macro-price stability and 0.554 for low-carbon continuity at four years.",
    "Macro-price stability has positive bias that grows from +0.435 to +0.728, while low-carbon continuity "
    "has negative bias from −0.094 to −0.319. RMSE also rises with horizon, reaching 0.970 for "
    "macro-price stability and 0.761 for low-carbon continuity at four years.","4.6 backtest")
sub("the compound-stage macro-price gap reaches 0.86 of its RMSE, the low-carbon gap 0.23.",
    "the compound-stage macro-price gap reaches 0.86 of its RMSE, the low-carbon gap 0.24 and the "
    "energy-service gap 0.04.","4.6 ratios")

open(P,"w",encoding="utf-8").write(x)
print(f"results edits applied: {done}")
if fails: print("FAILED:"); [print("  ",f) for f in fails]; sys.exit(1)
