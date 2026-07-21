#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path('/mnt/c/Users/code3/OneDrive/Desktop/Atlas_Project_Records/Card-Dice Games/dice_games.md')

GAMES = [
    dict(name='Farkle', slug='farkle', players='2+ players', player_tags=['2 Players','3+ Players'], dice='6 dice', time='15–30 min', complexity='Easy', vibe='Push your luck scoring', tags=['Dice','2 Players','3+ Players','Push Your Luck','Easy','Score Chart PDF','Scoresheet PDF'], needs=['6 dice','Pen or pencil','Score sheet'], printables=['Score chart PDF','Scoresheet PDF'], status='Needs printable'),
    dict(name='Liar’s Dice / Perudo', slug='liars-dice', players='3–6 ideal', player_tags=['3+ Players'], dice='5 dice per player', time='15–30 min', complexity='Easy', vibe='Bluffing and table talk', tags=['Dice','3+ Players','Bluffing','Party','Dice Cups','Wild 1s','Drinking Variant','Additional Items Required'], needs=['5 dice per player','Opaque dice cup per player'], printables=['Rules reference'], status='Ready; elimination and drinking variants'),
    dict(name='Ship, Captain, and Crew', slug='ship-captain-and-crew', players='2+ players', player_tags=['2 Players','3+ Players'], dice='5 dice', time='5–15 min', complexity='Very Easy', vibe='Quick pub game', tags=['Dice','2 Players','3+ Players','Pub Game','Very Easy','Quick'], needs=['5 dice'], printables=[], status='Ready'),
    dict(name='Pig', slug='pig', players='2+ players', player_tags=['2 Players','3+ Players'], dice='1–2 dice', time='5–20 min', complexity='Very Easy', vibe='Simple push your luck', tags=['Dice','2 Players','3+ Players','Push Your Luck','Very Easy','Quick'], needs=['1 die for classic Pig','2 dice for two-dice Pig'], printables=[], status='Ready'),
    dict(name='Going to Boston', slug='going-to-boston', players='2+ players', player_tags=['2 Players','3+ Players'], dice='3 dice', time='5–15 min', complexity='Very Easy', vibe='Light family filler', tags=['Dice','2 Players','3+ Players','Family Friendly','Very Easy','Quick'], needs=['3 dice'], printables=[], status='Ready'),
    dict(name='Yahtzee / Yacht', slug='yahtzee-yacht', players='2+ players', player_tags=['2 Players','3+ Players'], dice='5 dice', time='20–45 min', complexity='Moderate', vibe='Scorecard combinations', tags=['Dice','2 Players','3+ Players','Scorecard','Moderate','Scoresheet PDF','Additional Items Required'], needs=['5 dice','Pen or pencil','Score sheet'], printables=['Scoresheet PDF'], status='Needs printable'),
    dict(name='Mia', slug='mia', players='3+ players', player_tags=['3+ Players'], dice='2 dice', time='5–15 min', complexity='Easy', vibe='Tiny bluffing game', tags=['Dice','3+ Players','Bluffing','Pub Game','Dice Cups','Additional Items Required'], needs=['2 dice','One opaque cup'], printables=['Rules reference'], status='Ready'),
    dict(name='Beetle', slug='beetle', players='2+ players', player_tags=['2 Players','3+ Players'], dice='1 die', time='5–15 min', complexity='Very Easy', vibe='Kids drawing game', tags=['Dice','2 Players','3+ Players','Kids','Very Easy','Paper Needed'], needs=['1 die','Paper','Pen or pencil'], printables=['Beetle drawing sheet'], status='Needs printable'),
    dict(name='Tenzi', slug='tenzi', players='2+ players', player_tags=['2 Players','3+ Players'], dice='10 dice per player', time='Under 5 min', complexity='Very Easy', vibe='Speed party chaos', tags=['Dice','2 Players','3+ Players','Speed','Party','Kids','Very Easy'], needs=['10 dice per player'], printables=[], status='Ready'),
    dict(name='Bunco', slug='bunco', players='Group game', player_tags=['3+ Players','Teams'], dice='3 dice per table', time='30+ min', complexity='Easy', vibe='Large social group game', tags=['Dice','3+ Players','Teams','Party','Scorecard','Additional Items Required'], needs=['3 dice per table','Score sheets','Pen or pencil'], printables=['Scoresheet PDF'], status='Needs printable'),
    dict(name='Craps', slug='craps', players='1+ players', player_tags=['1 Player','2 Players','3+ Players'], dice='2 dice', time='Variable', complexity='Moderate', vibe='Casino-style pass line', tags=['Dice','1 Player','2 Players','3+ Players','Casino Style','Tokens/Chips','Additional Items Required'], needs=['2 dice','Optional tokens/chips'], printables=['Pass Line rules reference'], status='Ready; needs printable'),
    dict(name='Knucklebones', slug='knucklebones', players='2 players', player_tags=['2 Players'], dice='18 dice ideal', time='5–15 min', complexity='Moderate', vibe='Tactical head-to-head', tags=['Dice','2 Players','Tactical','Printable Board','Additional Items Required'], needs=['18 dice ideal','3x3 grid per player'], printables=['Printable board'], status='Needs printable'),
    dict(name='Can’t Stop', slug='cant-stop', players='2–4 players', player_tags=['2 Players','3+ Players'], dice='4 dice', time='20–40 min', complexity='Moderate', vibe='Push your luck board race', tags=['Dice','2 Players','3+ Players','Push Your Luck','Tactical','Printable Board'], needs=['4 dice','Number track from 2 to 12','Markers'], printables=['Printable board'], status='Needs printable'),
    dict(name='Shut the Box', slug='shut-the-box', players='1+ players', player_tags=['1 Player','2 Players','3+ Players'], dice='2 dice', time='5–15 min', complexity='Easy', vibe='Fast math puzzle', tags=['Dice','1 Player','2 Players','3+ Players','Tactical','Printable Board'], needs=['2 dice','Board or paper numbers 1–9/12'], printables=['Printable board'], status='Needs printable'),
    dict(name='Qwixx-Style Roll-and-Write', slug='qwixx-style-roll-and-write', players='2–5 players', player_tags=['2 Players','3+ Players'], dice='6 dice', time='15–30 min', complexity='Moderate', vibe='Roll-and-write score rows', tags=['Dice','2 Players','3+ Players','Scorecard','Tactical','Scoresheet PDF'], needs=['6 dice','Score sheets','Pen or pencil'], printables=['Scoresheet PDF'], status='Needs printable / house-safe wording'),
    dict(name='Martinetti / Mountain / Matterhorn', slug='martinetti-mountain-matterhorn', players='2+ players', player_tags=['2 Players','3+ Players'], dice='3 dice', time='10–20 min', complexity='Easy', vibe='Number-track race', tags=['Dice','2 Players','3+ Players','Tactical','Printable Board'], needs=['3 dice','Paper track','Pen or pencil'], printables=['Printable track'], status='Ready; track variants included'),
    dict(name='Chicago', slug='chicago', players='2+ players', player_tags=['2 Players','3+ Players'], dice='2 dice', time='5–15 min', complexity='Very Easy', vibe='Target-number rounds', tags=['Dice','2 Players','3+ Players','Very Easy','Quick','Scorecard'], needs=['2 dice','Optional score sheet'], printables=['Scoresheet PDF'], status='Needs printable'),
    dict(name='Threes / Thirty', slug='threes-thirty', players='2+ players', player_tags=['2 Players','3+ Players'], dice='5–6 dice', time='5–15 min', complexity='Easy', vibe='Low-score reroll game', tags=['Dice','2 Players','3+ Players','Easy','Quick','Pub Game'], needs=['5 or 6 dice'], printables=[], status='Ready'),
    dict(name='Drop Dead', slug='drop-dead', players='2+ players', player_tags=['2 Players','3+ Players'], dice='5 dice', time='5–15 min', complexity='Very Easy', vibe='Dice survival scoring', tags=['Dice','2 Players','3+ Players','Very Easy','Quick','Family Friendly'], needs=['5 dice','Optional score sheet'], printables=['Scoresheet PDF'], status='Needs printable'),
    dict(name='Poker Dice', slug='poker-dice', players='2+ players', player_tags=['2 Players','3+ Players'], dice='5 dice', time='5–15 min', complexity='Easy', vibe='Poker-style dice hands', tags=['Dice','2 Players','3+ Players','Easy','Pub Game','Rules Reference'], needs=['5 dice'], printables=['Hand ranking reference'], status='Needs printable'),
    dict(name='Sevens Out', slug='sevens-out', players='2+ players', player_tags=['2 Players','3+ Players'], dice='2 dice', time='5–15 min', complexity='Very Easy', vibe='Two-dice push your luck', tags=['Dice','2 Players','3+ Players','Push Your Luck','Very Easy','Quick'], needs=['2 dice','Optional score sheet'], printables=['Scoresheet PDF'], status='Needs printable'),
    dict(name='Beat That', slug='beat-that', players='2+ players', player_tags=['2 Players','3+ Players'], dice='2–4 dice', time='5–10 min', complexity='Very Easy', vibe='Make the biggest number', tags=['Dice','2 Players','3+ Players','Kids','Very Easy','Quick'], needs=['2–4 dice'], printables=[], status='Ready'),
    dict(name='Skunk', slug='skunk', players='3+ ideal; 2 works', player_tags=['2 Players','3+ Players'], dice='2 dice', time='10–20 min', complexity='Easy', vibe='Group push your luck', tags=['Dice','2 Players','3+ Players','Push Your Luck','Family Friendly','Scoresheet PDF'], needs=['2 dice','Score sheet','Pen or pencil'], printables=['Scoresheet PDF'], status='Ready; needs printable'),
    dict(name='Midnight', slug='midnight', players='2+ players', player_tags=['2 Players','3+ Players'], dice='6 dice', time='5–15 min', complexity='Easy', vibe='Quick pub game', tags=['Dice','2 Players','3+ Players','Pub Game','Quick','Easy'], needs=['6 dice','Optional score sheet'], printables=['Scoresheet PDF'], status='Ready; needs printable'),
    dict(name='Stuck in the Mud', slug='stuck-in-the-mud', players='2+ players', player_tags=['2 Players','3+ Players'], dice='5 dice', time='5–15 min', complexity='Very Easy', vibe='Simple family scoring', tags=['Dice','2 Players','3+ Players','Family Friendly','Very Easy','Scoresheet PDF'], needs=['5 dice','Score sheet','Pen or pencil'], printables=['Scoresheet PDF'], status='Ready'),
    dict(name='Three or More', slug='three-or-more', players='2+ players', player_tags=['2 Players','3+ Players'], dice='5 dice', time='10–20 min', complexity='Easy', vibe='Yahtzee-lite sets', tags=['Dice','2 Players','3+ Players','Scorecard','Easy','Scoresheet PDF'], needs=['5 dice','Score sheet','Pen or pencil'], printables=['Scoresheet PDF'], status='Ready; needs printable'),
    dict(name='Crag', slug='crag', players='2+ players', player_tags=['2 Players','3+ Players'], dice='3 dice', time='10–20 min', complexity='Moderate', vibe='Compact scorecard game', tags=['Dice','2 Players','3+ Players','Scorecard','Tactical','Scoresheet PDF'], needs=['3 dice','Scorecard','Pen or pencil'], printables=['Scorecard PDF'], status='Ready; needs printable'),
    dict(name='Aces in the Pot', slug='aces-in-the-pot', players='3+ players', player_tags=['3+ Players'], dice='2 dice', time='5–15 min', complexity='Very Easy', vibe='Token passing filler', tags=['Dice','3+ Players','Token Passing','Tokens/Chips','Additional Items Required','Very Easy'], needs=['2 dice','Tokens/chips/coins'], printables=['Rules reference'], status='Ready; needs printable'),
    dict(name='Cee-lo / 4-5-6', slug='cee-lo-456', players='2+ players', player_tags=['2 Players','3+ Players'], dice='3 dice', time='5–15 min', complexity='Easy', vibe='Dramatic ranking rounds', tags=['Dice','2 Players','3+ Players','Pub Game','Rules Reference'], needs=['3 dice','Optional tokens/chips'], printables=['Ranking reference'], status='Ready; needs printable'),
    dict(name='Left Center Right, Standard-Dice Version', slug='left-center-right', players='3+ players', player_tags=['3+ Players'], dice='3 dice', time='5–15 min', complexity='Very Easy', vibe='Party token passing', tags=['Dice','3+ Players','Token Passing','Tokens/Chips','Additional Items Required','Very Easy'], needs=['3 dice','Tokens/chips/coins'], printables=['Rules reference'], status='Ready; needs printable'),
    dict(name='Dice Golf', slug='dice-golf', players='2+ players', player_tags=['2 Players','3+ Players'], dice='Usually 5 dice', time='15–30 min', complexity='Moderate', vibe='Themed score-sheet play', tags=['Dice','2 Players','3+ Players','Scorecard','Scoresheet PDF'], needs=['5 dice','Score sheet','Pen or pencil'], printables=['Scorecard PDF'], status='Ready; needs printable'),
    dict(name='Sic Bo, Simplified Home Version', slug='sic-bo', players='2+ players', player_tags=['2 Players','3+ Players'], dice='3 dice', time='Flexible', complexity='Moderate', vibe='Casino-style fake-chip play', tags=['Dice','2 Players','3+ Players','Casino Style','Tokens/Chips','Betting Mat','Additional Items Required'], needs=['3 dice','Fake chips/tokens','Betting mat/reference'], printables=['Betting mat PDF'], status='Ready; needs printable'),
    dict(name='Help Your Neighbor', slug='help-your-neighbor', players='3–6 ideal', player_tags=['3+ Players'], dice='Usually 3 dice', time='10–20 min', complexity='Easy', vibe='Light social token play', tags=['Dice','3+ Players','Token Passing','Tokens/Chips','Additional Items Required'], needs=['3 dice','Tokens/chips/coins'], printables=['Rules reference'], status='Ready; needs printable'),
]


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


