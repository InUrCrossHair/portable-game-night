#!/usr/bin/env python3
"""Build combined PDF bundles for physical Portable Game Night printing.

The individual printables remain the source files. These bundles are convenience
files for bulk printing the physical kit:

- reusable boards/mats/tracks bundle: print 2 copies for one play set + backup
- reference bundle: print 1-2 copies as table/no-Wi-Fi backup
- write-on bundle: print as many copies as needed for score-sheet stock
"""
from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parents[1]
PRINTABLES = ROOT / 'printables'
OUT = PRINTABLES / 'bundles'
OUT.mkdir(parents=True, exist_ok=True)

REUSABLE_PRINTABLES = [
    'pair-pressure-board-score-sheet.pdf',
    'knucklebones-board.pdf',
    'cant-stop-board.pdf',
    'shut-the-box-board.pdf',
    'martinetti-mountain-matterhorn-track.pdf',
    'horse-race-dice-track.pdf',
    'sic-bo-betting-mat.pdf',
    'chuck-a-luck-betting-mat.pdf',
]

WRITE_ON_PRINTABLES = [
    'farkle-score-sheet.pdf',
    'yahtzee-yacht-score-sheet.pdf',
    'skunk-score-sheet.pdf',
    'stuck-in-the-mud-score-sheet.pdf',
    'three-or-more-score-sheet.pdf',
    'crag-scorecard.pdf',
    'dice-golf-scorecard.pdf',
    'midnight-score-sheet.pdf',
    'chicago-score-sheet.pdf',
    'bunco-score-sheet.pdf',
    'drop-dead-score-sheet.pdf',
    'sevens-out-score-sheet.pdf',
    'qwixx-style-roll-and-write-sheet.pdf',
    'golf-card-game-score-sheet.pdf',
    'rummy-score-sheet.pdf',
    'gin-rummy-score-sheet.pdf',
    'canasta-score-sheet.pdf',
    'hearts-score-sheet.pdf',
    'spades-score-sheet.pdf',
    'cribbage-score-sheet.pdf',
    'casino-cassino-score-sheet.pdf',
    'oh-hell-score-sheet.pdf',
    'euchre-score-sheet.pdf',
    'bowling-solitaire-score-sheet.pdf',
    'solo-farkle-challenge-sheet.pdf',
    'dice-solitaire-score-sheet.pdf',
    'bowling-dice-score-sheet.pdf',
    'knock-out-dice-score-sheet.pdf',
    'dice-baseball-score-sheet.pdf',
    'nerts-score-sheet.pdf',
    'beetle-drawing-sheet.pdf',
]

# All remaining reference/rules/ranking sheets after reusable + write-on are removed.
# Kept explicit so print planning remains stable and reviewable.
REFERENCE_PRINTABLES = [
    'ship-captain-and-crew-reference.pdf',
    'pig-reference.pdf',
    'going-to-boston-reference.pdf',
    'mia-reference.pdf',
    'tenzi-reference.pdf',
    'craps-pass-line-reference.pdf',
    'threes-thirty-reference.pdf',
    'poker-dice-ranking-reference.pdf',
    'beat-that-reference.pdf',
    'aces-in-the-pot-reference.pdf',
    'cee-lo-ranking-reference.pdf',
    'left-center-right-reference.pdf',
    'help-your-neighbor-reference.pdf',
    'liars-dice-reference.pdf',
    'crazy-eights-reference.pdf',
    'spoons-reference.pdf',
    'speed-reference.pdf',
    'spit-reference.pdf',
    'shithead-variant-worksheet.pdf',
    'bs-cheat-reference.pdf',
    'president-reference.pdf',
    'kemps-reference.pdf',
    'egyptian-rat-screw-reference.pdf',
    'spider-solitaire-reference.pdf',
    'twenty-one-dice-blackjack-reference.pdf',
    'mexico-reference.pdf',
    'bar-dice-ranking-reference.pdf',
    'durak-reference.pdf',
    'thirty-one-reference.pdf',
    'kings-in-the-corner-reference.pdf',
    'chase-the-ace-reference.pdf',
    'poker-hand-ranking-reference.pdf',
    'indian-poker-reference.pdf',
    'klondike-solitaire-reference.pdf',
    'freecell-reference.pdf',
    'pyramid-solitaire-reference.pdf',
    'accordion-solitaire-reference.pdf',
    'clock-solitaire-reference.pdf',
    'golf-solitaire-reference.pdf',
    'canfield-solitaire-reference.pdf',
    'cho-han-reference.pdf',
    'mao-starter-reference.pdf',
    'slapjack-reference.pdf',
    'ninety-nine-reference.pdf',
    'in-between-reference.pdf',
    'knockout-whist-reference.pdf',
]

BUNDLES = {
    'reusable-boards-mats-and-tracks-bundle.pdf': REUSABLE_PRINTABLES,
    'reference-printables-bundle.pdf': REFERENCE_PRINTABLES,
    'write-on-score-sheets-bundle.pdf': WRITE_ON_PRINTABLES,
}


def append_pdf(writer: PdfWriter, filename: str) -> int:
    path = PRINTABLES / filename
    if not path.exists():
        raise FileNotFoundError(f'Missing printable: {filename}')
    reader = PdfReader(str(path))
    for page in reader.pages:
        writer.add_page(page)
    return len(reader.pages)


def make_bundle(output_name: str, filenames: list[str]) -> tuple[Path, int]:
    writer = PdfWriter()
    pages = 0
    for filename in filenames:
        pages += append_pdf(writer, filename)
    out_path = OUT / output_name
    with out_path.open('wb') as f:
        writer.write(f)
    return out_path, pages


def validate_inventory() -> None:
    all_bundle_files = REUSABLE_PRINTABLES + REFERENCE_PRINTABLES + WRITE_ON_PRINTABLES
    duplicates = sorted({name for name in all_bundle_files if all_bundle_files.count(name) > 1})
    if duplicates:
        raise SystemExit('Duplicate bundle entries: ' + ', '.join(duplicates))
    root_pdfs = sorted(p.name for p in PRINTABLES.glob('*.pdf'))
    missing_from_bundles = sorted(set(root_pdfs) - set(all_bundle_files))
    extra_in_bundles = sorted(set(all_bundle_files) - set(root_pdfs))
    if missing_from_bundles or extra_in_bundles:
        raise SystemExit(
            'Bundle inventory mismatch. '
            f'Missing from bundles: {missing_from_bundles}; extra in bundles: {extra_in_bundles}'
        )


def main() -> None:
    validate_inventory()
    for output_name, filenames in BUNDLES.items():
        out_path, pages = make_bundle(output_name, filenames)
        print(f'{out_path.relative_to(ROOT)}: {len(filenames)} files, {pages} pages')


if __name__ == '__main__':
    main()
