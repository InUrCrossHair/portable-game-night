#!/usr/bin/env python3
"""Generate paper-saving Portable Game Night printable bundles.

The full-page PDFs remain the polished source library. These outputs are for
physical-kit printing where paper count matters: half-sheet references,
compact-score bundles, and 4-up quick-reference cards.
"""
from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory

import fitz
from PIL import Image, ImageDraw, ImageFont
from pypdf import PdfReader, PdfWriter

from generate_printable_bundles import REFERENCE_PRINTABLES, REUSABLE_PRINTABLES
from generate_compact_printables import CANDIDATES as COMPACT_SCORE_SOURCES

ROOT = Path(__file__).resolve().parents[1]
PRINTABLES = ROOT / 'printables'
OUT = PRINTABLES / 'paper-saver'
OUT.mkdir(parents=True, exist_ok=True)

PAGE_W, PAGE_H = 2550, 3300  # 8.5x11 at 300 DPI
M = 90
CUT = (135, 135, 135)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK = (64, 64, 64)
LIGHT = (244, 244, 244)
ALT = (226, 226, 226)

FONT_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)

F_TITLE = font(82, True)
F_H = font(52, True)
F_BODY = font(34)
F_BODY_B = font(34, True)
F_SMALL = font(28)
F_SMALL_B = font(28, True)
F_TINY = font(24)


def wrapped(draw: ImageDraw.ImageDraw, text: str, max_width: int, fnt: ImageFont.FreeTypeFont) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ''
    for word in words:
        test = word if not cur else f'{cur} {word}'
        if draw.textbbox((0, 0), test, font=fnt)[2] <= max_width:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def center(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, fnt: ImageFont.FreeTypeFont, fill=BLACK) -> None:
    x1, y1, x2, y2 = box
    bb = draw.textbbox((0, 0), text, font=fnt)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    draw.text((x1 + (x2-x1-tw)/2, y1 + (y2-y1-th)/2 - 3), text, font=fnt, fill=fill)


def render_pdf_page(path: Path) -> Image.Image:
    doc = fitz.open(path)
    if not doc.page_count:
        raise ValueError(f'{path} has no pages')
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(300/72, 300/72), alpha=False)
    img = Image.frombytes('RGB', (pix.width, pix.height), pix.samples)
    doc.close()
    return img


def paste_fit(canvas: Image.Image, source: Image.Image, box: tuple[int, int, int, int]) -> None:
    x1, y1, x2, y2 = box
    bw, bh = x2-x1, y2-y1
    scale = min(bw/source.width, bh/source.height)
    size = (round(source.width*scale), round(source.height*scale))
    resized = source.resize(size, Image.Resampling.LANCZOS)
    x = x1 + (bw - size[0])//2
    y = y1 + (bh - size[1])//2
    canvas.paste(resized, (x, y))


def save_multipage(images: list[Image.Image], path: Path) -> Path:
    if not images:
        raise ValueError(f'No pages for {path}')
    first, rest = images[0].convert('RGB'), [im.convert('RGB') for im in images[1:]]
    first.save(path, 'PDF', resolution=300.0, save_all=True, append_images=rest)
    return path


