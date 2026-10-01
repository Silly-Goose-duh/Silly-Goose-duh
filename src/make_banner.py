"""Generate a self-contained animated SVG banner for the GitHub profile.

Brand: neuro.ad -- orange #BE5205 primary, gold #F59E0B, cream #FFFDE1,
ink #1C1C1C, void #111111. All motion lives inside the SVG (CSS keyframes +
SMIL) because GitHub strips <script> and inline CSS from READMEs but does
render animations in SVGs embedded via <img>.
"""
import html

ORANGE = "#BE5205"
GOLD = "#F59E0B"
CREAM = "#FFFDE1"
INK = "#1C1C1C"
VOID = "#111111"

W, H = 920, 320
FS = 21          # body font size
LINE_H = 30
CURSOR_W = 12    # width of one monospace char at FS
MONO = "ui-monospace, 'Cascadia Code', 'JetBrains Mono', Menlo, Consolas, monospace"

LINES = [
    {"text": "Silly Goose", "size": 40, "color": CREAM, "weight": 700, "dur": 0.035},
    {"text": "AI / Marketing / Personal Branding", "size": FS, "color": GOLD, "weight": 600, "dur": 0.04},
    {"text": "Agentic AI systems · ad-tech · brand growth", "size": FS, "color": CREAM, "weight": 400, "dur": 0.028},
    {"text": "Building products that ship. Brands that stick.", "size": FS, "color": ORANGE, "weight": 600, "dur": 0.028},
]

# y positions, bottom-anchored block
base_y = 150
positions = []
y = base_y
for ln in LINES:
    positions.append(y)
    y += 34 if ln["size"] == 40 else LINE_H


def esc(s):
    return html.escape(s, quote=True)


def typing_line(ln, y, delay, idx):
    """One line of text revealed character-by-character via per-char opacity."""
    fs = ln["size"]
    weight = ln["weight"]
    color = ln["color"]
    dur = ln["dur"]
    out = [
        f'<text x="300" y="{y}" font-family="{MONO}" font-size="{fs}" '
        f'font-weight="{weight}" fill="{color}" letter-spacing="-0.3">'
    ]
    for i, ch in enumerate(ln["text"]):
        # slight per-char jitter reads as organic typing rather than a wipe
        d = delay + i * dur
        out.append(
            f'<tspan opacity="0"><animate attributeName="opacity" from="0" to="1" '
            f'dur="0.01s" begin="{d:.3f}s" fill="freeze"/>'
            f'{esc(ch)}</tspan>'
        )
    out.append("</text>")
    return "".join(out)


def cursor(x, y, fs, delay, total):
    """Block cursor that blinks after the line finishes typing."""
    h = fs * 0.78
    return (
        f'<rect x="{x}" y="{y - fs * 0.78:.1f}" width="{CURSOR_W}" height="{h:.1f}" '
        f'fill="{GOLD}" opacity="0.9">'
        f'<animate attributeName="opacity" values="0.9;0.9;0;0" '
        f'keyTimes="0;0.5;0.5;1" dur="1.1s" begin="{delay:.2f}s" repeatCount="indefinite"/>'
        f"</rect>"
    )


