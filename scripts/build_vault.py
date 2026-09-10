#!/usr/bin/env python3
"""
Build the Obsidian literature vault from the manuscript.

Pipeline (mirrors the workflow in the source screenshot):
  1. parse manuscript -> sections
  2. locate every in-text citation -> section map
  3. join against the curated reference database (priority tiers)
  4. emit one Obsidian note per reference + a prioritised index
"""
import re, os, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, "01-Manuscript", "manuscript_full.txt")
LIT  = os.path.join(ROOT, "02-Literature")

# ---------------------------------------------------------------- 1. sections
def parse_sections(text):
    """Split manuscript into (section_label, body) preserving order."""
    secs, cur, buf = [], "Front matter", []
    for line in text.split("\n"):
        m = re.match(r"\[HEADING [12]\] (.+)", line)
        if m:
            if buf: secs.append((cur, "\n".join(buf)))
            cur, buf = m.group(1).strip(), []
        else:
            buf.append(line)
    if buf: secs.append((cur, "\n".join(buf)))
    return secs

# ------------------------------------------------- 2. curated reference DB
# tier: P1 load-bearing | P2 supporting | P3 contextual | P0 data/policy source
# 'load' = what the manuscript's argument actually rests on for this cite.
REFS = [
 dict(key="zakeri2022", cite="Zakeri et al. 2022", tier="P1",
   authors="Zakeri, B., Paulavets, K., Barreto-Gomez, L., Echeverri, L. G., Pachauri, S., Boza-Kiss, B., Zimm, C., Rogelj, J., Creutzig, F., Ürge-Vorsatz, D., Victor, D. G., Bazilian, M. D., Fritz, S., Gielen, D., McCollum, D. L., Srivastava, L., Hunt, J. D., & Pouya, S.",
   year=2022, title="Pandemic, war, and global energy transitions", journal="Energies", vol="15(17)", pages="6114",
   doi="10.3390/en15176114", doi_status="unverified",
   load="Frames the two-shock sequence that defines the whole periodisation. The 2020-21 / 2022-23 split rests on this.",
   use="Keep. Anchor the periodisation in §3.2 explicitly to this source rather than asserting the split."),
 dict(key="guan2023", cite="Guan et al. 2023", tier="P1",
   authors="Guan, Y., Yan, J., Shan, Y., Zhou, Y., Hang, Y., Li, R., Liu, Y., Liu, B., Nie, Q., Bruckner, B., Feng, K., & Hubacek, K.",
   year=2023, title="Burden of the global energy price crisis on households", journal="Nature Energy", vol="8", pages="304-316",
   doi="10.1038/s41560-023-01209-8", doi_status="unverified",
   load="The price-dimension anchor. Also the source the manuscript uses to concede that headline CPI is not a household energy burden measure.",
   use="Load-bearing for the honest limitation in §5.1/§5.7. Strengthen: this paper is exactly what a reviewer will say you should have used instead of CPI. Pre-empt in the response letter."),
 dict(key="nijsse2023", cite="Nijsse et al. 2023", tier="P1",
   authors="Nijsse, F. J. M. M., Mercure, J.-F., Ameli, N., Larosa, F., Kothari, S., Rickman, J., Vercoulen, P., & Pollitt, H.",
   year=2023, title="The momentum of the solar energy transition", journal="Nature Communications", vol="14", pages="6542",
   doi="10.1038/s41467-023-41971-7", doi_status="unverified",
   load="Does DOUBLE duty: (a) justifies the log-linear counterfactual for RenCap in Table 3; (b) supplies the §5.3 interpretation that capacity has its own momentum. Also cited in §1 and §2.6 for secular-trend confounding.",
   use="Highest-leverage citation in the paper. The Table 3 justification is a methodological claim - make sure the cited paper actually supports proportional (not additive) growth, and quote the specific finding."),
 dict(key="oecdjrc2008", cite="OECD/JRC 2008", tier="P1", match=r"OECD/JRC",
   authors="OECD/JRC", year=2008, title="Handbook on constructing composite indicators: Methodology and user guide",
   journal="OECD Publishing", vol="", pages="", doi="10.1787/9789264043466-en", doi_status="unverified",
   load="The methodological foil. The paper's contribution is defined against composite-index benchmarking (Table 1 row 1) and it justifies equal weighting in §3.3.",
   use="Keep both uses. Note it is a 2008 handbook being used as the stand-in for all composite-index practice - consider adding one recent composite-index application so the foil is not 18 years old."),
 dict(key="roege2014", cite="Roege et al. 2014", tier="P1",
   authors="Roege, P. E., Collier, Z. A., Mancillas, J., McDonagh, J. A., & Linkov, I.",
   year=2014, title="Metrics for energy resilience", journal="Energy Policy", vol="72", pages="249-256",
   doi="10.1016/j.enpol.2014.04.012", doi_status="unverified",
   load="Framework anchor for reporting dimensions separately (§3.1) and for preparedness-before-response (§5.4). Table 1 row 2.",
   use="Keep. §5.4 leans on it for a preparedness claim that the Vietnam evidence does not cleanly support - see the Vietnam FIT flag."),
 dict(key="jasiunas2021", cite="Jasiūnas et al. 2021", tier="P1",
   authors="Jasiūnas, J., Lund, P. D., & Mikkola, J.", year=2021,
   title="Energy system resilience — A review", journal="Renewable and Sustainable Energy Reviews", vol="150", pages="111476",
   doi="10.1016/j.rser.2021.111476", doi_status="unverified",
   load="Resilience review; supports separate-dimension reporting (§3.1) and the resistance/recovery phase limit (§5.7). Table 1 row 2.",
   use="Keep. Use it to justify why 'resistance phase only' is a legitimate scope rather than a shortfall."),
 dict(key="monie2025", cite="Monie et al. 2025", tier="P1",
   authors="Monie, S. W., Gustafsson, M., Önnered, S., & Guruvita, K.", year=2025,
   title="Renewable and integrated energy system resilience — A review and generic resilience index",
   journal="Renewable and Sustainable Energy Reviews", vol="215", pages="115554",
   doi="10.1016/j.rser.2025.115554", doi_status="unverified",
   load="EXPLICIT terminology dependency: Table 1 notes state 'Phase terminology follows Monie et al. (2025)'. Also §3.1, §5.4, §6.",
   use="Because you adopt its phase vocabulary by name, the four phases must match its definitions exactly. Verify preparedness/mitigation/response/recovery are its terms, not Zhang et al."),
 dict(key="fan2023", cite="Fan et al. 2023", tier="P1",
   authors="Fan, W., Lv, W., & Wang, Z.", year=2023,
   title="How to measure and enhance the resilience of energy systems?", journal="Sustainable Production and Consumption",
   vol="39", pages="191-202", doi="10.1016/j.spc.2023.05.007", doi_status="unverified",
   load="Represents the regime-switching / process tradition in Table 1 row 4; used to argue that method needs several completed shock cycles you do not have.",
   use="Keep. This is your defence against 'why not a proper resilience model' - make the data requirement explicit and quantitative."),
 dict(key="tashman2000", cite="Tashman 2000", tier="P1",
   authors="Tashman, L. J.", year=2000,
   title="Out-of-sample tests of forecasting accuracy: An analysis and review", journal="International Journal of Forecasting",
   vol="16(4)", pages="437-450", doi="10.1016/S0169-2070(00)00065-0", doi_status="unverified",
   load="Sole methodological authority for the rolling-origin backtest, which supplies the RMSE denominators for every gap-to-RMSE ratio in the paper.",
   use="The entire 'bounded diagnostic' framing depends on this. Given the ratios are computed against a MEAN of two horizon RMSEs (see audit), state the convention explicitly and cite Tashman for the rolling-origin design only."),
 dict(key="schmitz2025", cite="Schmitz et al. 2025", tier="P1",
   authors="Schmitz, R., Flachsbarth, F., Plaga, L. S., Braun, M., & Härtel, P.", year=2025,
   title="Energy security and resilience: Revisiting concepts and advancing planning perspectives for transforming integrated energy systems",
   journal="Energy Policy", vol="207", pages="114796", doi="10.1016/j.enpol.2025.114796", doi_status="web-verified",
   load="Distinguishes performance-under-disturbance from average performance - the conceptual license for the whole design. Also §3.1 phase-scope and §5.1 closing claim.",
   use="Keep. Strongest recent conceptual cover for your framing; consider promoting it in §2.5 rather than leaving it as a trailing sentence."),
 dict(key="zhang2026a", cite="Zhang et al. 2026a", tier="P1", match=r"Zhang et al\.",
   authors="Zhang, C., Su, Y., Wang, J., Rezgui, Y., Luo, Z., Wu, Y., Sun, C., & Zhao, T.", year=2026,
   title="A critical review and future perspectives: How to define, assess, improve, and optimize the energy resilience for building energy systems by generalized flexible energy resources?",
   journal="Renewable and Sustainable Energy Reviews", vol="233", pages="116814",
   doi="10.1016/j.rser.2026.116814", doi_status="web-verified",
   load="Cited for the four-phase resilience formalisation (§1) and as Table 1 row 3 alongside Monie et al.",
   use="DUPLICATE ENTRY IN REFERENCE LIST - appears as both 'Zhang et al. (2026)' and 'Zhang et al. (2026a)'. Merge to 2026a and fix the §1 in-text cite. Also note: this is a BUILDING energy systems review being used to support a NATIONAL energy-system claim - a reviewer may challenge the scope transfer."),
 dict(key="zhang2026b", cite="Zhang et al. 2026b", tier="P1", match=r"Zhang et al\.",
   authors="Zhang, S., Sovacool, B. K., & Wei, C.", year=2026,
   title="Do clean energy transitions enhance global energy security? A comparative analysis of trends and tradeoffs across eight major economies, 1990–2020",
   journal="Energy Policy", vol="212", pages="115164", doi="10.1016/j.enpol.2026.115164", doi_status="web-verified",
   load="Supports the security-vs-average-performance distinction in §1 and §2.5.",
   use="Keep. Closest large-N comparator to your design - use it in the response letter to show the contribution is complementary, not duplicative."),

 dict(key="quitzow2021", cite="Quitzow et al. 2021", tier="P2",
   authors="Quitzow, R., Bersalli, G., Eicke, L., Jahn, J., Lilliestam, J., Lira, F., Marian, A., Süsser, D., Thapar, S., & Weko, S.",
   year=2021, title="The COVID-19 crisis deepens the gulf between leaders and laggards in the global energy transition",
   journal="Energy Research & Social Science", vol="74", pages="101981", doi="10.1016/j.erss.2021.101981", doi_status="unverified",
   load="Evidence that COVID widened cross-country divergence; used in §1, §2.1 and §5.1.",
   use="Keep. Directly relevant to your null COVID result - your finding of no measurable regional shortfall should be reconciled with their divergence claim, not just cited alongside it."),
 dict(key="tian2022", cite="Tian et al. 2022", tier="P2",
   authors="Tian, J., Yu, L., Xue, R., Zhuang, S., & Shan, Y.", year=2022,
   title="Global low-carbon energy transition in the post-COVID-19 era", journal="Applied Energy", vol="307", pages="118205",
   doi="10.1016/j.apenergy.2021.118205", doi_status="unverified",
   load="Evidence that low-carbon momentum continued post-2020; corroborates the positive low-carbon gap.",
   use="Keep in §2.2 and §5.1."),
 dict(key="li2022", cite="Li et al. 2022", tier="P2",
   authors="Li, K., Qi, S., & Shi, X.", year=2022,
   title="The COVID-19 pandemic and energy transitions: Evidence from low-carbon power generation in China",
   journal="Journal of Cleaner Production", vol="368", pages="132994", doi="10.1016/j.jclepro.2022.132994", doi_status="unverified",
   load="China low-carbon generation during COVID; supports the §5.1 reading.",
   use="Keep. Note this is a JCLP paper - if JCLP rejected you, this shows the topic was in scope there; the rejection was about contribution, not fit."),
 dict(key="xu2022", cite="Xu and Sharma 2022", tier="P2", match=r"Xu and Sharma",
   authors="Xu, Y., & Sharma, T.", year=2022,
   title="Explaining expedited energy transition toward renewables by COVID-19 in India", journal="Energy Policy",
   vol="165", pages="112986", doi="10.1016/j.enpol.2022.112986", doi_status="unverified",
   load="India acceleration case; cited ONCE, in §2.2 only.",
   use="Single-use citation. Either give it a role in the discussion or accept it as review furniture."),
 dict(key="crncec2023", cite="Crnčec et al. 2023", tier="P2",
   authors="Crnčec, D., Penca, J., & Lovec, M.", year=2023,
   title="The COVID-19 pandemic and the EU: From a sustainable energy transition to a green transition?",
   journal="Energy Policy", vol="175", pages="113453", doi="10.1016/j.enpol.2023.113453", doi_status="unverified",
   load="EU recovery instruments reshaping the transition agenda; §1 and §2.2.",
   use="Keep as the EU comparator that motivates the ASEAN gap."),
 dict(key="mersch2023", cite="Mersch et al. 2023", tier="P2",
   authors="Mersch, M., Markides, C. N., & Mac Dowell, N.", year=2023,
   title="The impact of the energy crisis on the UK's net-zero transition", journal="iScience", vol="26(5)", pages="106491",
   doi="10.1016/j.isci.2023.106491", doi_status="unverified",
   load="UK net-zero under the price episode; §1 and §2.2.",
   use="Keep. Useful precedent for 'price crisis did not derail decarbonisation' - your regional result agrees."),
 dict(key="jaeger2025", cite="Jaeger-Erben et al. 2025", tier="P2",
   authors="Jaeger-Erben, M., Gram-Hanssen, K., Hansen, A. R., Frąckowiak, M., Guilbert, A., Pluciński, P., Sahakian, M., Wethal, U. B., & Wertheim-Heck, S.",
   year=2025, title="Policies for times of disruptions: How households in Europe dealt with the energy crisis in the winter 2022/2023",
   journal="Energy Policy", vol="205", pages="114711", doi="10.1016/j.enpol.2025.114711", doi_status="unverified",
   load="Cited FOUR times (§1, §2.1, §2.2, §5.1, §5.2) and carries the §5.2 claim that instrument design matters more than presence.",
   use="Heavily loaded for a household-level European study supporting a macro-level ASEAN policy claim. Verify it actually makes a design-over-presence argument, or soften §5.2."),
 dict(key="horbach2026", cite="Horbach and Rammer 2026", tier="P2", match=r"Horbach and Rammer",
   authors="Horbach, J., & Rammer, C.", year=2026,
   title="Energy price shocks and short-term reactions of firms: The case of the German energy crisis in 2022",
   journal="German Economic Review", vol="(advance online publication)", pages="",
   doi="10.1515/ger-2025-0010", doi_status="web-verified",
   load="Firm-level adjustment to price shocks; §1, §2.2, §5.2.",
   use="CITATION DETAIL AT RISK: DOI is ger-2025-0010 and the paper was ahead-of-print. By submission it may have a final volume/issue/year. Re-check and replace 'advance online publication' with full details."),
 dict(key="dorazio2024", cite="D'Orazio 2024", tier="P2", match=r"D.Orazio",
   authors="D'Orazio, P.", year=2024,
   title="Charting the complexities of a post-COVID energy transition: Emerging research frontiers for a sustainable future",
   journal="Energy Research & Social Science", vol="108", pages="103365", doi="10.1016/j.erss.2023.103365", doi_status="unverified",
   load="Green-recovery-vs-lock-in debate; §1, §2.2, and §5.3 where you qualify the green-recovery framing.",
   use="Keep. §5.3 makes a real claim against this literature - that is a contribution, so state it more assertively."),
 dict(key="evro2025", cite="Evro et al. 2025", tier="P2",
   authors="Evro, S., Omonigho, E. N., Mayon, D., Ekpikie, A., Alamooti, M., & Tomomewo, O. S.", year=2025,
   title="Green recovery or fossil lock-in? Assessing sustainability and energy transition pathways in major economies",
   journal="Energy Research & Social Science", vol="127", pages="104205", doi="10.1016/j.erss.2025.104205", doi_status="unverified",
   load="Paired with D'Orazio for the lock-in debate; §1, §2.2, §5.3.",
   use="Keep as a pair with D'Orazio 2024."),
 dict(key="hussain2023", cite="Hussain et al. 2023", tier="P2",
   authors="Hussain, S. A., Razi, F., Hewage, K., & Sadiq, R.", year=2023,
   title="The perspective of energy poverty and 1st energy crisis of green transition", journal="Energy", vol="275", pages="127487",
   doi="10.1016/j.energy.2023.127487", doi_status="unverified",
   load="Competing-channels argument in §2.1; also §5.1 and §6 for the energy-price/energy-poverty link.",
   use="Keep. Supports the future-work call for energy-specific price series in §6."),
 dict(key="zhao2025", cite="Zhao et al. 2025", tier="P2",
   authors="Zhao, X., Zhao, J., & Taghizadeh-Hesary, F.", year=2025,
   title="Is energy system resilience improved in the energy transition? Evidence from China", journal="Energy Economics",
   vol="146", pages="108485", doi="10.1016/j.eneco.2025.108485", doi_status="unverified",
   load="Table 1 row 5 - the panel-econometric tradition you rule out at N=6.",
   use="Keep. This is your explicit justification for not running a panel regression; a reviewer WILL ask why not, so the Table 1 row must be airtight."),
 dict(key="aslam2024", cite="Aslam et al. 2024", tier="P2",
   authors="Aslam, N., Yang, W., Saeed, R., & Ullah, F.", year=2024,
   title="Energy transition as a solution for energy security risk: Empirical evidence from BRI countries", journal="Energy",
   vol="290", pages="130090", doi="10.1016/j.energy.2023.130090", doi_status="unverified",
   load="Import-structure conditioning of the transition/security relationship; §2.4 and Table 1 row 5.",
   use="Keep. Relevant to your Singapore-vs-Indonesia import-exposure contrast in §5.1 - consider citing it there too."),

 dict(key="aleluia2022", cite="Aleluia et al. 2022", tier="P3",
   authors="Aleluia, J., Tharakan, P., Chikkatur, A. P., Shrimali, G., & Chen, X.", year=2022,
   title="Accelerating a clean energy transition in Southeast Asia: Role of governments and public policy",
   journal="Renewable and Sustainable Energy Reviews", vol="159", pages="112226", doi="10.1016/j.rser.2022.112226", doi_status="unverified",
   load="Regional setting (§1, §2.3, §3.2) and the §5.5 electrification-budget recommendation.",
   use="Keep. Main regional-policy anchor."),
 dict(key="bai2023", cite="Bai et al. 2023", tier="P3",
   authors="Bai, W., Zhang, L., Lu, S., Ren, J., & Zhou, Z.", year=2023,
   title="Sustainable energy transition in Southeast Asia: Energy status analysis, comprehensive evaluation and influential factor identification",
   journal="Energy", vol="284", pages="128670", doi="10.1016/j.energy.2023.128670", doi_status="unverified",
   load="Closest regional composite-index comparator; §1, §2.3, §3.2, §5.6.",
   use="IMPORTANT: this is the ASEAN composite-index paper your method is defined AGAINST. Give it a dedicated contrast in §2.5/Table 1 rather than a passing cite - it is the reviewer's obvious 'this already exists' candidate."),
 dict(key="fahim2023", cite="Fahim et al. 2023", tier="P3",
   authors="Fahim, K. E., De Silva, L. C., Hussain, F., Shezan, S. A., & Yassin, H.", year=2023,
   title="An evaluation of ASEAN renewable energy path to carbon neutrality", journal="Sustainability", vol="15(9)", pages="6961",
   doi="10.3390/su15096961", doi_status="unverified",
   load="ASEAN carbon-neutrality pathway; §1, §2.3, §5.4 financing.",
   use="Keep, low load."),
 dict(key="safrina2023", cite="Safrina and Utama 2023", tier="P3", match=r"Safrina and Utama",
   authors="Safrina, R., & Utama, N. A.", year=2023,
   title="ASEAN energy transition pathway toward the 2030 agenda", journal="Environmental Progress & Sustainable Energy",
   vol="42(4)", pages="e14101", doi="10.1002/ep.14101", doi_status="unverified",
   load="Regional 2030 targets; §2.3 and §5.5.",
   use="Keep, low load."),
 dict(key="huweng2024", cite="Hu and Weng 2024", tier="P3", match=r"Hu and Weng",
   authors="Hu, Y., & Weng, L.", year=2024,
   title="Net-zero energy transition in ASEAN countries: The evolutionary model brings novel perspectives to the cooperative mechanism of climate governance",
   journal="Journal of Environmental Management", vol="351", pages="119999", doi="10.1016/j.jenvman.2023.119999", doi_status="unverified",
   load="ASEAN climate-governance cooperation; §1, §2.3, §5.6 monitoring recommendation, §6.",
   use="Keep. Carries the §5.6 'ASEAN already collects these series' claim - verify that is actually supported."),
 dict(key="zhong2025", cite="Zhong et al. 2025", tier="P3",
   authors="Zhong, S., Yang, L., Papageorgiou, D. J., Su, B., Ng, T. S., & Abubakar, S.", year=2025,
   title="Accelerating ASEAN's energy transition in the power sector through cross-border transmission and a net-zero 2050 view",
   journal="iScience", vol="28", pages="111547", doi="10.1016/j.isci.2024.111547", doi_status="unverified",
   load="Cross-border transmission; §1, §2.3, and the §5.3 dispatch-side recommendation.",
   use="Keep. Directly supports one of your five policy recommendations."),
 dict(key="kim2025", cite="Kim et al. 2025", tier="P3",
   authors="Kim, H., Lee, Y., Koo, J.-H., & Yeo, M. J.", year=2025,
   title="Changes in future carbon dioxide emissions and contributing factors in Southeast Asia under the shared socioeconomic pathways",
   journal="Energy for Sustainable Development", vol="86", pages="101721", doi="10.1016/j.esd.2025.101721", doi_status="unverified",
   load="Regional emissions projections; §1, §2.3, §5.6, §6.",
   use="Keep, low load."),
 dict(key="jindal2024", cite="Jindal et al. 2024", tier="P3",
   authors="Jindal, A., Shrimali, G., Gangwani, B., & Lall, R. B.", year=2024,
   title="Financing just energy transitions in Southeast Asia: Application of the Just Transition Transaction to Indonesia, Vietnam, and Philippines",
   journal="Energy for Sustainable Development", vol="81", pages="101472", doi="10.1016/j.esd.2024.101472", doi_status="unverified",
   load="Just-transition financing; §1, §2.4, and the §5.4 pipeline-financing recommendation.",
   use="Keep. Covers exactly your three pipeline-relevant countries."),
 dict(key="kilinc2024", cite="Kilinc-Ata and Proskuryakova 2024", tier="P3", match=r"Kilinc-Ata and Proskuryakova",
   authors="Kilinc-Ata, N., & Proskuryakova, L. N.", year=2024,
   title="The contribution of energy policies to green energy transition in the Asia-Pacific region", journal="Renewable Energy",
   vol="237", pages="121797", doi="10.1016/j.renene.2024.121797", doi_status="unverified",
   load="Administered-pricing mechanisms; §1, §2.4, §5.3.",
   use="Keep. Carries the claim that all six economies use administered pricing - a factual claim that needs a per-country source, not one regional citation."),
 dict(key="alirsyad2025", cite="al Irsyad et al. 2025", tier="P3", match=r"[Aa]l Irsyad",
   authors="Al Irsyad, M. I., Firmansyah, A. I., Hasibuan, V. T. F., et al.", year=2025,
   title="Comparative total cost assessments of electric and conventional vehicles in ASEAN: Commercial vehicles and motorcycle conversion",
   journal="Energy for Sustainable Development", vol="85", pages="101599", doi="10.1016/j.esd.2025.101599", doi_status="unverified",
   load="EV incentives as transition-continuity policy; §2.4 only.",
   use="Single-use. Also fix name form: reference list has 'Al Irsyad', in-text has 'al Irsyad'. Uses 'et al.' in the reference list - Springer requires full author lists."),
 dict(key="champee2025", cite="Champeecharoensuk et al. 2025", tier="P3",
   authors="Champeecharoensuk, T., Saisirirat, P., & Chollacoop, N.", year=2025,
   title="Global warming potential and environmental impacts of electric vehicles and batteries in Association of Southeast Asian Nations (ASEAN)",
   journal="Energy for Sustainable Development", vol="86", pages="101723", doi="10.1016/j.esd.2025.101723", doi_status="unverified",
   load="Paired with al Irsyad for EV policy; §2.4 only.",
   use="Single-use, low load. Safe to cut if you need to reach the 7,000-word limit."),

 dict(key="worldbank2026", cite="World Bank 2026", tier="P0",
   authors="World Bank", year=2026, title="World Development Indicators", journal="World Bank", vol="", pages="",
   doi="", doi_status="n/a",
   load="Source for TDLoss (EG.ELC.LOSS.ZS), AccessElec (EG.ELC.ACCS.ZS), Inflation (FP.CPI.TOTL.ZG) - i.e. all of energy-service security and all of macro-price stability.",
   use="MUST add an explicit access date. WDI is revised continuously; without a retrieval date the panel is not reproducible. You already promise a 'data-revision log' - cite its DOI."),
 dict(key="unsd2026", cite="United Nations Statistics Division 2026", tier="P0",
   authors="United Nations Statistics Division", year=2026,
   title="SDG indicators database: Indicators 7.2.1 and 7.3.1", journal="United Nations", vol="", pages="",
   doi="", doi_status="n/a",
   load="Source for RenTFEC (7.2.1) and EnergyIntensity (7.3.1) - two of five low-carbon indicators.",
   use="Add access date and the exact series codes as retrieved (EG_FEC_RNEW, EG_EGY_PRIM already given in Table 2 - good)."),
 dict(key="ember2024", cite="Ember 2024", tier="P0",
   authors="Ember", year=2024, title="Yearly electricity data", journal="Ember", vol="", pages="", doi="", doi_status="n/a",
   load="Source for CO2IntElec and RenElec - the two indicators that carry the largest positive low-carbon contributions in 2022-23 (+0.049 and +0.038).",
   use="Add access date and version. Your headline low-carbon decomposition rests on this source."),
 dict(key="irena2024", cite="IRENA 2024", tier="P0",
   authors="IRENA", year=2024, title="Renewable capacity statistics 2024", journal="International Renewable Energy Agency",
   vol="", pages="", doi="", doi_status="n/a",
   load="Source for RenCap - the indicator driving Vietnam's +0.358 and Malaysia's -0.348 country contributions.",
   use="The Vietnam 268 -> 391 W/person figure in §5.4 comes from here. Give the exact table and confirm whether it is total renewable capacity (incl. hydro) or non-hydro - the interpretation changes completely."),
 dict(key="iea2024", cite="International Energy Agency 2024", tier="P0",
   authors="International Energy Agency", year=2024, title="Policies and measures database", journal="IEA", vol="", pages="",
   doi="", doi_status="n/a",
   load="Policy-function inventory source (§3.5, Table 7).",
   use="Add access date. Because the inventory is coded by presence/absence, the retrieval date determines the coding - this is a reproducibility requirement, not a formality."),
 dict(key="imf2021", cite="International Monetary Fund 2021", tier="P0",
   authors="International Monetary Fund", year=2021, title="Policy responses to COVID-19", journal="IMF", vol="", pages="",
   doi="", doi_status="n/a",
   load="Policy-function inventory source (§3.5, Table 7).",
   use="PROBLEM: the IMF COVID-19 policy tracker was discontinued and covers to ~2021, but Table 7 codes 2022-2023 actions. State which source covers which stage, or the 2022-23 coding has no documented basis."),
]

