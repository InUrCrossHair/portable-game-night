#!/usr/bin/env python3
from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
SOURCE = Path('/mnt/c/Users/code3/OneDrive/Desktop/Atlas_Project_Records/Card-Dice Games/dice_games.md')

from data.game_data import CARD_GAMES, GAMES
DIFFICULTY_ORDER = {
    'Very Easy': 0,
    'Easy': 1,
    'Moderate': 2,
    'Crunchy': 3,
}

TIME_ORDER = {
    'Under 5 min': 0,
    '5–10 min': 1,
    '5–15 min': 2,
    '10–20 min': 3,
    '15–30 min': 4,
    '20–40 min': 5,
    '20–45 min': 6,
    '30+ min': 7,
    'Variable': 8,
    'Flexible': 8,
}


def difficulty_sort_key(game: dict) -> tuple[int, int, str]:
    """Sort easiest games first, then roughly shortest-to-longest, then by name."""
    return (
        DIFFICULTY_ORDER.get(game['complexity'], 99),
        TIME_ORDER.get(game['time'], 99),
        game['name'].lower(),
    )


def sorted_games(games: list[dict] | None = None) -> list[dict]:
    return sorted(games or GAMES, key=difficulty_sort_key)


def clean_source_lines(text: str) -> str:
    # Handles both raw Markdown and read_file-style line-prefixed dumps if ever used.
    out = []
    for line in text.splitlines():
        if re.match(r'^\d+\|', line):
            out.append(line.split('|', 1)[1])
        else:
            out.append(line)
    return '\n'.join(out)


def extract_sections(md: str) -> dict[str, str]:
    md = clean_source_lines(md)
    matches = list(re.finditer(r'^##\s+(\d+)\.\s+(.+)$', md, flags=re.M))
    sections = {}
    for i, m in enumerate(matches):
        title = m.group(2).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else md.find('\n# Best Games by Situation', start)
        if end == -1:
            end = len(md)
        body = md[start:end].strip()
        # Match by generated slug where possible.
        slug = next((g['slug'] for g in GAMES if g['name'] == title), None)
        if not slug:
            normalized = title.lower().replace('’', '').replace("'", '')
            slug = re.sub(r'[^a-z0-9]+', '-', normalized).strip('-')
        sections[slug] = body
    return sections


