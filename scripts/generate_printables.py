#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from shutil import copyfile
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'printables'
OUT.mkdir(exist_ok=True)
SRC_FARKLE = Path('/mnt/c/Users/code3/OneDrive/Desktop/Atlas_Project_Records/Card-Dice Games/_source_documents/farkle-official-score-sheet.pdf')

W, H = 2550, 3300  # 8.5x11 at 300 DPI
M = 110
DARK = (82, 82, 82)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ALT = (214, 214, 214)
LIGHT = (245, 245, 245)

FONT_BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
FONT_REG = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

def font(size, bold=False):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, size)

F_TITLE = font(170, True)
F_H1 = font(72, True)
F_H2 = font(56, True)
F_BODY = font(48, False)
F_BODY_B = font(48, True)
F_SMALL = font(38, False)
F_SMALL_B = font(38, True)
F_TINY = font(30, False)


def draw_die(draw, x, y, size, value=5, width=8):
    r = size // 7
    draw.rounded_rectangle([x, y, x+size, y+size], radius=size//8, outline=BLACK, width=width, fill=WHITE)
    pts = {
        1: [(0.5,0.5)],
        2: [(0.28,0.28),(0.72,0.72)],
        3: [(0.28,0.28),(0.5,0.5),(0.72,0.72)],
        4: [(0.28,0.28),(0.72,0.28),(0.28,0.72),(0.72,0.72)],
        5: [(0.28,0.28),(0.72,0.28),(0.5,0.5),(0.28,0.72),(0.72,0.72)],
        6: [(0.28,0.24),(0.72,0.24),(0.28,0.5),(0.72,0.5),(0.28,0.76),(0.72,0.76)],
    }[value]
    for px, py in pts:
        cx, cy = x + int(px*size), y + int(py*size)
        draw.ellipse([cx-r, cy-r, cx+r, cy+r], fill=BLACK)


def centered(draw, box, text, fnt, fill=BLACK):
    x1,y1,x2,y2 = box
    bb = draw.textbbox((0,0), text, font=fnt)
    tw, th = bb[2]-bb[0], bb[3]-bb[1]
    draw.text((x1+(x2-x1-tw)/2, y1+(y2-y1-th)/2-4), text, font=fnt, fill=fill)


def header(draw, title, subtitle=None):
    draw_die(draw, M+390, 50, 120, 5)
    draw_die(draw, M+510, 105, 120, 2)
    draw_die(draw, W-M-630, 105, 120, 5)
    draw_die(draw, W-M-510, 50, 120, 6)
    centered(draw, (M, 55, W-M, 220), title, F_TITLE)
    if subtitle:
        centered(draw, (M, 210, W-M, 275), subtitle, F_SMALL)


def draw_table(draw, x, y, col_widths, row_h, headers, rows, shaded=True):
    total_w = sum(col_widths)
    # header
    draw.rectangle([x, y, x+total_w, y+row_h], fill=DARK, outline=BLACK, width=5)
    cx=x
    for i,h in enumerate(headers):
        draw.rectangle([cx, y, cx+col_widths[i], y+row_h], outline=BLACK, width=5)
        centered(draw, (cx, y, cx+col_widths[i], y+row_h), h, F_H2 if len(h)<12 else F_SMALL_B, WHITE)
        cx += col_widths[i]
    # rows
    for r in range(rows):
        yy = y + row_h*(r+1)
        fill = ALT if shaded and r % 2 == 1 else WHITE
        draw.rectangle([x, yy, x+total_w, yy+row_h], fill=fill, outline=BLACK, width=5)
        cx=x
        for c,wid in enumerate(col_widths):
            draw.rectangle([cx, yy, cx+wid, yy+row_h], outline=BLACK, width=5)
            cx += wid
    return y + row_h*(rows+1)


def label_rows(draw, x, y, row_h, labels, fnt=F_H2):
    for i, lab in enumerate(labels):
        centered(draw, (x, y+row_h*(i+1), x+260, y+row_h*(i+2)), str(lab), fnt)


def notes(draw, x, y, lines, size='small'):
    f = F_SMALL if size == 'small' else F_BODY
    for line in lines:
        draw.text((x, y), line, font=f, fill=BLACK)
        y += f.size + 22
    return y


def save_pdf(img, filename):
    path = OUT / filename
    img.convert('RGB').save(path, 'PDF', resolution=300.0)
    return path


def base(title, subtitle=None):
    img = Image.new('RGB', (W,H), WHITE)
    d = ImageDraw.Draw(img)
    header(d, title, subtitle)
    return img, d


def player_round_sheet(title, filename, subtitle, rounds=10, player_cols=4, bottom_lines=None):
    img,d=base(title, subtitle)
    y=360
    cols=[290] + [(W-2*M-290)//player_cols]*player_cols
    headers=['Round']+[f'Player {i}' for i in range(1,player_cols+1)]
    end=draw_table(d, M, y, cols, 165, headers, rounds)
    label_rows(d, M, y, 165, list(range(1, rounds+1)))
    if bottom_lines:
        notes(d, M, end+70, bottom_lines)
    return save_pdf(img, filename)


def skunk():
    img,d=base('Skunk', 'S-K-U-N-K score sheet')
    y=380; rows=['S','K','U','N','K','TOTAL']
    cols=[260, 430,430,430,430]
    end=draw_table(d,M,y,cols,210,['Round','Player 1','Player 2','Player 3','Player 4'],len(rows))
    label_rows(d,M,y,210,rows)
    notes(d,M,end+70,['Rules: before each roll, stay in or sit out. One 1 ends the round for active players.','Double 1s: active players lose all game points. Highest total after K wins.'])
    return save_pdf(img,'skunk-score-sheet.pdf')


def three_or_more():
    img,d=base('Three or More','20 short • 50 normal • 100 long')
    y=360
    cols=[260,380,380,380,380,380]
    end=draw_table(d,M,y,cols,145,['Turn','P1','P2','P3','P4','P5'],15)
    label_rows(d,M,y,145,range(1,16),F_BODY_B)
    notes(d,M,end+55,['Scoring: 3 of a kind = 3 pts   |   4 of a kind = 6 pts   |   5 of a kind = 12 pts',
                       'If you roll one pair, keep the pair and reroll 3 dice OR reroll all 5 dice.'])
    return save_pdf(img,'three-or-more-score-sheet.pdf')


def crag():
    img,d=base('Crag','3-dice scorecard')
    y=340
    cats=['Ones','Twos','Threes','Fours','Fives','Sixes','Pair','3 of a Kind','Low Straight','High Straight','Thirteen','Crag','Chance','TOTAL']
    cols=[480,360,360,360,360,360]
    end=draw_table(d,M,y,cols,135,['Category','P1','P2','P3','P4','P5'],len(cats))
    label_rows(d,M,y,135,cats,F_SMALL_B)
    notes(d,M,end+45,['Low Straight 1-2-3 = 20   |   High Straight 4-5-6 = 20   |   Thirteen = 26',
                       'Crag = pair plus total of 13 = 50   |   Roll up to 3 times per turn.'])
    return save_pdf(img,'crag-scorecard.pdf')


def dice_golf():
    img,d=base('Dice Golf','9-hole scorecard')
    y=350
    cols=[220,300,300,300,300,300,300]
    end=draw_table(d,M,y,cols,135,['Hole','Par','P1','P2','P3','P4','P5'],10)
    label_rows(d,M,y,135,[1,2,3,4,5,6,7,8,9,'TOTAL'],F_BODY_B)
    # par column defaults
    for i in range(9): centered(d,(M+220,y+135*(i+1),M+520,y+135*(i+2)),'4',F_BODY_B)
    notes(d,M,end+45,['Scoring: 5-kind=1, 4-kind=2, Full House=3, Straight=4, 3-kind=5, Two Pair=6, Pair=7, None=8',
                       'Optional hazard: no pair and total 20+ adds +1 stroke. Lowest total wins.'])
    return save_pdf(img,'dice-golf-scorecard.pdf')


def simple_total(title, filename, subtitle, target_line):
    return player_round_sheet(title, filename, subtitle, 12, 4, [target_line, 'Use the blank boxes for running totals or round scores.'])


def chicago():
    img,d=base('Chicago','Targets 2 through 12')
    y=350; targets=list(range(2,13))+['TOTAL']
    cols=[260,390,390,390,390,390]
    end=draw_table(d,M,y,cols,145,['Target','P1','P2','P3','P4','P5'],len(targets))
    label_rows(d,M,y,145,targets,F_BODY_B)
    notes(d,M,end+50,['Each round, roll 2 dice once. If the total matches the target, score that target number.'])
    return save_pdf(img,'chicago-score-sheet.pdf')


def bunco():
    img,d=base('Bunco','6-round casual score sheet')
    y=350; rounds=[1,2,3,4,5,6,'TOTAL','BUNCOS']
    cols=[260,390,390,390,390,390]
    end=draw_table(d,M,y,cols,145,['Round','P1','P2','P3','P4','P5'],len(rounds))
    label_rows(d,M,y,145,rounds,F_BODY_B)
    notes(d,M,end+50,['Match the round number. One match=1, two matches=2, three matches=5, true Bunco=21.'])
    return save_pdf(img,'bunco-score-sheet.pdf')


def liars_ref():
    img,d=base("Liar's Dice",'Wild 1s quick reference')
    y=380
    notes(d,M,y,["Setup: 5 dice + cup per player. 1s are wild and count as any bid face.",
                 "Raise: increase quantity OR keep quantity and increase face. Do not bid directly on 1s.",
                 "Call liar: reveal all dice. If bid is met, caller loses. If not met, bidder loses.",
                 "Elimination: loser loses 1 die. Last player with dice wins.",
                 "Drinking variant: loser takes 1 drink instead of losing dice; everyone keeps 5 dice."], 'body')
    y=920
    draw_table(d,M,y,[520,520,520,520],140,['Bid','Can raise to','Wilds?','Loser'],6)
    notes(d,M,2050,['Safety note for drinking variant: small drinks, water/skips allowed, no pressure.'])
    return save_pdf(img,'liars-dice-reference.pdf')


def ceelo_ref():
    img,d=base('Cee-lo','4-5-6 ranking reference')
    y=380
    lines=['Goal: first player to win 5 rounds.',
           'Roll 3 dice. If unranked, reroll. Maximum 3 attempts, then bust.',
           'Ranking, high to low:',
           '1. 4-5-6 = automatic best result',
           '2. Triples: 6-6-6 down to 1-1-1',
           '3. Pair + odd die = point. Higher point wins.',
           '4. Bust = no ranked result after 3 attempts',
           '5. 1-2-3 = automatic worst result']
    notes(d,M,y,lines,'body')
    return save_pdf(img,'cee-lo-ranking-reference.pdf')


def sic_bo():
    img,d=base('Sic Bo','Simplified betting mat')
    y=350
    boxes=[('SMALL\n4-10\n1:1',M,y,760,740),('BIG\n11-17\n1:1',790,y,1470,740),('ODD\n1:1',1500,y,1980,740),('EVEN\n1:1',2010,y,W-M,740)]
    for text,x1,y1,x2,y2 in boxes:
        d.rounded_rectangle([x1,y1,x2,y2], radius=30, outline=BLACK, width=8, fill=LIGHT)
        centered(d,(x1,y1,x2,y2),text,F_H2)
    y=820
    draw_table(d,M,y,[360,360,360,360,360,360],140,['1','2','3','4','5','6'],2)
    for i in range(6):
        centered(d,(M+360*i,y+140,M+360*(i+1),y+280),'Specific\nnumber',F_SMALL_B)
    y=1220
    draw_table(d,M,y,[300]*7,140,['4','5','6','7','8','9','10'],1)
    draw_table(d,M,y+310,[300]*7,140,['11','12','13','14','15','16','17'],1)
    notes(d,M,1900,['Exact total pays 5:1. Any triple pays 10:1.',
                    'Specific number appears: once=1:1, twice=2:1, three times=3:1.',
                    'Big/Small exclude triples. Use fake chips only.'])
    return save_pdf(img,'sic-bo-betting-mat.pdf')


def shut_the_box_board():
    img,d=base('Shut the Box','Printable 1–12 board')
    y=500
    tile_w=(W-2*M)//12
    for i in range(12):
        x=M+i*tile_w
        fill=ALT if i%2 else WHITE
        d.rounded_rectangle([x+8,y,x+tile_w-8,y+360], radius=24, outline=BLACK, width=8, fill=fill)
        centered(d,(x+8,y,x+tile_w-8,y+260),str(i+1),font(92, True))
        d.line([x+38,y+285,x+tile_w-38,y+285], fill=BLACK, width=5)
        centered(d,(x+8,y+286,x+tile_w-8,y+350),'flip',F_TINY)
    notes(d,M,1050,['Use this as a paper/dry-erase board. Cross off or cover numbers as they are shut.',
                    'Common setup: use 1–9 for shorter games or 1–12 for the full board.'])
    return save_pdf(img,'shut-the-box-board.pdf')


def knucklebones_board():
    img,d=base('Knucklebones','Two-player 3x3 board')
    top=430
    grid=780; cell=grid//3
    for side,x0 in [('Player 1',M+180),('Player 2',W-M-180-grid)]:
        centered(d,(x0,top-110,x0+grid,top-20),side,F_H1)
        for r in range(3):
            for c in range(3):
                x=x0+c*cell; y=top+r*cell
                fill=ALT if (r+c)%2 else WHITE
                d.rectangle([x,y,x+cell,y+cell], fill=fill, outline=BLACK, width=8)
        centered(d,(x0,top+grid+20,x0+grid,top+grid+100),'Column totals',F_SMALL_B)
        for c in range(3):
            x=x0+c*cell
            d.rectangle([x,top+grid+110,x+cell,top+grid+230], outline=BLACK, width=6, fill=WHITE)
    notes(d,M,2300,['Place dice in your own 3x3 grid. Match values in a column to multiply that column score.',
                    'When you place a die, remove matching-value dice from your opponent’s same column.'])
    return save_pdf(img,'knucklebones-board.pdf')


def cant_stop_board():
    img,d=base("Can't Stop",'Number tracks 2 through 12')
    y=410
    nums=list(range(2,13))
    heights={2:3,3:5,4:7,5:9,6:11,7:13,8:11,9:9,10:7,11:5,12:3}
    col_w=(W-2*M)//len(nums)
    max_h=13; step=130
    for i,n in enumerate(nums):
        x=M+i*col_w
        centered(d,(x,y-90,x+col_w,y-20),str(n),F_H2)
        for j in range(heights[n]):
            yy=y+(max_h-j-1)*step
            fill=ALT if j%2 else WHITE
            d.rounded_rectangle([x+14,yy,x+col_w-14,yy+96], radius=20, outline=BLACK, width=5, fill=fill)
    notes(d,M,2350,['Use tokens/coins as climbers. Longer tracks in the middle reflect the classic odds curve.',
                    'On your turn, roll 4 dice, make two pairs, and advance those tracks; stop safely or risk losing progress.'])
    return save_pdf(img,'cant-stop-board.pdf')


def qwixx_sheet():
    img,d=base('Qwixx-Style','Roll-and-write sheet')
    y=430
    rows=[('RED','2 3 4 5 6 7 8 9 10 11 12'),('YELLOW','2 3 4 5 6 7 8 9 10 11 12'),('GREEN','12 11 10 9 8 7 6 5 4 3 2'),('BLUE','12 11 10 9 8 7 6 5 4 3 2')]
    for label,nums in rows:
        d.rectangle([M,y,W-M,y+95], fill=DARK, outline=BLACK, width=5)
        d.text((M+20,y+20), label, font=font(44, True), fill=WHITE)
        values=nums.split()
        start=M+330; box=(W-M-start)//12
        for i,v in enumerate(values):
            x=start+i*box
            d.rectangle([x,y,x+box,y+95], fill=WHITE if i<11 else ALT, outline=BLACK, width=4)
            centered(d,(x,y,x+box,y+95),v,F_SMALL_B)
        y += 180
    d.text((M, y+40), 'Penalties / misses', font=font(50, True), fill=BLACK)
    for i in range(4):
        x=M+520+i*180
        d.rectangle([x,y+25,x+120,y+145], outline=BLACK, width=6, fill=WHITE)
    notes(d,M,1750,['House-safe note: this is an original Qwixx-style practice/reference sheet, not an official commercial scorepad.',
                    'Cross out numbers left-to-right on red/yellow and right-to-left on green/blue. Locks are the far-right boxes.'])
    return save_pdf(img,'qwixx-style-roll-and-write-sheet.pdf')


def martinetti_track():
    img,d=base('Martinetti','Mountain / Matterhorn track')
    y=520
    seq=list(range(1,13))+list(range(11,0,-1))
    box_w=(W-2*M)//12
    for row in range(2):
        vals=seq[row*12:(row+1)*12]
        for i,v in enumerate(vals):
            x=M+i*box_w
            yy=y+row*360
            fill=ALT if (i+row)%2 else WHITE
            d.rounded_rectangle([x+8,yy,x+box_w-8,yy+170], radius=18, outline=BLACK, width=6, fill=fill)
            centered(d,(x+8,yy,x+box_w-8,yy+170),str(v),F_H2)
    notes(d,M,1450,['Race up from 1 to 12, then back down to 1. Mark your current space with a token or pencil.',
                    'Roll 3 dice. Use single dice or combinations to make the next needed number. First to finish wins.'])
    return save_pdf(img,'martinetti-mountain-matterhorn-track.pdf')


def main():
    if SRC_FARKLE.exists():
        copyfile(SRC_FARKLE, OUT/'farkle-score-sheet.pdf')
    paths=[]
    paths += [skunk(), three_or_more(), crag(), dice_golf(), chicago(), bunco(), liars_ref(), ceelo_ref(), sic_bo()]
    paths += [shut_the_box_board(), knucklebones_board(), cant_stop_board(), qwixx_sheet(), martinetti_track()]
    paths += [simple_total('Stuck in the Mud','stuck-in-the-mud-score-sheet.pdf','50 short • 100 normal • 200 long','2s and 5s are stuck. Score live dice until all dice are stuck.')]
    paths += [simple_total('Midnight','midnight-score-sheet.pdf','1 and 4 required','Score the four non-required dice. No 1 and 4 = 0 for the round.')]
    paths += [simple_total('Drop Dead','drop-dead-score-sheet.pdf','5-dice survival scoring','2s and 5s are dead. Score live dice until all dice are dead.')]
    paths += [simple_total('Sevens Out','sevens-out-score-sheet.pdf','Two-dice push your luck','Rolling a 7 ends the turn and loses unbanked points.')]
    print('Generated/copy printables:')
    for p in sorted(OUT.glob('*.pdf')):
        print(p.name, p.stat().st_size)

if __name__ == '__main__':
    main()
