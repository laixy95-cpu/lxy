from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
code = (root / "code" / "asean6_reproducible.py").read_text(encoding="utf-8")

cells = [
    {"cell_type": "markdown", "metadata": {}, "source": [
        "# ASEAN-6 sequential-crisis diagnostic\n",
        "This notebook reproduces the revised, non-causal diagnostic. Upload the six Excel inputs when prompted. "
        "All outputs are written to `revised_asean6_diagnostic/` and downloaded as a zip.\n"]},
    {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
        "!pip -q install pandas numpy scipy matplotlib seaborn openpyxl\n",
        "from google.colab import files\n",
        "from pathlib import Path\n",
        "import shutil\n",
        "INPUT = Path('/content/asean6_inputs')\n",
        "INPUT.mkdir(exist_ok=True)\n",
        "uploaded = files.upload()\n",
        "for name, payload in uploaded.items():\n",
        "    (INPUT / name).write_bytes(payload)\n",
        "required = {'1 ETRI_Core data.xlsx','2 crisis_exposure.xlsx','4 policy_response_price_cushioning.xlsx','6 policy_response_extended (1).xlsx'}\n",
        "missing = required - set(uploaded)\n",
        "assert not missing, f'Missing required files: {sorted(missing)}'\n"]},
    {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
        "script = r'''\n", code, "\n'''\n",
        "Path('/content/asean6_reproducible.py').write_text(script, encoding='utf-8')\n",
        "exec(compile(script, 'asean6_reproducible.py', 'exec').replace if False else compile(script, 'asean6_reproducible.py', 'exec'))\n"]},
    {"cell_type": "code", "execution_count": None, "metadata": {}, "outputs": [], "source": [
        "OUT = Path('/content/revised_asean6_diagnostic')\n",
        "run(INPUT, OUT)\n",
        "archive = shutil.make_archive('/content/revised_asean6_diagnostic_outputs', 'zip', OUT)\n",
        "files.download(archive)\n"]},
]

# Replace the awkward exec expression with a plain one after JSON assembly.
cells[2]["source"][-1] = "ns = {'__name__': 'asean6_module'}; exec(compile(script, 'asean6_reproducible.py', 'exec'), ns); run = ns['run']\n"
nb = {"cells": cells, "metadata": {"colab": {"name": "ASEAN6_Revised_Reproducible_Analysis.ipynb"},
      "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"}},
      "nbformat": 4, "nbformat_minor": 5}
(root / "code" / "ASEAN6_Revised_Reproducible_Analysis.ipynb").write_text(
    json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
