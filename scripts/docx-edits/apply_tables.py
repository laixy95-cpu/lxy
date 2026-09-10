# -*- coding: utf-8 -*-
"""Apply revised results to the manuscript tables. Every edit asserts its hit count."""
import re, sys
P="unpacked/word/document.xml"; x=open(P,encoding="utf-8").read()
fails=[]; done=0

def tbl(anchor):
    i=x.find(anchor)
    if i<0: return None,None
    s=x.find("<w:tbl>",i); return s, x.find("</w:tbl>",s)+8

def cells(anchor, pairs, label):
    """Replace unique cell texts inside one table."""
    global x,done
    s,e=tbl(anchor)
    if s is None: fails.append(f"[{label}] table missing"); return
    seg=x[s:e]
    for old,new in pairs:
        o=f">{old}</w:t>"
        if seg.count(o)!=1: fails.append(f"[{label}] {old!r} x{seg.count(o)}"); continue
        seg=seg.replace(o,f">{new}</w:t>"); done+=1
    x=x[:s]+seg+x[e:]

def row_cells(anchor, key, pairs, label):
    """Replace cells inside the one row containing `key` (for repeated cell text)."""
    global x,done
    s,e=tbl(anchor)
    if s is None: fails.append(f"[{label}] table missing"); return
    seg=x[s:e]
    rows=re.findall(r"<w:tr\b.*?</w:tr>",seg,re.S)
    hit=[r for r in rows if f">{key}</w:t>" in r]
    if len(hit)!=1: fails.append(f"[{label}] row {key!r} x{len(hit)}"); return
    r0=hit[0]; r=r0
    for old,new in pairs:
        o=f">{old}</w:t>"
        if r.count(o)!=1: fails.append(f"[{label}/{key}] {old!r} x{r.count(o)}"); continue
        r=r.replace(o,f">{new}</w:t>"); done+=1
    x=x[:s]+seg.replace(r0,r,1)+x[e:]

def drop(anchor, key, label):
    global x,done
    s,e=tbl(anchor)
    if s is None: fails.append(f"[{label}] table missing"); return
    seg=x[s:e]; rows=re.findall(r"<w:tr\b.*?</w:tr>",seg,re.S)
    hit=[r for r in rows if f">{key}</w:t>" in r]
    if len(hit)!=1: fails.append(f"[{label}] drop {key!r} x{len(hit)}"); return
    x=x[:s]+seg.replace(hit[0],"",1)+x[e:]; done+=1

def clone_row(anchor, key, newcells, label):
    """Duplicate the row containing `key` and set its cell texts, inserting after it."""
    global x,done
    s,e=tbl(anchor)
    if s is None: fails.append(f"[{label}] table missing"); return
    seg=x[s:e]; rows=re.findall(r"<w:tr\b.*?</w:tr>",seg,re.S)
    hit=[r for r in rows if f">{key}</w:t>" in r]
    if len(hit)!=1: fails.append(f"[{label}] clone {key!r} x{len(hit)}"); return
    src=hit[0]; new=src
    olds=re.findall(r"<w:t[^>]*>([^<]*)</w:t>",src)
    if len(olds)!=len(newcells):
        fails.append(f"[{label}] clone arity {len(olds)} vs {len(newcells)}"); return
    for o,n in zip(olds,newcells):
        new=new.replace(f">{o}</w:t>",f">{n}</w:t>",1)
    x=x[:s]+seg.replace(src,src+new,1)+x[e:]; done+=1

T2="Outcome dimensions, indicator definitions"
T3="Counterfactual specification by indicator"
T4="Regional maintenance gaps by crisis stage"
T5="Indicator contributions to the regional low-carbon"
T6="Country configurations of the 2022"
T8="Sensitivity of the 2022–2023 regional"
T9="Pre-crisis placebo gaps and rolling-origin forecast errors"

# ── Table 2: drop the two SDG indicators that end in 2022
drop(T2,"RenTFEC","T2 RenTFEC"); drop(T2,"EnergyIntensity","T2 EnergyIntensity")

