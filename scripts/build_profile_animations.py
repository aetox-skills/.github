from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "profile" / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

W, H = 1100, 540
BG_TOP = (4, 9, 18)
BG_BOTTOM = (8, 15, 30)
GRID = (17, 32, 55)
TEXT = (240, 246, 255)
MUTED = (150, 164, 190)
CYAN = (45, 212, 255)
GREEN = (84, 255, 170)
AMBER = (255, 192, 92)
VIOLET = (190, 120, 255)
ROSE = (255, 105, 145)
BLUE = (92, 142, 255)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    candidates = [
        "C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
    ]
    for candidate in candidates:
        try:
            return ImageFont.truetype(candidate, size)
        except OSError:
            continue
    return ImageFont.load_default()


TITLE = font(41, True)
SUB = font(20)
LABEL = font(20, True)
BODY = font(15)
SMALL = font(13)
MONO = font(14)


def clamp(t: float) -> float:
    return max(0.0, min(1.0, t))


def ease(t: float) -> float:
    t = clamp(t)
    return t * t * (3 - 2 * t)


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t = clamp(t)
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def glow(im: Image.Image, box: tuple[int, int, int, int], color: tuple[int, int, int], alpha: int = 90, blur: int = 24) -> None:
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle(box, radius=24, fill=color + (alpha,))
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(blur)))


def draw_background(im: Image.Image, draw: ImageDraw.ImageDraw, p: float, accent: tuple[int, int, int]) -> None:
    for y in range(H):
        draw.line((0, y, W, y), fill=mix(BG_TOP, BG_BOTTOM, y / H))

    for x in range(0, W, 48):
        draw.line((x, 0, x, H), fill=GRID, width=1)
    for y in range(0, H, 48):
        draw.line((0, y, W, y), fill=GRID, width=1)

    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    pulse = 0.55 + 0.45 * math.sin(p * math.tau)
    d.ellipse((-140, -170, 390, 330), fill=accent + (int(36 + 18 * pulse),))
    d.ellipse((780, 250, 1260, 720), fill=(20, 184, 166, int(24 + 16 * pulse)))
    im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(46)))

    draw.rounded_rectangle((24, 24, W - 24, H - 24), radius=26, outline=(38, 67, 112), width=2)


def draw_header(draw: ImageDraw.ImageDraw, title: str, subtitle: str, accent: tuple[int, int, int]) -> None:
    draw.text((62, 54), title, font=TITLE, fill=TEXT)
    draw.text((64, 104), subtitle, font=SUB, fill=MUTED)
    draw.line((64, 140, W - 64, 140), fill=accent, width=3)


def draw_chip(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, active: float, color: tuple[int, int, int]) -> None:
    draw.rounded_rectangle((x, y, x + 148, y + 34), radius=17, fill=mix((9, 17, 32), (16, 31, 55), active), outline=mix((43, 61, 92), color, active), width=2)
    draw.ellipse((x + 14, y + 11, x + 26, y + 23), fill=mix((58, 75, 103), color, active))
    draw.text((x + 36, y + 8), label, font=SMALL, fill=mix(MUTED, TEXT, active))


def draw_stage(
    im: Image.Image,
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    number: int,
    title: str,
    body: str,
    active: float,
    color: tuple[int, int, int],
) -> None:
    x1, y1, x2, y2 = box
    if active > 0.05:
        glow(im, (x1 - 4, y1 - 4, x2 + 4, y2 + 4), color, int(95 * active), 22)
    draw.rounded_rectangle(box, radius=18, fill=mix((9, 17, 32), (18, 32, 54), active), outline=mix((50, 67, 98), color, active), width=2)
    draw.ellipse((x1 + 18, y1 + 18, x1 + 46, y1 + 46), fill=mix((31, 42, 61), color, active))
    draw.text((x1 + 29 - (6 if number >= 10 else 0), y1 + 20), str(number), font=SMALL, fill=(5, 10, 18))
    draw.text((x1 + 60, y1 + 18), title, font=LABEL, fill=mix(MUTED, TEXT, active))
    draw.text((x1 + 60, y1 + 54), body, font=BODY, fill=mix((98, 112, 138), (200, 215, 238), active))


