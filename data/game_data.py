from __future__ import annotations

# Game metadata and generated rule HTML for Portable Game Night.
# Rendering logic lives in scripts/build_site.py.

GAMES = [{'name': 'Farkle',
  'slug': 'farkle',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '6 dice',
  'time': '15–30 min',
  'complexity': 'Easy',
  'vibe': 'Push your luck scoring',
  'tags': ['Dice', '2 Players', '3+ Players', 'Push Your Luck', 'Easy', 'Score Chart PDF', 'Scoresheet PDF'],
  'needs': ['6 dice', 'Pen or pencil', 'Score sheet'],
  'printables': ['Farkle score sheet PDF'],
  'status': 'Ready; official score sheet added'},
 {'name': 'Liar’s Dice / Perudo',
  'slug': 'liars-dice',
  'players': '3–6 ideal',
  'player_tags': ['3+ Players'],
  'dice': '5 dice per player',
  'time': '15–30 min',
  'complexity': 'Easy',
  'vibe': 'Bluffing and table talk',
  'tags': ['Dice',
           '3+ Players',
           'Bluffing',
           'Party',
           'Dice Cups',
           'Wild 1s',
           'Drinking Variant',
           'Additional Items Required'],
  'needs': ['5 dice per player', 'Opaque dice cup per player'],
  'printables': ['Rules reference'],
  'status': 'Ready; printable added; elimination and drinking variants'},
 {'name': 'Ship, Captain, and Crew',
  'slug': 'ship-captain-and-crew',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '5 dice',
  'time': '5–15 min',
  'complexity': 'Very Easy',
  'vibe': 'Quick pub game',
  'tags': ['Dice', '2 Players', '3+ Players', 'Pub Game', 'Very Easy', 'Quick'],
  'needs': ['5 dice'],
  'printables': [],
  'status': 'Ready; printable added'},
 {'name': 'Pig',
  'slug': 'pig',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '1–2 dice',
  'time': '5–20 min',
  'complexity': 'Very Easy',
  'vibe': 'Simple push your luck',
  'tags': ['Dice', '2 Players', '3+ Players', 'Push Your Luck', 'Very Easy', 'Quick'],
  'needs': ['1 die for classic Pig', '2 dice for two-dice Pig'],
  'printables': [],
  'status': 'Ready; printable added'},
 {'name': 'Going to Boston',
  'slug': 'going-to-boston',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '3 dice',
  'time': '5–15 min',
  'complexity': 'Very Easy',
  'vibe': 'Light family filler',
  'tags': ['Dice', '2 Players', '3+ Players', 'Family Friendly', 'Very Easy', 'Quick'],
  'needs': ['3 dice'],
  'printables': [],
  'status': 'Ready; printable added'},
 {'name': 'Yahtzee / Yacht',
  'slug': 'yahtzee-yacht',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '5 dice',
  'time': '20–45 min',
  'complexity': 'Moderate',
  'vibe': 'Scorecard combinations',
  'tags': ['Dice', '2 Players', '3+ Players', 'Scorecard', 'Moderate', 'Scoresheet PDF', 'Additional Items Required'],
  'needs': ['5 dice', 'Pen or pencil', 'Score sheet'],
  'printables': ['Scoresheet PDF'],
  'status': 'Ready; printable added'},
 {'name': 'Mia',
  'slug': 'mia',
  'players': '3+ players',
  'player_tags': ['3+ Players'],
  'dice': '2 dice',
  'time': '5–15 min',
  'complexity': 'Easy',
  'vibe': 'Tiny bluffing game',
  'tags': ['Dice', '3+ Players', 'Bluffing', 'Pub Game', 'Dice Cups', 'Additional Items Required'],
  'needs': ['2 dice', 'One opaque cup'],
  'printables': ['Rules reference'],
  'status': 'Ready; printable added'},
 {'name': 'Beetle',
  'slug': 'beetle',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '1 die',
  'time': '5–15 min',
  'complexity': 'Very Easy',
  'vibe': 'Kids drawing game',
  'tags': ['Dice', '2 Players', '3+ Players', 'Kids', 'Very Easy', 'Paper Needed'],
  'needs': ['1 die', 'Paper', 'Pen or pencil'],
  'printables': ['Beetle drawing sheet'],
  'status': 'Ready; printable added'},
 {'name': 'Tenzi',
  'slug': 'tenzi',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '10 dice per player',
  'time': 'Under 5 min',
  'complexity': 'Very Easy',
  'vibe': 'Speed party chaos',
  'tags': ['Dice', '2 Players', '3+ Players', 'Speed', 'Party', 'Kids', 'Very Easy'],
  'needs': ['10 dice per player'],
  'printables': [],
  'status': 'Ready; printable added'},
 {'name': 'Bunco',
  'slug': 'bunco',
  'players': 'Group game',
  'player_tags': ['3+ Players', 'Teams'],
  'dice': '3 dice per table',
  'time': '30+ min',
  'complexity': 'Easy',
  'vibe': 'Large social group game',
  'tags': ['Dice', '3+ Players', 'Teams', 'Party', 'Scorecard', 'Additional Items Required'],
  'needs': ['3 dice per table', 'Score sheets', 'Pen or pencil'],
  'printables': ['Scoresheet PDF'],
  'status': 'Ready; printable added'},
 {'name': 'Craps',
  'slug': 'craps',
  'players': '1+ players',
  'player_tags': ['1 Player', '2 Players', '3+ Players'],
  'dice': '2 dice',
  'time': 'Variable',
  'complexity': 'Moderate',
  'vibe': 'Casino-style pass line',
  'tags': ['Dice', '1 Player', '2 Players', '3+ Players', 'Casino Style', 'Tokens/Chips', 'Additional Items Required'],
  'needs': ['2 dice', 'Optional tokens/chips'],
  'printables': ['Pass Line rules reference'],
  'status': 'Ready; printable added'},
 {'name': 'Knucklebones',
  'slug': 'knucklebones',
  'players': '2 players',
  'player_tags': ['2 Players'],
  'dice': '18 dice ideal',
  'time': '5–15 min',
  'complexity': 'Moderate',
  'vibe': 'Tactical head-to-head',
  'tags': ['Dice', '2 Players', 'Tactical', 'Printable Board', 'Additional Items Required'],
  'needs': ['18 dice ideal', '3x3 grid per player'],
  'printables': ['Printable board'],
  'status': 'Ready; printable added'},
 {'name': 'Can’t Stop',
  'slug': 'cant-stop',
  'players': '2–4 players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '4 dice',
  'time': '20–40 min',
  'complexity': 'Moderate',
  'vibe': 'Push your luck board race',
  'tags': ['Dice', '2 Players', '3+ Players', 'Push Your Luck', 'Tactical', 'Printable Board'],
  'needs': ['4 dice', 'Number track from 2 to 12', 'Markers'],
  'printables': ['Printable board'],
  'status': 'Ready; printable added'},
 {'name': 'Shut the Box',
  'slug': 'shut-the-box',
  'players': '1+ players',
  'player_tags': ['1 Player', '2 Players', '3+ Players'],
  'dice': '2 dice',
  'time': '5–15 min',
  'complexity': 'Easy',
  'vibe': 'Fast math puzzle',
  'tags': ['Dice', '1 Player', '2 Players', '3+ Players', 'Tactical', 'Printable Board'],
  'needs': ['2 dice', 'Board or paper numbers 1–9/12'],
  'printables': ['Printable board'],
  'status': 'Ready; printable added'},
 {'name': 'Qwixx-Style Roll-and-Write',
  'slug': 'qwixx-style-roll-and-write',
  'players': '2–5 players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '6 dice',
  'time': '15–30 min',
  'complexity': 'Moderate',
  'vibe': 'Roll-and-write score rows',
  'tags': ['Dice', '2 Players', '3+ Players', 'Scorecard', 'Tactical', 'Scoresheet PDF'],
  'needs': ['6 dice', 'Score sheets', 'Pen or pencil'],
  'printables': ['Scoresheet PDF'],
  'status': 'Ready; printable added'},
 {'name': 'Martinetti / Mountain / Matterhorn',
  'slug': 'martinetti-mountain-matterhorn',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '3 dice',
  'time': '10–20 min',
  'complexity': 'Easy',
  'vibe': 'Number-track race',
  'tags': ['Dice', '2 Players', '3+ Players', 'Tactical', 'Printable Board'],
  'needs': ['3 dice', 'Paper track', 'Pen or pencil'],
  'printables': ['Printable track'],
  'status': 'Ready; printable added; track variants included'},
 {'name': 'Chicago',
  'slug': 'chicago',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '2 dice',
  'time': '5–15 min',
  'complexity': 'Very Easy',
  'vibe': 'Target-number rounds',
  'tags': ['Dice', '2 Players', '3+ Players', 'Very Easy', 'Quick', 'Scorecard'],
  'needs': ['2 dice', 'Optional score sheet'],
  'printables': ['Scoresheet PDF'],
  'status': 'Ready; printable added'},
 {'name': 'Threes / Thirty',
  'slug': 'threes-thirty',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '5–6 dice',
  'time': '5–15 min',
  'complexity': 'Easy',
  'vibe': 'Low-score reroll game',
  'tags': ['Dice', '2 Players', '3+ Players', 'Easy', 'Quick', 'Pub Game'],
  'needs': ['5 or 6 dice'],
  'printables': [],
  'status': 'Ready; printable added'},
 {'name': 'Drop Dead',
  'slug': 'drop-dead',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '5 dice',
  'time': '5–15 min',
  'complexity': 'Very Easy',
  'vibe': 'Dice survival scoring',
  'tags': ['Dice', '2 Players', '3+ Players', 'Very Easy', 'Quick', 'Family Friendly'],
  'needs': ['5 dice', 'Optional score sheet'],
  'printables': ['Scoresheet PDF'],
  'status': 'Ready; printable added'},
 {'name': 'Poker Dice',
  'slug': 'poker-dice',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '5 dice',
  'time': '5–15 min',
  'complexity': 'Easy',
  'vibe': 'Poker-style dice hands',
  'tags': ['Dice', '2 Players', '3+ Players', 'Easy', 'Pub Game', 'Rules Reference'],
  'needs': ['5 dice'],
  'printables': ['Hand ranking reference'],
  'status': 'Ready; printable added'},
 {'name': 'Sevens Out',
  'slug': 'sevens-out',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '2 dice',
  'time': '5–15 min',
  'complexity': 'Very Easy',
  'vibe': 'Two-dice push your luck',
  'tags': ['Dice', '2 Players', '3+ Players', 'Push Your Luck', 'Very Easy', 'Quick'],
  'needs': ['2 dice', 'Optional score sheet'],
  'printables': ['Scoresheet PDF'],
  'status': 'Ready; printable added'},
 {'name': 'Beat That',
  'slug': 'beat-that',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '2–4 dice',
  'time': '5–10 min',
  'complexity': 'Very Easy',
  'vibe': 'Make the biggest number',
  'tags': ['Dice', '2 Players', '3+ Players', 'Kids', 'Very Easy', 'Quick'],
  'needs': ['2–4 dice'],
  'printables': [],
  'status': 'Ready; printable added'},
 {'name': 'Skunk',
  'slug': 'skunk',
  'players': '3+ ideal; 2 works',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '2 dice',
  'time': '10–20 min',
  'complexity': 'Easy',
  'vibe': 'Group push your luck',
  'tags': ['Dice', '2 Players', '3+ Players', 'Push Your Luck', 'Family Friendly', 'Scoresheet PDF'],
  'needs': ['2 dice', 'Score sheet', 'Pen or pencil'],
  'printables': ['Scoresheet PDF'],
  'status': 'Ready; printable added'},
 {'name': 'Midnight',
  'slug': 'midnight',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '6 dice',
  'time': '5–15 min',
  'complexity': 'Easy',
  'vibe': 'Quick pub game',
  'tags': ['Dice', '2 Players', '3+ Players', 'Pub Game', 'Quick', 'Easy'],
  'needs': ['6 dice', 'Optional score sheet'],
  'printables': ['Scoresheet PDF'],
  'status': 'Ready; printable added'},
 {'name': 'Stuck in the Mud',
  'slug': 'stuck-in-the-mud',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '5 dice',
  'time': '5–15 min',
  'complexity': 'Very Easy',
  'vibe': 'Simple family scoring',
  'tags': ['Dice', '2 Players', '3+ Players', 'Family Friendly', 'Very Easy', 'Scoresheet PDF'],
  'needs': ['5 dice', 'Score sheet', 'Pen or pencil'],
  'printables': ['Scoresheet PDF'],
  'status': 'Ready; printable added'},
 {'name': 'Three or More',
  'slug': 'three-or-more',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '5 dice',
  'time': '10–20 min',
  'complexity': 'Easy',
  'vibe': 'Yahtzee-lite sets',
  'tags': ['Dice', '2 Players', '3+ Players', 'Scorecard', 'Easy', 'Scoresheet PDF'],
  'needs': ['5 dice', 'Score sheet', 'Pen or pencil'],
  'printables': ['Scoresheet PDF'],
  'status': 'Ready; printable added'},
 {'name': 'Crag',
  'slug': 'crag',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '3 dice',
  'time': '10–20 min',
  'complexity': 'Moderate',
  'vibe': 'Compact scorecard game',
  'tags': ['Dice', '2 Players', '3+ Players', 'Scorecard', 'Tactical', 'Scoresheet PDF'],
  'needs': ['3 dice', 'Scorecard', 'Pen or pencil'],
  'printables': ['Scorecard PDF'],
  'status': 'Ready; printable added'},
 {'name': 'Aces in the Pot',
  'slug': 'aces-in-the-pot',
  'players': '3+ players',
  'player_tags': ['3+ Players'],
  'dice': '2 dice',
  'time': '5–15 min',
  'complexity': 'Very Easy',
  'vibe': 'Token passing filler',
  'tags': ['Dice', '3+ Players', 'Token Passing', 'Tokens/Chips', 'Additional Items Required', 'Very Easy'],
  'needs': ['2 dice', 'Tokens/chips/coins'],
  'printables': ['Rules reference'],
  'status': 'Ready; printable added'},
 {'name': 'Cee-lo / 4-5-6',
  'slug': 'cee-lo-456',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '3 dice',
  'time': '5–15 min',
  'complexity': 'Easy',
  'vibe': 'Dramatic ranking rounds',
  'tags': ['Dice', '2 Players', '3+ Players', 'Pub Game', 'Rules Reference'],
  'needs': ['3 dice', 'Optional tokens/chips'],
  'printables': ['Ranking reference'],
  'status': 'Ready; printable added'},
 {'name': 'Left Center Right, Standard-Dice Version',
  'slug': 'left-center-right',
  'players': '3+ players',
  'player_tags': ['3+ Players'],
  'dice': '3 dice',
  'time': '5–15 min',
  'complexity': 'Very Easy',
  'vibe': 'Party token passing',
  'tags': ['Dice', '3+ Players', 'Token Passing', 'Tokens/Chips', 'Additional Items Required', 'Very Easy'],
  'needs': ['3 dice', 'Tokens/chips/coins'],
  'printables': ['Rules reference'],
  'status': 'Ready; printable added'},
 {'name': 'Dice Golf',
  'slug': 'dice-golf',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': 'Usually 5 dice',
  'time': '15–30 min',
  'complexity': 'Moderate',
  'vibe': 'Themed score-sheet play',
  'tags': ['Dice', '2 Players', '3+ Players', 'Scorecard', 'Scoresheet PDF'],
  'needs': ['5 dice', 'Score sheet', 'Pen or pencil'],
  'printables': ['Scorecard PDF'],
  'status': 'Ready; printable added'},
 {'name': 'Sic Bo, Simplified Home Version',
  'slug': 'sic-bo',
  'players': '2+ players',
  'player_tags': ['2 Players', '3+ Players'],
  'dice': '3 dice',
  'time': 'Flexible',
  'complexity': 'Moderate',
  'vibe': 'Casino-style fake-chip play',
  'tags': ['Dice',
           '2 Players',
           '3+ Players',
           'Casino Style',
           'Tokens/Chips',
           'Betting Mat',
           'Additional Items Required'],
  'needs': ['3 dice', 'Fake chips/tokens', 'Betting mat/reference'],
  'printables': ['Betting mat PDF'],
  'status': 'Ready; printable added'},
 {'name': 'Help Your Neighbor',
  'slug': 'help-your-neighbor',
  'players': '3–6 ideal',
  'player_tags': ['3+ Players'],
  'dice': 'Usually 3 dice',
  'time': '10–20 min',
  'complexity': 'Easy',
  'vibe': 'Light social token play',
  'tags': ['Dice', '3+ Players', 'Token Passing', 'Tokens/Chips', 'Additional Items Required'],
  'needs': ['3 dice', 'Tokens/chips/coins'],
  'printables': ['Rules reference'],
  'status': 'Ready; printable added'},
 {'name': 'Pair Pressure',
  'slug': 'pair-pressure',
  'players': '2 players',
  'player_tags': ['2 Players'],
  'dice': '6 dice',
  'time': '15–30 min',
  'complexity': 'Moderate',
  'vibe': 'Six-dice number-clearing race',
  'tags': ['Dice', '2 Players', 'Push Your Luck', 'Tactical', 'Scorecard', 'Printable Board', '6 Dice'],
  'needs': ['6 dice', 'Pair Pressure board or score sheet', 'Poker chips/tokens or pencil'],
  'printables': ['Printable board / score sheet'],
  'status': 'Ready; house version based on dice-pair clearing to 500 points'}]

