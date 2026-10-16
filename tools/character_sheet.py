"""Gera a ficha de personagem do README (SVG animado, temas claro e escuro, EN e PT).

Uso:
  python tools/character_sheet.py            -> grava assets/sheet-{en,pt}-{dark,light}.svg
  python tools/character_sheet.py pt dark    -> imprime um SVG só no stdout

Para mudar atributos, textos ou cores, edite as constantes abaixo e rode de novo.
"""

import sys
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

W, H = 900, 420
FONT = "ui-monospace, SFMono-Regular, Consolas, 'Liberation Mono', Menlo, monospace"

THEMES = {
    "dark": {
        "bg": "#0d1117", "border": "#30363d", "text": "#e6edf3", "muted": "#8b949e",
        "accent": "#f2cc60", "bar": "#f2cc60", "bar_off": "#21262d", "xp": "#58a6ff",
        "chip": "#1f242c", "portrait": "#1c3350", "star": "#c9d1d9", "glyph": "#7ee787",
    },
    "light": {
        "bg": "#ffffff", "border": "#d0d7de", "text": "#1f2328", "muted": "#59636e",
        "accent": "#9a6700", "bar": "#bf8700", "bar_off": "#eaeef2", "xp": "#0969da",
        "chip": "#f6f8fa", "portrait": "#ddf4ff", "star": "#54aeff", "glyph": "#1a7f37",
    },
}

TEXT = {
    "en": {
        "title": "CHARACTER SHEET",
        "save": "save file: iago-leles.sav",
        "name": "IAGO LELES",
        "level": "Lv. 26 · Full Stack",
        "info": [
            ("CLASS", "Full Stack Developer"),
            ("SPECIALTY", "Web + Mobile"),
            ("MAIN WEAPON", "TypeScript"),
            ("ORIGIN", "MG — Brazil"),
            ("ALIGNMENT", "Chaotic Curious"),
        ],
        "attr_title": "ATTRIBUTES",
        "stats": [
            ("FRONTEND", 9), ("MOBILE", 7), ("BACKEND", 6),
            ("TESTING", 6), ("AI MAGIC", 8), ("COFFEE", 10),
        ],
        "abil_title": "SPECIAL ABILITIES",
        "abilities": ["Summon AI agents", "Tame bugs in prod", "Deploy on Fridays"],
        "xp": "next level: birthday",
    },
    "pt": {
        "title": "FICHA DE PERSONAGEM",
        "save": "save: iago-leles.sav",
        "name": "IAGO LELES",
        "level": "Nv. 26 · Full Stack",
        "info": [
            ("CLASSE", "Dev Full Stack"),
            ("ESPECIALIDADE", "Web + Mobile"),
            ("ARMA PRINCIPAL", "TypeScript"),
            ("ORIGEM", "MG — Brasil"),
            ("ALINHAMENTO", "Caótico Curioso"),
        ],
        "attr_title": "ATRIBUTOS",
        "stats": [
            ("FRONTEND", 9), ("MOBILE", 7), ("BACKEND", 6),
            ("TESTES", 6), ("MAGIA (IA)", 8), ("CAFÉ", 10),
        ],
        "abil_title": "HABILIDADES ESPECIAIS",
        "abilities": ["Invocar agentes de IA", "Domar bug em produção", "Deploy na sexta"],
        "xp": "próximo nível: aniversário",
    },
}

# Personagem 24x24. Cada letra é uma cor (ver COLORS). "." é transparente.
HERO = [
    ".....KK.KKK..KKK.KK.....",
    "....KHHKHhHKKHhHKHHK....",
    "...KHhHHHHhHHhHHHHhHK...",
    "...KHHHhHHHHHHHHhHHHK...",
    "...KHhHHHhHHHHhHHHhHK...",
    "...KHHhHSSHhhHSSHhHHK...",
    "...KHHSSSSSSSSSSSSHHK...",
    "...KHSSSSSSSSSSSSSSHK...",
    "....KSSSwESSSSwESSSK....",
    "....KSSSEESSSSEESSSK....",
    "....KSSSSSSSSSSSSSSK....",
    "....KSSSSBBBBBBSSSSK....",
    "....KSSSSBSSSSBSSSSK....",
    ".....KSSSBBBBBBSSSK.....",
    ".....KWWWKBBBBKWWWK.....",
    "...KKWWWWWWWWWWWWWWKK...",
    "..KWWWWWWWWWWWWWWWWWWK..",
    ".KWWWWWWWWWWWWWWWWWWWWK.",
    ".KWWWWWWWWWWWWWWWWWWWWK.",
    "KKKKKKKKKKKKKKKKKKKKKKKK",
    "KLlLlLlLlLlLlLlLlLlLlLlK",
    "KLlLlLLLLLLLLLLLLlLlLlLK",
    "KKKKKKKKKKKKKKKKKKKKKKKK",
    "........................",
]
MUG = [
    "KKKKK..",
    "KTTTKK.",
    "KCCCK.K",
    "KCCCK.K",
    "KCCCKK.",
    "KKKKK..",
]
COLORS = {
    "K": "#0d1117", "H": "#2b1a10", "h": "#5a3a22", "B": "#3a2416", "S": "#e2a77c",
    "E": "#0d1117", "w": "#ffffff", "M": "#8a3b2a",
    "W": "#262a30", "L": "#d0d7de", "l": "#8b949e",
    "C": "#f0f6fc", "T": "#6f4e37",
}
for row in HERO + MUG:
    assert len(row) == len(HERO[0] if row in HERO else MUG[0]), row


