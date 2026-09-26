#!/usr/bin/env python3
"""Génère les textures 16x16 des items/blocs KubeJS du namespace dernier_moteur.

Usage : python3 tools/gen_textures.py [dossier_assets]
(par défaut pack/kubejs/assets/dernier_moteur/textures). Nécessite Pillow.
Les textures sont volontairement simples et lisibles (pixel art procédural).
"""
import os, sys
from PIL import Image

OUT = sys.argv[1] if len(sys.argv) > 1 else "pack/kubejs/assets/dernier_moteur/textures"
T = (0, 0, 0, 0)


def hexc(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3]) + (c[3],)


def from_map(rows, palette):
    img = Image.new("RGBA", (16, 16), T)
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch in palette:
                img.putpixel((x, y), palette[ch])
    return img


def save(img, kind, name):
    d = os.path.join(OUT, kind)
    os.makedirs(d, exist_ok=True)
    img.save(os.path.join(d, name + ".png"))


# --- Fragments du Noyau : éclat cristallin avec cœur lumineux ---
SHARD = [
    "................",
    "........o.......",
    ".......oLo......",
    "......oLlDo.....",
    "......oLlDo.....",
    ".....oLlcDDo....",
    ".....oLlcDDo....",
    "....oLllcDDDo...",
    "....oLlccDDDo...",
    "...oLllccDDDDo..",
    "...oLllcDDDDDo..",
    "....oLlcDDDDo...",
    ".....oLDDDDo....",
    "......oLDDo.....",
    ".......oDo......",
    "........o.......",
]
FRAGMENTS = {
    "core_fragment_gear": "#c9a45c",   # laiton
    "core_fragment_spark": "#58c7f0",  # électrique
    "core_fragment_ember": "#f06a2a",  # braise
    "core_fragment_storm": "#9a7cf2",  # tempête
    "core_fragment_void": "#3fd6a8",   # néant (vert d'Ender)
    "core_fragment_abyss": "#2f6fd6",  # abysse
}
for name, col in FRAGMENTS.items():
    c = hexc(col)
    pal = {"o": shade(c, 0.35), "L": shade(c, 1.35), "l": shade(c, 1.1), "D": shade(c, 0.75),
           "c": (255, 255, 240, 255)}
    save(from_map(SHARD, pal), "item", name)

# --- Codex : livre relié avec emblème coloré ---
BOOK = [
    "................",
    "..oooooooooooo..",
    "..oCCCCCCCCCCpo.",
    "..oCCCCCCCCCCpo.",
    "..oCCCgggggCCpo.",
    "..oCCgGGGGGgCpo.",
    "..oCCgGeeeGgCpo.",
    "..oCCgGeEeGgCpo.",
    "..oCCgGeeeGgCpo.",
    "..oCCgGGGGGgCpo.",
    "..oCCCgggggCCpo.",
    "..oCCCCCCCCCCpo.",
    "..oCCCCCCCCCCpo.",
    "..oBBBBBBBBBBBo.",
    "..oooooooooooo..",
    "................",
]
CODEX = {"codex_spark": ("#2c4f73", "#58c7f0"),
         "codex_forge": ("#5a3522", "#f0a22a"),
         "codex_automaton": ("#2f2f3a", "#3fd6a8")}
for name, (cover, emb) in CODEX.items():
    c, e = hexc(cover), hexc(emb)
    pal = {"o": shade(c, 0.45), "C": c, "p": (230, 222, 200, 255), "B": (200, 190, 165, 255),
           "g": hexc("#c9a45c"), "G": shade(c, 0.8), "e": e, "E": (255, 255, 255, 255)}
    save(from_map(BOOK, pal), "item", name)

# --- Journaux : carnet de cuir usé, numéroté par une couleur de marque-page ---
JOURNAL = [
    "................",
    "...ooooooooooo..",
    "...oLLLLLLLLLpo.",
    "...oLllllllLLpo.",
    "...oLlLLLLlLLpo.",
    "...oLlLLLLlLLpo.",
    "...oLllllllLLpo.",
    "...oLLLLLLLLLpo.",
    "...oLLLLLLLLLpo.",
    "...oLLLLLLLLLpo.",
    "...oLLLLLLLLLpo.",
    "...oLLLLLLLLLpo.",
    "...oPPPPPPPPPPo.",
    "...oooooooomooo.",
    "..........mm....",
    "................",
]
MARKS = ["#c0392b", "#e67e22", "#f1c40f", "#27ae60", "#16a085", "#2980b9", "#8e44ad", "#ecf0f1"]
for i, m in enumerate(MARKS, start=1):
    pal = {"o": hexc("#3b2414"), "L": hexc("#7a4a28"), "l": hexc("#9c6a3e"),
           "p": hexc("#e8dcc0"), "P": hexc("#d6c7a1"), "m": hexc(m)}
    save(from_map(JOURNAL, pal), "item", f"journal_{i}")