# --------------------------------------------------------- 3. citation mapping
def find_citations(secs, refs):
    """Map each ref key -> ordered list of sections where its surname pattern appears."""
    # build a matcher from the first author surname + year
    loc = collections.defaultdict(list)
    for r in refs:
        yr = str(r["year"])
        # explicit override wins; otherwise take the surname token(s) before
        # "et al."/"and"/the year, so multi-word surnames ("al Irsyad",
        # "Kilinc-Ata and Proskuryakova") are matched whole and not by fragment.
        if r.get("match"):
            head = r["match"]
        else:
            head = re.split(r"\s+(?:et al\.|and|\d{4})", r["cite"])[0].strip()
            head = re.escape(head)
        # require a word boundary on both sides so "al" cannot match inside a word,
        # and keep the year within the same citation parenthetical
        pat = re.compile(r"(?<![\w-])" + head + r"(?![\w-])[^;)\n]{0,45}?" + yr)
        for name, body in secs:
            if name == "References":
                continue
            if pat.search(body):
                loc[r["key"]].append(name)
    return loc

def slug(r):
    surname = re.split(r"[ ,]", r["cite"])[0].replace("/", "-")
    words = re.sub(r"[^A-Za-z0-9 ]", "", r["title"]).split()[:5]
    return f"{surname}-{r['year']}-{'-'.join(words)}"[:80]

