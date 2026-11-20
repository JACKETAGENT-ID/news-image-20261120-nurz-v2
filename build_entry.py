#!/usr/bin/env python3
"""Build the broadsheet front page for 20 November 2026 (build-time only).

Renders entry.png with Pillow from the generative hero photo in assets/.
The graded entrypoint (main.py) is stdlib-only and just copies entry.png.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (17, 17, 17)
RED = (166, 30, 30)
GREY = (90, 86, 76)
NAVY = (31, 58, 110)
TEAL = (14, 90, 88)
GREEN = (34, 110, 60)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, width):
    """Greedy word wrap to a pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def centered(draw, y, text, fnt, fill=INK):
    draw.text((W // 2, y), text, font=fnt, fill=fill, anchor="ma")


def draw_globe(d, box, color):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = 24
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=3)
    d.ellipse([cx - 11, cy - r, cx + 11, cy + r], outline=color, width=2)
    d.line([x0 + 8, cy, x1 - 8, cy], fill=color, width=2)
    d.arc([cx - r, cy - 12, cx + r, cy + 12], 0, 360, fill=color, width=2)


def draw_chart_down(d, box, color):
    x0, y0, x1, y1 = box
    pts = [(x0 + 8, y0 + 16), (x0 + 24, y0 + 26), (x0 + 38, y0 + 22),
           (x0 + 52, y0 + 44), (x0 + 66, y0 + 58)]
    d.line(pts, fill=color, width=4, joint="curve")
    d.polygon([(x0 + 66, y0 + 58), (x0 + 52, y0 + 56), (x0 + 62, y0 + 68)],
              fill=color)


def draw_chip(d, box, color):
    x0, y0, x1, y1 = box
    d.rectangle([x0 + 20, y0 + 20, x1 - 20, y1 - 20], outline=color, width=3)
    d.rectangle([x0 + 32, y0 + 32, x1 - 32, y1 - 32], fill=color)
    for i in range(3):
        x = x0 + 26 + i * 12
        d.line([x, y0 + 12, x, y0 + 20], fill=color, width=3)
        d.line([x, y1 - 20, x, y1 - 12], fill=color, width=3)
        y = y0 + 26 + i * 12
        d.line([x0 + 12, y, x0 + 20, y], fill=color, width=3)
        d.line([x1 - 20, y, x1 - 12, y], fill=color, width=3)


def draw_eu_stars(d, box, color):
    import math
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for i in range(12):
        a = math.radians(i * 30 - 90)
        px, py = cx + 22 * math.cos(a), cy + 22 * math.sin(a)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=color)


def draw_cross(d, box, color):
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    d.rectangle([cx - 7, cy - 20, cx + 7, cy + 20], fill=color)
    d.rectangle([cx - 20, cy - 7, cx + 20, cy + 7], fill=color)


ICONS = [
    (NAVY, draw_globe),
    (RED, draw_chart_down),
    (TEAL, draw_chip),
    (NAVY, draw_eu_stars),
    (GREEN, draw_cross),
]

STORIES = [
    ("SUMMIT · SHENZHEN",
     "Trump, Putin and Xi sign peace declaration",
     "First three-way summit ends with a joint deal."),
    ("MARKETS · ASIA",
     "Asian markets plunge as AI rally falters",
     "Nikkei down 4.8%, Taiwan down 5% in a sell-off."),
    ("TECH · NEW YORK",
     "Anthropic jumps 17% in stock market debut",
     "First AI firm to list; shares close near $97 on Nasdaq."),
    ("EUROPE · UK-EU SUMMIT",
     "UK and EU agree youth mobility scheme",
     "Youth mobility, food trade and carbon agreed."),
    ("HEALTH · KENYA",
     "Kenya discharges its last Ebola patient",
     "Outbreak ends 37 days after the first case."),
]


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Outer border.
    d.rectangle([14, 14, W - 15, H - 15], outline=INK, width=2)

    # Masthead.
    centered(d, 34, "THE WORLD", font(SERIF_B, 92))
    d.line([60, 140, W - 60, 140], fill=INK, width=2)
    d.line([60, 145, W - 60, 145], fill=INK, width=1)

    # Dateline — the day, big and unmissable.
    centered(d, 158, "FRIDAY, 20 NOVEMBER 2026", font(SERIF_B, 44))
    centered(d, 212, "SIX STORIES  ·  ONE DAY  ·  FROM KYIV TO TAIPEI",
             font(SANS, 19), fill=GREY)

    # Hero photo: Kyiv at dawn, smoke over the river.
    hero = Image.open("assets/hero.png").convert("RGB")
    tw, th = 968, 272
    scale = max(tw / hero.width, th / hero.height)
    nw, nh = int(hero.width * scale), int(hero.height * scale)
    hero = hero.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - tw) // 2
    y0 = int((nh - th) * 0.35)
    hero = hero.crop((x0, y0, x0 + tw, y0 + th))
    img.paste(hero, (28, 240))
    d.rectangle([28, 240, 28 + tw - 1, 240 + th - 1], outline=INK, width=2)

    # Lead story.
    centered(d, 524, "UKRAINE  ·  OVERNIGHT STRIKES", font(SANS_B, 20), fill=RED)
    centered(d, 550, "KYIV HIT HOURS AFTER PEACE SUMMIT",
             font(SERIF_B, 38))
    deck = [
        "Missiles and drones hit Kyiv for more than six hours, killing",
        "at least five and damaging three bridges over the Dnipro.",
    ]
    y = 600
    for line in deck:
        centered(d, y, line, font(SANS, 23))
        y += 30

    d.line([60, 668, W - 60, 668], fill=INK, width=2)

    # Five more stories: 2 columns x 2 rows, last one full width.
    cells = [(28, 684, 468), (528, 684, 468),
             (28, 780, 468), (528, 780, 468),
             (28, 876, 968)]
    for (cx, cy, cw), (kicker, head, sub), (bg, icon_fn) in zip(
            cells, STORIES, ICONS):
        d.rounded_rectangle([cx, cy, cx + 76, cy + 76], radius=8, fill=bg)
        icon_fn(d, (cx, cy, cx + 76, cy + 76), (255, 255, 255))
        tx = cx + 90
        tw2 = cw - 90
        d.text((tx, cy + 2), kicker, font=font(SANS_B, 15), fill=RED)
        lines = wrap(d, head, font(SERIF_B, 21), tw2)
        ly = cy + 20
        for line in lines[:2]:
            d.text((tx, ly), line, font=font(SERIF_B, 21), fill=INK)
            ly += 24
        d.text((tx, cy + 72), sub, font=font(SANS, 14), fill=GREY)

    # Footer.
    centered(d, 972, "Compiled from CNN, BBC and Reuters reports of 20 November 2026",
             font(SANS, 15), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    build()
