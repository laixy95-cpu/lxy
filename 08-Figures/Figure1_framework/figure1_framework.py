# -*- coding: utf-8 -*-
"""
Fig. 1. Overall research framework and technical workflow.

Converging resilience and diverging transition capacity: urban low-carbon
energy resilience in China's Yellow River Basin, 2015-2021.

Layout paradigm follows Fig. 2 of Huang et al. (2026, Urban Climate 70, 103145):
four tinted module columns with a dark title bar, stacked white boxes linked by
down-arrows, nested chips, a dark result box at the foot of each column, and
horizontal "evidence" arrows between columns.

Pure matplotlib. No external files. Paste into ONE Google Colab cell and run.
Outputs: Figure1_framework.svg / .pdf / .png (600 dpi)
"""

# =============================================================================
# 0. IMPORTS & FONT SET-UP
# =============================================================================
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D

# Arial first; Liberation Sans is metric-identical to Arial and ships with
# Colab/Linux; DejaVu Sans is the guaranteed last resort.
FONT_CANDIDATES = ["Arial", "Helvetica", "Liberation Sans", "DejaVu Sans"]


def _pick_font(cands):
    for name in cands:
        try:
            fm.findfont(name, fallback_to_default=False)
            return name
        except Exception:
            continue
    return "DejaVu Sans"


FONT = _pick_font(FONT_CANDIDATES)

# =============================================================================
# 1. GLOBAL PARAMETERS  (edit here)
# =============================================================================
# --- canvas -----------------------------------------------------------------
FIG_W, FIG_H = 7.48, 4.30          # inches (190 mm = Elsevier double column)
DPI = 300                          # working / on-screen dpi
PNG_DPI = 600                      # exported PNG dpi
OUT_NAME = "Figure1_framework"
SHOW_CAPTION = True                # False -> drop the caption line inside the art
CAPTION = ("Fig. 1.", " Overall research framework and technical workflow.")

# --- font sizes (pt) --------------------------------------------------------
FS_MODULE = 6.6      # module title bar (bold, white)
FS_BOXTITLE = 6.2    # white-box title (bold)
FS_BODY = 5.5        # body text
FS_CHIP = 5.4        # nested chips / badges
FS_RESULT = 5.5      # dark result boxes
FS_RESULT_BIG = 6.2  # emphasised number line in result boxes
FS_AUX = 5.4         # "evidence" labels
FS_BAND = 6.2        # bottom conclusion band
FS_CAPTION = 6.2
LINE_SPACING = 1.24  # line height = font size x LINE_SPACING
MATH_SCRIPT_SCALE = 0.92  # sub/superscript size in $..$ (matplotlib default 0.7);
                          # 0.92 keeps scripts >= 5 pt (5.5 pt x 0.92 = 5.06 pt)

# --- colours ----------------------------------------------------------------
PALETTE = {  # dark / light background / stroke
    1: dict(dark="#1B7FD4", light="#EAF2FB", edge="#A9CDEE"),
    2: dict(dark="#00A087", light="#E6F5F1", edge="#9FD4C6"),
    3: dict(dark="#F28522", light="#FDF0E3", edge="#F6C999"),
    4: dict(dark="#E64B35", light="#FCEDEA", edge="#F2B3A8"),
}
C_GREY = "#777777"        # inter-module arrows & auxiliary text
C_TEXT = "#262626"        # body text
C_BAND_BG, C_BAND_EDGE = "#F4F6F8", "#C9D2DA"

