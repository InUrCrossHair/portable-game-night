#!/usr/bin/env python3
"""Generate paper-saving 2-up versions of selected write-on score sheets.

Each output PDF keeps one game per sheet: the same printable appears once on the
top half and once on the bottom half, with a light cut line between them. The
original full-page PDFs remain unchanged.
"""
from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
PRINTABLES = ROOT / 'printables'
OUT = PRINTABLES / 'compact'
OUT.mkdir(parents=True, exist_ok=True)

PAGE_W, PAGE_H = 2550, 3300  # 8.5x11 at 300 DPI
HALF_H = PAGE_H // 2
DPI_SCALE = 300 / 72
CUT_LINE = (120, 120, 120)

CANDIDATES = [
    'farkle-score-sheet.pdf',
    'skunk-score-sheet.pdf',
    'stuck-in-the-mud-score-sheet.pdf',
    'three-or-more-score-sheet.pdf',
    'dice-golf-scorecard.pdf',
    'midnight-score-sheet.pdf',
    'chicago-score-sheet.pdf',
    'bunco-score-sheet.pdf',
    'drop-dead-score-sheet.pdf',
    'sevens-out-score-sheet.pdf',
    'golf-card-game-score-sheet.pdf',
    'rummy-score-sheet.pdf',
    'gin-rummy-score-sheet.pdf',
    'hearts-score-sheet.pdf',
    'euchre-score-sheet.pdf',
    'bowling-solitaire-score-sheet.pdf',
    'solo-farkle-challenge-sheet.pdf',
    'dice-solitaire-score-sheet.pdf',
    'bowling-dice-score-sheet.pdf',
    'knock-out-dice-score-sheet.pdf',
    'dice-baseball-score-sheet.pdf',
    'nerts-score-sheet.pdf',
]


def render_first_page(pdf_path: Path) -> Image.Image:
    doc = fitz.open(pdf_path)
    if not doc.page_count:
        raise ValueError(f'{pdf_path.name} has no pages')
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(DPI_SCALE, DPI_SCALE), alpha=False)
    image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    doc.close()
    return image


def paste_fit(canvas: Image.Image, source: Image.Image, box: tuple[int, int, int, int]) -> None:
    x1, y1, x2, y2 = box
    box_w, box_h = x2 - x1, y2 - y1
    scale = min(box_w / source.width, box_h / source.height)
    new_size = (round(source.width * scale), round(source.height * scale))
    resized = source.resize(new_size, Image.Resampling.LANCZOS)
    x = x1 + (box_w - new_size[0]) // 2
    y = y1 + (box_h - new_size[1]) // 2
    canvas.paste(resized, (x, y))


def make_2up(source_pdf: Path) -> Path:
    source = render_first_page(source_pdf)
    canvas = Image.new('RGB', (PAGE_W, PAGE_H), 'white')
    # Leave a modest printable margin around each half-sheet so titles and icons
    # do not sit on the physical page edge after scaling.
    side_margin = 80
    top_margin = 55
    cut_gap = 34
    paste_fit(canvas, source, (side_margin, top_margin, PAGE_W - side_margin, HALF_H - cut_gap))
    paste_fit(canvas, source, (side_margin, HALF_H + cut_gap, PAGE_W - side_margin, PAGE_H - top_margin))

    draw = ImageDraw.Draw(canvas)
    y = HALF_H
    dash = 44
    gap = 30
    x = 120
    while x < PAGE_W - 120:
        draw.line((x, y, min(x + dash, PAGE_W - 120), y), fill=CUT_LINE, width=3)
        x += dash + gap

    out_path = OUT / f'{source_pdf.stem}-2up.pdf'
    canvas.save(out_path, 'PDF', resolution=300.0)
    return out_path


def main() -> None:
    written = []
    missing = []
    for filename in CANDIDATES:
        source = PRINTABLES / filename
        if not source.exists():
            missing.append(filename)
            continue
        written.append(make_2up(source))
    if missing:
        raise SystemExit('Missing source printable(s): ' + ', '.join(missing))
    print(f'Generated {len(written)} compact 2-up printables in {OUT.relative_to(ROOT)}')
    for path in written:
        print(path.relative_to(ROOT))


if __name__ == '__main__':
    main()
