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


DIGEST_GROUPS = [
    ('Simple Dice and Push-Your-Luck', 'Fast dice fillers that teach quickly and use almost no table space.', [
        ('Pig', 'Roll one die to build a turn score; bank anytime; roll 1 and lose unbanked turn points.'),
        ('Going to Boston', 'Roll 3 dice, keep highest; roll 2, keep highest; roll 1; high total wins.'),
        ('Beat That', 'Roll 2-4 dice and arrange them into the largest possible number.'),
        ('Tenzi', 'Each player races to get all 10 dice showing the same chosen number.'),
        ('Cho-Han', 'Call Cho/even or Han/odd before two dice are revealed.'),
        ('Twenty-One Dice', 'Roll 2 dice, then stop or roll again; closest to 21 without busting wins.'),
        ('Threes / Thirty', 'Roll 5-6 dice up to three times; threes count as 0; lowest score wins.'),
    ]),
    ('Bluffing Dice and Dice Rankings', 'Good for groups that like reading faces more than reading rulebooks.', [
        ("Liar's Dice", 'Bid quantity/face across hidden dice; call liar to reveal; 1s are wild in this house version.'),
        ('Mia', 'Two dice read high-first; 21/Mia beats doubles, doubles beat normal rolls.'),
        ('Mexico', '21 is highest; doubles rank 66 to 11; other rolls read high die first.'),
        ('Cee-lo', '4-5-6 best, 1-2-3 worst, triples rank high, pair plus odd die scores the point.'),
        ('Poker Dice', 'Five kind, four kind, full house, straight, three kind, two pair, pair, high die.'),
        ('Bar Dice', 'Roll up to three times; score by poker-style dice hand rankings.'),
    ]),
    ('Tokens, Pots and Betting Mats', 'Use candy, coins, chips, or harmless markers; no real-money value needed.', [
        ('Aces in the Pot', 'Start with 3 tokens; 1s go to pot, 6s pass left; last player with tokens wins.'),
        ('Left Center Right', 'Roll up to 3 dice: 1 left, 2 right, 3 center, 4-6 keep.'),
        ('Help Your Neighbor', 'Players have numbers and tokens; rolled matching numbers remove tokens.'),
        ('Craps Pass Line', 'Come-out 7/11 wins, 2/3/12 loses; point numbers must repeat before 7.'),
        ('Chuck-a-Luck', 'Bet on 1-6; roll 3 dice; payout depends on how many dice match.'),
        ('Sic Bo', 'Bet small/big, odd/even, exact totals, triples, or specific numbers.'),
        ('In-Between', 'Bet whether the third card falls strictly between two face-up cards.'),
    ]),
    ('Fast Party Card Games', 'Best when you want quick rounds, laughter, and low setup time.', [
        ('Crazy Eights', 'Match rank or suit; 8s are wild and choose the next suit; first out wins.'),
        ('Spoons', 'Pass cards until someone makes four of a kind; once one spoon is grabbed, all may grab.'),
        ('Slapjack', 'Flip cards to center; first flat-hand slap on a jack wins the pile.'),
        ('BS / Cheat', 'Announce required ranks face down; callers challenge truthfulness; loser takes pile.'),
        ('Shithead', 'Play equal/higher or pick up; special-card rules should be agreed before play.'),
        ('Mao', 'Only explain basic play; hidden rules create penalties and chaos.'),
    ]),
    ('Trick-Taking and Hand Management', 'For groups that want more structure than party games, but still portable.', [
        ('Euchre', 'Trump-taking teams game; makers score for taking 3 or more tricks; defenders score on euchre.'),
        ('Hearts', 'Avoid hearts and queen of spades; lowest score wins; shoot the moon optional.'),
        ('Spades', 'Bid tricks with a partner; make bid for points, miss bid for penalties.'),
        ('Oh Hell', 'Bid exact tricks each hand; exact bid scores bonus; missed bid scores 0.'),
        ('Knockout Whist', 'Take at least one trick each hand or get knocked out / lose a token.'),
        ('President', 'Shedding game with ranks; first out becomes President next hand.'),
        ('Durak', 'Attack/defend with trump; last player with cards is the fool.'),
    ]),
    ('Solitaire Setup Digest', 'Use these as setup reminders; full move details stay on the site pages.', [
        ('Klondike', '7 columns, 1-7 cards; build alternating-color tableau; foundations ace to king.'),
        ('FreeCell', 'All cards face up in 8 columns; use 4 free cells; foundations ace to king.'),
        ('Pyramid', 'Remove exposed pairs totaling 13; kings remove alone; clear the pyramid.'),
        ('Clock', '13 piles of 4; move revealed cards to rank piles; fourth king ends the game.'),
        ('Golf', '7 columns of 5; move exposed cards one rank above/below the waste.'),
        ('Canfield', '13-card reserve, 4 tableau piles, foundations start at dealt rank and wrap.'),
        ('Spider', 'Two decks, 10 columns; build same-suit king-to-ace sequences to remove.'),
        ('Accordion', 'Move piles left by rank/suit matches; compress deck into fewer piles.'),
    ]),
    ('Two-Player and Table Card Games', 'Good alternates when only two people want to play.', [
        ('Speed', 'Both play simultaneously one rank up/down onto center piles; refill to 5 cards.'),
        ('Spit', 'Build personal tableau, spit center cards, play up/down fast, slap smaller pile.'),
        ('Kings in the Corner', 'Shared solitaire: descending alternating colors; only kings start corner piles.'),
        ('Thirty-One', 'Draw/discard or knock; get close to 31 in one suit; lowest loses a life.'),
        ('Indian Poker', 'One forehead card each; bet based on others cards; high card wins.'),
        ('Poker Hands', 'Use as ranking reference for casual token poker.'),
        ('Chase the Ace', 'Keep or swap one card; kings block swaps; lowest card loses a life.'),
    ]),
    ('Reaction, Signals and Oddballs', 'A catch-all page for games with special table behavior.', [
        ('Kemps', 'Partners use a secret signal for four of a kind; opponents can call Counter-Kemps.'),
        ('Egyptian Rat Screw', 'Face-card challenges plus legal slaps like doubles and sandwiches.'),
        ('Ship, Captain, Crew', 'Lock 6, then 5, then 4; remaining two dice are cargo.'),
        ('Ninety-Nine', 'Keep running total at/below 99; special card effects shift the total.'),
        ('Poker / Ranking reminders', 'Agree tie-breaks, token limits, and house variants before play.'),
        ('Safety note', 'Use flat-hand slaps, small tokens, water/skips for drinking variants, and no pressure.'),
    ]),
]