def t(x, y, s, size, fill, weight="normal", anchor="start", spacing=0, extra=""):
    return (
        f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{fill}" '
        f'font-weight="{weight}" text-anchor="{anchor}" letter-spacing="{spacing}"{extra}>{escape(s)}</text>'
    )


def pixels(grid, x0, y0, px, colors=COLORS, skip=""):
    out = []
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch != "." and ch not in skip:
                out.append(f'<rect x="{x0 + c * px}" y="{y0 + r * px}" width="{px}" height="{px}" fill="{colors[ch]}"/>')
    return "".join(out)


def portrait(x, y, size, c):
    """Retrato animado: personagem respirando e piscando, código saindo do notebook, café e estrelas."""
    px = 6
    hx, hy = x + 6, y + size - 24 * px + 2
    p = [f'<rect x="{x}" y="{y}" width="{size}" height="{size}" rx="8" fill="{c["portrait"]}" stroke="{c["border"]}"/>']

    # Estrelas piscando no fundo
    for i, (sx, sy) in enumerate([(18, 22), (172, 30), (150, 70), (30, 92), (185, 110), (96, 14)]):
        p.append(
            f'<rect x="{x + sx}" y="{y + sy}" width="4" height="4" fill="{c["star"]}" opacity="0.2">'
            f'<animate attributeName="opacity" values="0.15;0.9;0.15" dur="{2.4 + i * 0.5:.1f}s" '
            f'begin="{i * 0.4:.1f}s" repeatCount="indefinite"/></rect>'
        )

    # Símbolos de código subindo do notebook
    for i, g in enumerate(["</>", "{ }", "=>", "&&"]):
        gx = x + 24 + (i % 2) * 100 + (i // 2) * 12
        p.append(
            f'<g opacity="0">{t(gx, y + 130, g, 15, c["glyph"], "bold")}'
            f'<animateTransform attributeName="transform" type="translate" values="0 0; 0 -110" '
            f'dur="4s" begin="{i}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.15;0.6;1" '
            f'dur="4s" begin="{i}s" repeatCount="indefinite"/></g>'
        )

    # Personagem com respiração em dois quadros (pixel art pede movimento em degraus)
    p.append('<g shape-rendering="crispEdges">')
    # Blusa fixa por trás: preenche a fresta quando o corpo sobe
    p.append(pixels(HERO[16:18], hx, hy + 16 * px, px))
    p.append('<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -3" '
             'keyTimes="0;0.5" calcMode="discrete" dur="1.4s" repeatCount="indefinite"/>')
    p.append(pixels(HERO[:18], hx, hy, px))
    # Piscada: pálpebras cobrem os olhos por um instante
    lid = "".join(
        f'<rect x="{hx + cx * px}" y="{hy + 8 * px}" width="{2 * px}" height="{2 * px}" fill="{COLORS["S"]}"/>'
        f'<rect x="{hx + cx * px}" y="{hy + 9 * px}" width="{2 * px}" height="{px // 2 + 1}" fill="{COLORS["K"]}"/>'
        for cx in (8, 14)
    )
    p.append(f'<g opacity="0">{lid}<animate attributeName="opacity" values="0;1;0;0;1;0;0" '
             'keyTimes="0;0.03;0.06;0.5;0.53;0.56;1" calcMode="discrete" dur="5s" repeatCount="indefinite"/></g>')
    p.append("</g>")
    # Teclado fica parado; as teclas acendem enquanto ele digita
    p.append(pixels(HERO[18:], hx, hy + 18 * px, px))
    for i, col in enumerate((3, 9, 15, 5, 19, 11, 7, 17)):
        p.append(
            f'<rect x="{hx + col * px}" y="{hy + 20 * px}" width="{px}" height="{px}" fill="{c["glyph"]}" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;0" keyTimes="0;0.1;1" dur="1.6s" '
            f'begin="{i * 0.2:.1f}s" repeatCount="indefinite"/></rect>'
        )
    # Mãos digitando, alternando esquerda e direita
    for i, col in enumerate((6, 15)):
        p.append(
            f'<g>{pixels(["KKK", "SSS"], hx + col * px, hy + 18 * px, px)}'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {-px}" keyTimes="0;0.5" '
            f'calcMode="discrete" dur="0.5s" begin="{i * 0.25}s" repeatCount="indefinite"/></g>'
        )
    # Caneca de café com vapor
    mx, my = x + size - 44, y + size - 36
    p.append(pixels(MUG, mx, my, 5))
    p.append("</g>")
    for i in range(3):
        p.append(
            f'<rect x="{mx + 4 + i * 5}" y="{my - 6}" width="3" height="5" fill="{c["muted"]}" opacity="0">'
            f'<animateTransform attributeName="transform" type="translate" values="0 0; 0 -16" dur="2s" '
            f'begin="{i * 0.6:.1f}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0;0.8;0" dur="2s" begin="{i * 0.6:.1f}s" repeatCount="indefinite"/></rect>'
        )
    return "\n".join(p)


def build(lang, theme):
    c, tx = THEMES[theme], TEXT[lang]
    p = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
        f'role="img" aria-label="{escape(tx["title"])}: {escape(tx["name"])}">',
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="{c["bg"]}" stroke="{c["border"]}" stroke-width="2"/>',
        f'<rect x="8" y="8" width="{W-16}" height="{H-16}" rx="9" fill="none" stroke="{c["border"]}"/>',
    ]

    # Cabeçalho
    p.append(f'<rect x="28" y="26" width="10" height="10" fill="{c["accent"]}" transform="rotate(45 33 31)"/>')
    p.append(t(48, 36, tx["title"], 13, c["accent"], "bold", spacing=2))
    p.append(t(W - 30, 36, tx["save"], 12, c["muted"], anchor="end"))
    p.append(f'<line x1="24" y1="52" x2="{W-24}" y2="52" stroke="{c["border"]}" stroke-dasharray="4 4"/>')

    # Retrato, nome e nível
    p.append(portrait(32, 70, 200, c))
    p.append(t(132, 302, tx["name"], 20, c["text"], "bold", "middle", 2))
    p.append(t(132, 326, tx["level"], 13, c["muted"], anchor="middle"))

    # Informações
    x, y = 264, 84
    for label, value in tx["info"]:
        p.append(t(x, y, label, 11, c["muted"], spacing=1.5))
        p.append(t(x, y + 19, value, 15, c["text"]))
        y += 40

    # Atributos: os blocos acendem um a um, como um save carregando
    ax = 560
    p.append(t(ax, 84, tx["attr_title"], 11, c["accent"], "bold", spacing=1.5))
    y = 112
    for row, (label, val) in enumerate(tx["stats"]):
        p.append(t(ax, y, label, 12, c["text"]))
        bx = ax + 110
        for i in range(10):
            p.append(f'<rect x="{bx + i * 17}" y="{y - 11}" width="14" height="12" rx="2" fill="{c["bar_off"]}"/>')
            if i < val:
                begin = 0.3 + row * 0.12 + i * 0.06
                p.append(
                    f'<rect x="{bx + i * 17}" y="{y - 11}" width="14" height="12" rx="2" fill="{c["bar"]}" opacity="0">'
                    f'<animate attributeName="opacity" from="0" to="1" dur="0.15s" begin="{begin:.2f}s" fill="freeze"/></rect>'
                )
        p.append(t(bx + 10 * 17 + 6, y, "MAX" if val >= 10 else f"{val}", 12, c["muted"]))
        y += 28

    # Habilidades especiais
    p.append(t(264, 300, tx["abil_title"], 11, c["accent"], "bold", spacing=1.5))
    cx = 264
    for ab in tx["abilities"]:
        w = int(len(ab) * 8.4) + 24
        p.append(f'<rect x="{cx}" y="312" width="{w}" height="28" rx="6" fill="{c["chip"]}" stroke="{c["border"]}"/>')
        p.append(t(cx + w / 2, 331, ab, 13, c["text"], anchor="middle"))
        cx += w + 10

    # Barra de XP: enche ao abrir e para em 72%
    p.append(t(32, 382, "XP", 12, c["xp"], "bold", spacing=1))
    bw = W - 32 - 64 - 300
    p.append(f'<rect x="64" y="371" width="{bw}" height="14" rx="7" fill="{c["bar_off"]}"/>')
    p.append(
        f'<rect x="64" y="371" width="{int(bw * 0.72)}" height="14" rx="7" fill="{c["xp"]}">'
        f'<animate attributeName="width" from="0" to="{int(bw * 0.72)}" dur="1.6s" begin="0.3s" fill="freeze"/></rect>'
    )
    p.append(t(W - 290, 382, tx["xp"], 12, c["muted"]))
    cur_x = W - 290 + len(tx["xp"]) * 7.25
    p.append(
        f'<rect x="{cur_x:.0f}" y="372" width="7" height="13" fill="{c["muted"]}">'
        '<animate attributeName="opacity" values="1;0" dur="1s" calcMode="discrete" repeatCount="indefinite"/></rect>'
    )

    p.append("</svg>")
    return "\n".join(p)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        sys.stdout.reconfigure(encoding="utf-8")
        print(build(sys.argv[1], sys.argv[2]))
        raise SystemExit
    OUT.mkdir(exist_ok=True)
    for lang in TEXT:
        for theme in THEMES:
            f = OUT / f"sheet-{lang}-{theme}.svg"
            f.write_text(build(lang, theme), encoding="utf-8")
            print("ok", f.name)