# --- Mécanisme à vapeur : engrenage de laiton + tuyau de cuivre ---
save(from_map([
    "................",
    "......b..b......",
    "....bbBBBBbb....",
    "....bBBBBBBb....",
    "..bbBBboobBBbb..",
    "...bBBo..oBBb...",
    "...bBo.cc.oBb...",
    "...bBo.cc.oBb...",
    "...bBBo..oBBb...",
    "..bbBBboobBBbb..",
    "....bBBBBBBbCCCC",
    "....bbBBBBbbCccC",
    "......b..b..CCCC",
    "................",
    "................",
    "................",
], {"b": hexc("#7a5a22"), "B": hexc("#d4a94e"), "o": hexc("#5a4018"),
    "c": hexc("#e8e8e8"), "C": hexc("#a0522d"), }), "item", "steam_mechanism")

# --- Bobine galvanique : cylindre de cuivre bobiné, cœur d'acier ---
save(from_map([
    "................",
    "....ssssssss....",
    "...sSSSSSSSSs...",
    "...cCcCcCcCcC...",
    "...CcCcCcCcCc...",
    "...cCcCcCcCcC...",
    "...CcCcCcCcCc...",
    "...cCcCcCcCcC...",
    "...CcCcCcCcCc...",
    "...cCcCcCcCcC...",
    "...CcCcCcCcCc...",
    "...cCcCcCcCcC...",
    "...sSSSSSSSSs...",
    "....ssssssss....",
    "......y..y......",
    "......y..y......",
], {"s": hexc("#4a4f55"), "S": hexc("#8a9199"), "c": hexc("#b5652b"),
    "C": hexc("#e0894a"), "y": hexc("#58c7f0")}), "item", "galvanic_coil")

# --- Alliage du Noyau : lingot sombre veiné d'orange ---
save(from_map([
    "................",
    "................",
    "................",
    "................",
    "......oooooooo..",
    ".....oHHHHHHHo..",
    "....oHhhhhhhHAo.",
    "...oHhhvhhhhAAo.",
    "..oHhhhhvvhhAAo.",
    "..oAAAAAAAAAAAo.",
    "..oAAvAAAAAAAo..",
    "..oAAAAAvAAAo...",
    "..ooooooooooo...",
    "................",
    "................",
    "................",
], {"o": hexc("#15191c"), "H": hexc("#5b6b73"), "h": hexc("#3e4a50"),
    "A": hexc("#2a3236"), "v": hexc("#f07a2a")}), "item", "core_alloy")

# --- Processeur du Moteur : puce avec cœur fluix/braise ---
save(from_map([
    "................",
    "...g.g.g.g.g....",
    "..pppppppppppp..",
    "..pDDDDDDDDDDp..",
    ".gpDkkkkkkkkDpg.",
    "..pDkFFFFFFkDp..",
    ".gpDkFeeeeFkDpg.",
    "..pDkFeEEeFkDp..",
    ".gpDkFeEEeFkDpg.",
    "..pDkFeeeeFkDp..",
    ".gpDkFFFFFFkDpg.",
    "..pDkkkkkkkkDp..",
    "..pDDDDDDDDDDp..",
    "..pppppppppppp..",
    "...g.g.g.g.g....",
    "................",
], {"p": hexc("#1f2a2e"), "D": hexc("#2f4a3e"), "k": hexc("#3b3b46"), "g": hexc("#d4a94e"),
    "F": hexc("#7b54c8"), "e": hexc("#f07a2a"), "E": hexc("#fff2c0")}), "item", "engine_processor")

# --- Bloc d'alliage du Noyau ---
img = Image.new("RGBA", (16, 16), hexc("#2a3236"))
for x in range(16):
    for y in range(16):
        if x in (0, 15) or y in (0, 15):
            img.putpixel((x, y), hexc("#15191c"))
        elif x in (1, 14) or y in (1, 14):
            img.putpixel((x, y), hexc("#5b6b73"))
for (x, y) in [(4, 4), (5, 5), (6, 5), (7, 6), (8, 7), (9, 9), (10, 10), (11, 10), (5, 10), (6, 11)]:
    img.putpixel((x, y), hexc("#f07a2a"))
save(img, "block", "core_alloy_block")

print("Textures générées dans", OUT)
