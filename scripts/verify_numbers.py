#!/usr/bin/env python3
"""Recompute every regional statistic in the manuscript from the country-level
values it reports, and check them against the printed figures."""
import math, statistics as st

T = 2.571  # Student-t, df=5

def ci(vals):
    m = sum(vals)/len(vals)
    sd = st.stdev(vals)
    se = sd/math.sqrt(len(vals))
    return m, (m - T*se, m + T*se)

def chk(label, got, want, tol=0.0015):
    ok = abs(got-want) <= tol
    print(f"  {'PASS' if ok else 'FAIL':4} {label:<52} computed={got:+.4f}  printed={want:+.4f}")
    return ok

# ---- §4.2 country values -----------------------------------------------
price   = dict(SGP=-1.816, PHL=-1.150, THA=-1.117, MYS=-0.342, VNM=-0.194, IDN=+0.016)
service = dict(PHL=-0.445, VNM=-0.232, SGP=-0.109, THA=-0.018, MYS=-0.002, IDN=+0.185)
lowcarb = dict(VNM=+0.851, SGP=+0.246, IDN=+0.145, PHL=+0.107, MYS=-0.507, THA=-0.230)

print("== Table 4 regional means and Student-t intervals (compound crisis) ==")
allok=[]
for name, d, mean_p, ci_p in [
    ("Macro-price stability",  price,   -0.767, (-1.508, -0.026)),
    ("Energy-service security",service, -0.103, (-0.330, +0.124)),
    ("Low-carbon continuity",  lowcarb, +0.102, (-0.382, +0.586)),
]:
    m,(lo,hi) = ci(list(d.values()))
    allok += [chk(f"{name}: mean", m, mean_p),
              chk(f"{name}: CI lower", lo, ci_p[0], 0.002),
              chk(f"{name}: CI upper", hi, ci_p[1], 0.002)]

print("\n== Table 5 indicator decomposition sums to the dimension gap ==")
covid    = dict(RenTFEC=+0.022, CO2Int=+0.007, EnInt=-0.030, RenCap=+0.025, RenElec=+0.011)
compound = dict(RenTFEC=+0.039, CO2Int=+0.049, EnInt=-0.027, RenCap=+0.003, RenElec=+0.038)
allok += [chk("COVID-19 contributions sum",    sum(covid.values()),    +0.035),
          chk("Compound contributions sum",     sum(compound.values()), +0.102)]

print("\n== §4.6 leave-one-country-out range (low-carbon, compound) ==")
tot = sum(lowcarb.values())
loco = {k: (tot-v)/5 for k,v in lowcarb.items()}
lo_k = min(loco, key=loco.get); hi_k = max(loco, key=loco.get)
allok += [chk(f"LOCO min (drop {lo_k})", loco[lo_k], -0.048),
          chk(f"LOCO max (drop {hi_k})", loco[hi_k], +0.224)]
print(f"       -> sign reverses only when {lo_k} is dropped: "
      f"{[k for k,v in loco.items() if v<0]}")

print("\n== §4.1 / Abstract gap-to-RMSE ratios ==")
# Table 9 rolling-origin RMSE by horizon
rmse = {
 "service": {1:0.099, 2:0.137, 3:0.173, 4:0.213},
 "price":   {1:0.860, 2:0.802, 3:0.812, 4:0.970},
 "lowcarb": {1:0.208, 2:0.281, 3:0.348, 4:0.554},
}
gaps = {  # (covid gap, compound gap, printed covid ratio, printed compound ratio)
 "service": (-0.077, -0.103, 0.65, 0.54),
 "price":   (+0.120, -0.767, 0.14, 0.86),
 "lowcarb": (+0.035, +0.102, 0.14, 0.23),
}
print("  -- hypothesis A: single RMSE at the stage's LAST horizon (h=2 / h=4)")
for d,(gc,gk,pc,pk) in gaps.items():
    print(f"     {d:<9} covid {abs(gc)/rmse[d][2]:.2f} vs {pc}   compound {abs(gk)/rmse[d][4]:.2f} vs {pk}")
print("  -- hypothesis B: MEAN of the two RMSEs the stage spans (h=1,2 / h=3,4)")
for d,(gc,gk,pc,pk) in gaps.items():
    mc = (rmse[d][1]+rmse[d][2])/2
    mk = (rmse[d][3]+rmse[d][4])/2
    allok += [chk(f"{d} COVID ratio",    abs(gc)/mc, pc, 0.006),
              chk(f"{d} compound ratio", abs(gk)/mk, pk, 0.006)]

print("\n== §4.1 / §5 / §6 stage-reordering deltas ==")
allok += [chk("price reordering",   -0.767-0.120, -0.887),
          chk("service reordering", -0.103-(-0.077), -0.026),
          chk("lowcarb reordering", +0.102-0.035, +0.067)]

print("\n== §5.1 cross-country spread claim ==")
allok += [chk("price spread (max-min)", max(price.values())-min(price.values()), 1.83, 0.005)]

print("\n== COVID-stage CI (Table 4) - does energy-service also exclude zero? ==")
print("   printed: energy-service COVID CI = [-0.125, -0.029]  -> EXCLUDES ZERO")
print("   printed: energy-service COVID placebo range = [-0.026, +0.044]")
print("   printed: energy-service COVID gap = -0.077  -> BELOW every placebo window")
print("   => energy-service/COVID satisfies BOTH criteria the paper claims are")
print("      unique to macro-price/compound. See audit finding A1.")

print(f"\n{sum(allok)}/{len(allok)} arithmetic checks passed")
