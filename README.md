# GAN文献计量学
## 氮化镓（GaN）功率器件研究前沿趋势追踪

基于文献计量学方法，系统分析氮化镓（Gallium Nitride, GaN）功率器件领域的研究热点、前沿趋势、核心作者与机构分布，揭示第三代半导体材料的发展脉络。

### 核心研究领域
- 氮化镓（GaN）材料与生长
- 宽禁带半导体器件
- 功率电子器件
- 第三代半导体技术

### 检索数据源
- Web of Science（WOS） 核心合集（Web of Science Core Collection）
- 检索时间范围：2010–2025
- 检索字段包括：标题（Title）、摘要（Abstract）、作者关键词（Author Keywords）
- 文献类型：Article + Review

### 检索策略
采用如下布尔检索表达式构建数据集：
(TS=("GaN" OR "gallium nitride"))
AND
(TS=("power device*" OR "power transistor*" OR "HEMT" OR "high electron mobility transistor*" 
OR "power conversion" OR "power electronics" OR "switching"))
NOT
(TS=("LED" OR "light emitting" OR "laser" OR "optical" OR "photonics"))
### 检索策略说明
材料限定：使用“GaN”与“gallium nitride”并列，避免命名差异导致遗漏。
器件+应用双约束：引入 HEMT、power electronics 等关键词，将结果限定在功率器件与电力电子应用场景。
排除项：剔除 LED、laser、photonics 等高频光电子文献，避免样本偏移。

### 📊 数据获取与处理流程
Step 1 — 数据检索
在WOS中导出格式为 .txt (Plain Text) 的全记录与引用的参考文献
初始检索记录数：N = 9849

Step 2 — 去重处理
基于 DOI 进行主去重
对缺失 DOI 的记录采用标题匹配去重
去重后数据规模：N = XXXX（待补充）

Step 3 — 数据标准化
合并 Author Keywords（DE）与 Keywords Plus（ID）
关键词规范化处理：
全部转为小写
单复数统一
同义词归一（如“gan”→“gallium nitride”，“gan hemt”→“hemt”）
去除无效词（如“study”“method”等）
  
## 项目成员与分工

| 姓名 | 学号 | 分工内容 |
| :--- | :--- | :--- |
| **高楠** | 202416010212 | **项目总负责**：搭建Git版本控制体系，整合项目目录结构，统筹整体进度与代码合并。 |
| **向诗敏** | 202407010501 | **数据检索与清洗**：负责构建氮化镓（GaN）检索式，执行文献检索，完成数据去重与标准化。 |
| **王思创** | 202416010213 | **计量分析**：基于CiteSpace或Python代码，开展文献计量分析（发文量趋势、作者/机构分布、关键词共现）。 |
| **张帆** | 202416010304 | **可视化与报告**：生成可视化图谱，撰写最终分析报告，整理并提交作业文档。 |

---

### 💡 分工说明
本项目采用模块化分工，确保效率与质量。通过Git进行协作，每人独立开发分支，最后合并至主分支，保证项目版本可控。


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
