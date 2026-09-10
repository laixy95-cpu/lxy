import docx
from docx.document import Document as _Doc
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph

def iter_block_items(parent):
    if isinstance(parent, _Doc):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError
    for child in parent_elm.iterchildren():
        if isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)

d = docx.Document("/root/.claude/uploads/d3cbd561-45cc-5751-8bbd-75e9842593d3/74e041a1-Manuscript_EDS_Full.docx")
out = []
ti = 0
for b in iter_block_items(d):
    if isinstance(b, Paragraph):
        t = b.text.strip()
        st = b.style.name if b.style else ""
        if not t:
            continue
        if st.startswith("Heading") or st in ("Title","Subtitle"):
            out.append(f"\n[{st.upper()}] {t}")
        else:
            out.append(t)
    else:
        ti += 1
        out.append(f"\n[TABLE {ti}]")
        for r in b.rows:
            cells = [c.text.strip().replace("\n"," ") for c in r.cells]
            out.append(" | ".join(cells))
        out.append(f"[/TABLE {ti}]\n")
txt = "\n".join(out)
open("manuscript_full.txt","w").write(txt)
print("chars:", len(txt), "words:", len(txt.split()), "tables:", ti)
