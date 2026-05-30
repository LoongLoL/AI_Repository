---
name: answer-marker
description: "将选择题答案（Mark Scheme）标注到试卷 PDF 上。用户提供 ms 答案文档和 qp 问题文档，把 ms 中的选择答案以 26pt 红色字体写入 qp 对应题目的选项附近，仅写字母本身不加符号。无法处理的题目不写入但需在完成后列出题号。支持批量处理。当用户提到 PDF 答案标注、答题卡批改、mark scheme、答案标记时使用。"
allowed-tools:
  - read
  - write
  - exec
---

# 试卷答案标注助手

将 Mark Scheme 中的选择题答案，以 **26pt 红色字体**标注到试卷 PDF 对应题目的选项附近。

## 输入

- `ms_pdf`：答案卷（Mark Scheme）PDF 文件路径
- `qp_pdf`：题目卷（Question Paper）PDF 文件路径
- 可选：`output_pdf` 输出文件路径（默认在 qp 文件名后加 `_annotated`）

## 处理流程

### Step 1：提取答案

用 `exec` 运行 `mark_answers.py` 的 `parse_ms()` 函数，从 ms PDF 提取 `{题号: 答案字母}` 字典。

支持格式：
- 剑桥表格风格：`" 1  A  1 "`
- 列表格式：`"1. A"` / `"Q1: A"`
- 逐行：`"1 A"`
- 废除题：`"14 Question Discounted"` → 标记为 `"N/A"`

### Step 2：定位选项位置

在 qp PDF 中定位正确答案选项的坐标：

1. 扫描每行的字符，按 y 坐标分组为行
2. 识别**题号行**：行首为 `数字+空格`，x0 在 40-70 之间
3. 识别**选项行**：行首为 A/B/C/D + 空格/点，x0 在 60-100 之间
4. 将选项分配给最近的题（选项 top 在最近两个题号之间）
5. 定位正确答案字母的 (x0, top) 即为标注位置
6. 将选项行坐标向下偏移约 10pt 作为标注 y（使答案出现在选项文字下方附近）

**支持的选项格式**：
- 独立选项行：每行一个选项（A xxx / B xxx / C xxx / D xxx）
- 内联选项行：一行含多个选项（"A 17m/s B 31m/s C 54m/s D 150m/s"）

**无需标注的题**：
- 图表/图片型选择题（选项嵌入 PDF 图片，无法定位文字）
- 题目标记为 "N/A"（已废除）

### Step 3：写入标注

使用 `fitz.insert_text()` 将答案写入 qp PDF：

```python
page.insert_text(
    fitz.Point(x, y),
    ans_letter,          # 仅字母 A/B/C/D，不加任何符号
    fontname="helv",
    fontsize=26,         # 26pt
    color=(1, 0, 0),     # 红色
    render_mode=0,
)
```

- **x**：正确选项字母的 x0
- **y**：正确选项行的 top + 约 10pt（使字母出现在选项下方附近）
- **内容**：仅答案字母（A/B/C/D），不加括号、✓、下划线等任何符号
- **字体大小**：26pt
- **颜色**：红色 (1, 0, 0)

### Step 4：输出结果

1. 保存标注后的 PDF 文件
2. **末尾列出未处理的题号**（格式见下方）
3. 提供文件服务器预览链接

## 输出格式

**标注成功的题**：在 qp PDF 对应选项附近显示 26pt 红色字母。

**处理完成后输出摘要**：
```
标注成功: XX/YY
未处理的题号: [5, 11, 14, 25, 26, 27]
```

"未处理的题号"应当列出所有未能定位的题目编号（含图表型和废除题），无论原因。

## 存放位置

标注后的 PDF 保存到原文件同目录，文件名加 `_annotated` 后缀。

## 文件路径

- 主脚本：`workspace/skills/answer-marker/mark_answers.py`

## 注意事项

- 先预览试卷结构再标注
- 答案卷格式不一致时，优先用 pdfplumber 文字提取，降级用逐页 OCR
- 仅使用 `allowed-tools` 中声明的工具
- 未处理的题号必须在最后列出
