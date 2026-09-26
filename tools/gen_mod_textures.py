#!/usr/bin/env python3
"""Textures du mod dernier_moteur (blocs du Moteur, clé, cœur, Gardien du Noyau).

Usage : python3 tools/gen_mod_textures.py   (depuis la racine du dépôt ; nécessite Pillow)
Toutes les textures sont originales et procédurales : pas de ressource Mojang copiée.
La texture du Gardien (128×128) couvre toute la surface : le modèle du golem de fer
y lit ses UV, on obtient donc un golem d'alliage noirci veiné de braise.
"""
import os, random
from PIL import Image

OUT = "mod/src/main/resources/assets/dernier_moteur/textures"
rng = random.Random(1337)


def hexc(h, a=255):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) + (a,)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3]) + (c[3],)


def save(img, kind, name):
    os.makedirs(os.path.join(OUT, kind), exist_ok=True)
    img.save(os.path.join(OUT, kind, name + ".png"))


def metal(size, base="#2e363b", noise=0.12):
    img = Image.new("RGBA", (size, size))
    b = hexc(base)
    for x in range(size):
        for y in range(size):
            img.putpixel((x, y), shade(b, 1 + rng.uniform(-noise, noise)))
    return img


# --- Boîtier du Moteur : plaque rivetée, liseré de laiton
casing = metal(16)
for i in range(16):
    for j in (0, 15):
        casing.putpixel((i, j), hexc("#15191c"))
        casing.putpixel((j, i), hexc("#15191c"))
    for j in (1, 14):
        if 1 <= i <= 14:
            casing.putpixel((i, j), hexc("#8a6a2a"))
            casing.putpixel((j, i), hexc("#8a6a2a"))
for (x, y) in [(3, 3), (12, 3), (3, 12), (12, 12)]:
    casing.putpixel((x, y), hexc("#c9a45c"))
    casing.putpixel((x + 1, y + 1), hexc("#5a4018"))
for i in range(5, 11):
    casing.putpixel((i, 8), hexc("#1f2528"))
    casing.putpixel((8, i), hexc("#1f2528"))
save(casing, "block", "engine_casing")


# --- Façade du contrôleur : cadran central (éteint / allumé)
def front(lit):
    img = casing.copy()
    core = hexc("#f07a2a") if lit else hexc("#4a2a1a")
    glow = hexc("#ffd27a") if lit else hexc("#6a3a22")
    for x in range(4, 12):
        for y in range(4, 12):
            d = abs(x - 7.5) + abs(y - 7.5)
            if d <= 5:
                img.putpixel((x, y), hexc("#15191c"))
            if d <= 4:
                img.putpixel((x, y), core)
            if d <= 1.5:
                img.putpixel((x, y), glow)
    return img


save(front(False), "block", "engine_core_front")
save(front(True), "block", "engine_core_front_lit")

# --- Clé du Gardien
key = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
gold, dark, ember = hexc("#d4a94e"), hexc("#6b4f1a"), hexc("#f07a2a")
for (x, y) in [(3, 2), (4, 2), (5, 2), (2, 3), (6, 3), (2, 4), (6, 4), (2, 5), (6, 5), (3, 6), (4, 6), (5, 6)]:
    key.putpixel((x, y), gold)
key.putpixel((4, 4), ember)
for i in range(6):
    key.putpixel((5 + i, 6 + i), gold)
    key.putpixel((6 + i, 6 + i), dark)
for (x, y) in [(9, 12), (10, 13), (8, 11), (11, 10), (12, 11)]:
    key.putpixel((x, y), gold)
save(key, "item", "guardian_key")

# --- Cœur du Gardien : cœur mécanique incandescent
heart_map = [
    "................",
    "................",
    "...oo.....oo....",
    "..oEEo...oEEo...",
    ".oEeeEo.oEeeEo..",
    ".oEeYeEoEeYeEo..",
    ".oEeeeeEeeeeEo..",
    ".oEeeeeeeeeeEo..",
    "..oEeeeeeeeEo...",
    "...oEeeeeeEo....",
    "....oEeeeEo.....",
    ".....oEeEo......",
    "......oEo.......",
    ".......o........",
    "................",
    "................",
]
pal = {"o": hexc("#15191c"), "E": hexc("#5b6b73"), "e": hexc("#f07a2a"), "Y": hexc("#fff2c0")}
heart = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
for y, row in enumerate(heart_map):
    for x, ch in enumerate(row):
        if ch in pal:
            heart.putpixel((x, y), pal[ch])
save(heart, "item", "guardian_heart")

# --- Gardien du Noyau : 128×128, alliage noirci + veines de braise + rivets
g = metal(128, "#30393e", 0.15)
for _ in range(38):  # veines de braise
    x, y = rng.randrange(128), rng.randrange(128)
    for _ in range(rng.randrange(6, 18)):
        g.putpixel((x % 128, y % 128), hexc("#f07a2a"))
        if rng.random() < 0.4:
            g.putpixel(((x + 1) % 128, y % 128), hexc("#ffb05a"))
        x += rng.choice((-1, 0, 1))
        y += rng.choice((0, 1))
for x in range(0, 128, 8):  # rivets de laiton
    for y in range(0, 128, 8):
        if rng.random() < 0.35:
            g.putpixel((x + 3, y + 3), hexc("#c9a45c"))
save(g, "entity", "core_guardian")
print("Textures du mod générées dans", OUT)
