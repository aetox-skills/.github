from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "profile" / "assets"
ASSETS.mkdir(parents=True, exist_ok=True)

W, H = 880, 420
BG = (5, 10, 18)
PANEL = (10, 18, 32)
PANEL_2 = (14, 25, 44)
TEXT = (235, 242, 255)
MUTED = (148, 163, 184)
GRID = (18, 35, 58)


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


FONT_TITLE = font(34, True)
FONT_SUB = font(18)
FONT_LABEL = font(17, True)
FONT_SMALL = font(14)
FONT_MONO = font(14)


def mix(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    t = max(0.0, min(1.0, t))
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def pulse(t: float) -> float:
    return 0.5 + 0.5 * math.sin(t * math.tau)


def draw_background(draw: ImageDraw.ImageDraw) -> None:
    draw.rectangle((0, 0, W, H), fill=BG)
    for x in range(0, W, 44):
        draw.line((x, 0, x, H), fill=GRID, width=1)
    for y in range(0, H, 44):
        draw.line((0, y, W, y), fill=GRID, width=1)
    draw.rectangle((0, 0, W, H), outline=(30, 58, 96), width=2)


def draw_text_center(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    fnt: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int],
) -> None:
    box = draw.textbbox((0, 0), text, font=fnt)
    draw.text((xy[0] - (box[2] - box[0]) / 2, xy[1]), text, font=fnt, fill=fill)


def draw_node(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    title: str,
    body: str,
    active: float,
    color: tuple[int, int, int],
) -> None:
    border = mix((51, 65, 85), color, active)
    fill = mix(PANEL, PANEL_2, active)
    glow = mix((14, 22, 36), color, active * 0.18)

    x1, y1, x2, y2 = box
    if active > 0.05:
        draw.rounded_rectangle((x1 - 5, y1 - 5, x2 + 5, y2 + 5), radius=18, fill=glow)
    draw.rounded_rectangle(box, radius=14, fill=fill, outline=border, width=2)
    draw.ellipse((x1 + 16, y1 + 18, x1 + 34, y1 + 36), fill=mix((31, 41, 55), color, active))
    draw.text((x1 + 48, y1 + 17), title, font=FONT_LABEL, fill=mix(MUTED, TEXT, active))
    draw.text((x1 + 48, y1 + 48), body, font=FONT_SMALL, fill=mix((100, 116, 139), MUTED, active))


def draw_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[int, int],
    end: tuple[int, int],
    active: float,
    color: tuple[int, int, int],
) -> None:
    fill = mix((51, 65, 85), color, active)
    draw.line((*start, *end), fill=fill, width=3)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    head = 12
    pts = [
        end,
        (end[0] - head * math.cos(angle - 0.45), end[1] - head * math.sin(angle - 0.45)),
        (end[0] - head * math.cos(angle + 0.45), end[1] - head * math.sin(angle + 0.45)),
    ]
    draw.polygon(pts, fill=fill)


def draw_code_stack(draw: ImageDraw.ImageDraw, x: int, y: int, active: float, color: tuple[int, int, int]) -> None:
    draw.rounded_rectangle((x, y, x + 166, y + 96), radius=12, fill=(8, 13, 24), outline=mix((30, 41, 59), color, active), width=2)
    lines = [
        "src/app.ts",
        "routes/api.ts",
        "docs/adr.md",
        "tests/auth.spec",
    ]
    for i, line in enumerate(lines):
        yy = y + 16 + i * 18
        draw.text((x + 16, yy), line, font=FONT_MONO, fill=mix((71, 85, 105), TEXT, active))
    scan_y = y + 12 + int((72 * active) % 72)
    draw.rectangle((x + 12, scan_y, x + 154, scan_y + 4), fill=mix((14, 165, 233), color, active))


def draw_doc_scatter(draw: ImageDraw.ImageDraw, x: int, y: int, active: float, color: tuple[int, int, int]) -> None:
    docs = [
        (x, y + 12, "README"),
        (x + 58, y - 6, "notes"),
        (x + 112, y + 20, "plan"),
        (x + 38, y + 58, "TODO"),
        (x + 126, y + 70, "old"),
    ]
    for dx, dy, label in docs:
        draw.rounded_rectangle((dx, dy, dx + 74, dy + 42), radius=8, fill=(8, 13, 24), outline=mix((51, 65, 85), color, active * 0.65), width=2)
        draw.text((dx + 10, dy + 12), label, font=FONT_SMALL, fill=mix((100, 116, 139), TEXT, active))