TIER_NAME = {"P1":"P1 - load-bearing", "P2":"P2 - supporting evidence",
             "P3":"P3 - contextual / regional", "P0":"P0 - data & policy source"}

def main():
    text = open(SRC, encoding="utf-8").read()
    text = text.replace("\u2019", "'").replace("\u2018", "'")
    secs = parse_sections(text)
    loc  = find_citations(secs, REFS)
    os.makedirs(LIT, exist_ok=True)
    index = []
    for r in REFS:
        where = loc.get(r["key"], [])
        fn = slug(r) + ".md"
        vol = f", {r['vol']}" if r["vol"] else ""
        pg  = f", {r['pages']}" if r["pages"] else ""
        full = f"{r['authors']} ({r['year']}). {r['title']}. {r['journal']}{vol}{pg}."
        body = f"""---
cite_key: {r['key']}
in_text: "{r['cite']}"
year: {r['year']}
journal: "{r['journal']}"
priority: {r['tier']}
doi: "{r['doi']}"
doi_status: {r['doi_status']}
cited_in: {json.dumps(where)}
cite_count: {len(where)}
tags: [literature, {r['tier']}, eds-revision]
---

# {r['cite']}

> {full}

**Priority** :: {TIER_NAME[r['tier']]}
**Cited in** :: {', '.join(where) if where else '⚠️ NOT FOUND IN BODY TEXT'}
**DOI** :: {r['doi'] or '—'} ({r['doi_status']})

## What the argument rests on
{r['load']}

## Usage suggestion for the EDS revision
{r['use']}

## Verification
- [ ] Full record checked against publisher page (authors, volume, pages, year)
- [ ] DOI resolves
- [ ] The claim attributed to this source is actually made in it
- [ ] Springer/APA reference format applied

## Notes
<!-- daily capture goes here -->
"""
        open(os.path.join(LIT, fn), "w", encoding="utf-8").write(body)
        index.append((r, where, fn))
    return index, secs

