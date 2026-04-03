import re
import csv
import glob
import os
from collections import OrderedDict

# ========== 配置 ==========
INPUT_PATTERN = "savedrecs-*.txt"      # 匹配所有 savedrecs- 开头的 txt 文件
OUTPUT_FILE = "gan_power_devices_cleaned_all.csv"

# 无效词列表（需要移除的关键词）
STOPWORDS = {
    'study', 'method', 'analysis', 'approach', 'application',
    'technology', 'review', 'investigation', 'fabrication',
    'characterization', 'simulation', 'modeling', 'design',
    'optimization', 'evaluation', 'comparison', 'issue',
    'challenge', 'perspective', 'overview', 'progress',
    'development', 'state-of-the-art', 'recent', 'new',
    'based', 'effect', 'performance', 'high', 'low', 'using',
    'via', 'with', 'without', 'for', 'of', 'in', 'on', 'to'
}

# 同义词映射
SYNONYM_MAP = {
    'gan': 'gallium nitride',
    'gallium nitride (gan)': 'gallium nitride',
    'gan hemt': 'hemt',
    'gan hemts': 'hemt',
    'gan-hemt': 'hemt',
    'gan-hemts': 'hemt',
    'algan/gan hemt': 'hemt',
    'algan/gan hemts': 'hemt',
    'algan/gan': 'algan/gan',
    'algan-gan': 'algan/gan',
    'hemts': 'hemt',
    'gan-on-si': 'gallium nitride on silicon',
    'gan on si': 'gallium nitride on silicon',
    'gan-on-silicon': 'gallium nitride on silicon',
    'gan on silicon': 'gallium nitride on silicon',
    'normally-off': 'normally off',
    'normally off': 'normally off',
    'enhancement-mode': 'enhancement mode',
    'enhancement mode': 'enhancement mode',
    'depletion-mode': 'depletion mode',
    'depletion mode': 'depletion mode',
    'e-mode': 'enhancement mode',
    'd-mode': 'depletion mode',
    'power device': 'power device',
    'power devices': 'power device',
    'power electronics': 'power electronics',
    'breakdown voltage': 'breakdown voltage',
    'breakdown': 'breakdown voltage',
    'threshold voltage': 'threshold voltage',
    'vth': 'threshold voltage',
    'current collapse': 'current collapse',
    'dynamic ron': 'dynamic on-resistance',
    'dynamic on-resistance': 'dynamic on-resistance',
    'ron': 'on-resistance',
    'on-resistance': 'on-resistance',
    'on resistance': 'on-resistance',
    '2deg': 'two-dimensional electron gas',
    '2d electron gas': 'two-dimensional electron gas',
    'field plate': 'field plate',
    'field-plate': 'field plate',
    'mocvd': 'metal-organic chemical vapor deposition',
    'movpe': 'metal-organic vapor phase epitaxy',
    'mbe': 'molecular beam epitaxy',
    'tcad': 'technology computer-aided design',
    'hemt': 'hemt',
    'sbd': 'schottky barrier diode',
    'schottky': 'schottky barrier diode',
    'mosfet': 'mosfet',
    'jfet': 'jfet',
    'mis-hemt': 'mis-hemt',
    'mos-hemt': 'mos-hemt',
    'p-gan': 'p-gan',
    'pgan': 'p-gan',
    'p-gan gate': 'p-gan gate',
    'cascode': 'cascode',
    'superjunction': 'super junction',
    'super-junction': 'super junction',
    'resurf': 'resurf',
    'jte': 'junction termination extension',
    'edge termination': 'edge termination',
}


