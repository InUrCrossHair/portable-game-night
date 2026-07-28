#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import fitz

ROOT = Path(__file__).resolve().parents[1]
PRINTABLES = ROOT / 'printables'
REPORT = ROOT / 'printables' / '_qa_layout_report.txt'
PREVIEWS = ROOT / 'printables' / '_qa_previews'
PREVIEWS.mkdir(exist_ok=True)


def page_ink_bbox(pix, threshold=245):
    img = Image.frombytes('RGB', [pix.width, pix.height], pix.samples)
    # Difference from near-white background. Returns bbox in rendered pixels.
    mask = Image.new('L', img.size, 0)
    src = img.load(); dst = mask.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b = src[x, y]
            if r < threshold or g < threshold or b < threshold:
                dst[x, y] = 255
    return mask.getbbox(), img


def classify(path: Path, page_no: int, page, bbox, render_size):
    problems = []
    w, h = render_size
    # 0.18 inch at 144dpi equivalent. At zoom=0.5 page is usually 306x396, so use scaled margin.
    margin = max(8, int(min(w, h) * 0.025))
    if bbox:
        x0, y0, x1, y1 = bbox
        if x0 < margin: problems.append(f'ink near left edge x={x0}px')
        if y0 < margin: problems.append(f'ink near top edge y={y0}px')
        if w - x1 < margin: problems.append(f'ink near right edge gap={w-x1}px')
        if h - y1 < margin: problems.append(f'ink near bottom edge gap={h-y1}px')
    # Basic geometry sanity.
    pw, ph = page.rect.width, page.rect.height
    if abs(pw - 612) > 2 or abs(ph - 792) > 2:
        problems.append(f'unexpected page size {pw:.1f}x{ph:.1f}')
    return problems


def make_contact_sheet(page_images, out_path: Path, cols=5, thumb_w=260):
    thumbs = []
    font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 14)
    for label, img in page_images:
        scale = thumb_w / img.width
        thumb_h = int(img.height * scale)
        thumb = img.resize((thumb_w, thumb_h), Image.LANCZOS)
        canvas = Image.new('RGB', (thumb_w, thumb_h + 42), 'white')
        canvas.paste(thumb, (0, 0))
        d = ImageDraw.Draw(canvas)
        d.rectangle([0, thumb_h, thumb_w-1, thumb_h+41], fill=(245,245,245), outline=(160,160,160))
        short = label if len(label) <= 40 else label[:37] + '...'
        d.text((5, thumb_h+4), short, font=font, fill='black')
        thumbs.append(canvas)
    if not thumbs: return
    rows = (len(thumbs) + cols - 1) // cols
    cell_w = thumb_w; cell_h = max(t.height for t in thumbs)
    sheet = Image.new('RGB', (cols*cell_w, rows*cell_h), 'white')
    for i, t in enumerate(thumbs):
        x = (i % cols) * cell_w; y = (i // cols) * cell_h
        sheet.paste(t, (x, y))
    sheet.save(out_path)


def main():
    pdfs = sorted(PRINTABLES.glob('**/*.pdf'))
    lines = []
    flagged = []
    page_images = []
    total_pages = 0
    for pdf in pdfs:
        rel = pdf.relative_to(ROOT)
        try:
            doc = fitz.open(pdf)
        except Exception as e:
            lines.append(f'ERROR {rel}: cannot open: {e}')
            flagged.append((str(rel), 0, [f'cannot open: {e}']))
            continue
        for i, page in enumerate(doc, 1):
            total_pages += 1
            pix = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5), alpha=False)
            bbox, img = page_ink_bbox(pix)
            problems = classify(pdf, i, page, bbox, img.size)
            label = f'{rel.name} p{i}' if len(doc)>1 else rel.name
            page_images.append((label, img))
            if problems:
                flagged.append((str(rel), i, problems))
        doc.close()
    for rel, page_no, problems in flagged:
        lines.append(f'{rel} page {page_no}: ' + '; '.join(problems))
    if not lines:
        lines.append('No mechanical edge/page-size problems detected.')
    lines.append(f'Checked {len(pdfs)} PDFs / {total_pages} pages.')
    REPORT.write_text('\n'.join(lines) + '\n', encoding='utf-8')
    # Contact sheets in batches of 25 pages for visual review.
    for idx in range(0, len(page_images), 25):
        make_contact_sheet(page_images[idx:idx+25], PREVIEWS / f'contact_sheet_{idx//25+1:02d}.jpg')
    print(REPORT)
    print(f'contact sheets: {len(list(PREVIEWS.glob("contact_sheet_*.jpg")))} in {PREVIEWS}')
    print('\n'.join(lines[:30]))

if __name__ == '__main__':
    main()
