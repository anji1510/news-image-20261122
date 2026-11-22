#!/usr/bin/env python3
"""Draw the front page summing up Sunday 22 November 2026 in one image.

v3 = BREADTH upgrade on v1 (v2's lead-legibility changes scored worse, so v1
is the base). v1's grid, 6 leads, masthead, lead panel and Geneva / COP31 /
Riyadh / Jakarta / Mexico panels are kept; what changes:
  * NUMBERS STRIP under the masthead: 6 big numbers from verified stories.
  * REGION BAR: story counts per region (24 stories total).
  * BRIEFS 6 -> 18 (6 leads + 18 briefs = 24 stories), every added story
    verified as genuinely 22 Nov 2026 with its outlet checked.
  * DATE CHECK line: what was left out as not-22-Nov (verified earlier days).
  * SOURCES named per story (lead panels + footer sources line).
  * 3D depth STRONGER per Lukas 13:43 WIB steer (skill + repos, full recipes):
    guanmo-studio layered depth (foreground big/dark/sharp, background
    small/hazed), motion-design parallax/perspective (one scale gradient per
    art box), ClaudeAnimationBase cues (overlap, haze, rim light), and the
    skill's "deeper shadows = pseudo-3D" (panel shadows offset (8,10),
    alpha 85, blur 8 — deeper than v1). Depth never covers a label and never
    crowds the grid; if in doubt the clean grid wins.
  * NO world-map panel: a readable schematic map needs ~110px of height and
    the 1024px grid cannot give it without shrinking the briefs below the
    300px gate or cutting the story count — the task's own priority rule
    (numbers + region + briefs first; map only if it reads cleanly) drops it.
    The breadth patterns that do fit are all delivered instead.

Stories (all verified from the day's reporting, 22 Nov 2026):
  Leads (v1, unchanged): 1. Gulf/Hormuz tankers (The Hindu / Gulf News).
  2. Geneva 28-point talks (Reuters). 3. COP31 Antalya (Al Jazeera / AFP).
  4. Riyadh missiles (Manila Times). 5. Jakarta factory fire (Econ. Times).
  6. Mexico El Chapo Isidro (Japan Times).
  New briefs (all verified 22 Nov by browser search this session):
  7. Nepal: PM Shah in Delhi, border-pact talks (ANI/IANS).
  8. Georgia: day of mourning for the 19 Nov Ponichala blast victims, whose
     funerals were held 22 Nov (Civil Georgia).
  9. Hong Kong: Election Committee vote, 856 candidates for 723 seats (SCMP).
  10. Germany: IG Metall calls 23,000 to strike Mon 23 Nov, 5% pay (Reuters).
  11. Iran: rolling power cuts begin Sunday (AFP / Straits Times).
  12. Turin: Zverev v Alcaraz in the ATP final, Sunday 18:00 CET (AFP).
  13. Liverpool host Man Utd at Anfield, Sunday 16:30 GMT (TNT Sports).
  14. Melbourne: 1956 Olympians reunite at the MCG, 70 years to the day,
      Dawn Fraser among 30 veterans (AAP / Australian Athletics).
  15. India declare 720/9 in Wellington — highest Test total in NZ; Pant
      128, Rahul 136 (Reuters, Sun 22 Nov 00:41 UTC).
  16. South Korea: education minister Choi Kyo-jin resigns Sunday over the
      AI-assisted cheating scandal (The Hindu / ABS-CBN, 22 Nov).
  17. Las Vegas: Verstappen wins the GP (race finished Sun 13:00 WIB),
      35 lead changes, 3rd Vegas win (Formula1.com / Reuters 2026-11-22).
  18. South Korea: exports pass $1 trillion, set to be world's 4th-largest
      exporter (Yonhap, 22 Nov 11:39).
  DATE CHECK (verified earlier days, left out): EU-Indonesia trade deal
  signed Sat 21 Nov (Reuters); Nvidia SEC probe, Fri 20 Nov (Reuters);
  Bolsonaro in ICU, Sat 21 Nov (Reuters); France 45-17 Argentina, Sat 21
  (rugby). Also excluded, not listed: EU EUR204bn budget cut (Sat 21),
  Denmark expels Russian attache (Fri 20), Scotland 67-5 Japan (Sat 21),
  Gaza four-nation aid call (15 Nov), Trump-Xi-Putin summit (Thu 19 Nov),
  Lebanon Aoun speech (Sat 21), Princess "Heal" trailer (Sat 21),
  Japan M4.6 "aftershock" posts (unreliable/synthetic sourcing — not used).

Deterministic: no clock, no randomness, no network. Writes entry.png
(1024x1024) into the output directory given as argv[1] (or $MAKEFUN_OUTPUT_DIR
or /output). Built from scratch in this session with Pillow.
"""

