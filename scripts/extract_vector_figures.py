#!/usr/bin/env python3
"""
extract_vector_figures.py - Lossless Vector PDF Figure Extraction Tool

Extracts high-precision vector graphics from original textbook PDFs
using PyMuPDF (fitz) bounding box cropping, preserving 100% vector sharpness.

Usage:
    # Single figure crop:
    python3 extract_vector_figures.py --input book.pdf --page 25 --rect 100,68,345,230 --output fig_1_1.pdf

    # Batch extraction via JSON configuration:
    python3 extract_vector_figures.py --config figures_config.json
"""

import sys
import json
import argparse
from pathlib import Path

def extract_single_figure(pdf_path: Path, page_number: int, rect_coords: list, output_path: Path):
    """
    Extracts a vector bounding box from a specific page into a standalone PDF.
    rect_coords: [x0, y0, x1, y1] in PDF points.
    page_number: 1-based page number.
    """
    try:
        import fitz  # PyMuPDF
    except ImportError:
        print("[ERROR] PyMuPDF is not installed. Please run: pip install pymupdf")
        sys.exit(1)

    if not pdf_path.is_file():
        print(f"[ERROR] PDF file not found: {pdf_path}")
        sys.exit(1)

    doc = fitz.open(pdf_path)
    page_idx = page_number - 1
    if page_idx < 0 or page_idx >= len(doc):
        print(f"[ERROR] Page number {page_number} out of range (1 - {len(doc)}).")
        sys.exit(1)

    crop_rect = fitz.Rect(rect_coords[0], rect_coords[1], rect_coords[2], rect_coords[3])

    new_doc = fitz.open()
    # Insert source page into new document
    new_doc.insert_pdf(doc, from_page=page_idx, to_page=page_idx)
    target_page = new_doc[0]
    target_page.set_cropbox(crop_rect)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    new_doc.save(str(output_path), garbage=4, deflate=True)
    new_doc.close()
    doc.close()

    print(f"[SUCCESS] Vector figure saved: {output_path} (Crop: {crop_rect})")

def extract_batch_from_config(config_path: Path):
    with open(config_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    pdf_path = Path(data.get("source_pdf", ""))
    if not pdf_path.is_absolute():
        pdf_path = (config_path.parent / pdf_path).resolve()

    output_dir = Path(data.get("output_dir", "./figures"))
    if not output_dir.is_absolute():
        output_dir = (config_path.parent / output_dir).resolve()

    figures = data.get("figures", [])
    print(f"[*] Batch processing {len(figures)} vector figures from: {pdf_path}")

    for fig in figures:
        name = fig["name"]
        page_num = fig["page"]
        rect = fig["rect"]
        dest = output_dir / name
        extract_single_figure(pdf_path, page_num, rect, dest)

def main():
    parser = argparse.ArgumentParser(description="Lossless Vector Figure Cropper for LaTeX Publishing")
    parser.add_argument("--config", type=str, help="Path to JSON configuration file for batch processing")
    parser.add_argument("--input", type=str, help="Path to input original textbook PDF")
    parser.add_argument("--page", type=int, help="Page number in original PDF (1-based)")
    parser.add_argument("--rect", type=str, help="Bounding box coordinates 'x0,y0,x1,y1' in PDF points")
    parser.add_argument("--output", type=str, help="Output figure filename (.pdf)")

    args = parser.parse_args()

    if args.config:
        extract_batch_from_config(Path(args.config))
    elif args.input and args.page and args.rect and args.output:
        coords = [float(x.strip()) for x in args.rect.split(",")]
        extract_single_figure(Path(args.input), args.page, coords, Path(args.output))
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