def fox(cx, cy, s=1.0):
    """Geometric fox head.

    Deliberately NOT the Firefox mark: that logo is a wide circular swirl
    around a rounded head. This is built from tall separated ears, a narrow
    tapering skull, and a long pointed snout -- the silhouette that reads as
    an actual fox rather than a browser.
    """
    def p(pts):
        return " ".join(f"{x},{y}" for x, y in pts)

    # Tall, narrow, well-separated ears (Firefox's are short and swept wide).
    ear_l = f'<polygon points="{p([(4,4),(16,52),(40,34)])}" fill="{ORANGE}"/>'
    ear_r = f'<polygon points="{p([(76,4),(64,52),(40,34)])}" fill="{ORANGE}"/>'
    # Inner ear, set well inside each ear.
    in_l = f'<polygon points="{p([(13,16),(19,42),(30,34)])}" fill="{GOLD}" opacity="0.8"/>'
    in_r = f'<polygon points="{p([(67,16),(61,42),(50,34)])}" fill="{GOLD}" opacity="0.8"/>'
    # Narrow skull: widest at the brow, tapering to a snout.
    skull = f'<polygon points="{p([(40,26),(64,44),(58,74),(40,104),(22,74),(16,44)])}" fill="{ORANGE}"/>'
    # Cream cheek ruffs flaring either side of the snout.
    ruff = f'<polygon points="{p([(16,50),(6,72),(20,66),(26,86),(34,62)])}" fill="{CREAM}" opacity="0.9"/>'
    ruff_r = f'<polygon points="{p([(64,50),(74,72),(60,66),(54,86),(46,62)])}" fill="{CREAM}" opacity="0.9"/>'
    # Long pale snout running down the centre.
    snout = f'<polygon points="{p([(40,60),(50,80),(40,100),(30,80)])}" fill="{CREAM}" opacity="0.95"/>'
    # Eyes: small, set wide and slightly slanted.
    eye_l = f'<polygon points="{p([(24,50),(33,53),(25,58)])}" fill="{INK}"/>'
    eye_r = f'<polygon points="{p([(56,50),(47,53),(55,58)])}" fill="{INK}"/>'
    # Nose at the very tip of the snout.
    nose = f'<polygon points="{p([(35,90),(45,90),(40,99)])}" fill="{INK}"/>'
    g = ear_l + ear_r + in_l + in_r + skull + ruff + ruff_r + snout + eye_l + eye_r + nose
    return f'<g transform="translate({cx},{cy}) scale({s})">{g}</g>'


def build():
    parts = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" role="img" '
        f'aria-label="Silly Goose — AI, Marketing and Personal Branding">'
    )
    # background
    parts.append(f'<rect width="{W}" height="{H}" fill="{VOID}"/>')
    # faint grid, so the dark field is not flat
    parts.append(
        f'<g stroke="{CREAM}" stroke-opacity="0.045" stroke-width="1">'
        + "".join(
            f'<line x1="0" y1="{y}" x2="{W}" y2="{y}"/>' for y in range(0, H, 32)
        )
        + "".join(
            f'<line x1="{x}" y1="0" x2="{x}" y2="{H}"/>' for x in range(0, W, 32)
        )
        + "</g>"
    )
    # top + bottom brand rules
    parts.append(f'<rect x="0" y="0" width="{W}" height="4" fill="{ORANGE}"/>')
    parts.append(
        f'<rect x="0" y="{H-4}" width="{W}" height="4" fill="{GOLD}" opacity="0.8"/>'
    )

    # fox mark, with a one-shot fade-in
    parts.append(
        f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" '
        f'dur="0.7s" begin="0.15s" fill="freeze"/>'
        + fox(150, 92, 1.35)
        + "</g>"
    )

    # accent bar under the fox
    parts.append(
        f'<rect x="150" y="212" width="118" height="3" fill="{ORANGE}" opacity="0">'
        f'<animate attributeName="opacity" from="0" to="0.85" dur="0.5s" '
        f'begin="0.7s" fill="freeze"/></rect>'
    )

    # typing lines, staggered
    t = 0.55
    for ln, y in zip(LINES, positions):
        parts.append(typing_line(ln, y, t, 0))
        t += len(ln["text"]) * ln["dur"] + 0.22

    # cursor rides the end of the last line
    last = LINES[-1]
    last_len = len(last["text"])
    cur_delay = 0.55
    for ln in LINES[:-1]:
        cur_delay += len(ln["text"]) * ln["dur"] + 0.22
    cur_delay += last_len * last["dur"]
    parts.append(
        cursor(300 + last_len * CURSOR_W * 0.62, positions[-1], last["size"], cur_delay, 0)
    )

    # contact line, fades in last
    contact_y = positions[-1] + 46
    parts.append(
        f'<text x="300" y="{contact_y}" font-family="{MONO}" font-size="15" '
        f'fill="{CREAM}" opacity="0" letter-spacing="0.2">'
        f'<animate attributeName="opacity" from="0" to="0.62" dur="0.8s" '
        f'begin="{cur_delay + 0.5:.2f}s" fill="freeze"/>'
        f'gooseisback4u@gmail.com</text>'
    )

    parts.append("</svg>")
    return "".join(parts)


if __name__ == "__main__":
    svg = build()
    with open("D:/work/banner.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    print("wrote D:/work/banner.svg", len(svg), "bytes")
