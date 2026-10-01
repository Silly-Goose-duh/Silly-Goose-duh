"""Generate animated SVG project cards for the GitHub profile README.

GitHub strips <script> and inline CSS from README markdown, but it renders
SVGs embedded via <img> and runs their SMIL/CSS keyframes. So all motion
lives inside these SVGs. One file per work-type, laid out as a card grid.

Brand: neuro.ad -- orange #BE5205, gold #F59E0B, cream #FFFDE1 on #111111.
"""
import html

ORANGE = "#BE5205"
GOLD = "#F59E0B"
CREAM = "#FFFDE1"
MUTED = "#9a9a8f"
INK = "#1C1C1C"
CARD_BG = "#181818"
BORDER = "#2e2a24"

MONO = "ui-monospace, 'Cascadia Code', 'JetBrains Mono', Menlo, Consolas, monospace"

W = 800
CARD_W = 384
CARD_H = 92
GAP_X = 32
GAP_Y = 24
PAD = 0          # cards bleed to the edge, matching README width

# name, one-line descriptor, tag
GROUPS = [
    {
        "key": "ai",
        "cards": [
            ("DOT", "Android productivity agent", "Kotlin"),
            ("echo", "Voice-first AI companion", "Python"),
            ("agent-vault", "Memory for coding agents", "Python"),
            ("Refro", "DeepSeek Harness dashboard", "TypeScript"),
        ],
    },
    {
        "key": "marketing",
        "cards": [
            ("NeuroAd", "Ad-tech platform", "Next.js"),
            ("neuro.ad", "Brand + landing for ad-tech", "Identity"),
            ("CampusPass", "Event platform w/ analytics", "React"),
        ],
    },
    {
        "key": "brand",
        "cards": [
            ("Sharon Weds Amala", "Wedding RSVP platform", "Client"),
        ],
    },
]


def esc(s):
    return html.escape(s, quote=True)


def card(x, y, name, desc, tag, delay):
    """One project card: accent bar, name, descriptor, language chip."""
    parts = [f'<g opacity="0" transform="translate(0,{y + 14})">']
    # fade + rise into place, once, then freeze
    parts.append(
        f'<animateTransform attributeName="transform" type="translate" '
        f'from="0,{y + 14}" to="0,{y}" dur="0.5s" begin="{delay:.2f}s" fill="freeze"/>'
    )
    parts.append(
        f'<animate attributeName="opacity" from="0" to="1" dur="0.45s" '
        f'begin="{delay:.2f}s" fill="freeze"/>'
    )
    # body
    parts.append(
        f'<rect x="{x}" y="{y}" width="{CARD_W}" height="{CARD_H}" rx="12" '
        f'fill="{CARD_BG}" stroke="{BORDER}" stroke-width="1"/>'
    )
    # left accent bar -- reads as a hover/active state at rest
    parts.append(
        f'<rect x="{x}" y="{y + 14}" width="3" height="{CARD_H - 28}" rx="1.5" '
        f'fill="{ORANGE}"/>'
    )
    # name
    parts.append(
        f'<text x="{x + 22}" y="{y + 40}" font-family="{MONO}" font-size="19" '
        f'font-weight="700" fill="{CREAM}">{esc(name)}</text>'
    )
    # descriptor
    parts.append(
        f'<text x="{x + 22}" y="{y + 64}" font-family="{MONO}" font-size="13" '
        f'fill="{MUTED}">{esc(desc)}</text>'
    )
    # language chip, right aligned
    tw = len(tag) * 7.4 + 18
    tx = x + CARD_W - tw - 16
    parts.append(
        f'<rect x="{tx:.1f}" y="{y + 18}" width="{tw:.1f}" height="21" rx="10.5" '
        f'fill="{INK}" stroke="{ORANGE}" stroke-opacity="0.55" stroke-width="1"/>'
    )
    parts.append(
        f'<text x="{tx + tw / 2:.1f}" y="{y + 33}" font-family="{MONO}" '
        f'font-size="11" fill="{GOLD}" text-anchor="middle">{esc(tag)}</text>'
    )
    parts.append("</g>")
    return "".join(parts)


def build_group(group):
    cards = group["cards"]
    cols = 2 if len(cards) > 1 else 1
    rows = (len(cards) + cols - 1) // cols
    width = cols * CARD_W + (cols - 1) * GAP_X
    height = rows * CARD_H + (rows - 1) * GAP_Y
    ox = (W - width) / 2

    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{height}" '
        f'viewBox="0 0 {W} {height}" role="img" '
        f'aria-label="Project cards">'
    ]
    t = 0.1
    for i, (name, desc, tag) in enumerate(cards):
        r, c = divmod(i, cols)
        x = ox + c * (CARD_W + GAP_X)
        y = r * (CARD_H + GAP_Y)
        p.append(card(x, y, name, desc, tag, t))
        t += 0.09
    p.append("</svg>")
    return "".join(p), height


if __name__ == "__main__":
    for g in GROUPS:
        svg, h = build_group(g)
        path = f"D:/work/cards-{g['key']}.svg"
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"wrote {path}  {len(svg)} bytes  {W}x{h}")