# --- geometry (data units, canvas = 0-100 in x and y) ------------------------
MARGIN_X = 0.55           # left/right canvas margin
MARGIN_TOP = 0.9
COL_GAP = 5.0             # gap between module panels (holds "evidence" arrow)
TITLE_H = 8.2             # dark title bar height
PANEL_PAD_X = 1.05        # panel edge -> white boxes
PANEL_PAD_TOP = 1.6       # title bar -> first white box
PANEL_PAD_BOT = 1.3       # last box -> panel bottom
BOX_PAD_Y = 1.05          # inner top/bottom padding of white boxes
BOX_PAD_X = 0.75          # inner left/right padding (chips)
TITLE_GAP = 0.55          # box title -> first content row
ARROW_GAP = 2.6           # vertical gap between stacked boxes (down-arrow)
CHIP_H = 2.75             # chip height
CHIP_VGAP = 0.55          # vertical gap between chip rows
CHIP_HGAP = 0.55          # horizontal gap between chips
BADGE_W = 2.0             # width of number/letter badge inside an item chip
CHIP_INSET = 0.3          # min. clear space between chip text and chip edge
RULE_H = 1.5              # height reserved for a divider rule
RADIUS_PANEL = 1.1        # corner radius (x-units); y is auto-corrected
RADIUS_BOX = 0.8
RADIUS_CHIP = 0.45
LW_PANEL, LW_BOX, LW_CHIP = 0.7, 0.6, 0.45
BAND_H = 5.0              # bottom conclusion band height
BAND_GAP = 1.3            # panels -> band
CAPTION_H = 3.6           # space kept for the caption line
# Optional manual extra height for single boxes: {(module, box_index): units}
BOX_EXTRA = {}

# =============================================================================
# 2. CONTENT  (all text and numbers live here)
# =============================================================================
# Row types inside a box:
#   ("text",  "string")                          centred body line ($..$ = math)
#   ("rich",  [(txt, style), ...])               one line, mixed bold/colour
#   ("chips", ["a", "b", ...], ncols)            equal-width chip grid
#   ("item",  "badge", "label", "right", hl)     chip with badge (+ right tag)
#   ("note",  "string")                          italic line in module colour
#   ("rule",)                                    thin divider
#   ("space", h)                                 vertical space (units)
B = {"weight": "bold"}