CARD_GAMES = [{'name': 'War',
  'slug': 'war',
  'players': '2 players',
  'player_tags': ['2 Players'],
  'decks': '1 deck',
  'optional_deck': 'No',
  'time': '10–30 min',
  'complexity': 'Very Easy',
  'vibe': 'Simple high-card battles',
  'tags': ['Cards', '2 Players', '1 Deck', 'Very Easy', 'Kids', 'Luck', 'No Scoring'],
  'needs': ['1 standard 52-card deck'],
  'status': 'Draft rules added',
  'order': 10,
  'rules_html': '<h2>Object</h2>\n'
                '<p>Win all the cards, or have the most cards when you stop.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>Shuffle one deck and deal all cards evenly between two players. Players keep their stacks face '
                'down.</p>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>Each player flips the top card of their stack.</li>\n'
                '<li>Higher card wins both cards and places them at the bottom of their stack.</li>\n'
                '<li>If there is a tie, each player places three cards face down and one card face up. The higher '
                'face-up card wins the whole pile.</li>\n'
                '<li>Keep playing until one player has all the cards, or set a time limit and count cards when time '
                'runs out.</li>\n'
                '</ol>'},
 {'name': 'Crazy Eights',
  'slug': 'crazy-eights',
  'players': '2–5 players',
  'player_tags': ['2 Players', '3+ Players'],
  'decks': '1 deck',
  'optional_deck': 'Helpful for 5+ players',
  'time': '10–20 min',
  'complexity': 'Very Easy',
  'vibe': 'Classic shedding game',
  'tags': ['Cards', '2 Players', '3+ Players', '1 Deck', 'Very Easy', 'Family Friendly', 'Shedding'],
  'needs': ['1 standard 52-card deck', 'Optional second deck for bigger groups'],
  'status': 'Ready',
  'order': 20,
  'rules_html': '<h2>Object</h2>\n'
                '<p>Be the first player to get rid of all your cards.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>Deal 5 cards to each player. Place the rest face down as a draw pile and flip one card face '
                'up.</p>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>Play one card matching the discard by rank or suit.</li>\n'
                '<li>Eights are wild. When you play one, name the next suit.</li>\n'
                '<li>If you cannot play, draw one card.</li>\n'
                '<li>First player out wins the hand.</li>\n'
                '</ol>'},
 {'name': 'Spoons',
  'slug': 'spoons',
  'players': '3+ players',
  'player_tags': ['3+ Players'],
  'decks': '1 deck',
  'optional_deck': 'Helpful for 8+ players',
  'time': '10–20 min',
  'complexity': 'Very Easy',
  'vibe': 'Fast reaction party game',
  'tags': ['Cards', '3+ Players', '1 Deck', 'Party', 'Speed', 'Very Easy', 'Additional Items Required'],
  'needs': ['1 standard 52-card deck', 'Spoons or tokens: one fewer than players'],
  'status': 'Ready',
  'order': 30,
  'rules_html': '<h2>Object</h2>\n'
                '<p>Collect four of a kind, then grab a spoon before they are gone.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>Put one fewer spoon than players in the center. Deal 4 cards each.</p>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>Draw and pass one card left continuously.</li>\n'
                '<li>When you have four of a kind, grab a spoon.</li>\n'
                '<li>Once one spoon is taken, anyone may grab one.</li>\n'
                '<li>The player without a spoon gets a letter or is eliminated.</li>\n'
                '</ol>'},
 {'name': 'Speed',
  'slug': 'speed',
  'players': '2 players',
  'player_tags': ['2 Players'],
  'decks': '1 deck',
  'optional_deck': 'No',
  'time': '5–10 min',
  'complexity': 'Easy',
  'vibe': 'Real-time two-player race',
  'tags': ['Cards', '2 Players', '1 Deck', 'Speed', 'Quick', 'Easy'],
  'needs': ['1 standard 52-card deck'],
  'status': 'Ready',
  'order': 40,
  'rules_html': '<h2>Object</h2>\n'
                '<p>Be first to play all cards from your hand and stock pile.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>Each player has a 5-card hand and 15-card stock pile. Two center piles start face down, with two '
                '5-card side piles.</p>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>Flip the two center cards.</li>\n'
                '<li>Both players play at the same time onto either center pile if their card is one rank higher or '
                'lower.</li>\n'
                '<li>Refill your hand to 5 from your stock pile.</li>\n'
                '<li>If both players are stuck, flip side-pile cards onto the center piles.</li>\n'
                '</ol>'},
 {'name': 'Spit',
  'slug': 'spit',
  'players': '2 players',
  'player_tags': ['2 Players'],
  'decks': '1 deck',
  'optional_deck': 'No',
  'time': '10–20 min',
  'complexity': 'Easy',
  'vibe': 'Speed solitaire duel',
  'tags': ['Cards', '2 Players', '1 Deck', 'Speed', 'Easy', 'Tableau'],
  'needs': ['1 standard 52-card deck'],
  'status': 'Ready',
  'order': 50,
  'rules_html': '<h2>Object</h2>\n'
                '<p>Clear your tableau faster than your opponent.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>Split the deck evenly. Each player builds five tableau piles of 1, 2, 3, 4, and 5 cards, with top '
                'cards face up.</p>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>Both players flip one spit card into the center.</li>\n'
                '<li>Play tableau cards onto either center pile one rank higher or lower.</li>\n'
                '<li>Fill empty tableau spaces with face-up cards.</li>\n'
                '<li>When stuck, both players spit new center cards.</li>\n'
                '<li>When one player clears their tableau, slap the smaller center pile.</li>\n'
                '</ol>'},
 {'name': 'Shithead / Palace / Karma',
  'slug': 'shithead-palace-karma',
  'players': '2–5 players',
  'player_tags': ['2 Players', '3+ Players'],
  'decks': '1 deck',
  'optional_deck': 'Helpful for 5+ players',
  'time': '20–40 min',
  'complexity': 'Easy',
  'vibe': 'Last-player-loses shedding game',
  'tags': ['Cards', '2 Players', '3+ Players', '1 Deck', 'Shedding', 'House Rules', 'Take That'],
  'needs': ['1 standard 52-card deck', 'Optional second deck for larger groups'],
  'status': 'Ready; name aliases noted',
  'order': 60,
  'rules_html': '<h2>Name note</h2>\n'
                '<p>This game is commonly called <strong>Shithead</strong>. Closely related versions are often called '
                '<strong>Palace</strong> or <strong>Karma</strong>. Rules vary heavily, so this should become your '
                'house-rule version.</p>\n'
                '<h2>Object</h2>\n'
                '<p>Avoid being the last player stuck with cards.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>Deal each player 3 face-down table cards, 3 face-up cards on top of them, and a 3-card hand.</p>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>Play cards equal to or higher than the top discard.</li>\n'
                '<li>Draw back up to 3 while the draw pile exists.</li>\n'
                '<li>If you cannot play, pick up the discard pile.</li>\n'
                '<li>After your hand is gone, play face-up table cards, then face-down table cards blindly.</li>\n'
                '<li>Last player with cards loses.</li>\n'
                '</ol>\n'
                '<h2>Starter special cards</h2>\n'
                '<p>A clean starter set: 2 resets the pile, 10 burns the pile, and 7 forces the next card to be 7 or '
                'lower.</p>'},
 {'name': 'BS / Cheat',
  'slug': 'bs-cheat',
  'players': '3+ players',
  'player_tags': ['3+ Players'],
  'decks': '1 deck',
  'optional_deck': 'Helpful for 6+ players',
  'time': '15–30 min',
  'complexity': 'Easy',
  'vibe': 'Bluffing discard game',
  'tags': ['Cards', '3+ Players', '1 Deck', 'Bluffing', 'Party', 'Shedding'],
  'needs': ['1 standard 52-card deck', 'Optional second deck for larger groups'],
  'status': 'Ready',
  'order': 70,
  'rules_html': '<h2>Object</h2>\n'
                '<p>Get rid of all your cards by playing cards face down and bluffing when needed.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>Deal all cards evenly. Play proceeds by rank: aces, twos, threes, and so on.</p>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>Place 1 or more cards face down and announce the required rank.</li>\n'
                '<li>Any player may call “BS” or “Cheat.”</li>\n'
                '<li>Reveal the cards. If the player lied, they take the pile. If they told the truth, the caller '
                'takes the pile.</li>\n'
                '<li>First player with no cards wins.</li>\n'
                '</ol>'},
 {'name': 'President',
  'slug': 'president',
  'players': '4–7 players',
  'player_tags': ['3+ Players'],
  'decks': '1 deck',
  'optional_deck': 'Helpful for 6+ players',
  'time': '20–40 min',
  'complexity': 'Easy',
  'vibe': 'Social climbing shedding game',
  'tags': ['Cards', '3+ Players', '1 Deck', 'Party', 'Shedding', 'Climbing', 'Easy'],
  'needs': ['1 standard 52-card deck', 'Optional second deck for larger groups'],
  'status': 'Ready; house version uses 3 low, 2 high, singles/pairs/triples only',
  'order': 80,
  'rules_html': '<h2>Recommended Portable Game Night variant</h2>\n'
                '<p>Use a clean casual version: 3 is low, ace is high, 2 is the highest rank, and legal plays are '
                'singles, pairs, or triples. Skip complicated bombs/revolutions for the base rules.</p>\n'
                '<h2>Object</h2>\n'
                '<p>Get rid of your cards first and climb the ranks for the next hand.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>Deal all cards as evenly as possible. The player with the 3 of clubs leads the first hand. After '
                'the first hand, the lowest-ranked player leads.</p>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>Lead a single, pair, or triple.</li>\n'
                '<li>Each next player must play the same number of cards at a higher rank, or pass.</li>\n'
                '<li>Players who pass are out until the pile clears.</li>\n'
                '<li>When everyone passes, the last player who played clears the pile and leads next.</li>\n'
                '<li>First player out becomes President next hand. Last player out gets the lowest rank.</li>\n'
                '</ol>\n'
                '<h2>Rank privilege</h2>\n'
                '<p>For the next hand, the lowest-ranked player gives their best card to the President, and the '
                'President gives back any one card. For larger groups, the second-highest and second-lowest players '
                'may also trade one card.</p>'},
 {'name': 'Golf',
  'slug': 'golf-card-game',
  'players': '2–6 players',
  'player_tags': ['2 Players', '3+ Players'],
  'decks': '1 deck',
  'optional_deck': 'Recommended for 5+ players',
  'time': '20–40 min',
  'complexity': 'Easy',
  'vibe': 'Low-score memory tableau',
  'tags': ['Cards', '2 Players', '3+ Players', '1 Deck', 'Memory', 'Scorecard', 'Easy'],
  'needs': ['1 standard 52-card deck', 'Pen or pencil', 'Optional second deck for larger groups'],
  'status': 'Ready',
  'order': 90,
  'rules_html': '<h2>Object</h2>\n'
                '<p>Finish with the lowest score after a set number of rounds.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>For 6-card Golf, deal each player 6 cards face down in a 2 by 3 grid. Each player flips any two '
                'cards face up.</p>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>Draw from the deck or discard pile.</li>\n'
                '<li>Replace one card in your grid or discard the drawn card.</li>\n'
                '<li>When one player has all cards face up, everyone else gets one more turn.</li>\n'
                '</ol>\n'
                '<h2>Starter scoring</h2>\n'
                '<p>Aces = 1, numbers = face value, jacks/queens = 10, kings = 0. Matching cards in a column cancel to '
                '0.</p>'},
 {'name': 'Rummy',
  'slug': 'rummy',
  'players': '2–6 players',
  'player_tags': ['2 Players', '3+ Players'],
  'decks': '1 deck',
  'optional_deck': 'Recommended for 5+ players',
  'time': '20–45 min',
  'complexity': 'Moderate',
  'vibe': 'Sets and runs classic',
  'tags': ['Cards', '2 Players', '3+ Players', '1 Deck', 'Sets/Runs', 'Scorecard', 'Moderate'],
  'needs': ['1 standard 52-card deck', 'Pen or pencil', 'Optional second deck for larger groups'],
  'status': 'Ready; house version uses basic draw-one/discard-one Rummy with optional layoff',
  'order': 100,
  'rules_html': '<h2>Recommended Portable Game Night variant</h2>\n'
                '<p>Use basic Rummy: draw one, optionally lay down melds, discard one. Allow laying off on existing '
                'melds after a player has made their first meld.</p>\n'
                '<h2>Object</h2>\n'
                '<p>Make sets and runs, then go out before the other players.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>Deal 10 cards each for 2 players, 7 cards each for 3–4 players, or 6 cards each for 5–6 players. '
                'Place the rest as a draw pile and flip one card to start the discard pile.</p>\n'
                '<h2>Melds</h2>\n'
                '<ul>\n'
                '<li>Set: 3 or 4 cards of the same rank.</li>\n'
                '<li>Run: 3 or more cards in sequence of the same suit.</li>\n'
                '</ul>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>Draw one card from the deck or discard pile.</li>\n'
                '<li>Lay down a new meld if you can, or lay off cards onto existing melds after your first meld.</li>\n'
                '<li>Discard one card.</li>\n'
                '<li>Go out when all your cards are melded or laid off except the final discard.</li>\n'
                '</ol>\n'
                '<h2>Scoring</h2>\n'
                '<p>When a player goes out, everyone else scores the cards left in hand: aces = 1, number cards = face '
                'value, face cards = 10. Lowest score after a set number of hands wins.</p>'},
 {'name': 'Gin Rummy',
  'slug': 'gin-rummy',
  'players': '2 players',
  'player_tags': ['2 Players'],
  'decks': '1 deck',
  'optional_deck': 'No',
  'time': '20–45 min',
  'complexity': 'Moderate',
  'vibe': 'Two-player rummy duel',
  'tags': ['Cards', '2 Players', '1 Deck', 'Sets/Runs', 'Scorecard', 'Moderate'],
  'needs': ['1 standard 52-card deck', 'Pen or pencil'],
  'status': 'Ready',
  'order': 101,
  'rules_html': '<h2>Object</h2>\n'
                '<p>Build melds and reduce deadwood, then knock or go gin.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>Deal 10 cards to each player. Flip one discard.</p>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>Draw from the deck or discard pile.</li>\n'
                '<li>Form sets and runs. Unmatched cards are deadwood.</li>\n'
                '<li>Discard one card.</li>\n'
                '<li>Knock when deadwood is 10 points or less, or go gin when all cards are melded.</li>\n'
                '</ol>\n'
                '<h2>Scoring starter</h2>\n'
                '<p>Aces = 1, face cards = 10, number cards = face value.</p>'},
 {'name': 'Canasta',
  'slug': 'canasta',
  'players': '2–6 players; best 4',
  'player_tags': ['2 Players', '3+ Players'],
  'decks': '2 decks',
  'optional_deck': 'No; already uses 2 decks plus jokers',
  'time': '45–90 min',
  'complexity': 'Moderate',
  'vibe': 'Rummy-family team melds',
  'tags': ['Cards', '2 Players', '3+ Players', '2 Decks', 'Teams', 'Sets/Runs', 'Scorecard', 'Moderate'],
  'needs': ['2 standard 52-card decks plus jokers', 'Pen or pencil'],
  'status': 'Ready',
  'order': 102,
  'rules_html': '<h2>Object</h2>\n'
                '<p>Score points by making melds of matching ranks, especially canastas: melds of 7 or more '
                'cards.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>Use two decks plus jokers. For four players, play partners. Deal 11 cards each.</p>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>Draw two cards, or take the discard pile if you can legally use the top card.</li>\n'
                '<li>Build melds of 3 or more cards of the same rank.</li>\n'
                '<li>Discard one card.</li>\n'
                '<li>A canasta is 7 or more cards in one meld.</li>\n'
                '<li>To go out, your side usually needs at least one canasta.</li>\n'
                '</ol>\n'
                '<h2>Notes</h2>\n'
                '<p>Grouped beside Rummy and Gin Rummy because it is part of the same meld-building family.</p>'},
 {'name': 'Kemps',
  'slug': 'kemps',
  'players': '4+ players; even teams',
  'player_tags': ['3+ Players'],
  'decks': '1 deck',
  'optional_deck': 'Helpful for 8+ players',
  'time': '15–30 min',
  'complexity': 'Moderate',
  'vibe': 'Secret-signal team game',
  'tags': ['Cards', '3+ Players', '1 Deck', 'Teams', 'Party', 'Secret Signals', 'Moderate'],
  'needs': ['1 standard 52-card deck', 'Even number of players', 'Optional second deck for larger groups'],
  'status': 'Ready',
  'order': 110,
  'rules_html': '<h2>Object</h2>\n'
                '<p>Signal your partner when you have four of a kind without the other team catching you.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>Partners sit across from each other and secretly agree on a signal. Deal 4 cards each and put 4 '
                'cards face up in the center.</p>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>Swap cards from your hand with center cards.</li>\n'
                '<li>When no one wants the center cards, clear and reveal 4 new cards.</li>\n'
                '<li>When you have four of a kind, give the signal.</li>\n'
                '<li>Your partner calls “Kemps.” Another team may call “Counter-Kemps.”</li>\n'
                '</ol>'},
 {'name': 'Hearts',
  'slug': 'hearts',
  'players': '3–6 players; best 4',
  'player_tags': ['3+ Players'],
  'decks': '1 deck',
  'optional_deck': 'No',
  'time': '30–60 min',
  'complexity': 'Moderate',
  'vibe': 'Avoid points trick-taking',
  'tags': ['Cards', '3+ Players', '1 Deck', 'Trick-Taking', 'Avoid Points', 'Scorecard', 'Moderate'],
  'needs': ['1 standard 52-card deck', 'Pen or pencil'],
  'status': 'Ready; house version uses standard 4-player Hearts with pass cycle and shoot the moon',
  'order': 120,
  'rules_html': '<h2>Recommended Portable Game Night variant</h2>\n'
                '<p>Use standard 4-player Hearts as the base version: pass left, right, across, then hold; hearts are '
                '1 point; queen of spades is 13 points; game ends at 100.</p>\n'
                '<h2>Object</h2>\n'
                '<p>Avoid taking penalty cards. Lowest score wins.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>Deal all cards to 4 players. Each heart is worth 1 point. The queen of spades is worth 13 '
                'points.</p>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>Pass 3 cards according to the cycle: left, right, across, then no pass.</li>\n'
                '<li>The player with the 2 of clubs leads the first trick.</li>\n'
                '<li>Players must follow suit if able. Highest card of the led suit wins the trick.</li>\n'
                '<li>Hearts cannot be led until hearts are broken, unless a player has only hearts.</li>\n'
                '<li>Add penalty points after each hand. Game ends when someone reaches 100; lowest score wins.</li>\n'
                '</ol>\n'
                '<h2>Shooting the moon</h2>\n'
                '<p>If one player takes all hearts and the queen of spades, they score 0 and every other player scores '
                '26.</p>'},
 {'name': 'Spades',
  'slug': 'spades',
  'players': '4 players; partners',
  'player_tags': ['3+ Players'],
  'decks': '1 deck',
  'optional_deck': 'No',
  'time': '30–60 min',
  'complexity': 'Moderate',
  'vibe': 'Bid-based partner tricks',
  'tags': ['Cards', '3+ Players', '1 Deck', 'Teams', 'Trick-Taking', 'Bidding', 'Scorecard', 'Moderate'],
  'needs': ['1 standard 52-card deck', 'Pen or pencil'],
  'status': 'Ready; house version uses standard partnership Spades with bags and nil optional',
  'order': 130,
  'rules_html': '<h2>Recommended Portable Game Night variant</h2>\n'
                '<p>Use standard 4-player partnership Spades: spades are always trump, teams bid total tricks, and '
                'bags matter. Keep nil bids optional for the first few games.</p>\n'
                '<h2>Object</h2>\n'
                '<p>Bid how many tricks your team will take, then try to hit that bid.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>Deal all cards to four players in partnerships. Each player bids a number of tricks. Partner bids '
                'are combined into a team bid.</p>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>The player left of the dealer leads any non-spade card to the first trick.</li>\n'
                '<li>Players must follow suit if able. If unable, they may play a spade or discard.</li>\n'
                '<li>Highest card of the led suit wins unless a spade is played; highest spade wins.</li>\n'
                '<li>Spades cannot be led until broken, unless a player has only spades.</li>\n'
                '<li>Score after 13 tricks.</li>\n'
                '</ol>\n'
                '<h2>Scoring</h2>\n'
                '<p>If your team makes its bid, score 10 points per bid trick plus 1 point per extra trick. Extra '
                'tricks are bags. At 10 bags, subtract 100 points and clear the bag count. If your team misses its '
                'bid, subtract 10 points per bid trick.</p>\n'
                '<h2>Optional nil</h2>\n'
                '<p>A nil bid means that player tries to take zero tricks. Successful nil scores +100; failed nil '
                'scores -100. Keep this optional until the table is comfortable.</p>'},
 {'name': 'Egyptian Rat Screw',
  'slug': 'egyptian-rat-screw',
  'players': '2–6 players',
  'player_tags': ['2 Players', '3+ Players'],
  'decks': '1 deck',
  'optional_deck': 'Helpful for 5+ players',
  'time': '10–30 min',
  'complexity': 'Moderate',
  'vibe': 'Slapjack with combos',
  'tags': ['Cards', '2 Players', '3+ Players', '1 Deck', 'Speed', 'Slapping', 'Party', 'Moderate'],
  'needs': ['1 standard 52-card deck', 'Optional second deck for larger groups'],
  'status': 'Ready; house version uses doubles and sandwiches as legal slaps',
  'order': 140,
  'rules_html': '<h2>Recommended Portable Game Night variant</h2>\n'
                '<p>Use a focused slap set: doubles and sandwiches only. That keeps the game fast without turning '
                'every card into an argument.</p>\n'
                '<h2>Object</h2>\n'
                '<p>Win the whole deck through face-card challenges and legal slap opportunities.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>Deal all cards face down as evenly as possible. Players do not look at their cards.</p>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>Players take turns flipping one card face up into the center pile, flipping away from '
                'themselves.</li>\n'
                '<li>If a face card or ace appears, the next player gets chances to answer: jack = 1, queen = 2, king '
                '= 3, ace = 4.</li>\n'
                '<li>If the challenged player reveals another face card or ace, the challenge passes to the next '
                'player.</li>\n'
                '<li>If they fail, the previous face-card player takes the whole pile.</li>\n'
                '<li>Anyone may slap doubles, such as 8-8, or sandwiches, such as 8-4-8. First legal slap wins the '
                'pile.</li>\n'
                '<li>A false slap costs one card, placed under the center pile.</li>\n'
                '</ol>\n'
                '<h2>Safety note</h2>\n'
                '<p>Use a flat-hand slap and keep drinks away from the pile. The game is chaotic enough without a '
                'beverage expansion pack.</p>'},
 {'name': 'Spider Solitaire',
  'slug': 'spider-solitaire',
  'players': '1 player',
  'player_tags': ['1 Player'],
  'decks': '2 decks',
  'optional_deck': 'No; requires 2 decks',
  'time': '20–45 min',
  'complexity': 'Moderate',
  'vibe': 'Solo tableau puzzle',
  'tags': ['Cards', '1 Player', '2 Decks', 'Solitaire', 'Tableau', 'Quiet Game', 'Moderate'],
  'needs': ['2 standard 52-card decks; 104 cards total', 'Table space'],
  'status': 'Ready',
  'order': 150,
  'rules_html': '<h2>Object</h2>\n'
                '<p>Build full descending same-suit sequences from king to ace and remove them from the table.</p>\n'
                '<h2>Setup</h2>\n'
                '<p>Use two decks. Deal 10 columns: first 4 columns get 6 cards each, remaining 6 get 5 cards each. '
                'Only top cards are face up.</p>\n'
                '<h2>How to play</h2>\n'
                '<ol>\n'
                '<li>Move face-up cards in descending order.</li>\n'
                '<li>Move a packed sequence together only when it is the same suit.</li>\n'
                '<li>Empty columns can receive any card or valid packed sequence.</li>\n'
                '<li>When stuck, deal one stock card onto each column.</li>\n'
                '<li>Remove complete king-to-ace same-suit sequences. Win by removing all 8.</li>\n'
                '</ol>\n'
                '<h2>Easier variants</h2>\n'
                '<p>Use one suit for easiest play, two suits for medium, or four suits for the full challenge.</p>'}]