def draw_digest_page(title: str, subtitle: str, entries: list[tuple[str, str]]) -> Image.Image:
    canvas = Image.new('RGB', (PAGE_W, PAGE_H), WHITE)
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle([M, 70, PAGE_W-M, 225], radius=34, outline=BLACK, width=6, fill=LIGHT)
    center(draw, (M+35, 86, PAGE_W-M-35, 154), title, F_TITLE)
    center(draw, (M+45, 154, PAGE_W-M-45, 214), subtitle, F_SMALL)

    gap = 56
    col_w = (PAGE_W - 2*M - gap) // 2
    x_positions = [M, PAGE_W//2 + gap//2]
    y_start = 290
    y = [y_start, y_start]
    body_font = font(31)
    name_font = font(34, True)

    for idx, (name, text) in enumerate(entries):
        col = idx % 2 if len(entries) > 6 else (0 if idx < (len(entries)+1)//2 else 1)
        x = x_positions[col]
        lines = wrapped(draw, text, col_w - 56, body_font)
        block_h = 54 + 38*len(lines) + 38
        if y[col] + block_h > PAGE_H - 150 and col == 0:
            col = 1
            x = x_positions[col]
        yy = y[col]
        draw.rounded_rectangle([x, yy, x+col_w, yy+block_h], radius=22, outline=(120,120,120), width=3, fill=WHITE)
        draw.text((x+24, yy+18), name, font=name_font, fill=BLACK)
        text_y = yy + 72
        for line in lines:
            draw.text((x+30, text_y), line, font=body_font, fill=BLACK)
            text_y += 38
        y[col] = yy + block_h + 30

    draw.text((M, PAGE_H-88), 'Paper Saver Digest - full rules, score sheets, and printable downloads are on the Portable Game Night site.', font=F_SMALL_B, fill=BLACK)
    return canvas


def draw_digest_section(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], title: str, subtitle: str, entries: list[tuple[str, str]]) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle([x1, y1, x2, y2], radius=28, outline=BLACK, width=5, fill=WHITE)
    draw.rectangle([x1, y1, x2, y1+86], fill=LIGHT, outline=BLACK, width=4)
    title_font = font(52, True)
    while draw.textbbox((0, 0), title, font=title_font)[2] > (x2-x1-50) and title_font.size > 38:
        title_font = font(title_font.size - 2, True)
    center(draw, (x1+25, y1+8, x2-25, y1+58), title, title_font)
    center(draw, (x1+30, y1+55, x2-30, y1+84), subtitle, font(20))

    gap = 28
    col_w = (x2 - x1 - 60 - gap) // 2
    xs = [x1+30, x1+30+col_w+gap]
    ys = [y1+112, y1+112]
    name_font = font(24, True)
    body_font = font(22)
    for idx, (name, text) in enumerate(entries):
        col = idx % 2 if len(entries) > 6 else (0 if idx < (len(entries)+1)//2 else 1)
        tx = xs[col]
        lines = wrapped(draw, text, col_w - 24, body_font)
        block_h = 34 + 26*len(lines) + 18
        if ys[col] + block_h > y2 - 28 and col == 0:
            col = 1
            tx = xs[col]
        ty = ys[col]
        draw.rounded_rectangle([tx, ty, tx+col_w, ty+block_h], radius=12, outline=(150,150,150), width=2, fill=(252,252,252))
        draw.text((tx+12, ty+9), name, font=name_font, fill=BLACK)
        yy = ty + 40
        for line in lines[:4]:
            draw.text((tx+14, yy), line, font=body_font, fill=BLACK)
            yy += 26
        ys[col] = ty + block_h + 14


def make_reference_digest() -> Path:
    pages: list[Image.Image] = []
    batches = [DIGEST_GROUPS[0:3], DIGEST_GROUPS[3:6], DIGEST_GROUPS[6:8]]
    section_boxes_3 = [
        (M, 150, PAGE_W-M, 1040),
        (M, 1080, PAGE_W-M, 1970),
        (M, 2010, PAGE_W-M, PAGE_H-120),
    ]
    section_boxes_2 = [
        (M, 150, PAGE_W-M, 1260),
        (M, 1300, PAGE_W-M, 2410),
    ]
    for page_no, batch in enumerate(batches, 1):
        canvas = Image.new('RGB', (PAGE_W, PAGE_H), WHITE)
        draw = ImageDraw.Draw(canvas)
        center(draw, (0, 36, PAGE_W, 120), 'Portable Game Night • Grouped Reference Digest', F_TITLE)
        boxes = section_boxes_3 if len(batch) == 3 else section_boxes_2
        for group, box in zip(batch, boxes):
            title, subtitle, entries = group
            draw_digest_section(draw, box, title, subtitle, entries)
        if len(batch) == 2:
            # Use the final third of the last page for practical print guidance instead of dead white space.
            box = (M, 2450, PAGE_W-M, PAGE_H-120)
            draw.rounded_rectangle(box, radius=28, outline=BLACK, width=5, fill=LIGHT)
            center(draw, (box[0]+30, box[1]+20, box[2]-30, box[1]+82), 'Suggested Paper-Saver Print Plan', font(50, True))
            plan_lines = [
                '1) Start with the Digest Game Night kit for the smallest useful binder set.',
                '2) Print extra compact score sheets only for the games you expect to play often.',
                '3) Keep full-page PDFs available for low-vision players, teaching tables, or dense score sheets.',
                '4) Use the site pages for full rules; this digest is meant as a table reminder.',
            ]
            yy = box[1] + 115
            for line in plan_lines:
                draw.text((box[0]+55, yy), '•', font=F_SMALL_B, fill=BLACK)
                for wrapped_line in wrapped(draw, line, box[2]-box[0]-150, F_SMALL):
                    draw.text((box[0]+92, yy), wrapped_line, font=F_SMALL, fill=BLACK)
                    yy += 38
                yy += 10
        draw.text((M, PAGE_H-82), 'Paper Saver Digest - grouped quick reminders. Full rules, score sheets, and downloads are on the Portable Game Night site.', font=F_SMALL_B, fill=BLACK)
        pages.append(canvas)
    return save_multipage(pages, OUT / 'reference-digest-bundle.pdf')


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


def draw_bullets(draw: ImageDraw.ImageDraw, x: int, y: int, max_width: int, lines: list[str], fnt: ImageFont.FreeTypeFont = F_BODY) -> int:
    for line in lines:
        draw.text((x, y), '•', font=F_BODY_B, fill=BLACK)
        for wrapped_line in wrapped(draw, line, max_width - 60, fnt):
            draw.text((x + 50, y), wrapped_line, font=fnt, fill=BLACK)
            y += fnt.size + 14
        y += 18
    return y


def make_cover_page(out_dir: Path = OUT) -> Path:
    img = Image.new('RGB', (PAGE_W, PAGE_H), WHITE)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([M, 170, PAGE_W-M, PAGE_H-170], radius=46, outline=BLACK, width=9, fill=WHITE)
    center(d, (M+80, 400, PAGE_W-M-80, 560), 'Portable Game Night', font(150, True))
    center(d, (M+80, 575, PAGE_W-M-80, 690), 'Complete Binder Kit', font(92, True))
    center(d, (M+120, 760, PAGE_W-M-120, 850), 'Cards • Dice • Score Sheets • Reference Digests • Reusable Boards', F_H)
    d.line([M+220, 950, PAGE_W-M-220, 950], fill=BLACK, width=6)
    yy = 1080
    yy = draw_bullets(d, M+230, yy, PAGE_W-2*M-460, [
        'Built for a portable physical game kit with the website as the full rules source.',
        'Use standard playing cards, common dice, pencils, dry-erase sleeves, and tokens/candy/coins.',
        'Includes section dividers so this can be sent as one print job and loaded directly into a binder.',
        'No real-money betting required; use harmless markers and casual house limits.',
    ], F_BODY)
    center(d, (M+120, PAGE_H-620, PAGE_W-M-120, PAGE_H-520), 'Live site', F_H)
    center(d, (M+120, PAGE_H-515, PAGE_W-M-120, PAGE_H-440), 'https://inurcrosshair.github.io/portable-game-night/', F_BODY_B)
    center(d, (M+120, PAGE_H-330, PAGE_W-M-120, PAGE_H-260), 'Print, sleeve the reusable boards, and keep extra score sheets behind the master copies.', F_SMALL_B)
    return save_multipage([img], out_dir / '_binder_cover.pdf')


def make_start_here_page(out_dir: Path = OUT) -> Path:
    img = Image.new('RGB', (PAGE_W, PAGE_H), WHITE)
    d = ImageDraw.Draw(img)
    center(d, (M, 95, PAGE_W-M, 210), 'Start Here: How to Use This Binder', font(92, True))
    sections = [
        ('Best use', [
            'Use the binder as the no-Wi-Fi / table backup. The live website remains the complete rules library.',
            'Use the grouped digest and quick cards to pick games quickly; open the full site page when rules need more detail.',
        ]),
        ('Reusable pages', [
            'Put boards, tracks, and betting mats in clear sheet protectors.',
            'Use dry-erase markers, coins, candy, poker chips, or small tokens instead of writing directly on those pages.',
        ]),
        ('Score sheets', [
            'Keep the full-size score sheets as clean master copies.',
            'Use the compact 2-up score sheets as the first consumable stock, then reprint individual games that get used most.',
        ]),
        ('Printing notes', [
            'Print one-sided if you want easy section separation and sheet protectors.',
            'Print black-and-white/grayscale unless you want the cover and dividers to stand out more.',
            'The quick-reference card pages are meant to be cut apart; print those on cardstock if possible.',
        ]),
    ]
    y = 300
    for title, bullets in sections:
        d.rounded_rectangle([M, y, PAGE_W-M, y+92], radius=22, outline=BLACK, width=4, fill=LIGHT)
        d.text((M+45, y+22), title, font=F_H, fill=BLACK)
        y += 125
        y = draw_bullets(d, M+70, y, PAGE_W-2*M-140, bullets, F_BODY)
        y += 38
    return save_multipage([img], out_dir / '_binder_start_here.pdf')


def make_toc_page(out_dir: Path = OUT) -> Path:
    img = Image.new('RGB', (PAGE_W, PAGE_H), WHITE)
    d = ImageDraw.Draw(img)
    center(d, (M, 95, PAGE_W-M, 210), 'Binder Sections', font(98, True))
    items = [
        ('1. Quick Reference Digest', 'Grouped reminders for similar card and dice games.'),
        ('2. Reusable Boards, Mats and Tracks', 'Full-size play surfaces for sheet protectors, dry erase, and tokens.'),
        ('3. Full-Size Score Sheet Masters', 'Clean one-page originals for every write-on score sheet.'),
        ('4. Compact Score Sheet Stock', 'Two copies of each compact 2-up score sheet for actual play use.'),
        ('5. Cut-Apart Quick Cards', 'Two sets of 6-up quick-reference cards for table use.'),
        ('6. Half-Sheet Reference Backup', 'All individual references two per page for broader no-phone backup.'),
    ]
    y = 360
    for heading, desc in items:
        d.rounded_rectangle([M+120, y, PAGE_W-M-120, y+185], radius=24, outline=BLACK, width=4, fill=WHITE)
        d.text((M+170, y+28), heading, font=F_H, fill=BLACK)
        d.text((M+170, y+100), desc, font=F_BODY, fill=BLACK)
        y += 230
    d.text((M+120, PAGE_H-210), 'Suggested binder setup: divider tabs for each section, sheet protectors for reusable boards, and a pocket for cut cards and loose score sheets.', font=F_SMALL_B, fill=BLACK)
    return save_multipage([img], out_dir / '_binder_toc.pdf')


def make_divider_page(title: str, subtitle: str, bullets: list[str], number: int, out_dir: Path = OUT) -> Path:
    img = Image.new('RGB', (PAGE_W, PAGE_H), WHITE)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, PAGE_W, 360], fill=DARK)
    center(d, (M, 70, PAGE_W-M, 215), f'Section {number}', font(96, True), WHITE)
    center(d, (M, 205, PAGE_W-M, 330), title, font(88, True), WHITE)
    center(d, (M+100, 520, PAGE_W-M-100, 640), subtitle, F_H)
    d.rounded_rectangle([M+170, 840, PAGE_W-M-170, 2100], radius=36, outline=BLACK, width=6, fill=LIGHT)
    draw_bullets(d, M+260, 960, PAGE_W-2*M-520, bullets, F_BODY)
    center(d, (M+100, PAGE_H-500, PAGE_W-M-100, PAGE_H-420), 'Portable Game Night Binder Kit', F_H)
    center(d, (M+100, PAGE_H-405, PAGE_W-M-100, PAGE_H-340), 'Use the live site for full rules and updated downloads.', F_BODY)
    safe = ''.join(ch.lower() if ch.isalnum() else '-' for ch in title).strip('-')
    return save_multipage([img], out_dir / f'_binder_divider_{number}_{safe}.pdf')