MODULES = [
    dict(
        title="Module 1: Measurement and\npanel construction",
        boxes=[
            dict(title="Study area and sample", rows=[
                ("text", "HydroBASINS L8 units linked by"),
                ("text", "NEXT_SINK, intersected with cities"),
                ("text", "≥30% of city area in basin → 40"),
                ("text", "Haidong dropped (missing data)"),
                ("space", 0.35),
                ("chips", ["39 cities × 2015–2021 = 273"], 1),
            ]),
            dict(title="13 indicators, 4 subsystems", rows=[
                ("item", "A", "Energy service", "I01–03", False),
                ("item", "B", "Low-carbon transition", "I04–07", True),
                ("item", "C", "Social & infrastructure", "I08–09", False),
                ("item", "D", "Environmental gov.", "I10–13", False),
                ("note", "I05 and I11 enter inversely"),
            ]),
            dict(title="Normalisation and weighting", rows=[
                ("text", "Pooled min–max over 273 records"),
                ("text", "Entropy weights within subsystem"),
                ("text", "Fixed subsystem weight = 0.25"),
            ]),
        ],
        result=[
            ("rich", [("LCER index", B)]),
            ("rich", [("+ four subsystem scores (A–D)", {})]),
            ("rule",),
            ("rich", [("Accounting identity holds:", {})]),
            ("rich", [("error < 2 × $10^{-16}$", B)]),
        ],
    ),
    dict(
        title="Module 2: Convergence and\naccounting decomposition",
        boxes=[
            dict(title="Distribution and convergence", rows=[
                ("text", "39 cities, each year 2015–2021"),
                ("space", 0.3),
                ("chips", ["Mean · SD", "CV · Theil",
                           "σ: CV-slope test", "β: absolute"], 2),
            ]),
            dict(title="Spatial dependence", rows=[
                ("text", "Global Moran’s I by year"),
                ("text", "4-nearest-neighbour weights"),
                ("text", "999 random permutations"),
            ]),
            dict(title="Accounting decomposition", rows=[
                ("chips", ["Eq. (9): shares of mean gain",
                           "Eq. (10): yearly variance shares",
                           "Group gaps split by indicator"], 1),
            ]),
        ],
        result=[
            ("rich", [("Mean ", {}), ("0.3301 → 0.4082", B), (" (+23.7%)", {})]),
            ("rich", [("CV −25.4% · Theil −43.6%", {})]),
            ("rich", [("β = −0.0710", B)]),
            ("rule",),
            ("rich", [("but B’s variance share", {})]),
            ("rich", [("14.5% → 43.6%", {"weight": "bold", "size": FS_RESULT_BIG})]),
        ],
    ),
    dict(
        title="Module 3: Three-group design\nand divergence tests",
        boxes=[
            dict(title="Three-group design", rows=[
                ("item", "8", "Provincial capitals", "", True),
                ("item", "7", "Other non-resource cities", "", False),
                ("item", "24", "Resource-based cities", "", False),
                ("note", "No capital is resource-based, so a"),
                ("note", "two-group test reads hierarchy"),
                ("note", "as resource dependence"),
            ]),
            dict(title="Divergence model, Eq. (11)", rows=[
                ("text", r"$Y_{it}=\mu_i+\lambda_t+\gamma\,(\mathrm{RD01}_i\times t)$"),
                ("text", r"$+\;\delta\,(\mathrm{CAP}_i\times t)+\varepsilon_{it}$"),
                ("text", "City and year fixed effects"),
            ]),
            dict(title="Inference and robustness", rows=[
                ("chips", ["City-clustered SE", "Wild boot. 9,999",
                           "Permutation 200k", "City boot. 20,000",
                           "Drop each city", "Drop 2017 / 2020"], 2),
                ("chips", ["+ ln(registered population)"], 1),
            ]),
        ],
        result=[
            ("rich", [("δ = ", B), ("+0.0193", {"weight": "bold", "size": FS_RESULT_BIG}),
                      (" per year", {})]),
            ("rich", [("wild bootstrap ", {}), ("p", {"style": "italic"}), (" = 0.004", {})]),
            ("rule",),
            ("rich", [("Capitals: ", {}), ("87.1%", B), (" of B gap", {})]),
            ("rich", [("Green invention (I07):", {})]),
            ("rich", [("81.5%", B), (" of the capitals’ lead", {})]),
        ],
    ),
    dict(
        title="Module 4: Predictive attribution\nof city type",
        boxes=[
            dict(title="Learners and validation", rows=[
                ("chips", ["Baseline", "Ridge", "Random forest"], 3),
                ("space", 0.35),
                ("text", "Baseline = training-fold mean"),
                ("text", "5-fold GroupKFold, whole cities"),
                ("text", "Inner 4-fold tuning on MAE"),
                ("text", "Seed 20260928"),
            ]),
            dict(title="SHAP attribution", rows=[
                ("text", "Importance: mean |OOF SHAP|"),
                ("text", "Direction: Spearman ρ (x, SHAP)"),
            ]),
            dict(title="Four specifications", rows=[
                ("item", "1", "Published 9 predictors", "", False),
                ("item", "2", "+ Capital dummy", "", True),
                ("item", "3", "Capital replaces RB dummy", "", False),
                ("item", "4", "Drop 8 capitals (31 cities)", "", False),
            ]),
        ],
        result=[
            ("rich", [("+ capital dummy, target B:", {})]),
            ("rich", [("RB share ", {}), ("22.0% → 14.0%", B)]),
            ("rich", [("Capital ", {}), ("32.1%", B), (", 1st in 5/5 folds", {})]),
            ("rich", [("Hold-out R² ", {}), ("0.580 → 0.622", B)]),
            ("rule",),
            ("rich", [("No capitals: R² = ", {}), ("−0.308", B)]),
            ("rich", [("RB dummy 7th of 9 (6.4%)", {})]),
        ],
    ),
]

BAND_TEXT = [
    ("Overall resilience ", {}),
    ("converges", {"color": PALETTE[2]["dark"]}),
    (" while transition capacity ", {}),
    ("diverges along the urban hierarchy", {"color": PALETTE[3]["dark"]}),
    (", and the divergence runs through ", {}),
    ("green invention", {"color": PALETTE[4]["dark"]}),
]
EVIDENCE_LABEL = "evidence"

# =============================================================================
# 3. STYLE & HELPERS
# =============================================================================
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": [FONT] + [f for f in FONT_CANDIDATES if f != FONT],
    "mathtext.fontset": "custom",
    "mathtext.rm": FONT,
    "mathtext.it": FONT + ":italic",
    "mathtext.bf": FONT + ":bold",
    "mathtext.sf": FONT,
    "svg.fonttype": "none",      # SVG text stays editable
    "pdf.fonttype": 42,          # TrueType embedded
    "ps.fonttype": 42,
    "axes.unicode_minus": True,
})

try:  # enlarge mathtext sub/superscripts so they never fall below 5 pt
    import matplotlib._mathtext as _mt
    _mt.SHRINK_FACTOR = MATH_SCRIPT_SCALE
