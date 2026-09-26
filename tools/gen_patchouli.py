#!/usr/bin/env python3
"""Génère le contenu du Carnet de l'Ingénieur (Patchouli, livre externe patchouli:carnet)
et les advancements qui déverrouillent les journaux.

Sorties :
  pack/kubejs/assets/patchouli/patchouli_books/carnet/en_us/{categories,entries}/...
  pack/kubejs/data/dernier_moteur/advancement/journal/journal_N.json
Le texte est en français mais placé sous en_us : c'est la langue de repli de Patchouli,
donc tout le monde voit le carnet quelle que soit la langue du jeu.
"""
import json, os, shutil

ROOT = "pack/kubejs"
BOOK = os.path.join(ROOT, "assets/patchouli/patchouli_books/carnet/en_us")
ADV = os.path.join(ROOT, "data/dernier_moteur/advancement/journal")


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


CATEGORIES = {
    "journaux": ("Journaux de Vaucor", "dernier_moteur:journal_1",
                 "Les journaux de l'Ingénieure Iléa Vaucor. Chaque page apparaît quand tu retrouves le journal correspondant (quêtes, gardiens, coffres).", 0),
    "eres": ("Guide des ères", "dernier_moteur:codex_spark",
             "Ce qu'il faut accomplir à chaque ère pour rallumer le Moteur.", 1),
}

JOURNALS = [
    ("Le jour où le Moteur s'est tu", [
        "Je note ceci pour qui viendra après.$(br2)Ce matin, le Moteur s'est arrêté. Pas de fracas : un long soupir sous la roche, puis le silence. Les rivières se sont troublées avant midi. Au soir, le vent était froid comme un hiver avancé.",
        "Le Moteur ne faisait pas que tourner. Il $(l)tenait le monde$() : l'eau pure, les saisons douces, les bêtes à leur place. Sans lui, tout se dérègle.$(br2)Nos gardiens mécaniques — ceux qui protégeaient le Noyau — se sont figés, puis se sont réveillés… autrement.",
        "Le Noyau s'est brisé en six $(l)fragments$(). Chaque gardien en a emporté un.$(br2)Nos techniques se perdent avec nous. Je les consigne dans l'ordre où nous les avions apprises : le $(l)Rouage$(), l'$(l)Étincelle$(), la $(l)Forge$(), l'$(l)Automate$(). Qui les retrouvera pourra rallumer le Moteur."]),
    ("Notes sur les gardiens de fer", [
        "Le premier gardien, le $(l)Wroughtnaut$(), veillait sur l'atelier des rouages. C'est une armure vide que nous avions animée pour garder les mines.$(br2)Depuis l'arrêt, il erre dans les cavernes profondes et frappe tout ce qui bouge.",
        "Son point faible n'a pas changé : après une grande charge, il reste un instant exposé. Frappe-le $(l)dans le dos$() à ce moment-là.$(br2)Il porte le fragment du $(l)Rouage$(). Avec lui, un peu d'écaille de Naga et un mécanisme à vapeur, tu pourras relier le $(l)Codex de l'Étincelle$()."]),
    ("La tour de la Liche", [
        "Au-delà du portail du Crépuscule, une tour s'élève au-dessus des arbres. Son maître, la $(l)Liche$(), a trouvé le fragment de l'$(l)Étincelle$() tombé dans sa forêt, et s'en nourrit.$(br2)Elle se cache derrière des boucliers d'ombre et des doubles.",
        "Brise ses boucliers, ignore les faux reflets, frappe l'original.$(br2)Avec l'Étincelle, relie le $(l)Codex de la Forge$(). La forge était notre troisième leçon : fondre le monde, le séparer, le recomposer. Mekanism et les grands fourneaux t'attendent."]),
    ("La forge des âmes", [
        "Dans le Nether, notre forge-relais a été reprise par $(l)Ignis$(), un chevalier de flammes que nos maîtres-forgerons avaient éveillé pour attiser le feu.$(br2)Il garde le fragment de la $(l)Braise$().",
        "Prévois de quoi résister au feu et de quoi tenir longtemps : Ignis entre en rage quand son bouclier se brise.$(br2)La Braise et la Tempête, réunies avec l'alliage du Noyau, forment le $(l)Codex de l'Automate$()."]),
    ("L'usine ancienne", [
        "C'est ici que nous fabriquions les gardiens. Le $(l)Harbinger$(), notre contremaître mécanique, supervisait la chaîne.$(br2)Aujourd'hui il tire sur tout ce qui franchit les portes. Il garde le fragment de la $(l)Tempête$().",
        "Il se recharge sur ses bobines : coupe-lui l'accès, frappe pendant les pauses.$(br2)Si tu tiens ce journal, tu as vu l'usine. Tu sais maintenant que les machines peuvent fabriquer des machines. C'est la dernière leçon."]),
    ("Au-delà de l'End", [
        "Le fragment du $(l)Néant$() a été emporté jusqu'aux îles extérieures de l'End, dans une citadelle en ruine. Son gardien, l'$(l)Ender Guardian$(), fut notre sentinelle la plus loyale.$(br2)Il ne reconnaît plus personne.",
        "Automatise avant d'y aller : réseau ME, processeurs du Moteur, réserves d'énergie. Tu auras besoin de tout ce que tu as bâti pour la fin."]),
    ("Les cités englouties", [
        "Le dernier fragment, l'$(l)Abysse$(), repose dans une cité engloutie. Le $(l)Léviathan$() s'y est enroulé comme autour d'un œuf.$(br2)Il frappe depuis les profondeurs et attire ses proies dans les courants.",
        "Respiration aquatique, vitesse de nage, et du recul pour éviter son rayon.$(br2)Avec six fragments, tu pourras forger la $(l)Clé du Gardien$(). Le dernier gardien t'attend."]),
    ("Le dernier gardien", [
        "Le $(l)Gardien du Noyau$() n'est pas devenu fou. Nous l'avions conçu pour éprouver quiconque voudrait rallumer le Moteur.$(br2)Il se bat en trois temps : il frappe, puis il appelle ses serviteurs et tire, puis il ne retient plus rien.",
        "Son $(l)cœur$() est la dernière pièce. Bâtis le $(l)Moteur$() (5×5×5 de boîtiers autour du contrôleur), remplis sa réserve d'énergie, dépose-y les six fragments, le cœur et quatre processeurs du Moteur.$(br2)Puis rallume-le. Et écoute le monde respirer à nouveau."]),
]

