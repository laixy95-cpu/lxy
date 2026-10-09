# 08-Cleantech-Shock

清洁技术供给冲击与电力部门脱碳（197 经济体，2012–2024）。完整指令见 `docs/CLAUDE_CODE_BRIEF.md`。

**当前状态：停在第 1 步，原因与所需输入见 `output/diagnostics_report.md`。**

| 步骤 | 状态 |
|---|---|
| 0 面板审计 | 完成（`src/00_audit_panel.py`） |
| 1 BACI 提取 | 阻塞：缺 `extract_baci_cleantech.py` 或其输出 |
| 2 合并 BACI + 面板 + WDI | 阻塞：缺 BACI 输出与 WDI 文件 |
| 3–4 工具变量 + D3 与第一阶段（硬停止点） | 未开始 |
| 5–9 | 未开始 |

```
data/raw/    原始输入（只读）      data/built/  构造后的数据
src/         编号脚本，可逐步重跑   output/      tables、figures、diagnostics_report.md
logs/        每步日志
```
