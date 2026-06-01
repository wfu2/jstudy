# 批量生成 4 周内容的流程

## 前置条件

- 框架文件已到位：`framework/` 目录下各阶段文件齐全
- 推送模板可参考：`scripts/push_template.md`
- 当前周结构示例可参考：`content/week_01/`

## 生成命令

使用 agent 生成后续 4 周的内容。在 Hermes Agent 会话中执行以下指令：

```
请按框架文件生成 content/week_XX/ ~ content/week_YY/ 的日语学习内容。

参考框架：
- README.md（目录结构、注音规则、命名规范）
- framework/overview.md（阶段概览）
- framework/phaseX-weeks-XX-YY.md（具体周的 Day 1-7 主题安排）
- scripts/push_template.md（每日推送模板）
- content/week_01/day_001.md 等现有文件（格式参考）

每周7个文件（day_001 ~ day_007），按周目录组织。
每篇约1500-2000字，汉字全部标注读音（格式：漢字（かな））。
中文翻译/解释/词性标记不标注。
```

## 质量验证

生成后运行：

```bash
python3 scripts/check_quality.py
```

检查是否有日语文本的汉字未注音。

## 每日推送验证

```bash
cd ~/.hermes/scripts && python3 jpush.py status
cd ~/.hermes/scripts && python3 jpush.py next   # 预览下一条
```

## 注意事项

- 内容**不包含运行时状态**（jpush_state.json 已 gitignore）
- 每次批量生成4周（28天），周期内不修改已生成内容
- 周日（Day 7）为复习日：本周要点回顾 + 5题迷你测验
- 第4/8/20/34周周日为大复习/阶段测验
