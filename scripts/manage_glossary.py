#!/usr/bin/env python3
"""
manage_glossary.py - Master Academic Glossary Management Tool

Validates glossary terms JSON, checks for duplicates, and compiles
a publication-grade LaTeX longtable with bidirectional hyperlinked navigation:
- Links forward from in-text margin annotations: \\term -> \\hypertarget{glossary:key}
- Links back from glossary entry to text: \\hyperlink{termfirst:key} -> text location
"""

import sys
import json
import argparse
from pathlib import Path

def validate_glossary(data: list) -> bool:
    seen_keys = set()
    is_valid = True

    for idx, item in enumerate(data):
        key = item.get("key") or item.get("term_en")
        if not key:
            print(f"[FAIL] Entry #{idx+1} is missing 'key' or 'term_en'.")
            is_valid = False
            continue

        if key in seen_keys:
            print(f"[WARN] Duplicate term key detected: '{key}' (entry #{idx+1})")
        seen_keys.add(key)

        if not item.get("definition_zh"):
            print(f"[WARN] Entry '{key}' is missing 'definition_zh'.")

    return is_valid

def generate_latex_glossary(data: list, output_path: Path):
    """
    Renders entries into LaTeX longtable format with bidirectional hypertarget/hyperlinks.
    """
    # Sort terms alphabetically by key
    sorted_items = sorted(data, key=lambda x: (x.get("key") or x.get("term_en", "")).lower())

    latex_lines = [
        "% Auto-generated Academic Glossary with Bidirectional Hyperlinks",
        "\\begin{longtable}{p{2.8cm} p{4.2cm} p{3.6cm}}",
        "\\toprule",
        "\\textbf{English Term / 学术用语} & \\textbf{Chinese Definition / 中文规范释义} & \\textbf{Academic Context / 语境注记} \\\\",
        "\\midrule",
        "\\endhead",
        "\\bottomrule",
        "\\endfoot",
    ]

    for item in sorted_items:
        key = item.get("key") or item.get("term_en")
        term_en = item.get("term_en", key)
        def_zh = item.get("definition_zh", "")
        notes = item.get("notes", "")

        # LaTeX-safe escaping for underscores or special characters if needed
        anchor_key = key.replace("\\", "")

        # Target anchor for clicks arriving from margin notes (\term / \acnote)
        # Clicking the English term in the glossary table jumps back to its first occurrence in text
        entry_col1 = (
            f"\\hypertarget{{glossary:{anchor_key}}}{{}}"
            f"\\hyperlink{{termfirst:{anchor_key}}}{{\\textbf{{{term_en}}}}}"
        )
        entry_col2 = f"{{\\kaishu {def_zh}}}"
        entry_col3 = f"{{\\small\\textcolor{{black!70}}{{{notes}}}}}"

        latex_lines.append(f"{entry_col1} & {entry_col2} & {entry_col3} \\\\")

    latex_lines.append("\\end{longtable}\n")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(latex_lines), encoding="utf-8")
    print(f"[SUCCESS] LaTeX glossary table generated: {output_path} ({len(sorted_items)} terms)")

def main():
    parser = argparse.ArgumentParser(description="Academic Glossary Manager for LaTeX Bilingual Editions")
    parser.add_argument("--input", required=True, help="Input JSON glossary file")
    parser.add_argument("--export-tex", help="Output LaTeX glossary table file (.tex)")
    parser.add_argument("--validate", action="store_true", help="Validate terms integrity")

    args = parser.parse_args()
    input_path = Path(args.input)

    if not input_path.is_file():
        print(f"[ERROR] Glossary file not found: {input_path}")
        sys.exit(1)

    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        if isinstance(data, dict) and "terms" in data:
            data = data["terms"]
        else:
            print("[ERROR] JSON structure must be a list of term objects or contain a 'terms' list.")
            sys.exit(1)

    valid = validate_glossary(data)

    if args.export_tex:
        generate_latex_glossary(data, Path(args.export_tex))
    elif not args.validate:
        print(f"Glossary contains {len(data)} terms. Validation passed: {valid}")

if __name__ == "__main__":
    main()
