#!/usr/bin/env python3
"""Render first-page web previews for Portable Game Night printable PDFs.

The PDFs remain the printable source of truth. These WebP previews are embedded on
individual game pages so players can scan the site and read the play aid on a
phone without passing paper around.
"""
from __future__ import annotations

from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
PRINTABLES = ROOT / 'printables'
OUT = PRINTABLES / 'previews'
OUT.mkdir(parents=True, exist_ok=True)

# Good phone-readable size without making the repo enormous.
TARGET_WIDTH = 900
WEBP_QUALITY = 82


def render_preview(pdf_path: Path) -> Path:
    out_path = OUT / f'{pdf_path.stem}.webp'
    doc = fitz.open(pdf_path)
    if not doc.page_count:
        raise ValueError(f'{pdf_path.name} has no pages')
    page = doc[0]
    scale = TARGET_WIDTH / page.rect.width
    pix = page.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)
    image = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    image.save(out_path, 'WEBP', quality=WEBP_QUALITY, method=6)
    doc.close()
    return out_path


def main() -> None:
    pdfs = sorted(PRINTABLES.glob('*.pdf'))
    if not pdfs:
        raise SystemExit('No printable PDFs found. Run scripts/generate_printables.py first.')

    written = []
    for pdf in pdfs:
        written.append(render_preview(pdf))

    print(f'Generated {len(written)} printable preview images in {OUT.relative_to(ROOT)}')
    for path in written:
        print(path.relative_to(ROOT))


if __name__ == '__main__':
    main()
