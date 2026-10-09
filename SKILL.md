---
name: bilingual-math-annotator
description: >-
  Professional workflow, LaTeX architecture, and automation toolchain for creating
  publication-grade bilingual (English-Chinese) academic annotated editions of
  mathematics and STEM textbooks with bidirectional hyperlinked navigation,
  lossless vector graphics, and automated QA verification.
---

# Bilingual Academic Mathematics Book Annotator & Typesetter

This skill provides an end-to-end framework and operational runbook for producing high-fidelity, bilingual (English-Chinese) academic annotated editions of advanced mathematics and STEM textbooks.

Derived and battle-tested from the complete four-volume *Stein & Shakarchi Princeton Lectures in Analysis* bilingual edition project, this skill enforces the highest standards of mathematical precision, classical academic typography, and automated quality assurance.

---

## 1. Core Guiding Principles

1. **Fidelity Over Speed (原文完整性高于翻译速度)**: Never summarize, abbreviate, or omit any paragraph, derivation, step, or author note from the original textbook.
2. **Mathematical Rigor Over Literary Rhetoric (数学正确性高于文字流畅性)**: Mathematical logic, hypotheses, quantifiers, and implications must be translated with 100% precision. Never mask subtle mathematical conditions with vague prose.
3. **Classical Scholarly Typography (古典学术风格高于装饰性设计)**: Replicate the understated, dignified aesthetic of classic Princeton and Springer graduate texts (Palatino/Pagella serif, elegant Songti/Kaiti Chinese types, black-and-white tone with subtle soft-blue highlights). No garish modern slide cards or rainbow gradients.
4. **No Visual Hallucinations (严禁凭空拟构)**: Always cross-reference against the original PDF pages. If optical recognition or OCR is ambiguous, visually inspect the original bounding box.
5. **Full Reproducible Source (全源码可复现)**: All deliverables are preserved as modular, compilable LaTeX sources with automated scripts.

---

## 2. Directory Structure of a Bilingual Project

When working on a textbook with this skill, organize the project workspace as follows:

```text
my-bilingual-book/
├── templates/
│   ├── academic_bilingual.sty   # Core LaTeX styling & macros
│   └── math_macros.tex          # Mathematical notation macros
├── scripts/
│   ├── verify_qa.py             # 10-point automated QA validator
│   ├── extract_vector_figures.py# PyMuPDF lossless vector figure cropper
│   └── manage_glossary.py       # Master glossary compiler
├── data/
│   └── page_mapping.json        # Mapping between original book pages and new PDF
├── figures/                     # Vector PDF cropped figures (fig_1_1.pdf, etc.)
├── glossary/
│   └── terms_master.json        # Unified terminology database
├── src/
│   ├── frontmatter/             # Facsimiles, TOC, Foreword, Introduction
│   ├── chapter1/ ... chapterN/  # Individual chapter source files
│   └── backmatter/              # Notes, Bibliography, Glossary table
├── main.tex                     # Master document
└── uncertainties.md             # Review log for printing errata or subtle points
```

---

## 3. Step-by-Step Production Runbook

### Phase 1: Structural Analysis & Original Page Mapping
1. Extract original page breaks and establish a baseline mapping table (`page_mapping.json`).
2. Mark every original textbook page transition in the LaTeX source using `\origpage{N}`.
   - Example: `\origpage{42}` creates an outer margin anchor `[Orig. p. 42]`.

### Phase 2: Lossless Vector Graphic Extraction
1. Extract figures directly from the source textbook PDF using `scripts/extract_vector_figures.py`.
2. Do **not** take screenshots or convert to lossy PNG/JPEG formats.
3. Usage:
   ```bash
   python3 scripts/extract_vector_figures.py --input source.pdf --page 25 --rect 100,68,345,230 --output figures/fig_1_1.pdf
   ```

### Phase 3: Alternating Bilingual Typesetting
Translate and typeset in alternating narrative units:
- **English Original Above (`\en{...}`)**
- **Chinese Academic Translation Below (`\zh{...}`)**
- **Exact Column Widths**: Both blocks share the 122mm textwidth.
- **Rhythmic Vertical Separation**: 1.15em vertical spacing between units (`\vspace{1.15em}`).
- **Theorems & Proofs**: Use the dual-block environments `enblock` and `zhblock`:
  ```latex
  \begin{theorem}[Riesz Representation / 里斯表示定理]
  \label{thm:riesz}
  \begin{enblock}
  Every continuous linear functional $L$ on a Hilbert space $\mathcal{H}$ can be uniquely represented as...
  \end{enblock}
  \begin{zhblock}
  希尔伯特空间 $\mathcal{H}$ 上的每个连续线性泛函 $L$ 均可唯一表示为...
  \end{zhblock}
  \end{theorem}
  ```

### Phase 4: Academic Margin Annotations & Terminology
1. Annotate core technical terms and academic rhetorical collocations using `\term`:
   ```latex
   \term[dictionary_key]{term_to_display}{中文规范释义}{语境注记}
   ```
2. The term receives a subtle soft-blue highlight in the text and a structured note in the outer margin.
3. Register all terms in `glossary/terms_master.json`.
4. Compile the glossary table using:
   ```bash
   python3 scripts/manage_glossary.py --input glossary/terms_master.json --export-tex src/backmatter/glossary_table.tex
   ```
5. Navigation is **bidirectional**: Clicking a margin note jumps to the glossary entry; clicking the term in the glossary table jumps back to its first occurrence in the text.

### Phase 5: XeLaTeX Two-Pass Compilation
Compile using XeLaTeX to ensure font glyphs and hyperlinked anchors converge:
```bash
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

### Phase 6: Automated Quality Assurance (QA)
Execute `scripts/verify_qa.py` on the LaTeX files and compilation log:
```bash
python3 scripts/verify_qa.py src/chapter1/chapter1.tex --log main.log
```
The script automatically validates:
- Strict 1:1 parity between `\en` and `\zh` paragraph units.
- Balanced inline (`$`) and display (`\[\]`) math delimiters.
- Balanced LaTeX environments (`theorem`, `proof`, `align`, etc.).
- Absence of duplicate `\label{...}` entries.
- Presence of `\origpage{...}` markers.
- Compilation log free of missing glyphs or undefined references.

---

## 4. Academic Translation Standards

Consult [translation_guide.md](./references/translation_guide.md) for full details:
- **Strict Modality Preservation**:
  - `clearly`, `obviously` $\to$ 显然
  - `it follows that` $\to$ 由此可知 / 从而
  - `without loss of generality` $\to$ 不失一般性
  - `by virtue of` $\to$ 鉴于 / 依据
  - `appeal to` $\to$ 援引 / 借助于
  - `pass to the limit` $\to$ 取极限
- **Analysis Precision**:
  - `almost everywhere (a.e.)` $\to$ 几乎处处
  - `almost disjoint` $\to$ 几乎不相交 (交集测度为零)
  - `disjoint` $\to$ 不相交 (交集为空)
  - `pointwise limit` $\to$ 逐点极限
  - `uniform convergence` $\to$ 一致收敛

---

## 5. Reference Documentation

- [Typography & Page Layout Specification](./references/typography_spec.md)
- [Academic Translation Guide](./references/translation_guide.md)
- [10-Point QA Verification Protocol](./references/qa_protocol.md)
- [Minimal Compilable Example](./examples/README.md)
