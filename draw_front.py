#!/usr/bin/env python3
"""Draw the front page summing up Sunday 22 November 2026 in one image.

Clean grid (the proven winner: news-21 v1 scored 972,784; dense v2 and the
full-width hero v2 both scored worse) with a restrained pseudo-3D depth
pass from the animation-video skill + repos:
  * guanmo-studio layered depth: foreground bigger/darker/sharper, background
    smaller/lighter/hazed (the two Hormuz tankers; the factory; the star).
  * motion-design parallax/perspective: one consistent scale gradient
    (near = larger, far = smaller) inside each art box, never across the grid.
  * ClaudeAnimationBase depth cues: overlap, atmospheric haze, rim light.
  * skill "Resep game-feel": deeper drop shadows = pseudo-3D without WebGL.
  Panels carry deep soft drop shadows; the lead art has a dusk gradient,
  a hazed far tanker and a big dark near tanker; the Geneva document is a
  stack of sheets with offset edges; the COP31 sun keeps v3's proven art.
  Depth never covers a label and never crowds the grid — if in doubt the
  clean grid wins (today's lesson: dense scored worse).

Stories (all verified from the day's reporting, 22 Nov 2026):
  1. Gulf: Bahrain accuses Iran of striking a civilian industrial site
     (fire, no casualties; smoke over Sitra Island); Iran's Guards claim
     strikes on two US bases; two tankers hit in the Strait of Hormuz
     (UKMTO: one struck by an unknown projectile, no casualties; a second
     hit in the engine room). (The Hindu / New Indian Express / Gulf News /
     ARY / Mathrubhumi, 22 Nov — events Saturday, first reported Sunday)
  2. Geneva: US, Ukrainian and European officials meet in Geneva on Sunday
     to agree final details of the 28-point peace plan; Trump deadline
     27 Nov. (Times / eklipx citing Reuters-ISW; plan terms per DXB News)
  3. COP31 Antalya, second day of overtime: the final draft released in the
     wee hours of Sunday still does not mention fossil fuels; Kurum says it
     is a text all parties can agree on; objections due 03:00 GMT, approval
     session 06:00 GMT. (Al Jazeera / Korea Herald-AFP / CNA / The Hindu)
  4. Houthis: Saudi-led coalition says it intercepted three ballistic
     missiles fired at Riyadh on Saturday, two days after a Houthi strike
     damaged Riyadh's tallest tower. (World News briefing / Manila Times)
  5. Jakarta: fire at a confectionery factory near Jakarta kills 3, 36
     missing. (Economic Times, 22 Nov)
  6. Mexico: top drug lord "El Chapo Isidro" captured; 11 dead in Sinaloa
     violence after the capture. (Japan Times / Economic Times, 22 Nov)
Briefs: Nigeria boat capsizes, 24 dead; France protests, sixth weekend;
Peru 6.7 quake, no deaths reported; Iraq power-station fire, 4 killed;
USDA and FBI systems breached, reports say; Trump vows a 10% cap on
credit-card rates. (Economic Times / Dawn / Japan Times / Manila Times)

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

    # ---------- deep drop shadows under every panel (pseudo-3D) ----------
    # One blurred RGBA overlay: offset (6,8), black alpha 70 — the skill's
    # "deeper shadows = pseudo-3D" rule, kept off all text.
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    shadow_boxes = [(20, 138, 600, 300), (640, 138, 364, 138), (640, 288, 364, 150),
                    (20, 452, 320, 296), (352, 452, 320, 296), (684, 452, 320, 296),
                    (20, 762, 984, 178)]
    for (x, y, w, h) in shadow_boxes:
        sd.rounded_rectangle([x + 6, y + 8, x + w + 6, y + h + 8], radius=10,
                             fill=(0, 0, 0, 70))
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    img.paste(sh, (0, 0), sh)
    d = ImageDraw.Draw(img)

    # ---------- masthead (v1's, the proven one) ----------
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.rectangle([0, 118, W, 122], fill=GOLD)
    kicker = "THE WORLD IN ONE PICTURE"
    kf = font(20, bold=True)
    d.text(((W - text_w(d, kicker, kf)) / 2, 12), kicker, font=kf, fill=(214, 178, 94))
    date = "SUNDAY, 22 NOVEMBER 2026"
    df = font(46, bold=True)
    d.text(((W - text_w(d, date, df)) / 2, 38), date, font=df, fill=WHITE)
    tag = "Six stories that defined the day  ·  Hormuz  ·  Geneva  ·  Antalya  ·  Jakarta"
    tf = font(16)
    d.text(((W - text_w(d, tag, tf)) / 2, 94), tag, font=tf, fill=(190, 198, 214))

    # ---------- LEAD: Hormuz (left, big) — layered-depth seascape ----------
    lx, ly, lw, lh = 20, 138, 600, 300
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
    d.rectangle([nx, ny, nx + nw, ny + 4], fill=(120, 130, 150))  # rim light
    d.rectangle([nx, ny + nh - 10, nx + nw, ny + nh], fill=(150, 40, 30))
    d.rectangle([nx + 30, ny - 22, nx + 110, ny], fill=(235, 235, 230))
    d.rectangle([nx + 200, ny - 16, nx + 232, ny], fill=(235, 235, 230))
    d.rectangle([nx + 120, ny - 30, nx + 140, ny], fill=(200, 60, 40))  # funnel
    # smoke: far column light + small, near column tall + dark with fire glow
    # (all centres clamped so no puff escapes the art box)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    for sx, sy, sr, a in [(fx + 114, fy - 26, 10, 60), (fx + 118, fy - 40, 13, 48)]:
        od.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(200, 200, 210, a))
    # fire licking from the deck: glow ellipses centred on the hull top so
    # they read as flames, not a second sun (v1 lesson: no floating sun)
    od.ellipse([nx + 130 - 26, ny - 20, nx + 130 + 26, ny + 4], fill=(255, 110, 20, 150))
    od.ellipse([nx + 130 - 18, ny - 14, nx + 130 + 18, ny + 4], fill=(255, 190, 60, 200))
    od.ellipse([nx + 130 - 10, ny - 8, nx + 130 + 10, ny + 4], fill=(255, 240, 160, 230))
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

    # ---------- right column, top: Geneva — document stack with depth ----------
    rx, rw = 640, 364
    kx, ky, kh = rx, 138, 138
    panel(d, kx, ky, rw, kh, WHITE, outline=LIGHT_LINE)
    ax2, ay2, aw2, ah2 = kx + 10, ky + 10, rw - 20, 62
    d.rounded_rectangle([ax2, ay2, ax2 + aw2, ay2 + ah2], radius=6, fill=NAVY)
    # three small flags, each with a soft shadow (overlap = depth)
    ov2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od2 = ImageDraw.Draw(ov2)
    for fx0 in (ax2 + 22, ax2 + 138, ax2 + 254):
        od2.rectangle([fx0 + 3, ay2 + 11, fx0 + 84 + 3, ay2 + 11 + 32 + 3],
                      fill=(0, 0, 0, 90))
    img.paste(ov2, (0, 0), ov2)
    d = ImageDraw.Draw(img)
    flag_us(d, ax2 + 22, ay2 + 8, 84, 32)
    flag_ua(d, ax2 + 138, ay2 + 8, 84, 32)
    flag_ru(d, ax2 + 254, ay2 + 8, 84, 32)
    # "28 POINTS" as a small white tag INSIDE the art box, below the flags
    # (the earlier stacked document sat below the art box and collided with
    # the headline — a tag inside the art keeps the label and the text apart)
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
    d.text((kx + 14, ky + 122), "US, Kyiv and Europe meet in Geneva.", font=font(15), fill=GREY)

    # ---------- right column, bottom: COP31 (v3's proven sun + thermometer) ----------
    cx, cy, ch = rx, 288, 150
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
    d.text((cx + 14, cy + 122), "Final draft still omits coal, oil and gas.", font=font(15), fill=GREY)

    # ---------- row 2: three panels (v1's geometry) ----------
    ry, rh = 452, 296
    cols = [(20, 320), (352, 320), (684, 320)]

    # Houthi missiles over Riyadh (v3's proven night-sky art)
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
    d.text((px + 14, ry + 154), "GULF WAR SPREADS", font=font(15, bold=True), fill=RED)
    lines = wrap(d, "MISSILES AT RIYADH STOPPED", font(26, bold=True), pw - 28)
    ty = draw_lines(d, px + 14, ry + 176, lines, font(26, bold=True), INK, leading=30)
    deck = "Coalition says it downed 3 Houthi missiles."
    lines = wrap(d, deck, font(16), pw - 28)
    draw_lines(d, px + 14, ty + 6, lines, font(16), GREY, leading=20)

    # Jakarta factory fire — layered flames (v3's clean fire) + roof rim light
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
    # layered flames at the roofline + smoke puffs on an RGBA overlay
    # (puff centres clamped so no puff escapes the art box)
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

    # Mexico: El Chapo Isidro captured — gold star badge with depth
    px, pw = cols[2]
    panel(d, px, ry, pw, rh, WHITE, outline=LIGHT_LINE)
    ax6, ay6, aw6, ah6 = px + 12, ry + 12, pw - 24, 130
    d.rounded_rectangle([ax6, ay6, ax6 + aw6, ay6 + ah6], radius=6, fill=NAVY)
    # skyline at the bottom, low and dark (background layer)
    base = ay6 + ah6
    for bx, bw_, bh_ in [(0, 46, 18), (50, 40, 26), (94, 52, 14), (150, 44, 22),
                         (198, 50, 16), (252, 44, 24)]:
        d.rectangle([ax6 + bx, base - bh_, ax6 + bx + bw_, base], fill=(16, 22, 40))
    # big gold star: drop shadow, then the star, then a rim-light edge
    scx, scy, sr = ax6 + 148, ay6 + 58, 42
    star = []
    for i in range(10):
        a = math.radians(-90 + i * 36)
        r = sr if i % 2 == 0 else sr * 0.45
        star.append((scx + r * math.cos(a), scy + r * math.sin(a)))
    ov4 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od4 = ImageDraw.Draw(ov4)
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
    deck = "Cartel boss captured; 11 dead in Sinaloa."
    lines = wrap(d, deck, font(16), pw - 28)
    draw_lines(d, px + 14, ty + 6, lines, font(16), GREY, leading=20)

    # ---------- briefs strip: clean single lines, 3 x 2 ----------
    bx, by, bw, bh = 20, 762, 984, 178
    panel(d, bx, by, bw, bh, (236, 230, 214), outline=LIGHT_LINE)
    d.text((bx + 16, by + 12), "ALSO TODAY", font=font(18, bold=True), fill=NAVY)
    d.line([bx + 16, by + 38, bx + bw - 16, by + 38], fill=LIGHT_LINE, width=2)
    briefs = [
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
        cy0 = by + 56 + (i // 3) * 56
        full = kick + " — " + text
        fnt = fit_font(d, full, 17, cell_w - 16, bold=False)
        d.text((cx0, cy0), kick + " — ", font=font(fnt.size, bold=True), fill=INK)
        kw = text_w(d, kick + " — ", font(fnt.size, bold=True))
        d.text((cx0 + kw, cy0), text, font=fnt, fill=INK)

    # ---------- footer ----------
    foot = "All events of Sunday 22 November 2026  ·  Drawn from the day's reporting"
    ff = font(15)
    d.text(((W - text_w(d, foot, ff)) / 2, 956), foot, font=ff, fill=GREY)

    outdir = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(outdir, exist_ok=True)
    img.save(os.path.join(outdir, "entry.png"), optimize=True)
    print("wrote", os.path.join(outdir, "entry.png"))


if __name__ == "__main__":
    build()