def tag_list(tags: list[str]) -> str:
    return '<div class="tags">' + ''.join(f'<span class="tag">{html.escape(t)}</span>' for t in tags) + '</div>'


def game_card(g: dict, depth: int = 0) -> str:
    prefix = rel_prefix(depth)
    top_tags = g['tags'][:5]
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
  <p>The dice section now has structured game cards and individual rule pages. Variant-heavy games are marked so the house rules can be locked before final printables are made.</p>
  <div class="mini-link-row">
    <a href="dice/">Browse dice games</a>
    <a href="players/2-players/">Find 2-player games</a>
    <a href="players/3-plus/">Find group games</a>
  </div>
</section>'''
    write(ROOT / 'index.html', layout('Home', body, 0, 'Portable dice and card game rules for travel and game nights.'))


def build_dice_index() -> None:
    cards = '\n'.join(game_card(g, depth=1) for g in GAMES)
    body = f'''<p class="breadcrumb"><a href="../">← Home</a></p>
<header class="hero compact-hero">
  <p class="eyebrow">Normal six-sided dice</p>
  <h1>Dice Games</h1>
  <p>Browse dice games by player count, components, complexity, and whether they still need a printable or locked house-rule version.</p>
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
        rules_html = md_to_html(rules) if rules else '<p>Rules content still needs to be imported.</p>'
        printable_items = ''.join(f'<li>{html.escape(p)}</li>' for p in (g['printables'] or ['No printable currently planned.']))
        needs_items = ''.join(f'<li>{html.escape(n)}</li>' for n in g['needs'])
        body = f'''<p class="breadcrumb"><a href="../../">← Home</a> / <a href="../">Dice Games</a></p>
<article class="game-page">
  <header class="hero compact-hero game-hero">
    <p class="eyebrow">Dice game</p>
    <h1>{html.escape(g['name'])}</h1>
    <p>{html.escape(g['vibe'])}</p>
    {tag_list(g['tags'])}
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
      <h2>Planned printables</h2>
      <ul>{printable_items}</ul>
    </div>
  </section>

  <section class="rules panel">
    <h2>Rules draft</h2>
    {rules_html}
  </section>
</article>'''
        write(ROOT / f'dice/{g["slug"]}/index.html', layout(g['name'], body, 2, f'Rules and quick reference for {g["name"]}.'))


def build_player_page(slug: str, title: str, tag: str) -> None:
    chosen = [g for g in GAMES if tag in g['player_tags']]
    cards = '\n'.join(game_card(g, depth=2) for g in chosen)
    body = f'''<p class="breadcrumb"><a href="../../">← Home</a></p>
<header class="hero compact-hero">
  <p class="eyebrow">Browse by player count</p>
  <h1>{html.escape(title)}</h1>
  <p>Dice games that fit this player count. Card games can be added here later using the same structure.</p>
</header>
<section class="game-grid" aria-label="{html.escape(title)}">
{cards}
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
    missing = [g['name'] for g in GAMES if g['slug'] not in sections]
    if missing:
        raise SystemExit('Missing source sections: ' + ', '.join(missing))
    build_home()
    build_dice_index()
    build_game_pages(sections)
    build_player_page('1-player', '1 Player Games', '1 Player')
    build_player_page('2-players', '2 Player Games', '2 Players')
    build_player_page('3-plus', '3+ Player Games', '3+ Players')
    build_cards_placeholder()
    print(f'Built {len(GAMES)} dice game pages plus index/player pages.')


if __name__ == '__main__':
    main()
