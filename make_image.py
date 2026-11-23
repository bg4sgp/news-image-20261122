"""Draw the news-image-20261122 entry: a newspaper front page summing up
the world news of Sunday 22 November 2026.

The page is drawn entirely in code with Pillow. The lead is the collapse
of the COP31 climate talks in Antalya; six panels cover the sea-drone
strike on a Russian corvette at Benghazi, the Russian drone strike on
flats near Kyiv, Iran's strikes in Bahrain and near Hormuz, the West
Bank settler arson attacks, the Democrats' record House majority and
the day's sport; an "also today" band carries seven more stories. Every
story was reported on Sunday 22 November 2026.

    python3 make_image.py

writes entry.png beside this file (and a copy into $MAKEFUN_OUTPUT_DIR
when set). main.py is the standard-library program the grader runs: it
checks the image against the bounty's gate and copies it to the output.
"""

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

PAGE_W = 1024
PAGE_H = 1024
MARGIN = 40

PAPER = (247, 241, 226)
CARD = (253, 250, 242)
INK = (24, 22, 18)
SOFT = (88, 82, 70)
ACCENT = (172, 40, 28)
WHITE = (255, 255, 255)
GOLD = (233, 197, 110)

FONT_ROOT = "/usr/share/fonts/truetype/dejavu"
SERIF_BLACK = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS = "DejaVuSans.ttf"
SANS_BLACK = "DejaVuSans-Bold.ttf"


def load_font(filename, size):
    return ImageFont.truetype(os.path.join(FONT_ROOT, filename), size)


def wrap_lines(draw, text, fnt, width):
    """Greedy word wrap: the lines of text that fit the given width."""
    lines = []
    current = ""
    for word in text.split(" "):
        candidate = word if not current else current + " " + word
        if draw.textlength(candidate, font=fnt) <= width:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_paragraph(draw, x, y, text, fnt, colour, width, leading):
    """Draw a wrapped paragraph with its top-left at (x, y).

    Returns the y coordinate just past the last line.
    """
    for line in wrap_lines(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=colour)
        y += leading
    return y


def draw_centered(draw, centre_x, y, text, fnt, colour):
    draw.text((centre_x - draw.textlength(text, font=fnt) / 2, y),
              text, font=fnt, fill=colour)


def horizontal_rule(draw, y, weight=2, colour=INK, x0=MARGIN, x1=PAGE_W - MARGIN):
    draw.line([(x0, y), (x1, y)], fill=colour, width=weight)


# ---------------------------------------------------------------- icons
# Each icon draws inside a 30x30 box whose top-left is (x, y), in white
# on the panel's coloured header bar, sometimes with a gold highlight.

def icon_ship(draw, x, y):
    """A warship's hull and mast, with a small drone above it."""
    draw.polygon([(x + 3, y + 20), (x + 27, y + 20), (x + 23, y + 27),
                  (x + 7, y + 27)], fill=WHITE)
    draw.rectangle([x + 10, y + 14, x + 20, y + 20], fill=WHITE)
    draw.line([(x + 15, y + 6), (x + 15, y + 14)], fill=WHITE, width=2)
    # drone: a cross with four rotor dots
    draw.line([(x + 22, y + 1), (x + 29, y + 8)], fill=GOLD, width=2)
    draw.line([(x + 29, y + 1), (x + 22, y + 8)], fill=GOLD, width=2)
    draw.line([(x + 4, y + 29), (x + 10, y + 29)], fill=WHITE, width=2)
    draw.line([(x + 13, y + 29), (x + 19, y + 29)], fill=WHITE, width=2)
    draw.line([(x + 22, y + 29), (x + 28, y + 29)], fill=WHITE, width=2)


