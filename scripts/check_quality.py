#!/usr/bin/env python3
"""
日语内容质量检查工具 — v2 精确版

仅检查日语文本部分的注音完整性：
- 词汇条目中的日语词（例：私（わたし）→ 检查"私"前面的部分）
- 「」内的日语例句
- ▸/▶ 后的日语结构
- 以〜开头的语法模式

跳过中文翻译/解释。
"""
import re
import os
import sys

CONTENT_DIR = os.path.expanduser("~/generated/japanese/content")
KANJI = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\u9faf]')
FURIGANA_PAIR = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\u9faf]+（[ぁ-んゔゝ・\u30a0-\u30ff]+）')
LINE_SEP = re.compile(r'^━+|^[━─═]+')
SKIP_HEADERS = re.compile(r'^📅|^📐|^🔤|^🎬|^💡|^📌|^📋|^📝|^🎯|^🔑|^─')
NO_KANJI = re.compile(r'^[^一-龯ぁ-んァ-ン]*$')

def extract_japanese_portions(line):
    """从一行中提取需要检查注音的日语文本片段"""
    stripped = line.strip()
    if not stripped or LINE_SEP.match(stripped) or SKIP_HEADERS.match(stripped):
        return []
    
    portions = []
    
    # 1. 提取「」内的日语例句
    for m in re.finditer(r'「([^」]*)」', stripped):
        portions.append(('quote', m.group(1)))
    
    # 2. 提取 ▸/▶ 开头的日语结构（如 ▸ い形容詞肯定/否定）
    for m in re.finditer(r'[▶▸]\s*(.+?)(?:\s*[:：]|$)', stripped):
        text = m.group(1)
        if KANJI.search(text):
            portions.append(('bullet', text))
    
    # 3. 提取词汇条目中的日语词（: 或 ： 之前的部分）
    # 格式：私（わたし）[代]：我  或  食べる [他動]：吃
    for m in re.finditer(r'^([^：:]+?)(?:[：:]\s*)', stripped):
        text = m.group(1)
        if KANJI.search(text):
            portions.append(('vocab', text))
    
    # 4. 包含〜开头的语法模式行
    if '〜' in stripped:
        portions.append(('grammar', stripped))
    
    return portions


def check_portions(portions):
    """检查片段中的汉字是否有注音，返回未注音汉字列表"""
    results = []
    for ptype, text in portions:
        # 移除已注音部分
        cleaned = FURIGANA_PAIR.sub('', text)
        # 移除英文、数字、标点
        cleaned = re.sub(r'[0-9０-９①②③④⑤⑥⑦⑧⑨⑩a-zA-Z\[\]\{\}\(\)「」]', '', cleaned)
        cleaned = re.sub(r'[、。，．：；？！～〜・･━─═\-—\|▶▸※＠\s]', '', cleaned)
        # 移除纯假名
        cleaned = re.sub(r'[ぁ-ん]+', '', cleaned)
        cleaned = re.sub(r'[ァ-ンー]+', '', cleaned)
        # 检查剩余汉字
        unannotated = KANJI.findall(cleaned)
        if unannotated:
            results.append((ptype, unannotated))
    return results


def scan_file(fpath):
    """检查单个文件"""
    with open(fpath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    issues = []
    for i, line in enumerate(lines, 1):
        portions = extract_japanese_portions(line)
        if not portions:
            continue
        results = check_portions(portions)
        if results:
            for ptype, chars in results:
                issues.append((i, ptype, len(chars), chars[:8]))
    
    # 字数统计
    content_text = ''.join(lines)
    # 去掉分隔线行
    meaningful = [l for l in lines if l.strip() and not LINE_SEP.match(l.strip()) and not l.strip().startswith('---')]
    total_chars = sum(len(l.strip()) for l in meaningful)
    
    return issues, total_chars


def scan_all():
    """扫描全部文件"""
    all_results = []
    total_issues = 0
    
    for root, dirs, files in os.walk(CONTENT_DIR):
        for fname in sorted(files):
            if not fname.startswith('day_') or not fname.endswith('.md'):
                continue
            fpath = os.path.join(root, fname)
            issues, length = scan_file(fpath)
            
            if issues:
                print(f"❌ {fname}（{length}字, {len(issues)}处）")
                for lineno, ptype, count, chars in issues[:6]:
                    print(f"        L{lineno}[{ptype}]: {''.join(chars)}")
                    total_issues += count
                if len(issues) > 6:
                    print(f"        ... 还有{len(issues)-6}处")
            else:
                print(f"✅ {fname}（{length}字）")
    
    return total_issues


if __name__ == '__main__':
    total = scan_all()
    print(f"\n总计未注音汉字: {total}")
    print("注：仅检查日语文本部分（「」内、词汇条目日语词、▸语法结构、〜句式）")