def make_complete_binder_kit(reference_digest: Path, compact_scores: Path, quick_cards: Path, reference_half: Path) -> Path:
    reusable_bundle = PRINTABLES / 'bundles' / 'reusable-boards-mats-and-tracks-bundle.pdf'
    score_masters = PRINTABLES / 'bundles' / 'write-on-score-sheets-bundle.pdf'

    with TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        cover = make_cover_page(tmp_dir)
        start = make_start_here_page(tmp_dir)
        toc = make_toc_page(tmp_dir)
        sections: list[Path] = [cover, start, toc]
        sections += [
            make_divider_page('Quick Reference Digest', 'A fast grouped overview for picking and teaching games.', [
                'Use this section first when choosing a game.',
                'Each page groups similar games together so you can compare options quickly.',
                'Open the website when you need complete rules or game-specific details.',
            ], 1, tmp_dir),
            reference_digest,
            make_divider_page('Reusable Boards, Mats and Tracks', 'Full-size table aids meant for sheet protectors and tokens.', [
                'Put these pages in clear sheet protectors when possible.',
                'Use dry-erase markers, coins, candy, chips, or tokens to mark progress.',
                'Print an extra copy later if you expect multiple tables.',
            ], 2, tmp_dir),
            reusable_bundle,
            make_divider_page('Full-Size Score Sheet Masters', 'Clean master copies for every write-on sheet.', [
                'Use these as archive/master versions and teaching copies.',
                'Photocopy or reprint individual sheets when a game becomes popular.',
                'Keep compact score sheets behind this section for everyday use.',
            ], 3, tmp_dir),
            score_masters,
            make_divider_page('Compact Score Sheet Stock', 'Paper-saving two-up score sheets for actual game-night use.', [
                'This section includes two complete copies of the compact score-sheet bundle.',
                'Cut sheets in half when useful, or leave them full page for easier handling.',
                'Reprint only the games that run out fastest.',
            ], 4, tmp_dir),
            compact_scores,
            compact_scores,
            make_divider_page('Cut-Apart Quick Cards', 'Small table cards for common quick games.', [
                'Two complete sets are included.',
                'Print on cardstock if possible, then cut apart and keep in a pouch or binder pocket.',
                'Use these for fast reminders; use the site or digest for fuller context.',
            ], 5, tmp_dir),
            quick_cards,
            quick_cards,
            make_divider_page('Half-Sheet Reference Backup', 'Individual reference sheets compressed two per page.', [
                'This section is broader than the digest and keeps every individual reference available.',
                'Use it when you want a specific game reference without relying on a phone.',
                'The digest is faster; this section is more complete.',
            ], 6, tmp_dir),
            reference_half,
        ]
        return merge_pdfs('complete-binder-kit.pdf', sections)