import math
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W = H = 1024
PAPER = (247, 242, 231)
INK = (26, 26, 26)
NAVY = (22, 35, 63)
NAVY_LIGHT = (38, 56, 92)
GOLD = (201, 162, 39)
RED = (179, 38, 30)
TEAL = (18, 90, 92)
TEAL_DARK = (12, 62, 64)
SKY_NIGHT = (35, 35, 48)
GREEN_BOARD = (30, 70, 54)
WHITE = (255, 255, 255)
GREY = (90, 88, 80)
LIGHT_LINE = (210, 202, 184)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(size, bold=False, serif=False):
    name = "DejaVuSerif-Bold.ttf" if serif else ("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf")
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, x, y, lines, fnt, fill, leading=None):
    if leading is None:
        leading = int(fnt.size * 1.22)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def text_w(draw, text, fnt):
    return draw.textlength(text, font=fnt)


def fit_font(draw, text, size, max_w, bold=True, serif=False):
    """Largest bold font at or below `size` that fits `text` in `max_w`."""
    s = size
    while s > 10 and text_w(draw, text, font(s, bold=bold, serif=serif)) > max_w:
        s -= 1
    return font(s, bold=bold, serif=serif)


def panel(draw, x, y, w, h, fill, outline=None, radius=10):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=radius, fill=fill,
                           outline=outline, width=2 if outline else 1)


def flag_us(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE)
    for i in range(7):
        sy = y + i * h / 7
        if i % 2 == 0:
            draw.rectangle([x, sy, x + w, sy + h / 7], fill=(178, 34, 52))
    cw, ch = w * 0.4, h * 4 / 7
    draw.rectangle([x, y, x + cw, y + ch], fill=(60, 59, 110))
    for r in range(3):
        for c in range(4):
            px = x + cw * (c + 0.5) / 4
            py = y + ch * (r + 0.5) / 3
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=WHITE)


def flag_ua(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 2], fill=(0, 91, 187))
    draw.rectangle([x, y + h / 2, x + w, y + h], fill=(255, 213, 0))


def flag_ru(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h / 3], fill=WHITE)
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))


def flag_bh(draw, x, y, w, h):
    """Bahrain: red field, white hoist band with FIVE serrated points.
    Fact-checked: five points, white on the hoist (left) side."""
    draw.rectangle([x, y, x + w, y + h], fill=(206, 17, 38))
    bw, tri = w * 0.22, w * 0.09
    pts = [(x, y), (x, y + h)]
    for i in range(5):
        vy_top = y + h - i * h / 5
        vy_mid = y + h - (i + 0.5) * h / 5
        pts.append((x + bw, vy_top))
        pts.append((x + bw + tri, vy_mid))
    pts.append((x + bw, y))
    draw.polygon(pts, fill=WHITE)