except Exception:
    MATH_SCRIPT_SCALE = 0.7

PT2U = 100.0 / (FIG_H * 72.0)        # 1 pt in y data units
ASPECT = FIG_W / FIG_H               # x-unit / y-unit in inches (corner fix)


def lh(fs):
    """Line height (y units) for font size fs."""
    return fs * LINE_SPACING * PT2U


fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")
fig.patch.set_facecolor("white")
RENDERER = fig.canvas.get_renderer()

QA_TEXT = []      # (text artist, container (x0, y0, x1, y1), tag)
QA_ARROWS = []    # arrow artists
QA_COLS = []      # (panel_y0, panel_y1, result_y0, result_y1)


def rbox(x, y, w, h, fc, ec, lw, r, z=1, ls="-"):
    """Rounded box with circular corners despite unequal x/y units."""
    p = FancyBboxPatch((x, y), w, h,
                       boxstyle=f"round,pad=0,rounding_size={r}",
                       mutation_aspect=ASPECT, fc=fc, ec=ec, lw=lw, ls=ls,
                       zorder=z, joinstyle="round")
    ax.add_patch(p)
    return p


def arrow(x0, y0, x1, y1, color, lw=0.8, ms=5.0, z=6):
    a = FancyArrowPatch((x0, y0), (x1, y1),
                        arrowstyle="-|>,head_length=0.55,head_width=0.32",
                        mutation_scale=ms, color=color, lw=lw,
                        shrinkA=0, shrinkB=0, zorder=z, joinstyle="miter")
    ax.add_patch(a)
    QA_ARROWS.append(a)
    return a


def text(x, y, s, fs, container, tag="", **kw):
    kw.setdefault("color", C_TEXT)
    kw.setdefault("ha", "center")
    kw.setdefault("va", "center")
    t = ax.text(x, y, s, fontsize=fs, zorder=8, **kw)
    if container is not None:
        QA_TEXT.append((t, container, tag))
    return t


def width_u(s, fs, **kw):
    """Rendered width of a string in x data units."""
    t = ax.text(0, 0, s, fontsize=fs, **kw)
    bb = t.get_window_extent(RENDERER)
    t.remove()
    return bb.width / ax.bbox.width * 100.0


def rich(xc, y, segs, fs, container, color, tag=""):
    """Centred single line made of differently styled segments."""
    ws = []
    for s, st in segs:
        st2 = {k: v for k, v in st.items() if k != "size"}
        ws.append(width_u(s, st.get("size", fs), **st2))
    x = xc - sum(ws) / 2.0
    for (s, st), w in zip(segs, ws):
        kw = dict(color=st.get("color", color), fontweight=st.get("weight", "normal"),
                  fontstyle=st.get("style", "normal"))
        text(x, y, s, st.get("size", fs), container, tag, ha="left", **kw)
        x += w