# ========== 1. 解析 WOS 文件 ==========
def parse_wos_file(filename):
    """解析 Web of Science 导出的纯文本文件"""
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    records = []
    current_record = {}
    current_field = None
    current_value = []
    
    for line in lines:
        line = line.rstrip('\n\r')
        
        # 新记录开始
        if line.startswith('PT J'):
            if current_record:
                records.append(current_record)
            current_record = {}
            current_field = None
            current_value = []
            continue
        
        # 记录结束
        if line.startswith('ER'):
            if current_record:
                records.append(current_record)
            current_record = {}
            current_field = None
            current_value = []
            continue
        
        # 新字段开始（行首是两位大写字母 + 空格）
        if len(line) >= 2 and line[0:2].isupper() and line[2:3] == ' ':
            # 保存上一个字段
            if current_field and current_value:
                current_record[current_field] = ' '.join(current_value).strip()
            
            # 开始新字段
            current_field = line[0:2]
            current_value = [line[3:].strip()]
        else:
            # 续行（上一字段的继续）
            if current_field and line.strip():
                current_value.append(line.strip())
    
    # 添加最后一条记录
    if current_record:
        records.append(current_record)
    
    return records


# ========== 2. 去重处理 ==========
def deduplicate_records(records):
    """基于 DOI 和 Title 去重"""
    seen_doi = set()
    seen_title = set()
    unique = []
    
    for rec in records:
        doi = rec.get('DI', '').strip()
        title = rec.get('TI', '').strip()
        
        # 优先使用 DOI 去重
        if doi:
            if doi in seen_doi:
                continue
            seen_doi.add(doi)
        else:
            # 无 DOI 时使用标题去重
            if not title:
                continue
            title_key = title.lower()
            if title_key in seen_title:
                continue
            seen_title.add(title_key)
        
        unique.append(rec)
    
    return unique


# ========== 3. 关键词标准化 ==========
def normalize_keywords(de_str, id_str):
    """合并 DE 和 ID，进行标准化处理"""
    # 合并
    combined = ""
    if de_str and de_str.strip():
        combined = de_str.lower()
    if id_str and id_str.strip():
        if combined:
            combined += "; " + id_str.lower()
        else:
            combined = id_str.lower()
    
    if not combined:
        return ""
    
    # 按分隔符拆分
    keywords = re.split(r'[;,]\s*', combined)
    
    normalized = []
    for kw in keywords:
        kw = kw.strip()
        if not kw or len(kw) < 2:
            continue
        
        # 去除尾部的 's'（单复数统一）
        if kw.endswith('s') and kw[:-1] in SYNONYM_MAP:
            kw = kw[:-1]
        elif kw.endswith('s') and not kw.endswith('ss'):
            kw = kw[:-1]
        
        # 同义词映射
        if kw in SYNONYM_MAP:
            kw = SYNONYM_MAP[kw]
        
        # 去除无效词
        if kw in STOPWORDS:
            continue
        # 去除纯数字或太短的词
        if kw.isdigit() or len(kw) < 3:
            continue
        
        normalized.append(kw)
    
    # 去重并排序
    normalized = sorted(set(normalized))
    return '; '.join(normalized)


# ========== 4. 辅助函数：安全获取字段值 ==========
def get_field(record, field_name, default=''):
    value = record.get(field_name, '')
    if value is None:
        return default
    return value.strip() if isinstance(value, str) else default


# ========== 5. 获取所有输入文件 ==========
def get_input_files(pattern):
    """获取所有匹配的文件，并按数字顺序排序"""
    files = glob.glob(pattern)
    
    # 提取文件名中的数字范围进行排序
    def extract_number(filename):
        match = re.search(r'(\d+)', filename)
        if match:
            return int(match.group(1))
        return 0
    
    files.sort(key=extract_number)
    return files