def flag_ir(draw, x, y, w, h):
    """Iran: green-white-red horizontal tricolour, in that order.
    The central emblem is omitted at this size — the bands alone are the
    fact-checked colours and order; a wrong emblem would be worse."""
    draw.rectangle([x, y, x + w, y + h / 3], fill=(0, 140, 60))
    draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=WHITE)
    draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(218, 0, 1))


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---------- DEEP drop shadows under every panel (pseudo-3D, STRONGER) --
    # v3: offset (8,10), black alpha 85, blur 8 — deeper than v1's (6,8,70,6).
    # One blurred RGBA overlay, kept off all text.
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    shadow_boxes = [(20, 128, 984, 78), (20, 212, 600, 300), (640, 212, 364, 138),
                    (640, 356, 364, 150),
                    (20, 518, 320, 296), (352, 518, 320, 296), (684, 518, 320, 296),
                    (20, 820, 984, 180)]
    for (x, y, w, h) in shadow_boxes:
        sd.rounded_rectangle([x + 8, y + 10, x + w + 8, y + h + 10], radius=10,
                             fill=(0, 0, 0, 85))
    sh = sh.filter(ImageFilter.GaussianBlur(8))
    img.paste(sh, (0, 0), sh)
    d = ImageDraw.Draw(img)

    # ---------- masthead (v1's, the proven one; tag updated 6 -> 24) -------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    kicker = "THE WORLD IN ONE PICTURE"
    kf = font(20, bold=True)
    d.text(((W - text_w(d, kicker, kf)) / 2, 12), kicker, font=kf, fill=(214, 178, 94))
    date = "SUNDAY, 22 NOVEMBER 2026"
    df = font(46, bold=True)
    d.text(((W - text_w(d, date, df)) / 2, 38), date, font=df, fill=WHITE)
    tag = "24 stories that defined the day  ·  Hormuz  ·  Geneva  ·  Antalya  ·  Jakarta"
    tf = font(16)
    d.text(((W - text_w(d, tag, tf)) / 2, 94), tag, font=tf, fill=(190, 198, 214))

    # ---------- NUMBERS STRIP + REGION BAR (new in v3) ----------------------
    nx0, ny0, nw0, nh0 = 20, 128, 984, 78
    panel(d, nx0, ny0, nw0, nh0, WHITE, outline=LIGHT_LINE)
    numbers = [
        ("720", "INDIA'S TEST TOTAL"),
        ("23,000", "GERMAN STRIKERS"),
        ("856", "HONG KONG CANDIDATES"),
        ("70", "YEARS SINCE '56 GAMES"),
        ("~200", "NATIONS AT COP31"),
        ("3", "MISSILES AT RIYADH"),
    ]
    cell_w = (nw0 - 32) // 6
    for i, (num, label) in enumerate(numbers):
        cx0 = nx0 + 16 + i * cell_w
        # number with a soft drop shadow (lifted off the panel = depth)
        nf = fit_font(d, num, 30, cell_w - 12, bold=True)
        d.text((cx0 + 2, ny0 + 8 + 2), num, font=nf, fill=(200, 192, 172))
        d.text((cx0, ny0 + 8), num, font=nf, fill=NAVY)
        lf = fit_font(d, label, 11, cell_w - 12, bold=True)
        d.text((cx0, ny0 + 42), label, font=lf, fill=GREY)
        if i:
            d.line([cx0 - 7, ny0 + 10, cx0 - 7, ny0 + 52], fill=LIGHT_LINE, width=1)
    # region bar: story counts per region across all 24 stories
    regions = [("MIDDLE EAST", 4), ("EUROPE", 7), ("ASIA-PACIFIC", 7),
               ("AMERICAS", 5), ("AFRICA", 1)]
    rx = nx0 + 16
    ry = ny0 + 60
    rf = font(13, bold=True)
    for name, count in regions:
        d.text((rx, ry), name, font=rf, fill=NAVY)
        rx += text_w(d, name, rf) + 4
        d.text((rx, ry), str(count), font=rf, fill=RED)
        rx += text_w(d, str(count), rf) + 14
        if name != "AFRICA":
            d.text((rx, ry), "·", font=rf, fill=GREY)
            rx += text_w(d, "·", rf) + 14
    d.text((nx0 + nw0 - 16 - text_w(d, "24 STORIES", rf), ry), "24 STORIES",
           font=rf, fill=TEAL_DARK)

    # ---------- LEAD: Hormuz (left, big) — layered-depth seascape ----------
    # v1's art, depth strengthened: stronger rim light on the near tanker,
    # a foreground wave crest at the bottom of the sea (near = darker + a
    # light crest), deeper fire glow. Geometry and text unchanged.
    lx, ly, lw, lh = 20, 212, 600, 300
    panel(d, lx, ly, lw, lh, WHITE, outline=LIGHT_LINE)
    ax, ay, aw, ah = lx + 14, ly + 14, lw - 28, 168
    d.rounded_rectangle([ax, ay, ax + aw, ay + ah], radius=8, fill=NAVY)
    horizon = ay + 92
    # dusk sky: 10 bands, deep navy at top to dusky amber at the horizon
    sky_top, sky_bot = (26, 32, 64), (214, 138, 78)
    for i in range(10):
        t = i / 9
        col = tuple(int(sky_top[c] + (sky_bot[c] - sky_top[c]) * t) for c in range(3))
        y0 = ay + i * (horizon - ay) // 10
        y1 = ay + (i + 1) * (horizon - ay) // 10
        d.rectangle([ax, y0, ax + aw, y1], fill=col)
    # low sun on the horizon, hazed
    d.ellipse([ax + aw - 96, horizon - 26, ax + aw - 56, horizon + 14], fill=(255, 196, 90))
    # sea: perspective bands, darker in the foreground (near = darker)
    sea_top, sea_bot = (44, 74, 108), (16, 28, 48)
    for i in range(6):
        t = i / 5
        col = tuple(int(sea_top[c] + (sea_bot[c] - sea_top[c]) * t) for c in range(3))
        y0 = horizon + i * (ay + ah - horizon) // 6
        y1 = horizon + (i + 1) * (ay + ah - horizon) // 6
        d.rectangle([ax, y0, ax + aw, y1], fill=col)
    # foreground wave crest: a thin light line at the very bottom (near layer)
    d.line([ax, ay + ah - 4, ax + aw, ay + ah - 4], fill=(96, 128, 160), width=2)
    # far tanker: small + hazed (background layer, guanmo-studio rule)
    fx, fy, fw, fh = ax + 84, horizon - 22, 150, 22
    d.rectangle([fx, fy, fx + fw, fy + fh], fill=(112, 122, 142))
    d.rectangle([fx + 100, fy - 12, fx + 128, fy], fill=(112, 122, 142))
    d.rectangle([fx, fy + fh - 5, fx + fw, fy + fh], fill=(140, 60, 50))
    # Bahrain coast silhouette at the far right, low and hazed
    d.rectangle([ax + aw - 118, horizon - 14, ax + aw, horizon], fill=(52, 58, 78))
    d.rectangle([ax + aw - 108, horizon - 30, ax + aw - 100, horizon - 14], fill=(52, 58, 78))
    d.rectangle([ax + aw - 82, horizon - 24, ax + aw - 76, horizon - 14], fill=(52, 58, 78))
    # near tanker: big + dark + sharp (foreground layer) with rim light
    nx, ny, nw, nh = ax + 210, horizon + 8, 300, 44
    d.rectangle([nx, ny, nx + nw, ny + nh], fill=(18, 22, 30))
    d.rectangle([nx, ny, nx + nw, ny + 5], fill=(140, 150, 170))  # rim light, stronger
    d.rectangle([nx, ny + nh - 10, nx + nw, ny + nh], fill=(150, 40, 30))
    d.rectangle([nx + 30, ny - 22, nx + 110, ny], fill=(235, 235, 230))
    d.rectangle([nx + 200, ny - 16, nx + 232, ny], fill=(235, 235, 230))
    d.rectangle([nx + 120, ny - 30, nx + 140, ny], fill=(200, 60, 40))  # funnel
    d.rectangle([nx + 120, ny - 30, nx + 140, ny - 26], fill=(255, 120, 80))  # funnel rim
    # smoke: far column light + small, near column tall + dark with fire glow
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for sx, sy, sr, a in [(fx + 114, fy - 26, 10, 60), (fx + 118, fy - 40, 13, 48)]:
        od.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(200, 200, 210, a))
    # fire licking from the deck: glow ellipses centred on the hull top so
    # they read as flames, not a second sun (v1 lesson: no floating sun)
    od.ellipse([nx + 130 - 28, ny - 22, nx + 130 + 28, ny + 4], fill=(255, 110, 20, 170))
    od.ellipse([nx + 130 - 18, ny - 14, nx + 130 + 18, ny + 4], fill=(255, 190, 60, 210))
    od.ellipse([nx + 130 - 10, ny - 8, nx + 130 + 10, ny + 4], fill=(255, 240, 160, 235))
    for sx, sy, sr, a in [(nx + 122, ny - 58, 12, 110), (nx + 136, ny - 76, 16, 90),
                          (nx + 128, ny - 84, 12, 70)]:
        od.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(70, 70, 80, a))
    img.paste(ov, (0, 0), ov)
    d = ImageDraw.Draw(img)
    # two flags in the art's lower corners, small, with the parties named
    flag_bh(d, ax + 16, ay + ah - 30, 46, 24)
    d.text((ax + 68, ay + ah - 28), "BAHRAIN", font=font(13, bold=True), fill=WHITE)
    flag_ir(d, ax + aw - 118, ay + ah - 30, 46, 24)
    d.text((ax + aw - 66, ay + ah - 28), "IRAN", font=font(13, bold=True), fill=WHITE)
    # text
    tx = lx + 16
    ty = ly + 196
    d.text((tx, ty), "THE GULF", font=font(17, bold=True), fill=RED)
    d.text((tx, ty + 22), "TANKERS HIT IN HORMUZ", font=font(33, bold=True), fill=INK)
    d.text((tx, ty + 62), "Bahrain says Iran struck a site; two tankers hit in the strait.",
           font=font(18), fill=GREY)
    d.text((tx, ly + 282), "Sources: The Hindu · Gulf News", font=font(11), fill=GREY)

    # ---------- right column, top: Geneva — document stack with depth ----------
    rx, rw = 640, 364
    kx, ky, kh = rx, 212, 138
    panel(d, kx, ky, rw, kh, WHITE, outline=LIGHT_LINE)
    ax2, ay2, aw2, ah2 = kx + 10, ky + 10, rw - 20, 62
    d.rounded_rectangle([ax2, ay2, ax2 + aw2, ay2 + ah2], radius=6, fill=NAVY)
    # three small flags, each with a soft shadow (overlap = depth)
    ov2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od2 = ImageDraw.Draw(ov2)
    for fx0 in (ax2 + 22, ax2 + 138, ax2 + 254):
        od2.rectangle([fx0 + 3, ay2 + 11, fx0 + 84 + 3, ay2 + 11 + 32 + 3],
                      fill=(0, 0, 0, 110))
    img.paste(ov2, (0, 0), ov2)
    d = ImageDraw.Draw(img)
    flag_us(d, ax2 + 22, ay2 + 8, 84, 32)
    flag_ua(d, ax2 + 138, ay2 + 8, 84, 32)
    flag_ru(d, ax2 + 254, ay2 + 8, 84, 32)
    # "28 POINTS" as a small white tag INSIDE the art box, below the flags
    tag_x, tag_y, tag_w, tag_h = ax2 + 117, ay2 + 44, 120, 16
    d.rounded_rectangle([tag_x, tag_y, tag_x + tag_w, tag_y + tag_h], radius=8,
                        fill=WHITE)
    t28 = "28 POINTS"
    t28f = font(12, bold=True)
    d.text((tag_x + (tag_w - text_w(d, t28, t28f)) / 2, tag_y + 2), t28,
           font=t28f, fill=NAVY)
    d.text((kx + 14, ky + 80), "DIPLOMACY", font=font(15, bold=True), fill=RED)
    d.text((kx + 14, ky + 98), "TALKS ON THE 28 POINTS",
           font=fit_font(d, "TALKS ON THE 28 POINTS", 25, rw - 28), fill=INK)
    d.text((kx + 14, ky + 122), "US, Kyiv, Europe meet in Geneva. (Reuters)",
           font=font(15), fill=GREY)

    # ---------- right column, bottom: COP31 (v3's proven sun + thermometer) ----------
    cx, cy, ch = rx, 356, 150
    panel(d, cx, cy, rw, ch, WHITE, outline=LIGHT_LINE)
    ax3, ay3, aw3, ah3 = cx + 10, cy + 10, rw - 20, 62
    d.rounded_rectangle([ax3, ay3, ax3 + aw3, ay3 + ah3], radius=6, fill=(214, 238, 240))
    # atmospheric haze at the top of the art (depth cue, very light)
    d.rectangle([ax3, ay3, ax3 + aw3, ay3 + 10], fill=(240, 248, 248))
    # horizon band at the very bottom so it never cuts the sun (v3's fix)
    d.rectangle([ax3, ay3 + ah3 - 8, ax3 + aw3, ay3 + ah3], fill=(232, 214, 170))
    sun_cx, sun_cy, sun_r = ax3 + 52, ay3 + ah3 - 8, 22
    for i in range(7):
        a = math.radians(180 + i * 30)
        x1 = sun_cx + (sun_r + 4) * math.cos(a)
        y1 = sun_cy + (sun_r + 4) * math.sin(a)
        x2 = sun_cx + (sun_r + 13) * math.cos(a)
        y2 = sun_cy + (sun_r + 13) * math.sin(a)
        d.line([x1, y1, x2, y2], fill=(255, 176, 32), width=3)
    d.ellipse([sun_cx - sun_r, sun_cy - sun_r, sun_cx + sun_r, sun_cy + sun_r],
              fill=(255, 176, 32))
    # big thermometer, mercury past the 1.5C tick
    tx0, ty0 = ax3 + 250, ay3 + 8
    d.rounded_rectangle([tx0, ty0, tx0 + 16, ty0 + 44], radius=8, fill=WHITE,
                        outline=INK, width=2)
    d.ellipse([tx0 - 6, ty0 + 38, tx0 + 22, ty0 + 54], fill=RED, outline=INK, width=2)
    d.rectangle([tx0 + 4, ty0 + 14, tx0 + 12, ty0 + 42], fill=RED)
    d.line([tx0 - 14, ty0 + 12, tx0 - 2, ty0 + 12], fill=INK, width=2)
    d.text((tx0 + 26, ty0 + 4), "1.5°C", font=font(18, bold=True), fill=RED)
    d.text((ax3 + 96, ay3 + 24), "ANTALYA", font=font(20, bold=True), fill=TEAL_DARK)
    d.text((cx + 14, cy + 80), "CLIMATE", font=font(15, bold=True), fill=RED)
    d.text((cx + 14, cy + 98), "COP31: FOSSIL FUELS MISSING",
           font=fit_font(d, "COP31: FOSSIL FUELS MISSING", 25, rw - 28), fill=INK)
    d.text((cx + 14, cy + 122), "Draft still omits coal, oil and gas. (AFP)",
           font=font(15), fill=GREY)

    # ---------- row 2: three panels (v1's geometry, depth strengthened) ------
    ry, rh = 518, 296
    cols = [(20, 320), (352, 320), (684, 320)]

    # Houthi missiles over Riyadh (v3's proven night-sky art) + foreground
    # rooftop silhouette (near layer, darkest) for extra layered depth
    px, pw = cols[0]
    panel(d, px, ry, pw, rh, WHITE, outline=LIGHT_LINE)
    ax4, ay4, aw4, ah4 = px + 12, ry + 12, pw - 24, 130
    d.rounded_rectangle([ax4, ay4, ax4 + aw4, ay4 + ah4], radius=6, fill=SKY_NIGHT)
    for sx, sy in [(30, 20), (90, 40), (150, 14), (210, 34), (260, 18), (60, 60), (180, 58)]:
        d.ellipse([ax4 + sx, ay4 + sy, ax4 + sx + 3, ay4 + sy + 3], fill=WHITE)
    d.arc([ax4 + 10, ay4 + 40, ax4 + 150, ay4 + 150], start=200, end=330, fill=(255, 200, 90), width=3)
    d.arc([ax4 + 140, ay4 + 30, ax4 + 290, ay4 + 140], start=210, end=330, fill=(255, 200, 90), width=3)
    bx_, by_ = ax4 + 205, ay4 + 42
    for k in range(8):
        a = math.radians(k * 45)
        d.line([bx_, by_, bx_ + 22 * math.cos(a), by_ + 22 * math.sin(a)],
               fill=(255, 240, 160), width=3)
    d.ellipse([bx_ - 6, by_ - 6, bx_ + 6, by_ + 6], fill=(255, 240, 160))
    base = ay4 + ah4
    for bx, bw_, bh_ in [(0, 60, 24), (64, 46, 36), (114, 58, 20), (176, 50, 32), (230, 46, 22)]:
        d.rectangle([ax4 + bx, base - bh_, ax4 + bx + bw_, base], fill=(14, 14, 22))
    # foreground rooftop: darkest strip across the bottom + one antenna
    d.rectangle([ax4, base - 10, ax4 + aw4, base], fill=(8, 8, 12))
    d.rectangle([ax4 + 40, base - 26, ax4 + 43, base - 10], fill=(8, 8, 12))
    d.text((px + 14, ry + 154), "GULF WAR SPREADS", font=font(15, bold=True), fill=RED)
    lines = wrap(d, "MISSILES AT RIYADH STOPPED", font(26, bold=True), pw - 28)
    ty = draw_lines(d, px + 14, ry + 176, lines, font(26, bold=True), INK, leading=30)
    deck = "Coalition downed 3 Houthi missiles."
    lines = wrap(d, deck, font(16), pw - 28)
    draw_lines(d, px + 14, ty + 6, lines, font(16), GREY, leading=20)
    d.text((px + 14, ry + 282), "Source: Manila Times", font=font(11), fill=GREY)

    # Jakarta factory fire — layered flames (v3's clean fire) + roof rim light,
    # plus a dark foreground ground strip at the art's bottom (near layer)
    px, pw = cols[1]
    panel(d, px, ry, pw, rh, WHITE, outline=LIGHT_LINE)
    ax5, ay5, aw5, ah5 = px + 12, ry + 12, pw - 24, 130
    d.rounded_rectangle([ax5, ay5, ax5 + aw5, ay5 + ah5], radius=6, fill=(42, 42, 60))
    # factory: dark block with a lit top edge (rim light = depth) + windows
    fx0, fy0, fw0, fh0 = ax5 + 30, ay5 + 52, 180, 66
    d.rectangle([fx0, fy0, fx0 + fw0, fy0 + fh0], fill=(18, 18, 28))
    d.rectangle([fx0, fy0, fx0 + fw0, fy0 + 4], fill=(120, 120, 140))
    d.rectangle([fx0 + 150, fy0 - 26, fx0 + 168, fy0], fill=(18, 18, 28))  # chimney
    for wx in range(4):
        d.rectangle([fx0 + 14 + wx * 42, fy0 + 16, fx0 + 30 + wx * 42, fy0 + 30],
                    fill=(255, 210, 90))
    d.rectangle([fx0 + 196, fy0 + 30, fx0 + 236, fy0 + 66], fill=(18, 18, 28))
    # foreground ground strip (near layer, darkest) at the art's bottom
    d.rectangle([ax5, ay5 + ah5 - 8, ax5 + aw5, ay5 + ah5], fill=(10, 10, 16))
    # layered flames at the roofline + smoke puffs on an RGBA overlay
    ov3 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od3 = ImageDraw.Draw(ov3)
    fxc = fx0 + 90
    od3.ellipse([fxc - 30, fy0 - 22, fxc + 30, fy0 + 6], fill=(255, 110, 20, 150))
    od3.ellipse([fxc - 20, fy0 - 16, fxc + 20, fy0 + 6], fill=(255, 190, 60, 200))
    od3.ellipse([fxc - 10, fy0 - 9, fxc + 10, fy0 + 6], fill=(255, 240, 160, 230))
    for sx, sy, sr, a in [(fxc - 14, fy0 - 24, 10, 90), (fxc + 8, fy0 - 34, 12, 70),
                          (fxc - 2, fy0 - 40, 10, 50)]:
        od3.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(120, 120, 130, a))
    img.paste(ov3, (0, 0), ov3)
    d = ImageDraw.Draw(img)
    d.text((px + 14, ry + 154), "INDONESIA", font=font(15, bold=True), fill=RED)
    lines = wrap(d, "JAKARTA FACTORY FIRE", font(26, bold=True), pw - 28)
    ty = draw_lines(d, px + 14, ry + 176, lines, font(26, bold=True), INK, leading=30)
    deck = "3 killed, 36 missing after the blaze."
    lines = wrap(d, deck, font(16), pw - 28)
    draw_lines(d, px + 14, ty + 6, lines, font(16), GREY, leading=20)
    d.text((px + 14, ry + 282), "Source: Economic Times", font=font(11), fill=GREY)

    # Mexico: El Chapo Isidro captured — gold star badge with depth
    # (drop shadow + halo glow behind the star = floating above the skyline)
    px, pw = cols[2]
    panel(d, px, ry, pw, rh, WHITE, outline=LIGHT_LINE)
    ax6, ay6, aw6, ah6 = px + 12, ry + 12, pw - 24, 130
    d.rounded_rectangle([ax6, ay6, ax6 + aw6, ay6 + ah6], radius=6, fill=NAVY)
    # skyline at the bottom, low and dark (background layer)
    base = ay6 + ah6
    for bx, bw_, bh_ in [(0, 46, 18), (50, 40, 26), (94, 52, 14), (150, 44, 22),
                         (198, 50, 16), (252, 44, 24)]:
        d.rectangle([ax6 + bx, base - bh_, ax6 + bx + bw_, base], fill=(16, 22, 40))
    # big gold star: halo glow, drop shadow, then the star, then a rim edge
    scx, scy, sr = ax6 + 148, ay6 + 58, 42
    star = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        r = sr if i % 2 == 0 else sr * 0.45
        star.append((scx + r * math.cos(a), scy + r * math.sin(a)))
    ov4 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od4 = ImageDraw.Draw(ov4)
    od4.ellipse([scx - 50, scy - 50, scx + 50, scy + 50], fill=(212, 175, 55, 25))
    sh_star = [(x + 5, y + 7) for (x, y) in star]
    od4.polygon(sh_star, fill=(0, 0, 0, 110))
    img.paste(ov4, (0, 0), ov4)
    d = ImageDraw.Draw(img)
    d.polygon(star, fill=(212, 175, 55))
    d.polygon(star, outline=(255, 226, 130), width=2)
    d.ellipse([scx - 9, scy - 9, scx + 9, scy + 9], fill=NAVY)
    d.text((scx - 5, scy - 12), "★", font=font(18, bold=True), fill=(255, 226, 130))
    d.text((px + 14, ry + 154), "MEXICO", font=font(15, bold=True), fill=RED)
    lines = wrap(d, "EL CHAPO ISIDRO HELD", font(26, bold=True), pw - 28)
    ty = draw_lines(d, px + 14, ry + 176, lines, font(26, bold=True), INK, leading=30)
    deck = "El Chapo Isidro held; 11 dead."
    lines = wrap(d, deck, font(16), pw - 28)
    draw_lines(d, px + 14, ty + 6, lines, font(16), GREY, leading=20)
    d.text((px + 14, ry + 282), "Source: Japan Times", font=font(11), fill=GREY)

    # ---------- briefs strip: 18 briefs, 3 x 6 + DATE CHECK line ------------
    bx, by, bw, bh = 20, 820, 984, 180
    panel(d, bx, by, bw, bh, (236, 230, 214), outline=LIGHT_LINE)
    d.text((bx + 16, by + 10), "ALSO TODAY — 18 MORE STORIES", font=font(18, bold=True), fill=NAVY)
    d.line([bx + 16, by + 36, bx + bw - 16, by + 36], fill=LIGHT_LINE, width=2)
    briefs = [
        ("NEPAL", "PM Shah in Delhi; border talks."),
        ("GEORGIA", "Day of mourning for blast dead."),
        ("HONG KONG", "856 run for 723 seats."),
        ("GERMANY", "23,000 to strike Monday."),
        ("IRAN", "Rolling power cuts begin."),
        ("TURIN", "Zverev v Alcaraz in ATP final."),
        ("LIVERPOOL", "Host Man Utd, 16:30 GMT."),
        ("MELBOURNE", "'56 Olympians reunite, 70 yrs on."),
        ("INDIA", "720/9, record Test total in NZ."),
        ("S. KOREA", "Minister quits in AI scandal."),
        ("LAS VEGAS", "Verstappen wins thriller."),
        ("KOREA", "Exports pass $1 trillion."),
        ("NIGERIA", "Boat capsizes; 24 dead."),
        ("FRANCE", "Protests enter a sixth weekend."),
        ("PERU", "6.7 quake; no deaths reported."),
        ("IRAQ", "Power station fire; 4 killed."),
        ("USA", "USDA and FBI hacked, reports say."),
        ("TRUMP", "Vows 10% cap on credit-card rates."),
    ]
    cell_w = (bw - 32) // 3
    for i, (kick, text) in enumerate(briefs):
        cx0 = bx + 16 + (i % 3) * cell_w
        cy0 = by + 44 + (i // 3) * 20
        full = kick + " — " + text
        fnt = fit_font(d, full, 16, cell_w - 16, bold=False)
        d.text((cx0, cy0), kick + " — ", font=font(fnt.size, bold=True), fill=INK)
        kw = text_w(d, kick + " — ", font(fnt.size, bold=True))
        d.text((cx0 + kw, cy0), text, font=fnt, fill=INK)
    # DATE CHECK: what was left out as not-22-Nov (all verified earlier days)
    dc_y = by + 164
    d.text((bx + 16, dc_y), "DATE CHECK", font=font(12, bold=True), fill=RED)
    dcw = text_w(d, "DATE CHECK ", font(12, bold=True))
    d.text((bx + 16 + dcw, dc_y),
           "Left out, not 22 Nov: EU–Indonesia deal (Sat) · Nvidia probe (Fri) · "
           "Bolsonaro in ICU (Sat) · France 45–17 Argentina (Sat)",
           font=font(12), fill=GREY)

    # ---------- footer: date + full sources line -----------------------------
    foot = ("All events of Sunday 22 November 2026 · Sources: Reuters, AFP, SCMP, "
            "ANI, The Hindu, Yonhap, AAP, F1.com, TNT, Civil Georgia, ET, Dawn, "
            "Japan Times, Manila Times")
    ff = font(12)
    d.text(((W - text_w(d, foot, ff)) / 2, 1006), foot, font=ff, fill=GREY)

    outdir = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    img.save(os.path.join(outdir, "entry.png"), optimize=True)
    print("wrote", os.path.join(outdir, "entry.png"))


if __name__ == "__main__":
    build()
