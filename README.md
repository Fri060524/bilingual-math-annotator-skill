# Bilingual Academic Mathematics Book Annotator
### 高等数学教材中英双语学术注释版制作框架与 AI Agent Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Engine: XeLaTeX](https://img.shields.io/badge/LaTeX-XeLaTeX-green.svg)](https://www.tug.org/xetex/)
[![Python: 3.9+](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Agent: Antigravity / Claude Code](https://img.shields.io/badge/Agent%20Skill-Antigravity%20%7C%20Claude-purple.svg)](SKILL.md)

**Bilingual Academic Mathematics Book Annotator** 是一个用于制作出版级**中英双语学术注释版高等数学与理工科经典教材**的端到端工程框架与 AI Agent 技能包（Skill）。

本项目起源于普林斯顿大学分析学讲义全四卷（*Stein & Shakarchi: Princeton Lectures in Analysis*）中英双语学术注释版的完整数字化与翻译工程实践，沉淀出了一套兼顾**严谨数学保真度**、**古典学者排版美学**与**自动化质量保障**的现代化技术流水线。

---

## 🌟 核心特性 (Key Features)

### 1. 上下交替双语排版 (Alternating Bilingual Layout)
- 英文原文在上（`\en{...}`），中文学术翻译在下（`\zh{...}`），按数学论证逻辑单元交替排列。
- **版芯完全对齐**：中文版芯宽度与英文严格一致（A4 textwidth 122mm），消除现代双栏排版的拥挤感与断行破碎。
- **自然呼吸韵律**：双语单元间保留 1.15em 舒适垂直留白，定理与证明内采用 `enblock` / `zhblock` 保持逻辑结构清晰。

### 2. 双向互通学术边注系统 (Bidirectional Interactive Margin Notes)
- **正文轻柔高亮**：核心术语以浅蓝底色（`#E8EFF7`）标注，优雅内敛。
- **外侧页边留白**：48mm 宽外边注呈现粗体英文术语、楷体规范释义与学术用法语境。
- **双向超链接跳转**：
  - 点击正文/边注中的术语 $\to$ 瞬间跳转至书末的《学术术语总表》。
  - 点击术语总表中的词条 $\to$ 无缝返回该词在正文中的首次出现位置。

### 3. 原书印刷页码全锚定 (Original Book Page Anchors)
- 在外边注精确标注 `\origpage{N}`（呈现为 `[Orig. p. N]`），建立 1:1 双向映射索引，便于读者与原版教材、教授授课页码无缝互查。

### 4. 无损矢量图截取 (Lossless Vector PDF Figure Extraction)
- 基于 PyMuPDF (`fitz`) 直接从原版 PDF 文本与矢量流中按精确坐标裁剪高精度图形，绝不使用模糊位图截屏，100% 保持矢量线条锐度。

### 5. 10 维全要素自动化质检流水线 (10-Point Automated QA Pipeline)
- 内置 `verify_qa.py`，自动检查：
  - 中英文落段 1:1 严格对齐（零漏句、零漏段）。
  - 行内与行间数学公式定界符配对（`$`、`\[...\]`）。
  - 定理、引理、证明环境完整闭合。
  - 标签唯一性检查（避免重复定义）。
  - 编译日志深度扫描（零缺失字符 `Missing glyph`，零未定义引用 `Undefined reference`）。

### 6. 古典普林斯顿教材排版风格 (Classical Typography)
- 正文字体：`TeX Gyre Pagella`（克隆自古典 Palatino）。
- 数学字体：`texgyrepagella-math.otf`，通过 `unicode-math` 实现公式与正文英文字形完美融合。
- 中文字体：典雅宋体（`Songti SC`）为主体，学术边注采用典雅楷体（`Kaiti SC`）。

---

## 📐 页面几何布局 (Page Layout Geometry)

```text
|<------------- A4 Paper (210mm x 297mm) ------------->|
+---------------+------------------------+---+---------+
| 装订留白       | 正文版芯 (Textwidth)    |   | 学术边注 |
| (Inner: 22mm) | (122mm)                |   | (48mm)  |
|               |                        |   |         |
|               | \en{English text...}   |   | [Orig.  |
|               |                        |   |   p. 1] |
|               | \zh{中文学术翻译...}    |   |         |
|               |                        |   | exterior|
|               | [Vertical gap: 1.15em] |   | measure |
|               |                        |   | 外测度  |
|               | \begin{theorem}        |   |         |
|               |   \begin{enblock}...   |   |         |
|               |   \begin{zhblock}...   |   |         |
|               | \end{theorem}          |   |         |
+---------------+------------------------+---+---------+
                                         |<- 6mm sep ->|
```

---

## 📁 目录结构 (Directory Layout)

```text
bilingual-math-annotator-skill/
├── SKILL.md                      # AI Agent 技能规格说明书 (YAML frontmatter + 完整指令)
├── README.md                     # 项目介绍与使用指南
├── LICENSE                       # MIT 开源许可证
├── .gitignore                    # LaTeX、Python、操作系统忽略规则
├── scripts/                      # 自动化工具链
│   ├── verify_qa.py              # LaTeX 源码与编译日志自动化质检脚本
│   ├── extract_vector_figures.py # PyMuPDF 原版 PDF 无损矢量图裁剪工具
│   ├── manage_glossary.py        # 学术术语库管理与双向超链接 LaTeX 表格生成器
│   └── requirements.txt          # Python 依赖清单 (pymupdf>=1.23.0)
├── templates/                    # 通用 LaTeX 模板与样式表
│   ├── academic_bilingual.sty    # 核心样式包 (几何参数、字体、双向跳转宏、双语环境)
│   ├── math_macros.tex           # 现代数学常用符号与简写宏
│   └── main_template.tex         # 新书起步排版总模板
├── references/                   # 深度规范与学术标准手册
│   ├── translation_guide.md      # 数学学术翻译规范、语力动词与术语审查指南
│   ├── typography_spec.md        # 页面几何、字体搭配与边注排版技术参数
│   └── qa_protocol.md            # 10 维质量门禁与常见错误修复方案
└── examples/                     # 最小可编译范例 (MWE)
    ├── README.md                 # 范例编译指南
    └── minimal_book/
        ├── main.tex              # 可直接编译的书籍主文档
        ├── sample_chapter.tex    # 包含定理、证明、公式、边注的示例章节
        ├── sample_glossary.json  # 示例术语数据库
        └── glossary_table.tex    # 自动生成的双向跳转术语表
```

---

## 🚀 快速上手 (Quick Start)

### 方式一：作为 AI Agent 技能使用 (Antigravity / Claude Code)

将本文件夹放置于您工作区的自定义技能目录下：

```bash
# 复制到 Antigravity 工作区技能库
cp -r bilingual-math-annotator-skill /path/to/your/project/.agents/skills/bilingual-math-annotator

# 或者全局安装到用户配置
cp -r bilingual-math-annotator-skill ~/.gemini/config/skills/bilingual-math-annotator
```

在对话中对 Agent 下达指令即可自动调用：
> *"请使用 bilingual-math-annotator 技能，将这篇数学论文/章节翻译排版为高质量双语学术注释版 LaTeX。"*

---

### 方式二：手动编译示例工程 (Minimal Working Example)

#### 1. 安装 Python 依赖
```bash
pip install -r scripts/requirements.txt
```

#### 2. 编译示例书籍
确保系统已安装 TeX Live 或 MacTeX（包含 `xelatex` 以及 TeX Gyre Pagella 字体）：
```bash
cd examples/minimal_book

# 双遍编译以收敛超链接与页码锚点
xelatex main.tex
xelatex main.tex
```

#### 3. 运行自动化质量核验
```bash
python3 ../../scripts/verify_qa.py sample_chapter.tex --log main.log
```
输出：
```text
==================================================
  Bilingual Academic LaTeX QA Verification Tool
==================================================

[*] Checking: sample_chapter.tex
    - Bilingual Units: EN=6, ZH=6
    - Original Page Markers: 2
    - Annotated Terms / Notes: 5
    [PASS] Source code integrity verified.

[*] Checking Compilation Log: main.log
    [PASS] Log is clean (0 missing glyphs, 0 undefined references).

==================================================
  RESULT: ALL QA CHECKS PASSED SUCCESSFULLY (PASS)
==================================================
```

---

## 🛠️ 自动化工具说明 (Toolchain Overview)

### 1. 矢量插图裁剪 (`extract_vector_figures.py`)
```bash
# 单图精准裁剪（点坐标可利用预览工具获取）
python3 scripts/extract_vector_figures.py \
  --input original_book.pdf \
  --page 25 \
  --rect 100,68,345,230 \
  --output figures/fig_1_1.pdf
```

### 2. 术语库与双向链接生成 (`manage_glossary.py`)
```bash
python3 scripts/manage_glossary.py \
  --input glossary/terms.json \
  --export-tex src/glossary_table.tex
```

### 3. 全要素质量检查 (`verify_qa.py`)
```bash
python3 scripts/verify_qa.py src/chapter1/*.tex --log build.log
```

---

## 📜 开源协议 (License)

本项目采用 [MIT License](LICENSE) 开源。欢迎广大数学工作者、科研学者与 LaTeX 爱好者自由使用、拓展并回馈社区！
