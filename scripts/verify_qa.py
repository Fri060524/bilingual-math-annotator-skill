#!/usr/bin/env python3
"""
verify_qa.py - Automated Quality Assurance for Bilingual Academic LaTeX Projects

Checks LaTeX source files and compilation logs for:
1. Parity between English and Chinese paragraph units (\\en vs \\zh, enblock vs zhblock)
2. Mathematical delimiter balance ($...$, \\[...\\])
3. LaTeX environment matching (theorem, proof, align, etc.)
4. Label uniqueness (\\label{...})
5. Original page markers (\\origpage{...})
6. Compilation log cleanliness (missing glyphs, undefined references)
"""

import sys
import re
import argparse
from pathlib import Path

def check_latex_source(tex_path: Path):
    issues = []
    warnings = []

    try:
        content = tex_path.read_text(encoding="utf-8")
    except Exception as e:
        return {
            "file": str(tex_path),
            "issues": [f"Cannot read file: {e}"],
            "warnings": [],
            "passed": False
        }

    # 1. Check Bilingual Block Parity
    en_paras = len(re.findall(r"\\en\{", content))
    zh_paras = len(re.findall(r"\\zh\{", content))
    if en_paras != zh_paras:
        issues.append(f"Parity mismatch: \\en count ({en_paras}) != \\zh count ({zh_paras})")

    en_blocks = len(re.findall(r"\\begin\{enblock\}", content))
    zh_blocks = len(re.findall(r"\\begin\{zhblock\}", content))
    if en_blocks != zh_blocks:
        issues.append(f"Parity mismatch: \\begin{{enblock}} ({en_blocks}) != \\begin{{zhblock}} ({zh_blocks})")

    # 2. Check Math Delimiters Balance
    # Inline math dollars (excluding escaped \$)
    inline_math_dollars = len(re.findall(r"(?<!\\)\$", content))
    if inline_math_dollars % 2 != 0:
        issues.append(f"Unmatched inline math dollar signs ($): count is {inline_math_dollars} (odd)")

    open_display = len(re.findall(r"(?<!\\)\\\[", content))
    close_display = len(re.findall(r"(?<!\\)\\\]", content))
    if open_display != close_display:
        issues.append(f"Unmatched display math: \\[ ({open_display}) != \\] ({close_display})")

    # Common LaTeX environments
    common_envs = [
        "equation", "equation*", "align", "align*", "gather", "gather*",
        "theorem", "lemma", "proposition", "corollary", "definition",
        "remark", "example", "exercise", "problem", "proof"
    ]
    for env in common_envs:
        escaped_env = re.escape(env)
        opens = len(re.findall(rf"\\begin\{{{escaped_env}\}}", content))
        closes = len(re.findall(rf"\\end\{{{escaped_env}\}}", content))
        if opens != closes:
            issues.append(f"Unmatched environment: \\begin{{{env}}} ({opens}) != \\end{{{env}}} ({closes})")

    # 3. Check Labels Uniqueness
    labels = re.findall(r"\\label\{([^}]+)\}", content)
    duplicate_labels = [lbl for lbl in set(labels) if labels.count(lbl) > 1]
    if duplicate_labels:
        issues.append(f"Duplicate labels detected: {duplicate_labels}")

    # 4. Check Margin Notes & Page Markers
    orig_pages = re.findall(r"\\origpage\{([^}]+)\}", content)
    terms = re.findall(r"\\term(?:\[[^\]]*\])?\{([^}]+)\}", content)
    acnotes = re.findall(r"\\acnote(?:\[[^\]]*\])?\{([^}]+)\}", content)

    if not orig_pages:
        warnings.append("No \\origpage markers found in file.")

    return {
        "file": str(tex_path),
        "en_units": en_paras + en_blocks,
        "zh_units": zh_paras + zh_blocks,
        "orig_pages_count": len(orig_pages),
        "terms_count": len(terms),
        "acnotes_count": len(acnotes),
        "issues": issues,
        "warnings": warnings,
        "passed": len(issues) == 0
    }

def check_compilation_log(log_path: Path):
    issues = []
    warnings = []

    if not log_path.exists():
        return {
            "log_file": str(log_path),
            "issues": [f"Log file not found: {log_path}"],
            "warnings": [],
            "passed": False
        }

    try:
        log_content = log_path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        return {
            "log_file": str(log_path),
            "issues": [f"Cannot read log file: {e}"],
            "warnings": [],
            "passed": False
        }

    for line in log_content.splitlines():
        if "Missing character: There is no" in line:
            issues.append(f"Missing glyph detected: {line.strip()}")
        elif "LaTeX Warning: Reference" in line and "undefined" in line:
            issues.append(f"Undefined reference: {line.strip()}")
        elif "LaTeX Warning: There were undefined references" in line:
            issues.append("Summary warning: There were undefined references.")
        elif "! LaTeX Error" in line or "! Emergency stop" in line:
            issues.append(f"Compilation error: {line.strip()}")
        elif "Overfull \\hbox" in line:
            warnings.append(line.strip())

    return {
        "log_file": str(log_path),
        "issues": issues,
        "warnings": warnings,
        "passed": len(issues) == 0
    }

def main():
    parser = argparse.ArgumentParser(description="Automated QA Validator for Bilingual Academic LaTeX Projects")
    parser.add_argument("tex_files", nargs="+", help="Path to LaTeX source file(s) (.tex)")
    parser.add_argument("--log", type=str, default=None, help="Optional path to compilation log file (.log)")
    args = parser.parse_args()

    all_passed = True

    print("==================================================")
    print("  Bilingual Academic LaTeX QA Verification Tool")
    print("==================================================\n")

    for file_str in args.tex_files:
        path = Path(file_str)
        if not path.is_file():
            print(f"[-] Skipping non-file path: {file_str}")
            continue

        res = check_latex_source(path)
        print(f"[*] Checking: {res['file']}")
        print(f"    - Bilingual Units: EN={res['en_units']}, ZH={res['zh_units']}")
        print(f"    - Original Page Markers: {res['orig_pages_count']}")
        print(f"    - Annotated Terms / Notes: {res['terms_count'] + res['acnotes_count']}")

        if res["warnings"]:
            for w in res["warnings"]:
                print(f"    [WARN] {w}")

        if res["issues"]:
            all_passed = False
            for iss in res["issues"]:
                print(f"    [FAIL] {iss}")
        else:
            print("    [PASS] Source code integrity verified.")
        print()

    if args.log:
        log_res = check_compilation_log(Path(args.log))
        print(f"[*] Checking Compilation Log: {log_res['log_file']}")
        if log_res["issues"]:
            all_passed = False
            for iss in log_res["issues"]:
                print(f"    [FAIL] {iss}")
        else:
            print("    [PASS] Log is clean (0 missing glyphs, 0 undefined references).")
        print()

    print("==================================================")
    if all_passed:
        print("  RESULT: ALL QA CHECKS PASSED SUCCESSFULLY (PASS)")
        print("==================================================")
        sys.exit(0)
    else:
        print("  RESULT: QA ISSUES DETECTED. PLEASE REVIEW LOG ABOVE (FAIL)")
        print("==================================================")
        sys.exit(1)

if __name__ == "__main__":
    main()