def inline_md(s: str) -> str:
    s = html.escape(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    return s


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out = []
    i = 0
    in_ul = False
    in_ol = False
    in_pre = False
    para = []

    def close_para():
        nonlocal para
        if para:
            out.append('<p>' + inline_md(' '.join(para)) + '</p>')
            para = []

    def close_lists():
        nonlocal in_ul, in_ol
        if in_ul:
            out.append('</ul>')
            in_ul = False
        if in_ol:
            out.append('</ol>')
            in_ol = False

    while i < len(lines):
        line = lines[i].rstrip()
        stripped = line.strip()
        if stripped.startswith('```'):
            close_para(); close_lists()
            if not in_pre:
                out.append('<pre><code>')
                in_pre = True
            else:
                out.append('</code></pre>')
                in_pre = False
            i += 1
            continue
        if in_pre:
            out.append(html.escape(line))
            i += 1
            continue
        if not stripped or stripped == '---':
            close_para(); close_lists(); i += 1; continue
        if stripped.startswith('### '):
            close_para(); close_lists(); out.append(f'<h2>{inline_md(stripped[4:])}</h2>'); i += 1; continue
        if stripped.startswith('#### '):
            close_para(); close_lists(); out.append(f'<h3>{inline_md(stripped[5:])}</h3>'); i += 1; continue
        if stripped.startswith('- '):
            close_para()
            if in_ol:
                out.append('</ol>'); in_ol = False
            if not in_ul:
                out.append('<ul>'); in_ul = True
            out.append(f'<li>{inline_md(stripped[2:])}</li>')
            i += 1; continue
        m = re.match(r'^(\d+)\.\s+(.*)$', stripped)
        if m:
            close_para()
            if in_ul:
                out.append('</ul>'); in_ul = False
            if not in_ol:
                out.append('<ol>'); in_ol = True
            out.append(f'<li>{inline_md(m.group(2))}</li>')
            i += 1; continue
        close_lists()
        para.append(stripped.replace('  ', ' '))
        i += 1
    close_para(); close_lists()
    if in_pre:
        out.append('</code></pre>')
    return '\n'.join(out)


def strip_source_quick_facts(md: str) -> str:
    """Remove the old Markdown quick-fact field block; the page template owns that now."""
    lines = md.splitlines()
    while lines and lines[0].strip().startswith('**'):
        lines.pop(0)
    while lines and not lines[0].strip():
        lines.pop(0)
    return '\n'.join(lines)


def rel_prefix(depth: int) -> str:
    return '../' * depth


def layout(title: str, body: str, depth: int = 0, description: str = 'Portable dice and card game rules.') -> str:
    prefix = rel_prefix(depth)
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{html.escape(description)}">
  <title>{html.escape(title)} | Portable Game Night</title>
  <link rel="stylesheet" href="{prefix}styles.css">
</head>
<body>
  <main class="page">
    {body}
  </main>
</body>
</html>
'''


PRINTABLE_LINKS = {
    'farkle': [('Farkle score sheet', 'farkle-score-sheet.pdf')],
    'pair-pressure': [('Pair Pressure board / score sheet', 'pair-pressure-board-score-sheet.pdf')],
    'liars-dice': [('Liar’s Dice quick reference', 'liars-dice-reference.pdf')],
    'ship-captain-and-crew': [('Ship, Captain, and Crew quick reference', 'ship-captain-and-crew-reference.pdf')],
    'pig': [('Pig quick reference', 'pig-reference.pdf')],
    'going-to-boston': [('Going to Boston quick reference', 'going-to-boston-reference.pdf')],
    'yahtzee-yacht': [('Yahtzee / Yacht score sheet', 'yahtzee-yacht-score-sheet.pdf')],
    'mia': [('Mia quick reference', 'mia-reference.pdf')],
    'beetle': [('Beetle drawing sheet', 'beetle-drawing-sheet.pdf')],
    'tenzi': [('Tenzi quick reference', 'tenzi-reference.pdf')],
    'bunco': [('Bunco score sheet', 'bunco-score-sheet.pdf')],
    'craps': [('Craps Pass Line reference', 'craps-pass-line-reference.pdf')],
    'knucklebones': [('Knucklebones board', 'knucklebones-board.pdf')],
    'cant-stop': [('Can’t Stop board', 'cant-stop-board.pdf')],
    'shut-the-box': [('Shut the Box board', 'shut-the-box-board.pdf')],
    'qwixx-style-roll-and-write': [('Qwixx-style roll-and-write sheet', 'qwixx-style-roll-and-write-sheet.pdf')],
    'martinetti-mountain-matterhorn': [('Martinetti / Mountain / Matterhorn track', 'martinetti-mountain-matterhorn-track.pdf')],
    'chicago': [('Chicago score sheet', 'chicago-score-sheet.pdf')],
    'threes-thirty': [('Threes / Thirty quick reference', 'threes-thirty-reference.pdf')],
    'drop-dead': [('Drop Dead score sheet', 'drop-dead-score-sheet.pdf')],
    'poker-dice': [('Poker Dice hand ranking reference', 'poker-dice-ranking-reference.pdf')],
    'sevens-out': [('Sevens Out score sheet', 'sevens-out-score-sheet.pdf')],
    'beat-that': [('Beat That quick reference', 'beat-that-reference.pdf')],
    'skunk': [('Skunk score sheet', 'skunk-score-sheet.pdf')],
    'midnight': [('Midnight score sheet', 'midnight-score-sheet.pdf')],
    'stuck-in-the-mud': [('Stuck in the Mud score sheet', 'stuck-in-the-mud-score-sheet.pdf')],
    'three-or-more': [('Three or More score sheet', 'three-or-more-score-sheet.pdf')],
    'crag': [('Crag scorecard', 'crag-scorecard.pdf')],
    'aces-in-the-pot': [('Aces in the Pot quick reference', 'aces-in-the-pot-reference.pdf')],
    'dice-golf': [('Dice Golf scorecard', 'dice-golf-scorecard.pdf')],
    'cee-lo-456': [('Cee-lo ranking reference', 'cee-lo-ranking-reference.pdf')],
    'sic-bo': [('Sic Bo betting mat', 'sic-bo-betting-mat.pdf')],
    'left-center-right': [('Left Center Right quick reference', 'left-center-right-reference.pdf')],
    'help-your-neighbor': [('Help Your Neighbor quick reference', 'help-your-neighbor-reference.pdf')],
    'crazy-eights': [('Crazy Eights quick reference', 'crazy-eights-reference.pdf')],
    'spoons': [('Spoons quick reference', 'spoons-reference.pdf')],
    'speed': [('Speed setup reference', 'speed-reference.pdf')],
    'spit': [('Spit setup reference', 'spit-reference.pdf')],
    'shithead-palace-karma': [('Shithead variant worksheet', 'shithead-variant-worksheet.pdf')],
    'bs-cheat': [('BS / Cheat quick reference', 'bs-cheat-reference.pdf')],
    'president': [('President quick reference', 'president-reference.pdf')],
    'golf-card-game': [('Golf score sheet', 'golf-card-game-score-sheet.pdf')],
    'rummy': [('Rummy score sheet', 'rummy-score-sheet.pdf')],
    'gin-rummy': [('Gin Rummy score sheet', 'gin-rummy-score-sheet.pdf')],
    'canasta': [('Canasta score sheet', 'canasta-score-sheet.pdf')],
    'kemps': [('Kemps quick reference', 'kemps-reference.pdf')],
    'hearts': [('Hearts score sheet', 'hearts-score-sheet.pdf')],
    'spades': [('Spades score sheet', 'spades-score-sheet.pdf')],
    'egyptian-rat-screw': [('Egyptian Rat Screw quick reference', 'egyptian-rat-screw-reference.pdf')],
    'spider-solitaire': [('Spider Solitaire setup reference', 'spider-solitaire-reference.pdf')],
    'twenty-one-dice-blackjack': [('Twenty-One / Dice Blackjack quick reference', 'twenty-one-dice-blackjack-reference.pdf')],
    'mexico': [('Mexico quick reference', 'mexico-reference.pdf')],
    'bar-dice': [('Bar Dice ranking reference', 'bar-dice-ranking-reference.pdf')],
    'cribbage': [('Cribbage score sheet', 'cribbage-score-sheet.pdf')],
    'casino-cassino': [('Casino / Cassino score sheet', 'casino-cassino-score-sheet.pdf')],
    'durak': [('Durak quick reference', 'durak-reference.pdf')],
    'oh-hell-oh-pshaw': [('Oh Hell score sheet', 'oh-hell-score-sheet.pdf')],
    'euchre': [('Euchre score sheet', 'euchre-score-sheet.pdf')],
    'thirty-one-scat-blitz': [('Thirty-One quick reference', 'thirty-one-reference.pdf')],
    'kings-in-the-corner': [('Kings in the Corner quick reference', 'kings-in-the-corner-reference.pdf')],
    'chase-the-ace': [('Chase the Ace quick reference', 'chase-the-ace-reference.pdf')],
    'five-card-draw-poker': [('Poker hand ranking / betting reference', 'poker-hand-ranking-reference.pdf')],
    'texas-holdem': [('Poker hand ranking / betting reference', 'poker-hand-ranking-reference.pdf')],
    'indian-poker-blind-mans-bluff': [('Indian Poker quick reference', 'indian-poker-reference.pdf')],
    'klondike-solitaire': [('Klondike Solitaire setup reference', 'klondike-solitaire-reference.pdf')],
    'freecell': [('FreeCell setup reference', 'freecell-reference.pdf')],
    'pyramid-solitaire': [('Pyramid Solitaire quick reference', 'pyramid-solitaire-reference.pdf')],
    'accordion-solitaire': [('Accordion Solitaire quick reference', 'accordion-solitaire-reference.pdf')],
    'clock-solitaire': [('Clock Solitaire setup reference', 'clock-solitaire-reference.pdf')],
    'golf-solitaire': [('Golf Solitaire quick reference', 'golf-solitaire-reference.pdf')],
    'canfield-solitaire': [('Canfield Solitaire setup reference', 'canfield-solitaire-reference.pdf')],
    'bowling-solitaire': [('Bowling Solitaire score sheet', 'bowling-solitaire-score-sheet.pdf')],
    'solo-farkle-challenge': [('Solo Farkle challenge sheet', 'solo-farkle-challenge-sheet.pdf')],
    'pair-pressure-solo-challenge': [('Pair Pressure board / score sheet', 'pair-pressure-board-score-sheet.pdf')],
    'dice-solitaire-patience-dice': [('Dice Solitaire score sheet', 'dice-solitaire-score-sheet.pdf')],
    'bowling-dice': [('Bowling Dice score sheet', 'bowling-dice-score-sheet.pdf')],
    'cho-han': [('Cho-Han quick reference', 'cho-han-reference.pdf')],
    'chuck-a-luck': [('Chuck-a-Luck betting mat', 'chuck-a-luck-betting-mat.pdf')],
    'knock-out-dice': [('Knock Out Dice score sheet', 'knock-out-dice-score-sheet.pdf')],
    'dice-baseball': [('Dice Baseball score sheet', 'dice-baseball-score-sheet.pdf')],
    'horse-race-dice': [('Horse Race Dice track', 'horse-race-dice-track.pdf')],
    'mao': [('Mao starter reference', 'mao-starter-reference.pdf')],
    'nerts-pounce': [('Nerts score sheet', 'nerts-score-sheet.pdf')],
    'slapjack': [('Slapjack quick reference', 'slapjack-reference.pdf')],
    'ninety-nine-card-game': [('Ninety-Nine quick reference', 'ninety-nine-reference.pdf')],
    'in-between-acey-deucey': [('In-Between quick reference', 'in-between-reference.pdf')],
    'knockout-whist': [('Knockout Whist quick reference', 'knockout-whist-reference.pdf')],

}


def display_tags(g: dict) -> list[str]:
    tags = list(g['tags'])
    if g['slug'] in PRINTABLE_LINKS and 'Printable Available' not in tags:
        insert_at = min(3, len(tags))
        tags.insert(insert_at, 'Printable Available')
    return tags


def printable_items(g: dict, depth: int) -> str:
    prefix = rel_prefix(depth)
    links = PRINTABLE_LINKS.get(g['slug'], [])
    if links:
        return ''.join(
            f'<li><a class="download-link" href="{prefix}printables/{filename}">Download {html.escape(label)}</a></li>'
            for label, filename in links
        )
    return '<li>No printable needed or currently planned.</li>'


def printable_preview_section(g: dict, depth: int) -> str:
    """Embed web-friendly preview images of any printable aids linked to this game."""
    links = PRINTABLE_LINKS.get(g['slug'], [])
    if not links:
        return ''
    prefix = rel_prefix(depth)
    cards = []
    for label, filename in links:
        preview_name = Path(filename).with_suffix('.webp').name
        preview_path = ROOT / 'printables' / 'previews' / preview_name
        if not preview_path.exists():
            continue
        safe_label = html.escape(label)
        cards.append(f'''<figure class="printable-preview-card">
      <a href="{prefix}printables/{filename}">
        <img src="{prefix}printables/previews/{preview_name}" alt="{safe_label} preview" loading="lazy">
      </a>
      <figcaption><a class="download-link" href="{prefix}printables/{filename}">Open printable PDF</a></figcaption>
    </figure>''')
    if not cards:
        return ''
    return f'''<section class="panel printable-preview-section">
    <h2>Visual play aid</h2>
    <p class="preview-note">Use this on a phone during play so everyone can see the score chart, board, or reference without passing paper around. Keep 1–2 printed copies as a no-Wi-Fi backup.</p>
    <div class="printable-preview-grid">
    {''.join(cards)}
    </div>
  </section>
'''


def tag_list(tags: list[str]) -> str:
    return '<div class="tags">' + ''.join(f'<span class="tag">{html.escape(t)}</span>' for t in tags) + '</div>'


def game_card(g: dict, depth: int = 0) -> str:
    prefix = rel_prefix(depth)
    top_tags = display_tags(g)[:5]
    return f'''<article class="game-card">
  <div class="card-topline"><span>{html.escape(g['time'])}</span><span>{html.escape(g['complexity'])}</span></div>
  <h2><a href="{prefix}dice/{g['slug']}/">{html.escape(g['name'])}</a></h2>
  <p>{html.escape(g['vibe'])}</p>
  <dl class="quick-dl"><div><dt>Players</dt><dd>{html.escape(g['players'])}</dd></div><div><dt>Dice</dt><dd>{html.escape(g['dice'])}</dd></div></dl>
  {tag_list(top_tags)}
  <p class="status"><strong>Status:</strong> {html.escape(g['status'])}</p>
</article>'''


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')


def build_home() -> None:
    body = '''<header class="hero">
  <p class="eyebrow">Travel-ready card and dice rules</p>
  <h1>Portable Game Night</h1>
  <p>A quick reference for dice games, card games, player-count picks, printable table aids, and a grab-and-go game kit.</p>
</header>

<section class="button-grid" aria-label="Main navigation">
  <a class="nav-card" href="dice/">Dice Games</a>
  <a class="nav-card" href="cards/">Card Games</a>
  <a class="nav-card" href="players/1-player/">1 Player</a>
  <a class="nav-card" href="players/2-players/">2 Players</a>
  <a class="nav-card" href="players/3-plus/">3+ Players</a>
</section>

<section class="panel">
  <h2>Start here</h2>
  <p>The dice section has structured game cards and individual rule pages. The card section now follows the same template, including deck counts and optional extra-deck notes.</p>
  <div class="mini-link-row">
    <a href="dice/">Browse dice games</a>
    <a href="cards/">Browse card games</a>
    <a href="players/2-players/">Find 2-player games</a>
    <a href="players/3-plus/">Find group games</a>
    <a href="printables/">Download printables</a>
  </div>
</section>

<section class="panel two-column">
  <div>
    <h2>Grab-and-go kit</h2>
    <ul>
      <li>6 standard dice</li>
      <li>1 standard 52-card deck</li>
      <li>Optional second 52-card deck for larger card games and Spider Solitaire</li>
      <li>Pencil plus printed score sheets or scrap paper</li>
      <li>Small tokens, candy, coins, or chips for betting/token games</li>
    </ul>
  </div>
  <div>
    <h2>Collection boundaries</h2>
    <p>The current card library focuses on games that work with ordinary playing cards. Specialty-deck games like Uno, Phase 10, or Skip-Bo can wait. Poker variants still fit the portable-kit idea because any small items can stand in as chips.</p>
  </div>
</section>'''
    write(ROOT / 'index.html', layout('Home', body, 0, 'Portable dice and card game rules for travel and game nights.'))


def build_dice_index() -> None:
    games = sorted_games()
    cards = '\n'.join(game_card(g, depth=1) for g in games)
    body = f'''<p class="breadcrumb"><a href="../">← Home</a></p>
<header class="hero compact-hero">
  <p class="eyebrow">Normal six-sided dice</p>
  <h1>Dice Games</h1>
  <p>Browse dice games by player count, components, complexity, and whether they still need a printable or locked house-rule version. Games are ordered easiest to hardest.</p>
</header>

<section class="panel stat-panel">
  <h2>Dice game library status</h2>
  <ul class="status-list">
    <li><strong>{len(GAMES)}</strong> dice games listed</li>
    <li><strong>{sum('house-rule' in g['status'].lower() for g in GAMES)}</strong> marked for house-rule cleanup</li>
    <li><strong>{sum(bool(g['printables']) for g in GAMES)}</strong> have planned printables or reference sheets</li>
  </ul>
</section>

<section class="game-grid" aria-label="Dice game list">
{cards}
</section>'''
    write(ROOT / 'dice/index.html', layout('Dice Games', body, 1, 'Dice game rules using normal six-sided dice.'))


def build_game_pages(sections: dict[str, str]) -> None:
    for g in GAMES:
        rules = strip_source_quick_facts(sections.get(g['slug'], ''))
        rules_html = g.get('rules_html') or (md_to_html(rules) if rules else '<p>Rules content still needs to be imported.</p>')
        printable_downloads = printable_items(g, depth=2)
        printable_previews = printable_preview_section(g, depth=2)
        needs_items = ''.join(f'<li>{html.escape(n)}</li>' for n in g['needs'])
        body = f'''<p class="breadcrumb"><a href="../../">← Home</a> / <a href="../">Dice Games</a></p>
<article class="game-page">
  <header class="hero compact-hero game-hero">
    <p class="eyebrow">Dice game</p>
    <h1>{html.escape(g['name'])}</h1>
    <p>{html.escape(g['vibe'])}</p>
    {tag_list(display_tags(g))}
  </header>

  <section class="quick-facts panel">
    <h2>Quick facts</h2>
    <dl class="facts-grid">
      <div><dt>Players</dt><dd>{html.escape(g['players'])}</dd></div>
      <div><dt>Dice needed</dt><dd>{html.escape(g['dice'])}</dd></div>
      <div><dt>Typical length</dt><dd>{html.escape(g['time'])}</dd></div>
      <div><dt>Complexity</dt><dd>{html.escape(g['complexity'])}</dd></div>
      <div><dt>Status</dt><dd>{html.escape(g['status'])}</dd></div>
    </dl>
  </section>

  <section class="panel two-column">
    <div>
      <h2>Kit needed</h2>
      <ul>{needs_items}</ul>
    </div>
    <div>
      <h2>Printable downloads</h2>
      <ul>{printable_downloads}</ul>
    </div>
  </section>

  {printable_previews}

  <section class="rules panel">
    <h2>Rules</h2>
    {rules_html}
  </section>
</article>'''
        write(ROOT / f'dice/{g["slug"]}/index.html', layout(g['name'], body, 2, f'Rules and quick reference for {g["name"]}.'))



def sorted_card_games(games: list[dict] | None = None) -> list[dict]:
    """Sort card games by deliberate index order, with Rummy/Gin/Canasta kept together."""
    return sorted(games or CARD_GAMES, key=lambda g: (g.get('order', 999), g['name'].lower()))


def card_game_card(g: dict, depth: int = 0) -> str:
    prefix = rel_prefix(depth)
    top_tags = display_tags(g)[:5]
    return f'''<article class="game-card">
  <div class="card-topline"><span>{html.escape(g['time'])}</span><span>{html.escape(g['complexity'])}</span></div>
  <h2><a href="{prefix}cards/{g['slug']}/">{html.escape(g['name'])}</a></h2>
  <p>{html.escape(g['vibe'])}</p>
  <dl class="quick-dl"><div><dt>Players</dt><dd>{html.escape(g['players'])}</dd></div><div><dt>Decks</dt><dd>{html.escape(g['decks'])}</dd></div></dl>
  {tag_list(top_tags)}
  <p class="status"><strong>Optional deck:</strong> {html.escape(g['optional_deck'])}</p>
</article>'''


def card_deck_bucket(g: dict) -> str:
    decks = g['decks'].lower()
    if decks.startswith('1'):
        return '1 Deck'
    if decks.startswith('2'):
        return '2 Decks'
    return '3+ Decks'


def deck_filter_section(label: str, games: list[dict], depth: int = 1) -> str:
    cards = '\n'.join(card_game_card(g, depth=depth) for g in games)
    slug = label.lower().replace('+', 'plus').replace(' ', '-')
    return f'''<section id="{slug}">
  <h2>{html.escape(label)}</h2>
  <div class="game-grid" aria-label="{html.escape(label)} card games">
{cards}
  </div>
</section>'''


def build_cards_index() -> None:
    games = sorted_card_games()
    cards = '\n'.join(card_game_card(g, depth=1) for g in games)
    optional_count = sum(g['optional_deck'] != 'No' and not g['optional_deck'].startswith('No;') for g in CARD_GAMES)
    one_deck_games = [g for g in games if card_deck_bucket(g) == '1 Deck']
    two_deck_games = [g for g in games if card_deck_bucket(g) == '2 Decks']
    three_plus_deck_games = [g for g in games if card_deck_bucket(g) == '3+ Decks']
    deck_sections = '\n'.join([
        deck_filter_section('1 Deck', one_deck_games),
        deck_filter_section('2 Decks', two_deck_games),
        deck_filter_section('3+ Decks', three_plus_deck_games),
    ])
    body = f'''<p class="breadcrumb"><a href="../">← Home</a></p>
<header class="hero compact-hero">
  <p class="eyebrow">Standard deck card games</p>
  <h1>Card Games</h1>
  <p>Browse card games by player count, deck count, complexity, and table style. This section is intentionally focused on ordinary playing cards instead of specialty decks.</p>
</header>

<section class="panel stat-panel">
  <h2>Card game library status</h2>
  <ul class="status-list">
    <li><strong>{len(CARD_GAMES)}</strong> card games listed</li>
    <li><strong>{len(one_deck_games)}</strong> use 1 deck</li>
    <li><strong>{len(two_deck_games)}</strong> use 2 decks</li>
    <li><strong>{len(three_plus_deck_games)}</strong> use 3+ decks</li>
    <li><strong>{optional_count}</strong> can benefit from an optional additional deck</li>
  </ul>
  <div class="mini-link-row">
    <a href="#1-deck">1 deck</a>
    <a href="#2-decks">2 decks</a>
    <a href="#3plus-decks">3+ decks</a>
  </div>
</section>

<section class="panel two-column">
  <div>
    <h2>Index notes</h2>
    <p>Rummy, Gin Rummy, and Canasta are grouped together because they share the same meld-building family. Deck counts are shown on every card so it is easy to pack the right kit before leaving the house.</p>
  </div>
  <div>
    <h2>Future additions</h2>
    <p>Hold specialty-deck games for later. Poker variants are a good future category because they still only need a standard deck, and betting can use candy, coins, chips, or any harmless table tokens.</p>
  </div>
</section>

<section>
  <h2>All card games</h2>
  <div class="game-grid" aria-label="Card game list">
{cards}
  </div>
</section>

{deck_sections}'''
    write(ROOT / 'cards/index.html', layout('Card Games', body, 1, 'Card game rules for Portable Game Night.'))


def build_card_game_pages() -> None:
    for g in CARD_GAMES:
        needs_items = ''.join(f'<li>{html.escape(n)}</li>' for n in g['needs'])
        printable_previews = printable_preview_section(g, depth=2)
        body = f'''<p class="breadcrumb"><a href="../../">← Home</a> / <a href="../">Card Games</a></p>
<article class="game-page">
  <header class="hero compact-hero game-hero">
    <p class="eyebrow">Card game</p>
    <h1>{html.escape(g['name'])}</h1>
    <p>{html.escape(g['vibe'])}</p>
    {tag_list(display_tags(g))}
  </header>

  <section class="quick-facts panel">
    <h2>Quick facts</h2>
    <dl class="facts-grid">
      <div><dt>Players</dt><dd>{html.escape(g['players'])}</dd></div>
      <div><dt>Decks needed</dt><dd>{html.escape(g['decks'])}</dd></div>
      <div><dt>Optional extra deck</dt><dd>{html.escape(g['optional_deck'])}</dd></div>
      <div><dt>Typical length</dt><dd>{html.escape(g['time'])}</dd></div>
      <div><dt>Complexity</dt><dd>{html.escape(g['complexity'])}</dd></div>
      <div><dt>Status</dt><dd>{html.escape(g['status'])}</dd></div>
    </dl>
  </section>

  <section class="panel two-column">
    <div>
      <h2>Kit needed</h2>
      <ul>{needs_items}</ul>
    </div>
    <div>
      <h2>Printable downloads</h2>
      <ul>{printable_items(g, depth=2)}</ul>
    </div>
  </section>

  {printable_previews}

  <section class="rules panel">
    <h2>Rules</h2>
    {g['rules_html']}
  </section>
</article>'''
        write(ROOT / f'cards/{g["slug"]}/index.html', layout(g['name'], body, 2, f'Rules and quick reference for {g["name"]}.'))

def build_player_page(slug: str, title: str, tag: str) -> None:
    chosen_dice = sorted_games([g for g in GAMES if tag in g['player_tags']])
    chosen_cards = sorted_card_games([g for g in CARD_GAMES if tag in g['player_tags']])
    dice_cards = '\n'.join(game_card(g, depth=2) for g in chosen_dice)
    card_cards = '\n'.join(card_game_card(g, depth=2) for g in chosen_cards)
    body = f'''<p class="breadcrumb"><a href="../../">← Home</a></p>
<header class="hero compact-hero">
  <p class="eyebrow">Browse by player count</p>
  <h1>{html.escape(title)}</h1>
  <p>Dice and card games that fit this player count. Dice games are ordered easiest to hardest; card games follow the card-game index order.</p>
</header>
<section>
  <h2>Dice games</h2>
  <div class="game-grid" aria-label="{html.escape(title)} dice games">
{dice_cards}
  </div>
</section>
<section>
  <h2>Card games</h2>
  <div class="game-grid" aria-label="{html.escape(title)} card games">
{card_cards}
  </div>
</section>'''
    write(ROOT / f'players/{slug}/index.html', layout(title, body, 2, f'{title} for Portable Game Night.'))


def build_cards_placeholder() -> None:
    body = '''<p class="breadcrumb"><a href="../">← Home</a></p>
<header class="hero compact-hero">
  <p class="eyebrow">Coming later</p>
  <h1>Card Games</h1>
  <p>This section is reserved for card games once the dice game rules and templates are locked.</p>
</header>'''
    write(ROOT / 'cards/index.html', layout('Card Games', body, 1, 'Card game rules for Portable Game Night.'))


def main() -> None:
    sections = extract_sections(SOURCE.read_text(encoding='utf-8'))
    missing = [g['name'] for g in GAMES if g['slug'] not in sections and not g.get('rules_html')]
    if missing:
        raise SystemExit('Missing source sections: ' + ', '.join(missing))
    build_home()
    build_dice_index()
    build_game_pages(sections)
    build_player_page('1-player', '1 Player Games', '1 Player')
    build_player_page('2-players', '2 Player Games', '2 Players')
    build_player_page('3-plus', '3+ Player Games', '3+ Players')
    build_cards_index()
    build_card_game_pages()
    print(f'Built {len(GAMES)} dice game pages and {len(CARD_GAMES)} card game pages plus index/player pages.')


if __name__ == '__main__':
    main()