# ========== 6. 主函数 ==========
def main():
    print("=" * 60)
    print("Web of Science 文献数据清洗工具（多文件合并版）")
    print("=" * 60)
    
    # 获取所有输入文件
    input_files = get_input_files(INPUT_PATTERN)
    
    if not input_files:
        print(f"\n❌ 错误：没有找到匹配 '{INPUT_PATTERN}' 的文件")
        print("请确保所有 savedrecs-*.txt 文件在当前目录下")
        return
    
    print(f"\n找到 {len(input_files)} 个数据文件：")
    for f in input_files:
        print(f"   - {f}")
    
    # 步骤1：解析所有文件
    print("\n[1/4] 正在解析所有文件...")
    all_records = []
    file_counts = []
    
    for i, filename in enumerate(input_files, 1):
        try:
            records = parse_wos_file(filename)
            all_records.extend(records)
            file_counts.append((filename, len(records)))
            print(f"      [{i}/{len(input_files)}] {filename}: {len(records)} 条记录")
        except Exception as e:
            print(f"      ⚠️ 解析 {filename} 时出错: {e}")
    
    print(f"\n      📊 总计原始记录数: {len(all_records)}")
    
    # 步骤2：去重
    print("\n[2/4] 正在执行去重处理...")
    unique_records = deduplicate_records(all_records)
    print(f"      📊 去重后记录数: {len(unique_records)}")
    print(f"      📊 去除重复记录: {len(all_records) - len(unique_records)} 条")
    
    # 步骤3：关键词标准化
    print("\n[3/4] 正在标准化关键词（可能需要一点时间）...")
    for i, rec in enumerate(unique_records):
        de = get_field(rec, 'DE')
        id_ = get_field(rec, 'ID')
        rec['Normalized_Keywords'] = normalize_keywords(de, id_)
        
        # 进度提示
        if (i + 1) % 500 == 0:
            print(f"      已处理 {i+1}/{len(unique_records)} 条记录...")
    
    print(f"      完成！共处理 {len(unique_records)} 条记录")
    
    # 步骤4：输出 CSV
    print(f"\n[4/4] 正在写入 CSV: {OUTPUT_FILE}")
    
    fieldnames = [
        'DOI', 'Title', 'Authors', 'Journal', 'Year',
        'Volume', 'Issue', 'Pages', 'Times_Cited',
        'Author_Keywords_DE', 'Keywords_Plus_ID',
        'Normalized_Keywords', 'Author_Affiliation_C1'
    ]
    
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        
        for rec in unique_records:
            # 处理页码
            bp = get_field(rec, 'BP')
            ep = get_field(rec, 'EP')
            pages = f"{bp}-{ep}" if bp and ep else (bp or ep or '')
            
            writer.writerow({
                'DOI': get_field(rec, 'DI'),
                'Title': get_field(rec, 'TI'),
                'Authors': get_field(rec, 'AU'),
                'Journal': get_field(rec, 'SO'),
                'Year': get_field(rec, 'PY'),
                'Volume': get_field(rec, 'VL'),
                'Issue': get_field(rec, 'IS'),
                'Pages': pages,
                'Times_Cited': get_field(rec, 'TC'),
                'Author_Keywords_DE': get_field(rec, 'DE'),
                'Keywords_Plus_ID': get_field(rec, 'ID'),
                'Normalized_Keywords': rec.get('Normalized_Keywords', ''),
                'Author_Affiliation_C1': get_field(rec, 'C1'),
            })
    
    # 输出统计信息
    print(f"\n✅ 清洗完成！")
    print(f"   输出文件: {OUTPUT_FILE}")
    print(f"\n📊 统计摘要:")
    print(f"   - 处理文件数: {len(input_files)}")
    print(f"   - 原始记录总数: {len(all_records)}")
    print(f"   - 去重后记录数: {len(unique_records)}")
    print(f"   - 重复记录数: {len(all_records) - len(unique_records)}")
    
    # 按年份统计
    year_counts = {}
    for rec in unique_records:
        year = get_field(rec, 'PY')
        if year and year.isdigit():
            year_counts[year] = year_counts.get(year, 0) + 1
    
    if year_counts:
        print(f"\n📊 按年份分布（前10年）:")
        sorted_years = sorted(year_counts.items(), reverse=True)[:10]
        for year, count in sorted_years:
            print(f"   {year}: {count} 篇")
    
    # 预览前几条
    print("\n[预览] 前3条记录的标题和标准化关键词：")
    for i, rec in enumerate(unique_records[:3]):
        title = get_field(rec, 'TI')
        keywords = rec.get('Normalized_Keywords', '')
        print(f"\n{i+1}. {title[:80]}..." if len(title) > 80 else f"\n{i+1}. {title}")
        kw_preview = keywords[:100] + "..." if len(keywords) > 100 else keywords
        print(f"   关键词: {kw_preview}" if keywords else "   关键词: (无)")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()