# ── Table 3: TDLoss becomes log-linear (A18); drop the two SDG rows
row_cells(T3,"TDLoss",[("Secular decline, far from bounds","Secular decline approaching the zero bound"),
                       ("Linear trend","Log-linear trend"),
                       ("Standard specification for a trending, unconstrained series",
                        "Losses are bounded below at zero; a linear path yields negative expected losses for Singapore")],"T3 TDLoss")
drop(T3,"RenTFEC","T3 RenTFEC"); drop(T3,"EnergyIntensity","T3 EnergyIntensity")

# ── Table 4
cells(T4,[("−0.077 (0.65)","−0.047 (0.43)"),("[−0.125, −0.029]","[−0.082, −0.012]"),
          ("−0.103 (0.54)","−0.007 (0.04)"),("[−0.330, +0.124]","[−0.157, +0.142]"),
          ("−0.026","+0.040"),
          ("+0.035 (0.14)","+0.073 (0.22)"),("[−0.211, +0.281]","[−0.328, +0.475]"),
          ("+0.102 (0.23)","+0.150 (0.24)"),("[−0.382, +0.586]","[−0.554, +0.854]"),
          ("+0.067","+0.077")],"T4")

# ── Table 5: three indicators
drop(T5,"Renewables in final energy","T5 RenTFEC"); drop(T5,"Energy intensity","T5 EnergyIntensity")
row_cells(T5,"Electricity carbon intensity",[("+0.007","+0.012"),("+0.049","+0.082")],"T5 CO2")
row_cells(T5,"Renewable capacity per capita",[("+0.025","+0.042"),("+0.003","+0.005"),
                                              ("Small offset","Negligible")],"T5 RenCap")
row_cells(T5,"Renewable electricity share",[("+0.011","+0.019"),("+0.038","+0.063")],"T5 RenElec")
row_cells(T5,"Net low-carbon gap",[("+0.035","+0.073"),("+0.102","+0.150")],"T5 net")

# ── Table 6: recomputed configurations
for c,(net,ln,lnv,lp,lpv) in {
 "Indonesia":("+0.257","None; all contributions positive","—","Electricity carbon intensity","+0.134"),
 "Malaysia":("−0.687","Renewable capacity per capita","−0.580","None; all contributions negative","—"),
 "Philippines":("+0.103","Renewable capacity per capita","−0.002","Electricity carbon intensity","+0.054"),
 "Singapore":("+0.295","Electricity carbon intensity","−0.065","Renewable capacity per capita","+0.324"),
 "Thailand":("−0.343","Renewable capacity per capita","−0.328","Electricity carbon intensity","+0.009"),
 "Vietnam":("+1.277","None; all contributions positive","—","Renewable capacity per capita","+0.596"),
}.items():
    s,e=tbl(T6); seg=x[s:e]
    rows=re.findall(r"<w:tr\b.*?</w:tr>",seg,re.S)
    hit=[r for r in rows if f">{c}</w:t>" in r]
    if len(hit)!=1: fails.append(f"[T6] {c} x{len(hit)}"); continue
    src=hit[0]; old=re.findall(r"<w:t[^>]*>([^<]*)</w:t>",src)
    if len(old)!=6: fails.append(f"[T6] {c} arity {len(old)}"); continue
    new=src
    for o,n in zip(old,[c,net,ln,lnv,lp,lpv]):
        new=new.replace(f">{o}</w:t>",f">{n}</w:t>",1)
    x=x[:s]+seg.replace(src,new,1)+x[e:]; done+=1

# ── Table 8: revised values, consistent 36-gap denominator (A10), new uniform-linear row (A4)
cells(T8,[("+0.102","+0.150"),
          ("Pearson r = 0.955; sign match = 100%","Pearson r = 0.953; sign match = 100.0% of 36 gaps"),("+0.030","+0.042"),
          ("Pearson r = 0.964; sign match = 88.9%","Pearson r = 0.952; sign match = 88.9% of 36 gaps"),("+0.170","+0.245"),
          ("Country low-carbon sign match = 50.0%","Pearson r = 0.878; sign match = 55.6% of 36 gaps"),("+0.296","+0.448"),
          ("Country low-carbon sign match = 66.7%","Pearson r = 0.872; sign match = 63.9% of 36 gaps"),("+0.315","+0.471"),
          ("−0.048 to +0.224","−0.075 to +0.318"),("+0.066 to +0.162","+0.102 to +0.218")],"T8")