def make_animation(
    name: str,
    title: str,
    subtitle: str,
    nodes: list[tuple[str, str]],
    output_lines: list[str],
    color: tuple[int, int, int],
    accent: tuple[int, int, int],
    side: str,
) -> None:
    frames: list[Image.Image] = []
    total = 52
    node_boxes = [
        (255, 140, 420, 230),
        (462, 140, 627, 230),
        (255, 266, 420, 356),
        (462, 266, 627, 356),
    ]

    for i in range(total):
        p = i / (total - 1)
        im = Image.new("RGB", (W, H), BG)
        draw = ImageDraw.Draw(im)
        draw_background(draw)

        glow = int(28 + 28 * pulse(p * 2))
        draw.ellipse((-160, -190, 320, 290), fill=(0, glow // 2, glow))
        draw.ellipse((650, 235, 1040, 540), fill=(glow // 3, 10, glow // 2))
        draw.rectangle((0, 0, W, H), fill=BG + (0,))

        draw.text((42, 34), title, font=FONT_TITLE, fill=TEXT)
        draw.text((44, 82), subtitle, font=FONT_SUB, fill=MUTED)
        draw.line((44, 116, 836, 116), fill=mix((30, 41, 59), color, 0.75), width=2)

        stage = min(3, int(p * 4.25))
        local = (p * 4.25) - stage

        if side == "code":
            draw_code_stack(draw, 52, 176, min(1, p * 2.1), color)
        elif side == "idea":
            draw.rounded_rectangle((58, 176, 202, 302), radius=18, fill=(8, 13, 24), outline=mix((51, 65, 85), color, min(1, p * 2)), width=2)
            draw_text_center(draw, (130, 196), "RAW", FONT_LABEL, mix(MUTED, TEXT, min(1, p * 2)))
            draw_text_center(draw, (130, 224), "IDEA", FONT_TITLE, mix(MUTED, color, min(1, p * 2)))
            draw_text_center(draw, (130, 275), "intent first", FONT_SMALL, MUTED)
        else:
            draw_doc_scatter(draw, 40, 170, min(1, p * 2), color)

        for index, box in enumerate(node_boxes):
            active = 1 if index < stage else max(0, min(1, local)) if index == stage else 0
            draw_node(draw, box, nodes[index][0], nodes[index][1], active, color if index % 2 == 0 else accent)

        arrows = [
            ((420, 185), (462, 185)),
            ((545, 230), (545, 266)),
            ((462, 311), (420, 311)),
        ]
        for index, (start, end) in enumerate(arrows):
            active = max(0, min(1, (p * 4.25 - index - 0.55)))
            draw_arrow(draw, start, end, active, color if index != 1 else accent)

        output_active = max(0, min(1, (p - 0.72) / 0.25))
        out_x, out_y = 680, 166
        draw.rounded_rectangle((out_x, out_y, 824, out_y + 146), radius=16, fill=mix(PANEL, PANEL_2, output_active), outline=mix((51, 65, 85), accent, output_active), width=2)
        draw_text_center(draw, (752, out_y + 24), "OUTPUT", FONT_LABEL, mix(MUTED, TEXT, output_active))
        for line_index, line in enumerate(output_lines):
            yy = out_y + 58 + line_index * 25
            draw.rectangle((out_x + 24, yy + 7, out_x + 36, yy + 19), fill=mix((31, 41, 55), accent, output_active))
            draw.text((out_x + 48, yy), line, font=FONT_SMALL, fill=mix((100, 116, 139), TEXT, output_active))

        frames.append(im.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))

    frames[0].save(
        ASSETS / f"{name}.gif",
        save_all=True,
        append_images=frames[1:],
        duration=82,
        loop=0,
        optimize=True,
        disposal=2,
    )


def main() -> None:
    make_animation(
        "senior-architect-agent",
        "Senior Architect Agent",
        "Map the real system before the agent edits code.",
        [
            ("Inspect", "files, docs, history"),
            ("Map", "bounds + workflows"),
            ("Question", "risks and unknowns"),
            ("Handoff", "safe next actions"),
        ],
        ["maps", "risks", "handoff"],
        (56, 189, 248),
        (34, 197, 94),
        "code",
    )
    make_animation(
        "idea-to-architecture-agent",
        "Idea To Architecture Agent",
        "Turn a raw idea into a reviewable proposal.",
        [
            ("Capture", "intent + constraints"),
            ("Ask", "key questions"),
            ("Shape", "options and tradeoffs"),
            ("Propose", "reviewable plan"),
        ],
        ["options", "tradeoffs", "proposal"],
        (168, 85, 247),
        (245, 158, 11),
        "idea",
    )
    make_animation(
        "docstruct",
        "DocStruct",
        "Keep project docs small, owned, and reusable.",
        [
            ("Audit", "read before writing"),
            ("Route", "one source of truth"),
            ("Clean", "dedupe docs"),
            ("Continue", "agent friendly"),
        ],
        ["owners", "truth", "clean docs"],
        (20, 184, 166),
        (248, 113, 113),
        "docs",
    )


if __name__ == "__main__":
    main()