ERAS = [
    ("Ère 0 — Réveil", "minecraft:campfire",
     "Survis d'abord. Bois de l'eau purifiée (gourde, purificateur de Tough As Nails), habille-toi selon la saison, mange varié.$(br2)Les mobs deviennent plus forts avec le temps : abrite-toi vite. Objectif : ton premier $(l)alliage d'andésite$() (Create)."),
    ("Ère I — Vapeur", "create:cogwheel",
     "Create : roues à eau, presse, mixeur, laiton, mécanisme de précision, machine à vapeur. Construis le $(l)mécanisme à vapeur$() (assemblage séquencé).$(br2)Portes : la $(l)Naga$() (écaille) et le $(l)Ferrous Wroughtnaut$() (fragment du Rouage). Puis relie le $(l)Codex de l'Étincelle$()."),
    ("Ère II — Électricité", "immersiveengineering:hammer",
     "Le Codex de l'Étincelle déverrouille le marteau et l'établi d'Immersive Engineering, et la $(l)bobine galvanique$() (alternateur, moteur électrique, dynamo).$(br2)Four à coke, acier, fils. Porte : la $(l)Liche$() (fragment de l'Étincelle) → $(l)Codex de la Forge$()."),
    ("Ère III — Industrie lourde", "mekanism:steel_casing",
     "Le Codex de la Forge déverrouille le boîtier en acier et l'infuseur de Mekanism, et l'ingénierie lourde d'IE.$(br2)Minerais ×5, $(l)alliage du Noyau$(). Portes : $(l)Ignis$() et le $(l)Harbinger$() (Braise, Tempête) → $(l)Codex de l'Automate$()."),
    ("Ère IV — Automatisation", "ae2:controller",
     "Le Codex de l'Automate déverrouille le graveur AE2 et les cadres d'Industrial Foregoing. Grave le $(l)processeur du Moteur$().$(br2)Portes : l'$(l)Ender Guardian$() (Néant) et le $(l)Léviathan$() (Abysse). Avec six fragments, forge la $(l)Clé du Gardien$()."),
    ("Épilogue — Le Moteur", "dernier_moteur:core_fragment_gear",
     "Invoque le $(l)Gardien du Noyau$() avec la clé et prends son cœur.$(br2)Bâtis le $(l)Moteur$(), remplis-le d'énergie (FE) et d'items : six fragments, cœur du gardien, quatre processeurs du Moteur. Puis active-le."),
]


def main():
    if os.path.isdir(BOOK):
        shutil.rmtree(BOOK)
    for cid, (name, icon, desc, order) in CATEGORIES.items():
        write(f"{BOOK}/categories/{cid}.json",
              {"name": name, "description": desc, "icon": icon, "sortnum": order})
    for i, (title, pages) in enumerate(JOURNALS, start=1):
        entry = {
            "name": f"n°{i} — {title}",
            "icon": f"dernier_moteur:journal_{i}",
            "category": "patchouli:journaux",
            "sortnum": i,
            "pages": [{"type": "patchouli:text", "text": p} for p in pages],
        }
        if i > 1:
            entry["advancement"] = f"dernier_moteur:journal/journal_{i}"
        write(f"{BOOK}/entries/journaux/journal_{i}.json", entry)
        write(f"{ADV}/journal_{i}.json", {
            "criteria": {"has_journal": {
                "trigger": "minecraft:inventory_changed",
                "conditions": {"items": [{"items": f"dernier_moteur:journal_{i}"}]}}},
            "requirements": [["has_journal"]],
        })
    for i, (title, icon, text) in enumerate(ERAS):
        write(f"{BOOK}/entries/eres/era_{i}.json", {
            "name": title, "icon": icon, "category": "patchouli:eres", "sortnum": i,
            "pages": [{"type": "patchouli:text", "text": text}],
        })
    print("Carnet généré.")


if __name__ == "__main__":
    main()
