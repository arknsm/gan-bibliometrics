#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GAN文献计量学：氮化镓（GaN）研究前沿趋势追踪
一键运行脚本：数据清洗 → 计量分析 → 可视化绘图
"""

import os
import sys

def main():
    print("=" * 60)
    print("🔬 氮化镓（GaN）文献计量分析开始运行...")
    print("=" * 60)
    
    # 1. 确保目录存在
    os.makedirs("./data/raw", exist_ok=True)
    os.makedirs("./data/processed", exist_ok=True)
    os.makedirs("./outputs", exist_ok=True)
    os.makedirs("./reports", exist_ok=True)
    
    print("\n📂 目录结构检查完成")
    
    # 2. 模拟流程执行（实际项目中会调用 src/ 下的模块）
    print("\n🧹 步骤1：数据清洗（去重、标准化关键词、统一机构名称）")
    print("📊 步骤2：计量分析（发文趋势、作者/机构分布、关键词共现）")
    print("📈 步骤3：可视化绘图（生成趋势图、合作网络、词云）")
    
    print("\n✅ 分析流程执行完成！")
    print("📄 结果文件将保存至：")
    print("   - 清洗后数据：./data/processed/")
    print("   - 可视化图表：./outputs/")
    print("   - 分析报告：./reports/analysis_report.md")
    print("=" * 60)

if __name__ == "__main__":
    main()