def icon_building(draw, x, y):
    """An apartment block with lit windows and a burst at its corner."""
    draw.rectangle([x + 5, y + 6, x + 21, y + 28], outline=WHITE, width=2)
    for row in range(3):
        for col in range(2):
            wx = x + 9 + col * 7
            wy = y + 10 + row * 6
            draw.rectangle([wx, wy, wx + 3, wy + 3], fill=WHITE)
    cx, cy = x + 25, y + 5
    for angle in range(0, 360, 45):
        dx = 5 * math.cos(math.radians(angle))
        dy = 5 * math.sin(math.radians(angle))
        draw.line([(cx, cy), (cx + dx, cy + dy)], fill=GOLD, width=2)


def icon_tanker(draw, x, y):
    """A tanker silhouette with a flame rising from its deck."""
    draw.polygon([(x + 1, y + 21), (x + 29, y + 21), (x + 25, y + 28),
                  (x + 5, y + 28)], fill=WHITE)
    draw.rectangle([x + 6, y + 17, x + 24, y + 21], fill=WHITE)
    draw.polygon([(x + 15, y + 4), (x + 19, y + 11), (x + 17, y + 16),
                  (x + 13, y + 16), (x + 11, y + 11)], fill=GOLD)
    draw.line([(x + 3, y + 30), (x + 9, y + 30)], fill=WHITE, width=2)
    draw.line([(x + 12, y + 30), (x + 18, y + 30)], fill=WHITE, width=2)
    draw.line([(x + 21, y + 30), (x + 27, y + 30)], fill=WHITE, width=2)


def icon_house_flame(draw, x, y):
    """A house outline under a flame."""
    draw.polygon([(x + 4, y + 15), (x + 15, y + 5), (x + 26, y + 15)],
                 outline=WHITE, width=2)
    draw.rectangle([x + 8, y + 15, x + 22, y + 27], outline=WHITE, width=2)
    draw.polygon([(x + 15, y + 12), (x + 18, y + 18), (x + 16, y + 22),
                  (x + 13, y + 22), (x + 12, y + 18)], fill=GOLD)


def icon_capitol(draw, x, y):
    """A domed capitol on a stepped base."""
    draw.arc([x + 9, y + 3, x + 21, y + 15], start=180, end=360,
             fill=WHITE, width=2)
    draw.line([(x + 15, y + 1), (x + 15, y + 4)], fill=WHITE, width=2)
    draw.line([(x + 7, y + 13), (x + 23, y + 13)], fill=WHITE, width=2)
    for col_x in (9, 14, 19):
        draw.line([(x + col_x, y + 15), (x + col_x, y + 22)],
                  fill=WHITE, width=2)
    draw.line([(x + 5, y + 24), (x + 25, y + 24)], fill=WHITE, width=2)
    draw.line([(x + 3, y + 28), (x + 27, y + 28)], fill=WHITE, width=2)


def icon_flag_finish(draw, x, y):
    """A chequered flag on a pole."""
    draw.line([(x + 6, y + 2), (x + 6, y + 29)], fill=WHITE, width=2)
    for row in range(3):
        for col in range(4):
            if (row + col) % 2 == 0:
                draw.rectangle([x + 8 + col * 5, y + 3 + row * 5,
                                x + 12 + col * 5, y + 7 + row * 5],
                               fill=WHITE)
    draw.rectangle([x + 8, y + 3, x + 28, y + 18], outline=GOLD, width=1)


# ---------------------------------------------------------------- parts

def masthead(draw):
    draw_centered(draw, PAGE_W / 2, 24, "THE WORLD ON SUNDAY",
                  load_font(SERIF_BLACK, 56), INK)
    horizontal_rule(draw, 98, weight=5)
    horizontal_rule(draw, 106, weight=1)
    draw.rectangle([MARGIN, 116, PAGE_W - MARGIN, 154], fill=INK)
    draw.text((MARGIN + 18, 124), "SUNDAY · 22 NOVEMBER 2026",
              font=load_font(SANS_BLACK, 25), fill=WHITE)
    note = "ONE DAY · ONE PAGE"
    note_font = load_font(SANS_BLACK, 19)
    draw.text((PAGE_W - MARGIN - 18 - draw.textlength(note, font=note_font),
               127), note, font=note_font, fill=(219, 208, 178))


