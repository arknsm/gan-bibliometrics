# GAN文献计量学
## 氮化镓（GaN）研究前沿趋势追踪

基于文献计量学方法，系统分析氮化镓（Gallium Nitride, GaN）领域的研究热点、前沿趋势、核心作者与机构分布，揭示第三代半导体材料的发展脉络。

### 核心研究领域
- 氮化镓（GaN）材料与生长
- 宽禁带半导体器件
- 功率电子器件
- 光电子器件（LED、激光器等）
- 第三代半导体技术

### 检索数据源
- Scopus / Web of Science 数据库
- 检索时间范围：2015–2025

### 项目目录结构
gan-bibliometrics/
├── data/
│ ├── raw/ # 原始文献数据
│ └── processed/ # 清洗后的数据
├── src/ # 代码文件夹
│ ├── data_clean.py # 数据清洗
│ ├── analysis.py # 计量分析
│ └── visualization.py # 可视化绘图
├── outputs/ # 输出结果（图表、表格）
├── reports/ # 报告文档（检索式、同义词表）
├── paper/ # 论文 / 分析报告
├── run_pipeline.py # 一键运行脚本
├── requirements.txt # 依赖清单
└── README.md # 项目说明
## 环境依赖
核心依赖：
- `pandas>=2.0.0`：数据处理
- `numpy>=1.24.0`：数值计算
- `matplotlib>=3.7.0`：可视化
- `pybliometrics>=3.0.0`：Scopus 数据获取

## 运行方式
```bash
python run_pipeline.py