def draw_arrow(draw: ImageDraw.ImageDraw, start: tuple[int, int], end: tuple[int, int], active: float, color: tuple[int, int, int]) -> None:
    col = mix((54, 69, 96), color, active)
    draw.line((*start, *end), fill=col, width=4)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    size = 13
    pts = [
        end,
        (end[0] - size * math.cos(angle - 0.45), end[1] - size * math.sin(angle - 0.45)),
        (end[0] - size * math.cos(angle + 0.45), end[1] - size * math.sin(angle + 0.45)),
    ]
    draw.polygon(pts, fill=col)


def draw_output(im: Image.Image, draw: ImageDraw.ImageDraw, title: str, items: list[str], active: float, color: tuple[int, int, int]) -> None:
    x, y = 860, 185
    if active > 0.05:
        glow(im, (x - 6, y - 6, x + 186, y + 222), color, int(85 * active), 25)
    draw.rounded_rectangle((x, y, x + 186, y + 222), radius=22, fill=mix((9, 17, 32), (21, 28, 50), active), outline=mix((50, 67, 98), color, active), width=2)
    draw.text((x + 26, y + 26), title, font=LABEL, fill=mix(MUTED, TEXT, active))
    for i, item in enumerate(items):
        yy = y + 72 + i * 33
        draw.rounded_rectangle((x + 26, yy + 2, x + 44, yy + 20), radius=4, fill=mix((43, 55, 78), color, active))
        draw.text((x + 58, yy), item, font=BODY, fill=mix((98, 112, 138), TEXT, active))


def draw_left_scene(draw: ImageDraw.ImageDraw, kind: str, p: float, active: float, accent: tuple[int, int, int]) -> None:
    x, y = 70, 238
    if kind == "code":
        draw.rounded_rectangle((x, y, x + 205, y + 144), radius=18, fill=(7, 13, 25), outline=mix((44, 65, 100), accent, active), width=2)
        draw.text((x + 22, y + 18), "SYSTEM", font=LABEL, fill=mix(MUTED, TEXT, active))
        for i, line in enumerate(["src/app.ts", "routes/api.ts", "docs/adr.md", "tests/auth.spec"]):
            draw.text((x + 24, y + 53 + i * 22), line, font=MONO, fill=mix((88, 101, 124), (196, 226, 255), active))
        sy = y + 48 + int(82 * ((p * 3) % 1))
        draw.rounded_rectangle((x + 18, sy, x + 187, sy + 6), radius=3, fill=accent)
    elif kind == "idea":
        draw.rounded_rectangle((x, y, x + 205, y + 144), radius=22, fill=(13, 11, 30), outline=mix((60, 48, 112), accent, active), width=2)
        draw.text((x + 45, y + 25), "RAW", font=LABEL, fill=mix(MUTED, TEXT, active))
        draw.text((x + 43, y + 58), "IDEA", font=TITLE, fill=mix((116, 82, 180), accent, active))
        draw.text((x + 43, y + 112), "intent first", font=BODY, fill=MUTED)
    else:
        labels = [("README", 0, 36), ("notes", 70, 4), ("plan", 112, 54), ("TODO", 30, 92)]
        for label, dx, dy in labels:
            draw.rounded_rectangle((x + dx, y + dy, x + dx + 92, y + dy + 42), radius=10, fill=(7, 13, 25), outline=mix((44, 65, 100), accent, active), width=2)
            draw.text((x + dx + 13, y + dy + 12), label, font=SMALL, fill=mix(MUTED, TEXT, active))


