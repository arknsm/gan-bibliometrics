# 输出结果目录说明
本目录存放代码运行后生成的所有输出文件（图表、分析结果、报告）。

## 输出文件清单
- `gan\\\\\\\_analysis\\\\\\\_result.csv`: 文献计量分析核心结果（作者/机构统计、关键词频次等）
- `visualizations/`: 可视化图表（自动生成）
  - `gan\\\\\\\_publication\\\\\\\_trend.png`: 年度发文趋势图
  - `gan\\\\\\\_keywords\\\\\\\_wordcloud.png`: 关键词词云图
- `gan\\\\\\\_final\\\\\\\_report.pdf`: 最终分析报告（PDF 版）

## 生成说明
- 所有文件由 `src/main.py` 运行后自动生成
- 每次重新运行代码会覆盖旧文件，如需保留历史版本，可按日期重命名（如 `gan\\\\\\\_analysis\\\\\\\_result\\\\\\\_20260319.csv`）