clone_row(T8,"Pre-crisis min–max scaling",
          ["Uniform linear form","Pearson r = 0.818; sign match = 80.6% of 36 gaps","+0.294",
           "Magnitude changes; feasibility gate rejects it"],"T8 uniform-linear row")

# ── Table 9: placebo windows named (A3), counts and floors corrected (A2)
W5="2014–2015 … 2018–2019"; W3="2016–2017 … 2018–2019"
for key,win,rng,pv in [
 ("Energy-service security; COVID-19",W5,"−0.089 to +0.064","p = 0.333; floor 0.167"),
 ("Energy-service security; compound",W3,"+0.000 to +0.078","p = 0.250; floor 0.250"),
 ("Macro-price stability; COVID-19",  W5,"+0.127 to +1.025","p = 1.000; floor 0.167"),
 ("Macro-price stability; compound",  W3,"+0.630 to +0.925","p = 0.250; floor 0.250"),
 ("Low-carbon continuity; COVID-19",  W5,"−0.197 to −0.039","p = 0.167; floor 0.167"),
 ("Low-carbon continuity; compound",  W3,"−0.336 to −0.226","p = 0.250; floor 0.250"),
]:
    row_cells(T9,key,[("2016–2018",win)],f"T9 win {key[:22]}")
    s,e=tbl(T9); seg=x[s:e]
    rows=re.findall(r"<w:tr\b.*?</w:tr>",seg,re.S)
    hit=[r for r in rows if f">{key}</w:t>" in r]
    if len(hit)!=1: fails.append(f"[T9] {key} x{len(hit)}"); continue
    src=hit[0]; old=re.findall(r"<w:t[^>]*>([^<]*)</w:t>",src); new=src
    new=new.replace(f">{old[3]}</w:t>",f">{rng}</w:t>",1)
    new=new.replace(f">{old[4]}</w:t>",f">{pv}</w:t>",1)
    x=x[:s]+seg.replace(src,new,1)+x[e:]; done+=1

# backtest rows: energy-service and low-carbon change; macro-price is unchanged
BT={("Energy-service security",1):("+0.015; MAE 0.069","RMSE 0.093"),
    ("Energy-service security",2):("+0.037; MAE 0.099","RMSE 0.127"),
    ("Energy-service security",3):("+0.061; MAE 0.126","RMSE 0.161"),
    ("Energy-service security",4):("+0.058; MAE 0.156","RMSE 0.185"),
    ("Low-carbon continuity",1):("−0.094; MAE 0.168","RMSE 0.278"),
    ("Low-carbon continuity",2):("−0.130; MAE 0.246","RMSE 0.377"),
    ("Low-carbon continuity",3):("−0.186; MAE 0.349","RMSE 0.487"),
    ("Low-carbon continuity",4):("−0.319; MAE 0.523","RMSE 0.761")}
s,e=tbl(T9); seg=x[s:e]
rows=re.findall(r"<w:tr\b.*?</w:tr>",seg,re.S)
for (dim,h),(bm,rm) in BT.items():
    hit=[r for r in rows if f">{dim}</w:t>" in r and f">h = {h}</w:t>" in r]
    if len(hit)!=1: fails.append(f"[T9 bt] {dim} h={h} x{len(hit)}"); continue
    src=hit[0]; old=re.findall(r"<w:t[^>]*>([^<]*)</w:t>",src)
    new=src.replace(f">{old[3]}</w:t>",f">{bm}</w:t>",1).replace(f">{old[4]}</w:t>",f">{rm}</w:t>",1)
    seg=seg.replace(src,new,1); done+=1
x=x[:s]+seg+x[e:]

open(P,"w",encoding="utf-8").write(x)
print(f"table edits applied: {done}")
if fails: print("FAILED:"); [print("  ",f) for f in fails]; sys.exit(1)