def main() -> None:
    reference_half = make_half_sheet_bundle(REFERENCE_PRINTABLES, 'reference-half-sheets-bundle.pdf', 'Reference half sheets')
    compact_score_files = [OUT.parent / 'compact' / f'{Path(name).stem}-2up.pdf' for name in COMPACT_SCORE_SOURCES]
    for path in compact_score_files:
        if not path.exists():
            raise FileNotFoundError(f'Missing compact score sheet: {path}')
    compact_scores = merge_pdfs('compact-score-sheets-bundle.pdf', compact_score_files)
    quick_cards = make_quick_cards()
    reference_digest = make_reference_digest()
    reusable_paths = [PRINTABLES / name for name in REUSABLE_PRINTABLES]
    lean = merge_pdfs('lean-game-night-kit.pdf', reusable_paths + [quick_cards] + [compact_scores])
    digest_kit = merge_pdfs('digest-game-night-kit.pdf', reusable_paths + [reference_digest] + [compact_scores])
    full_saver = merge_pdfs('full-paper-saver-kit.pdf', reusable_paths + [reference_half] + [compact_scores])
    binder = make_complete_binder_kit(reference_digest, compact_scores, quick_cards, reference_half)

    outputs = [reference_half, reference_digest, compact_scores, quick_cards, lean, digest_kit, full_saver, binder]
    for path in outputs:
        print(f'{path.relative_to(ROOT)}: {len(PdfReader(str(path)).pages)} pages')


if __name__ == '__main__':
    main()
