# Minimal Working Example (MWE) / 最小可编译范例

This directory provides a self-contained, compilable demonstration of the bilingual academic textbook layout.

---

## What It Demonstrates

1. **Alternating Layout**: English source (`\en{...}`) and Chinese translation (`\zh{...}`) with identical textwidth and vertical rhythm.
2. **Dual-Block Environments**: Theorems, definitions, and proofs structured using `enblock` and `zhblock`.
3. **Academic Annotations**:
   - `\term`: In-text highlight with soft blue background (`#E8EFF7`) + outer margin note.
   - `\acnote`: Margin academic English annotations.
   - `\origpage`: Original printed edition page tracking anchors (`[Orig. p. N]`).
4. **Bidirectional Navigation**:
   - In-text terms link directly to the Master Glossary table at the end of the book.
   - Clicking terms in the glossary table returns to the first occurrence in the text.
   - Running headers click to return to the Table of Contents.

---

## How to Compile

Run `xelatex` twice to resolve reciprocal hyperlinked references:

```bash
cd minimal_book
xelatex main.tex
xelatex main.tex
```

Verify quality using the automated QA script:

```bash
python3 ../../scripts/verify_qa.py sample_chapter.tex --log main.log
```