def make_half_sheet_bundle(filenames: list[str], output_name: str, title: str) -> Path:
    pages: list[Image.Image] = []
    for i in range(0, len(filenames), 2):
        canvas = Image.new('RGB', (PAGE_W, PAGE_H), WHITE)
        draw = ImageDraw.Draw(canvas)
        top = PRINTABLES / filenames[i]
        paste_fit(canvas, render_pdf_page(top), (70, 70, PAGE_W-70, PAGE_H//2-45))
        if i + 1 < len(filenames):
            bottom = PRINTABLES / filenames[i+1]
            paste_fit(canvas, render_pdf_page(bottom), (70, PAGE_H//2+45, PAGE_W-70, PAGE_H-70))
        # Cut line and tiny footer keep the sheet self-explanatory without stealing space.
        y = PAGE_H // 2
        x = 130
        while x < PAGE_W - 130:
            draw.line((x, y, min(x+55, PAGE_W-130), y), fill=CUT, width=3)
            x += 90
        center(draw, (0, y-34, PAGE_W, y-4), 'cut line', F_TINY, fill=(105,105,105))
        pages.append(canvas)
    return save_multipage(pages, OUT / output_name)


QUICK_CARDS = [
    ('Pig', ['Roll one die and build a temporary turn score.', 'Bank to keep points. Roll a 1: lose unbanked points and end turn.', 'First to 100 wins.']),
    ('Going to Boston', ['Roll 3 dice; keep the highest.', 'Roll remaining 2; keep highest. Roll final die.', 'Add kept dice. Highest score wins the round.']),
    ('Beat That', ['Roll 2–4 dice.', 'Arrange dice into the biggest possible number.', 'Example: 5, 3, 1 becomes 531. Highest number wins.']),
    ('Cho-Han', ['Cho = even. Han = odd.', 'Roll 2 dice under a cup and reveal the total.', 'Correct callers win the round or take a token.']),
    ('Aces in the Pot', ['Start with 3 tokens each. Roll 2 dice.', 'Each 1 sends a token to the pot. Each 6 passes one left.', 'No tokens: skip, but re-enter if passed a token.']),
    ('Left Center Right', ['Start with 3 tokens. Roll up to 3 dice.', '1=left, 2=right, 3=center, 4/5/6=keep.', 'Last player with tokens wins.']),
    ('Help Your Neighbor', ['Give each player 10 tokens and a number.', 'Roll 3 dice. Matching players remove 1 token.', 'First player to remove all tokens wins.']),
    ('Tenzi', ['Each player uses 10 dice.', 'Pick a target number after first roll.', 'Keep target dice and reroll the rest. First all-matching wins.']),
    ('Craps Pass Line', ['Come-out: 7/11 wins; 2/3/12 loses.', '4/5/6/8/9/10 sets the point.', 'Then roll point again to win; 7 loses.']),
    ('Poker Dice', ['High to low: five kind, four kind, full house, straight, three kind, two pair, pair, high die.', 'Roll up to 3 times.']),
    ('Bar Dice', ['Roll up to three times, keeping any dice.', 'Rankings: five kind, four kind, full house, straight, three kind, two pair, pair.']),
    ('Cee-lo', ['4-5-6 is best. 1-2-3 is worst.', 'Triples rank 6s down to 1s.', 'Pair + odd die scores the odd die.']),
    ('Mia', ['Rolls read high die first: 6 and 4 = 64.', 'Ranking: 21/Mia, doubles 66–11, then 65–31.', 'Announce higher or challenge. False claim loses a life.']),
    ('Mexico', ['21 is Mexico and highest.', 'Doubles rank 66 down to 11. Other rolls read high die first.', 'Accept and beat the roll, or challenge.']),
    ("Liar's Dice", ['5 dice + cup per player. 1s are wild.', 'Raise quantity or face. Call liar to reveal.', 'If bid is met caller loses; otherwise bidder loses.']),
    ('Twenty-One Dice', ['Roll 2 dice, then stop or roll again.', 'Closest to 21 wins. Over 21 busts.', 'Play rounds for tokens or points.']),
    ('Crazy Eights', ['Play matching rank/suit, or play an 8 wild.', 'After an 8, name the next suit.', 'If unable to play, draw one card. First out wins.']),
    ('Spoons', ['Use one fewer spoon/token than players.', 'Pass cards until someone gets four of a kind.', 'Once one spoon is taken, anyone may grab. No spoon loses.']),
    ('BS / Cheat', ['Play cards face down and announce the required rank.', 'You may bluff. Anyone may call BS/Cheat.', 'Liar takes pile; false caller takes pile.']),
    ('Chase the Ace', ['Deal one card each. Aces low, kings high.', 'Keep or swap left; kings block swaps.', 'Lowest card loses a life. Last alive wins.']),
    ('Slapjack', ['Deal all cards face down.', 'Players flip one card to center.', 'When a jack appears, first flat-hand slap wins pile.']),
    ('Thirty-One', ['Get close to 31 in one suit.', 'A=11, faces=10, numbers face value.', 'Draw/discard or knock. Lowest loses a life.']),
    ('Poker Hands', ['High to low: royal flush, straight flush, four kind, full house, flush, straight, three kind, two pair, pair, high card.', 'Use casual token limits.']),
    ('Indian Poker', ['Ante one token and hold one card on forehead without looking.', 'Bet based on everyone else’s cards.', 'Highest card wins.']),
]


def draw_card(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, bullets: list[str]) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle([x1, y1, x2, y2], radius=28, outline=BLACK, width=6, fill=WHITE)
    draw.rectangle([x1, y1, x2, y1+92], fill=DARK, outline=BLACK, width=5)
    title_font = F_H
    while draw.textbbox((0, 0), title, font=title_font)[2] > (x2-x1-44) and title_font.size > 36:
        title_font = font(title_font.size - 2, True)
    center(draw, (x1+20, y1+8, x2-20, y1+86), title, title_font, WHITE)
    yy = y1 + 125
    for bullet in bullets:
        draw.text((x1+42, yy), '•', font=F_BODY_B, fill=BLACK)
        for line in wrapped(draw, bullet, x2-x1-118, F_BODY):
            draw.text((x1+82, yy), line, font=F_BODY, fill=BLACK)
            yy += 44
        yy += 18


def make_quick_cards() -> Path:
    pages: list[Image.Image] = []
    cols = 2
    rows = 3
    cards_per_page = cols * rows
    top = 170
    gap_x = 70
    gap_y = 48
    card_w = (PAGE_W - 2*M - gap_x) // cols
    card_h = (PAGE_H - top - M - gap_y*(rows-1)) // rows
    for i in range(0, len(QUICK_CARDS), cards_per_page):
        canvas = Image.new('RGB', (PAGE_W, PAGE_H), WHITE)
        draw = ImageDraw.Draw(canvas)
        center(draw, (0, 28, PAGE_W, 126), 'Portable Game Night • 6-Up Quick Reference Cards', F_TITLE)
        boxes = []
        for r in range(rows):
            for c in range(cols):
                x1 = M + c * (card_w + gap_x)
                y1 = top + r * (card_h + gap_y)
                boxes.append((x1, y1, x1 + card_w, y1 + card_h))
        for box, (title, bullets) in zip(boxes, QUICK_CARDS[i:i+cards_per_page]):
            draw_card(draw, box, title, bullets)
        # Cut guides between rows/columns.
        x_mid = PAGE_W // 2
        draw.line((x_mid, top-18, x_mid, PAGE_H-M), fill=CUT, width=2)
        for r in range(1, rows):
            y = top + r*card_h + (r-1)*gap_y + gap_y//2
            draw.line((M, y, PAGE_W-M, y), fill=CUT, width=2)
        pages.append(canvas)
    return save_multipage(pages, OUT / 'quick-reference-cards-6up.pdf')


def merge_pdfs(output_name: str, paths: list[Path]) -> Path:
    writer = PdfWriter()
    for path in paths:
        reader = PdfReader(str(path))
        for page in reader.pages:
            writer.add_page(page)
    out = OUT / output_name
    with out.open('wb') as f:
        writer.write(f)
    return out


def main() -> None:
    reference_half = make_half_sheet_bundle(REFERENCE_PRINTABLES, 'reference-half-sheets-bundle.pdf', 'Reference half sheets')
    compact_score_files = [OUT.parent / 'compact' / f'{Path(name).stem}-2up.pdf' for name in COMPACT_SCORE_SOURCES]
    for path in compact_score_files:
        if not path.exists():
            raise FileNotFoundError(f'Missing compact score sheet: {path}')
    compact_scores = merge_pdfs('compact-score-sheets-bundle.pdf', compact_score_files)
    quick_cards = make_quick_cards()
    reusable_paths = [PRINTABLES / name for name in REUSABLE_PRINTABLES]
    lean = merge_pdfs('lean-game-night-kit.pdf', reusable_paths + [quick_cards] + [compact_scores])
    full_saver = merge_pdfs('full-paper-saver-kit.pdf', reusable_paths + [reference_half] + [compact_scores])

    outputs = [reference_half, compact_scores, quick_cards, lean, full_saver]
    for path in outputs:
        print(f'{path.relative_to(ROOT)}: {len(PdfReader(str(path)).pages)} pages')


if __name__ == '__main__':
    main()
