# 文件结构

```
japanese/
├── README.md                    ← 本文件
├── .gitignore                   ← jpush_state.json 不入库
├── framework/                   ← 48周课程框架（按阶段拆分）
│   ├── overview.md              ← 48周速览表 + 内容结构说明
│   ├── phase1-weeks-01-08.md    ← 基石期 N5
│   ├── phase2-weeks-09-20.md    ← 构建期 N4
│   ├── phase3-weeks-21-34.md    ← 突破期 N3
│   └── phase4-weeks-35-48.md    ← 实战期 N2
├── scripts/                     ← 工具脚本和模板
│   ├── check_quality.py         ← 注音/字数质量检查
│   ├── push_template.md         ← 每日推送内容模板
│   └── generate_batch.md        ← 批量生成4周内容的流程文档
└── content/                     ← 按周组织的推送内容
    ├── week_01/day_001.md       ← 第1周Day1
    ├── week_01/...
    ├── week_02/...
    ├── ...
    └── index.md                 ← 内容索引（各周概要）
```

# 命名规则

| 要素 | 规则 | 示例 |
|------|------|------|
| 按周目录 | `week_XX` | `week_05` |
| 每日文件 | `day_XXX.md`（3位数字） | `day_035.md` |
| 阶段文件 | `phaseN-weeks-XX-YY.md` | `phase2-weeks-09-20.md` |

# 注音规则

- **日语文本**（词汇条目中的日语词、「」内的例句、〜语法模式、▸后的结构）：**所有汉字必须标注读音**
- **中文翻译/解释**（词汇后面的中文释义、语法说明）：**不标注**
- **词性标记**（[名], [代], [他動]等）：**不标注**
- **标题/导航行**（📅开头等）：**不标注**
- 注音格式：`漢字（かな）`，如 `日本語（にほんご）`
- 复合词单独注音：`日本語（にほんご）の勉強（べんきょう）`

# 推送流程

1. 内容已按周预生成在 `content/week_XX/day_XXX.md`
2. cronjob `jpush`（ID: 346dc7387e85, 每日21:00）调用 `jpush.py next`
3. jpush.py 按数字顺序查找下一条未推送内容
4. 输出内容 → 微信推送
5. 状态记录在 `~/.hermes/scripts/jpush_state.json`

# 质量检查

```bash
python3 scripts/check_quality.py        # 检查所有文件的注音完整性
python3 scripts/check_quality.py --file path/to/file  # 检查单个文件
```

# Git 仓库

- 远程: `git@github.com:wfu2/jstudy.git`
- 分支: `main`
- 注意：`jpush_state.json` 由 `.gitignore` 排除，不入库