if __name__ == "__main__":
    idx, secs = main()
    print(f"sections parsed : {len(secs)}")
    print(f"notes written   : {len(idx)}")
    orphan = [r['cite'] for r,w,f in idx if not w]
    print(f"orphan refs     : {orphan if orphan else 'none'}")
    for tier in ("P1","P2","P3","P0"):
        n=[r['cite'] for r,w,f in idx if r['tier']==tier]
        print(f"  {tier}: {len(n)}")
    print("\nMost-cited:")
    for r,w,f in sorted(idx, key=lambda x:-len(x[1]))[:8]:
        print(f"  {len(w)}x {r['cite']:<40} {w}")

# ---------------------------------------------------------------- 4. index
def write_index(idx):
    """Emit the prioritised reading order used by the daily workflow."""
    TIERDESC = {
      "P1": "Read first. The argument does not survive if one of these is misused.",
      "P2": "Substantive evidence cited in support of specific claims.",
      "P3": "Regional and contextual framing. Low load; first candidates for cuts.",
      "P0": "Data and policy sources. Needs access dates, not reading.",
    }
    out = ["---", "type: index", "total: %d" % len(idx),
           "tags: [literature, index]", "---", "",
           "# Literature index — prioritised", "",
           "Generated by `scripts/build_vault.py`. `cited_in` is parsed from the",
           "manuscript itself, so this stays true if the text changes — re-run it.", ""]
    for tier in ("P1","P2","P3","P0"):
        rows = [(r,w,f) for r,w,f in idx if r["tier"]==tier]
        rows.sort(key=lambda x:-len(x[1]))
        out += [f"## {TIER_NAME[tier]} ({len(rows)})", "", f"*{TIERDESC[tier]}*", "",
                "| × | Reference | Journal | DOI | Cited in |", "|---|---|---|---|---|"]
        for r,w,f in rows:
            mark = "✅" if r["doi_status"]=="web-verified" else ("—" if r["doi_status"]=="n/a" else "🔍")
            secs = ", ".join(s.split(" ")[0].rstrip(".") for s in w) or "—"
            out.append(f"| {len(w)} | [[{f[:-3]}\\|{r['cite']}]] | {r['journal']} | {mark} | {secs} |")
        out.append("")
    out += ["## DOI verification status", "",
            "✅ web-verified this session · 🔍 reconstructed, **must be confirmed** · — n/a", "",
            "See [[../03-Audit/Needs-Verification#NV11]].", ""]
    open(os.path.join(LIT, "_Index.md"), "w", encoding="utf-8").write("\n".join(out))