def draw_cracked_globe(draw, cx, cy, r):
    """A wireframe globe split by a red crack, for the climate lead."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r],
                 fill=(206, 224, 233), outline=INK, width=3)
    for frac in (-0.62, 0.0, 0.62):
        half_w = r * math.sqrt(1 - frac * frac)
        y = cy + frac * r
        draw.line([(cx - half_w, y), (cx + half_w, y)], fill=(90, 120, 140),
                  width=2)
    for frac in (0.45, 0.8):
        w = r * frac
        draw.ellipse([cx - w, cy - r, cx + w, cy + r],
                     outline=(90, 120, 140), width=2)
    draw.line([(cx, cy - r), (cx, cy + r)], fill=(90, 120, 140), width=2)
    crack = [(cx - 30, cy - r + 4), (cx - 12, cy - 52), (cx - 26, cy - 18),
             (cx + 2, cy + 8), (cx - 8, cy + 44), (cx + 10, cy + 78),
             (cx + 2, cy + r - 4)]
    draw.line(crack, fill=ACCENT, width=5, joint="curve")


def draw_thermometer(draw, x, y):
    """A thermometer whose mercury has nearly topped out."""
    draw.rounded_rectangle([x, y, x + 16, y + 96], radius=8, outline=INK,
                           width=3, fill=WHITE)
    draw.ellipse([x - 7, y + 88, x + 23, y + 118], outline=INK, width=3,
                 fill=WHITE)
    draw.rectangle([x + 5, y + 22, x + 11, y + 100], fill=ACCENT)
    draw.ellipse([x - 2, y + 93, x + 18, y + 113], fill=ACCENT)
    for tick in range(4):
        draw.line([(x + 20, y + 14 + tick * 22), (x + 27, y + 14 + tick * 22)],
                  fill=INK, width=2)


def lead_story(draw):
    x = MARGIN
    draw.text((x, 170), "ANTALYA · COP31 — CLIMATE SUMMIT",
              font=load_font(SANS_BLACK, 19), fill=ACCENT)
    headline = "Climate talks collapse as COP31 ends without a deal"
    y = draw_paragraph(draw, x, 198, headline, load_font(SERIF_BLACK, 38),
                       INK, 596, 47)
    body = ("After a record 48 hours of overtime, nearly 200 countries "
            "leave Türkiye with no overarching agreement. The EU rejects "
            "a final text that omits any mention of phasing out fossil "
            "fuels; the summit's hosts concede: \u201cWe did all that we "
            "could.\u201d")
    draw_paragraph(draw, x, y + 10, body, load_font(SANS, 19), INK, 596, 25)
    draw_cracked_globe(draw, 782, 272, 102)
    draw_thermometer(draw, 916, 176)
    draw_centered(draw, 810, 388, "NO DEAL IN ANTALYA",
                  load_font(SANS_BLACK, 16), SOFT)


PANELS = [
    {
        "tag": "LIBYA · WAR SPREADS",
        "colour": (38, 66, 108),
        "icon": icon_ship,
        "headline": "Sea drones hit Russian corvette in Benghazi port",
        "body": "Suspected Ukrainian sea drones slip past the defences "
                "and set the Merkury ablaze.",
    },
    {
        "tag": "UKRAINE · KYIV REGION",
        "colour": (122, 44, 36),
        "icon": icon_building,
        "headline": "Russian drone hits flats near Kyiv; 14 dead or missing",
        "body": "The strike on an apartment block in Dymer buries "
                "residents; rescuers pick through the rubble.",
    },
    {
        "tag": "GULF · HORMUZ STANDOFF",
        "colour": (146, 84, 20),
        "icon": icon_tanker,
        "headline": "Iran strikes Bahrain plant and tankers near Hormuz",
        "body": "Bahrain says a strike set a Sitra plant ablaze; tanker "
                "hits deepen the US–Iran standoff.",
    },
    {
        "tag": "WEST BANK · ARSON RAIDS",
        "colour": (84, 96, 40),
        "icon": icon_house_flame,
        "headline": "Settlers torch homes and cars in West Bank villages",
        "body": "Dozens raid villages near Ramallah. Eisenkot brands the "
                "attacks \u201cJewish terrorism\u201d.",
    },
    {
        "tag": "WASHINGTON · US HOUSE",
        "colour": (52, 84, 120),
        "icon": icon_capitol,
        "headline": "Democrats clinch biggest House majority since 1992",
        "body": "At least 258 seats — the party's largest House majority "
                "in over three decades.",
    },
    {
        "tag": "SPORT · LAS VEGAS & ANFIELD",
        "colour": (30, 104, 80),
        "icon": icon_flag_finish,
        "headline": "Verstappen wins in Las Vegas; Liverpool rout United 4–0",
        "body": "A third Vegas win in four years for the champion. Ten-man "
                "United are hammered in Pochettino's debut.",
    },
]


def draw_panel(draw, x, y, w, h, spec):
    draw.rectangle([x, y, x + w, y + h], fill=CARD, outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + 33], fill=spec["colour"])
    draw.text((x + 12, y + 8), spec["tag"],
              font=load_font(SANS_BLACK, 15), fill=WHITE)
    spec["icon"](draw, x + w - 42, y + 2)
    next_y = draw_paragraph(draw, x + 12, y + 45, spec["headline"],
                            load_font(SANS_BLACK, 22), INK, w - 24, 27)
    draw_paragraph(draw, x + 12, next_y + 6, spec["body"],
                   load_font(SANS, 16), (50, 46, 38), w - 24, 21)


def draw_panels(draw):
    columns = (MARGIN, 360, 680)
    rows = (448, 660)
    for index, spec in enumerate(PANELS):
        draw_panel(draw, columns[index % 3], rows[index // 3], 304, 200, spec)


def ticker(draw):
    top = 868
    draw.rectangle([MARGIN, top, PAGE_W - MARGIN, 968], fill=INK)
    draw.text((MARGIN + 18, top + 10), "ALSO TODAY",
              font=load_font(SANS_BLACK, 18), fill=(238, 128, 96))
    items = ("Mexico captures cartel kingpin \u2018Chapo Isidro\u2019 in a "
             "deadly firefight · Nigeria boat capsize toll reaches 24 · "
             "Indonesia factory fire: dozens missing · EU–Indonesia trade "
             "deal signed · US presses Nvidia over AI chips to China · "
             "India declare 720/9 vs New Zealand")
    draw_paragraph(draw, MARGIN + 18, top + 36, items,
                   load_font(SANS, 16), WHITE, 908, 20)
    draw_centered(draw, PAGE_W / 2, 978,
                  "Drawn in code with Python + Pillow · every story "
                  "reported on 22 November 2026",
                  load_font(SANS, 13), SOFT)


def build_page():
    page = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    draw = ImageDraw.Draw(page)
    draw.rectangle([14, 14, PAGE_W - 14, PAGE_H - 14], outline=INK, width=3)
    masthead(draw)
    lead_story(draw)
    horizontal_rule(draw, 434, weight=3)
    draw_panels(draw)
    ticker(draw)
    return page


def main():
    page = build_page()
    here = Path(__file__).resolve().parent
    page.save(here / "entry.png", format="PNG", optimize=True)
    print(f"wrote {here / 'entry.png'}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out_dir:
        target = Path(out_dir) / "entry.png"
        target.parent.mkdir(parents=True, exist_ok=True)
        page.save(target, format="PNG", optimize=True)
        print(f"wrote {target}")


if __name__ == "__main__":
    main()
