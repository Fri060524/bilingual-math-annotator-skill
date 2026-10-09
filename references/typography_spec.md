# Typography and Page Layout Specification

This document details the LaTeX typesetting architecture, font configuration, and page geometry standards for the bilingual academic textbook template.

---

## 1. Design Philosophy

- **Classical Academic Dignity**: Inspired by the Princeton Lectures in Analysis and classical Springer Graduate Texts in Mathematics.
- **Pure Black-and-White & Subtle Grayscales**: No garish web-style card blocks, rainbow gradients, or cartoonish icons.
- **Alternating Bilingual Rhythm**: English source text directly followed by Chinese academic translation, with rhythmic vertical separation (1.15em) before the next logical block.
- **Matched Column Widths**: English and Chinese share the identical textwidth (122mm on A4) without awkward indentations or pinched sub-columns.

---

## 2. Geometry & Asymmetric Margins

The layout uses a two-sided book format (`twoside`) with an enlarged outer margin specifically designed for academic annotations and original page references:

```text
+-------------------+----------------------------+--------+
|   Inner Margin    |        Main Text           | Margin |
|      (22mm)       |       Width: 122mm         | (48mm) |
|                   |                            |        |
|                   | \en{English text paragraph | [Orig. |
|                   | containing a \term...}     |  p. 1] |
|                   |                            |        |
|                   | \zh{对应中文学术翻译段落...}  | Term   |
|                   |                            | 术语释义|
|                   | [Vertical spacing: 1.15em] |        |
+-------------------+----------------------------+--------+
```

### Key Parameters (`geometry`):
- Paper size: A4 (`210mm × 297mm`)
- `top`: 26mm
- `bottom`: 26mm
- `inner`: 22mm (binding margin)
- `textwidth`: 122mm
- `marginparsep`: 6mm (separation between text and margin notes)
- `marginparwidth`: 48mm (usable width for annotations)

---

## 3. Font Hierarchy

| Script / Function | Font Family | Typical File Name | Fallback (Linux) |
| :--- | :--- | :--- | :--- |
| **English Body Serif** | TeX Gyre Pagella | `texgyrepagella-regular.otf` | Palatino / URW Palladio |
| **English Math Font** | TeX Gyre Pagella Math | `texgyrepagella-math.otf` | Asana Math / STIX Two Math |
| **Chinese Main Body** | Songti SC (宋体) | System `Songti SC` | `FandolSong-Regular` / `Noto Serif CJK SC` |
| **Chinese Annotation** | Kaiti SC (楷体) | System `Kaiti SC` | `FandolKai-Regular` / `Noto Serif CJK SC` |
| **Chinese Sans / Headings** | PingFang SC (黑体) | System `PingFang SC` | `FandolHei-Regular` / `Noto Sans CJK SC` |

---

## 4. Key LaTeX Macros & Environments

### Alternating Narrative Units
- `\en{...}`: English paragraph. Fully justifies with `\emergencystretch=2.5em` to prevent overfull hbox.
- `\zh{...}`: Chinese paragraph. Rendered at `\small` (9.5pt) with `\linespread{1.3}` and followed by `\vspace{1.15em}`.
- `\origpage{N}`: Renders `[Orig. p. N]` in the outer margin and anchors `\hypertarget{origpage:N}{}`.

### In-Text Annotation with Bidirectional Hyperlinks
- `\term[dictionary_key]{English Text}{中文规范释义}{语境注记}`:
  1. In-text text receives a soft blue highlight background (`#E8EFF7`).
  2. Outer margin receives a structured note with the bold English term, Kaiti Chinese translation, and context.
  3. Clicking the term jumps to the Master Glossary entry at the end of the book.
  4. In the Master Glossary, clicking the entry returns to this exact location in the text.
- `\acnote[key]{English Term}{中文释义}{注记}`:
  Same as `\term`, but does not apply background color to the text (useful for longer expressions or equations).

### Mathematical Theorem Environments
Inside `\begin{theorem}`, `\begin{lemma}`, `\begin{proof}`, etc., use dual blocks:
```latex
\begin{theorem}
\begin{enblock}
Let $f$ be an integrable function...
\end{enblock}
\begin{zhblock}
设 $f$ 为可积函数...
\end{zhblock}
\end{theorem}
```
This guarantees synchronized structure and clean visual distinction between original statements and translations.