# --- row heights ----------------------------------------------------------------
def row_h(row, fs_text):
    k = row[0]
    if k in ("text", "note"):
        return lh(fs_text)
    if k == "rich":
        big = max([st.get("size", fs_text) for _, st in row[1]] + [fs_text])
        return lh(big)
    if k == "chips":
        n = -(-len(row[1]) // row[2])
        return n * CHIP_H + (n - 1) * CHIP_VGAP + CHIP_VGAP
    if k == "item":
        return CHIP_H + CHIP_VGAP
    if k == "rule":
        return RULE_H
    if k == "space":
        return row[1]
    raise ValueError(k)


def content_h(title, rows, fs_text):
    h = sum(row_h(r, fs_text) for r in rows)
    if title:
        h += lh(FS_BOXTITLE) + TITLE_GAP
    return h


# --- row drawing ------------------------------------------------------------------
def draw_rows(x0, w, y_top, rows, pal, fs_text, color, container, tag):
    y = y_top
    for row in rows:
        k, h = row[0], row_h(row, fs_text)
        yc = y - h / 2.0
        if k == "text":
            text(x0 + w / 2, yc, row[1], fs_text, container, tag, color=color)
        elif k == "note":
            text(x0 + w / 2, yc, row[1], fs_text, container, tag,
                 color=pal["dark"], fontstyle="italic")
        elif k == "rich":
            rich(x0 + w / 2, yc, row[1], fs_text, container, color, tag)
        elif k == "rule":
            ax.add_line(Line2D([x0 + 1.2, x0 + w - 1.2], [yc, yc], lw=0.4,
                               color="white", alpha=0.75, zorder=7))
        elif k == "chips":
            labels, nc = row[1], row[2]
            inner = w - 2 * BOX_PAD_X - (nc - 1) * CHIP_HGAP
            cy = y - CHIP_VGAP / 2.0
            if nc == len(labels) and nc > 1:
                # single row: chip widths proportional to label widths
                tw = [width_u(lab, FS_CHIP) for lab in labels]
                extra = (inner - sum(tw)) / nc
                widths = [t + extra for t in tw]
            else:
                widths = [inner / nc] * nc
            for i, lab in enumerate(labels):
                r, c = divmod(i, nc)
                cw = widths[c]
                cx = x0 + BOX_PAD_X + sum(widths[:c]) + c * CHIP_HGAP
                yy = cy - r * (CHIP_H + CHIP_VGAP) - CHIP_H
                rbox(cx, yy, cw, CHIP_H, pal["light"], pal["edge"], LW_CHIP, RADIUS_CHIP, z=4)
                text(cx + cw / 2, yy + CHIP_H / 2, lab, FS_CHIP,
                     (cx, yy, cx + cw, yy + CHIP_H), tag + ":chip")
        elif k == "item":
            _, badge, label, right, hl = row
            cx, cw = x0 + BOX_PAD_X, w - 2 * BOX_PAD_X
            yy = y - CHIP_VGAP / 2.0 - CHIP_H
            rbox(cx, yy, cw, CHIP_H, pal["light"], pal["dark"] if hl else pal["edge"],
                 LW_CHIP * (1.6 if hl else 1.0), RADIUS_CHIP, z=4)
            bw = BADGE_W if len(badge) > 1 else BADGE_W * 0.82
            rbox(cx + 0.35, yy + 0.35, bw, CHIP_H - 0.7, pal["dark"], "none", 0,
                 RADIUS_CHIP * 0.8, z=5)
            text(cx + 0.35 + bw / 2, yy + CHIP_H / 2, badge, FS_CHIP,
                 (cx, yy, cx + 0.7 + bw, yy + CHIP_H), tag + ":badge",
                 color="white", fontweight="bold")
            lx = cx + 0.35 + bw + 0.55
            text(lx, yy + CHIP_H / 2, label, FS_CHIP, (cx, yy, cx + cw, yy + CHIP_H),
                 tag + ":item", ha="left", fontweight="bold" if hl else "normal")
            if right:
                text(cx + cw - 0.45, yy + CHIP_H / 2, right, FS_CHIP,
                     (cx, yy, cx + cw, yy + CHIP_H), tag + ":tag", ha="right",
                     color=pal["dark"], fontweight="bold")
        y -= h


def draw_box(x, y0, w, h, title, rows, pal, tag, dark=False):
    """White (or dark result) box; content block centred vertically."""
    if dark:
        rbox(x, y0, w, h, pal["dark"], pal["dark"], LW_BOX, RADIUS_BOX, z=3)
        fs, color = FS_RESULT, "white"
    else:
        rbox(x, y0, w, h, "white", pal["edge"], LW_BOX, RADIUS_BOX, z=3)
        fs, color = FS_BODY, C_TEXT
    cont = (x, y0, x + w, y0 + h)
    ch = content_h(title, rows, fs)
    y = y0 + h / 2 + ch / 2
    if title:
        text(x + w / 2, y - lh(FS_BOXTITLE) / 2, title, FS_BOXTITLE, cont, tag + ":title",
             color=pal["dark"], fontweight="bold")
        y -= lh(FS_BOXTITLE) + TITLE_GAP
    draw_rows(x, w, y, rows, pal, fs, color, cont, tag)


# =============================================================================
# 4. BUILD THE FIGURE
# =============================================================================
y_caption = CAPTION_H if SHOW_CAPTION else 0.6
band_y0 = y_caption + 0.6
panel_y0 = band_y0 + BAND_H + BAND_GAP
panel_y1 = 100 - MARGIN_TOP
col_w = (100 - 2 * MARGIN_X - 3 * COL_GAP) / 4.0
box_w = col_w - 2 * PANEL_PAD_X

# common result-box height = tallest natural result content
res_h = max(content_h(None, m["result"], FS_RESULT) for m in MODULES) + 2 * BOX_PAD_Y
res_y0 = panel_y0 + PANEL_PAD_BOT
stack_top = panel_y1 - TITLE_H - PANEL_PAD_TOP
stack_bot = res_y0 + res_h + ARROW_GAP          # bottom of last white box

result_boxes = []
for mi, mod in enumerate(MODULES, start=1):
    pal = PALETTE[mi]
    px = MARGIN_X + (mi - 1) * (col_w + COL_GAP)
    # panel + title bar (dark bar with squared lower corners)
    rbox(px, panel_y0, col_w, panel_y1 - panel_y0, pal["light"], pal["edge"], LW_PANEL,
         RADIUS_PANEL, z=0)
    rbox(px, panel_y1 - TITLE_H, col_w, TITLE_H, pal["dark"], pal["dark"], LW_PANEL,
         RADIUS_PANEL, z=1)
    ax.add_patch(plt.Rectangle((px, panel_y1 - TITLE_H), col_w, TITLE_H / 2,
                               fc=pal["dark"], ec="none", zorder=1.1))
    ax.add_line(Line2D([px, px], [panel_y1 - TITLE_H, panel_y1 - TITLE_H / 2],
                       color=pal["dark"], lw=LW_PANEL, zorder=1.2))
    ax.add_line(Line2D([px + col_w, px + col_w], [panel_y1 - TITLE_H, panel_y1 - TITLE_H / 2],
                       color=pal["dark"], lw=LW_PANEL, zorder=1.2))
    text(px + col_w / 2, panel_y1 - TITLE_H / 2, mod["title"], FS_MODULE,
         (px, panel_y1 - TITLE_H, px + col_w, panel_y1), f"M{mi}:title",
         color="white", fontweight="bold", linespacing=1.15)

    # natural heights + equal share of the slack
    bx = px + PANEL_PAD_X
    nat = [content_h(b["title"], b["rows"], FS_BODY) + 2 * BOX_PAD_Y
           + BOX_EXTRA.get((mi, i), 0) for i, b in enumerate(mod["boxes"])]
    avail = stack_top - stack_bot - ARROW_GAP * (len(nat) - 1)
    slack = avail - sum(nat)
    hs = [h + slack / len(nat) for h in nat]

    y = stack_top
    for i, (b, h) in enumerate(zip(mod["boxes"], hs)):
        draw_box(bx, y - h, box_w, h, b["title"], b["rows"], pal, f"M{mi}B{i + 1}")
        y -= h
        # down arrow to next box (or to the result box)
        arrow(bx + box_w / 2, y - 0.15, bx + box_w / 2, y - ARROW_GAP + 0.15,
              pal["dark"], lw=0.8, ms=5)
        y -= ARROW_GAP

    draw_box(bx, res_y0, box_w, res_h, None, mod["result"], pal, f"M{mi}R", dark=True)
    result_boxes.append((bx, res_y0, box_w, res_h))
    QA_COLS.append((panel_y0, panel_y1, res_y0, res_y0 + res_h))
    if slack < 0:
        print(f"[WARN] Module {mi}: content exceeds column by {-slack:.2f} units")

# --- "evidence" arrows between result boxes ----------------------------------------
for i in range(3):
    x0 = result_boxes[i][0] + result_boxes[i][2]
    x1 = result_boxes[i + 1][0]
    ya = res_y0 + res_h / 2
    arrow(x0 + 0.2, ya, x1 - 0.2, ya, C_GREY, lw=1.0, ms=6, z=9)
    gx0 = MARGIN_X + (i + 1) * col_w + i * COL_GAP
    text((x0 + x1) / 2, ya + 1.9, EVIDENCE_LABEL, FS_AUX,
         (gx0 - PANEL_PAD_X, ya, gx0 + COL_GAP + PANEL_PAD_X, ya + 4), f"EV{i + 1}",
         color=C_GREY, fontstyle="italic")

# --- bottom conclusion band ------------------------------------------------------------
band = (MARGIN_X, band_y0, 100 - MARGIN_X, band_y0 + BAND_H)
rbox(MARGIN_X, band_y0, 100 - 2 * MARGIN_X, BAND_H, C_BAND_BG, C_BAND_EDGE, LW_PANEL,
     RADIUS_BOX, z=1)
rich(50, band_y0 + BAND_H / 2,
     [(s, dict(st, weight="bold")) for s, st in BAND_TEXT], FS_BAND, band, "#333333", "BAND")

# --- caption -------------------------------------------------------------------------------
if SHOW_CAPTION:
    rich(50, y_caption / 2 + 0.3, [(CAPTION[0], B), (CAPTION[1], {})], FS_CAPTION,
         (0, 0, 100, y_caption + 0.6), "#000000", "CAPTION")


# =============================================================================
# 5. LAYOUT QA  (overflow, arrows over text, column alignment, font sizes)
# =============================================================================
def layout_report(tol_px=0.5):
    fig.canvas.draw()
    rend = fig.canvas.get_renderer()
    to_disp = ax.transData.transform
    issues = []
    tbbs = []
    for t, (x0, y0, x1, y1), tag in QA_TEXT:
        bb = t.get_window_extent(rend)
        (cx0, cy0), (cx1, cy1) = to_disp((x0, y0)), to_disp((x1, y1))
        if tag.endswith((":chip", ":item", ":tag")):     # chips need a visible inset
            inset = CHIP_INSET / 100.0 * ax.bbox.width
            cx0, cx1 = cx0 + inset, cx1 - inset
        tbbs.append((bb, tag, t.get_text()))
        if (bb.x0 < cx0 - tol_px or bb.x1 > cx1 + tol_px or
                bb.y0 < cy0 - tol_px or bb.y1 > cy1 + tol_px):
            issues.append(f"(a) overflow  [{tag}] '{t.get_text()}'")
        fs_eff = t.get_fontsize() * (MATH_SCRIPT_SCALE if "$" in t.get_text() else 1)
        if fs_eff < 5.0:
            issues.append(f"(d) font < 5 pt [{tag}] {fs_eff:.2f}")
    for a in QA_ARROWS:
        ab = a.get_window_extent(rend)
        for bb, tag, s in tbbs:
            if ab.overlaps(bb):
                issues.append(f"(b) arrow crosses text [{tag}] '{s}'")
    for i in range(len(tbbs)):                       # text-on-text overlap
        for j in range(i + 1, len(tbbs)):
            bi, bj = tbbs[i][0], tbbs[j][0]
            if bi.overlaps(bj):
                ox = min(bi.x1, bj.x1) - max(bi.x0, bj.x0)
                oy = min(bi.y1, bj.y1) - max(bi.y0, bj.y0)
                if ox > 1 and oy > 1:
                    issues.append(f"    text overlap '{tbbs[i][2]}' / '{tbbs[j][2]}'")
    if len({(round(a, 6), round(b, 6), round(c, 6), round(d, 6)) for a, b, c, d in QA_COLS}) != 1:
        issues.append("(c) columns not aligned")
    fs_all = [t.get_fontsize() * (MATH_SCRIPT_SCALE if "$" in t.get_text() else 1)
              for t in ax.texts]
    print(f"Font: {FONT} | min font size (incl. math scripts) = {min(fs_all):.2f} pt | "
          f"texts checked = {len(QA_TEXT)} | arrows checked = {len(QA_ARROWS)}")
    print(f"Columns: 4 panels share y = [{QA_COLS[0][0]:.2f}, {QA_COLS[0][1]:.2f}], "
          f"result boxes y = [{QA_COLS[0][2]:.2f}, {QA_COLS[0][3]:.2f}]")
    print("Layout QA:", "PASS - no issues" if not issues else f"{len(issues)} issue(s)")
    for s in issues:
        print("  ", s)
    return issues


layout_report()

# =============================================================================
# 6. EXPORT
# =============================================================================
fig.savefig(f"{OUT_NAME}.svg", format="svg", facecolor="white")
fig.savefig(f"{OUT_NAME}.pdf", format="pdf", facecolor="white")
fig.savefig(f"{OUT_NAME}.png", format="png", dpi=PNG_DPI, facecolor="white")
print("Saved:", ", ".join(f"{OUT_NAME}.{e}" for e in ("svg", "pdf", "png")))

try:                                   # Google Colab: download the three files
    from google.colab import files
    for ext in ("svg", "pdf", "png"):
        files.download(f"{OUT_NAME}.{ext}")
except ImportError:
    pass

plt.show()