def make_animation(name: str, title: str, subtitle: str, kind: str, stages: list[tuple[str, str, tuple[int, int, int]]], chips: list[str], output: list[str], accent: tuple[int, int, int]) -> None:
    frames: list[Image.Image] = []
    boxes = [
        (320, 196, 500, 300),
        (544, 196, 724, 300),
        (430, 350, 610, 454),
        (650, 350, 830, 454),
    ]

    for i in range(58):
        p = i / 57
        im = Image.new("RGBA", (W, H), (0, 0, 0, 255))
        draw = ImageDraw.Draw(im)
        draw_background(im, draw, p, accent)
        draw_header(draw, title, subtitle, accent)

        stage_float = p * 5.15
        active = [ease(stage_float - idx) for idx in range(5)]

        for idx, chip in enumerate(chips):
            draw_chip(draw, 64 + idx * 168, 160, chip, active[min(idx + 1, 4)], stages[idx % len(stages)][2])

        draw_left_scene(draw, kind, p, active[0], accent)

        for idx, box in enumerate(boxes):
            stage_title, body, color = stages[idx]
            draw_stage(im, draw, box, idx + 1, stage_title, body, active[idx], color)

        draw_arrow(draw, (275, 310), (320, 248), active[0], accent)
        draw_arrow(draw, (500, 248), (544, 248), active[1], stages[1][2])
        draw_arrow(draw, (637, 300), (520, 350), active[2], stages[2][2])
        draw_arrow(draw, (610, 402), (650, 402), active[3], stages[3][2])
        draw_arrow(draw, (830, 402), (860, 300), active[4], accent)
        draw_output(im, draw, "OUTPUT", output, active[4], accent)

        draw.text((64, 492), "behavior package:", font=SMALL, fill=MUTED)
        gates = ["purpose", "rules", "templates", "handoff"]
        for idx, gate in enumerate(gates):
            t = active[min(idx + 1, 4)]
            x = 198 + idx * 156
            draw.rounded_rectangle((x, 487, x + 128, 516), radius=14, fill=mix((10, 20, 36), (15, 46, 42), t), outline=mix((45, 61, 88), accent, t), width=1)
            draw.text((x + 18, 493), gate, font=SMALL, fill=mix((112, 126, 152), TEXT, t))

        frames.append(im.convert("P", palette=Image.Palette.ADAPTIVE, colors=160))

    frames[0].save(ASSETS / f"{name}.gif", save_all=True, append_images=frames[1:], duration=78, loop=0, optimize=True, disposal=2)


def main() -> None:
    make_animation(
        "senior-architect-agent",
        "Senior Architect Agent",
        "Map the real system before the agent edits code.",
        "code",
        [
            ("Inspect", "files, docs, history", CYAN),
            ("Classify", "facts vs unknowns", GREEN),
            ("Question", "risks before design", AMBER),
            ("Map", "boundaries + flows", BLUE),
        ],
        ["Evidence first", "No hallucination", "Right-sized pass"],
        ["maps", "risks", "questions", "handoff"],
        CYAN,
    )
    make_animation(
        "idea-to-architecture-agent",
        "Idea To Architecture Agent",
        "Turn a raw idea into an approval-ready architecture proposal.",
        "idea",
        [
            ("Capture", "intent + constraints", VIOLET),
            ("Ask", "key decisions", AMBER),
            ("Shape", "options + tradeoffs", BLUE),
            ("Propose", "reviewable plan", GREEN),
        ],
        ["Intent first", "Question first", "Proposal until approved"],
        ["options", "tradeoffs", "risks", "proposal"],
        VIOLET,
    )
    make_animation(
        "docstruct",
        "DocStruct",
        "Keep project docs small, owned, and reusable.",
        "docs",
        [
            ("Audit", "read before writing", GREEN),
            ("Route", "one source of truth", CYAN),
            ("Clean", "dedupe + label gaps", ROSE),
            ("Continue", "future-agent friendly", AMBER),
        ],
        ["One truth", "Small docs", "Agent-readable"],
        ["owners", "links", "unknowns", "clean docs"],
        GREEN,
    )


if __name__ == "__main__":
    main()
