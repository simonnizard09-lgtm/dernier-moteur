#!/usr/bin/env python3
"""Injecte des copies des journaux d'ingénieur (25 %) dans des coffres de structures.

Écrit (Global Loot Modifiers NeoForge, type neoforge:add_table) :
  pack/kubejs/data/dernier_moteur/loot_table/inject/journal_N.json
  pack/kubejs/data/dernier_moteur/loot_modifiers/journal_N_<table>.json
  pack/kubejs/data/neoforge/loot_modifiers/global_loot_modifiers.json
Les tables citées doivent exister (vérifiées contre le dump : loot_tables).
"""
import json, os, shutil

ROOT = "pack/kubejs/data"
CHANCE = 0.25
# Chaque journal va dans des structures liées à son chapitre de lore.
JOURNALS = {
    2: [  # gardiens de fer, cavernes et mines
        "minecraft:chests/abandoned_mineshaft", "minecraft:chests/simple_dungeon",
        "betterdungeons:zombie_dungeon/chests/common", "betterdungeons:skeleton_dungeon/chests/common",
        "dungeons_arise:chests/mining_system/mining_system_treasure",
        "dungeons_arise:chests/mining_complex/mining_complex_treasure",
    ],
    3: [  # la tour de la Liche
        "twilightforest:chests/tower_library", "twilightforest:chests/tower_room",
        "twilightforest:chests/tower_enchanting",
    ],
    4: [  # la forge des âmes (Nether)
        "minecraft:chests/nether_bridge", "minecraft:chests/bastion_treasure",
        "betterfortresses:chests/keep", "betterfortresses:chests/hall",
        "nova_structures:chests/nether_keep/vault_keep",
        "dungeons_arise:chests/scorched_mines/scorched_mines_treasure",
    ],
    5: [  # l'usine ancienne
        "minecraft:chests/stronghold_library", "minecraft:chests/ancient_city",
        "betterstrongholds:chests/grand_library", "betterstrongholds:chests/library_md",
        "dungeons_arise:chests/foundry/foundry_treasure",
        "dungeons_arise:chests/mechanical_nest/mechanical_nest_treasure",
    ],
    6: [  # au-delà de l'End
        "minecraft:chests/end_city_treasure",
        "nova_structures:chests/end_castle/greater_loot", "nova_structures:chests/end_lighthouse/vault_lighthouse",
    ],
    7: [  # les cités englouties
        "minecraft:chests/underwater_ruin_big", "minecraft:chests/buried_treasure",
        "betteroceanmonuments:chests/upper_side_chamber",
        "aquamirae:chests/ship_1", "aquamirae:chests/ship_2", "cataclysm:chests/acropolis_treasure",
    ],
}


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")


def main():
    shutil.rmtree(f"{ROOT}/dernier_moteur/loot_modifiers", ignore_errors=True)
    entries = []
    for n, tables in JOURNALS.items():
        write(f"{ROOT}/dernier_moteur/loot_table/inject/journal_{n}.json", {
            "type": "minecraft:chest",
            "pools": [{"rolls": 1,
                       "entries": [{"type": "minecraft:item", "name": f"dernier_moteur:journal_{n}"}],
                       "conditions": [{"condition": "minecraft:random_chance", "chance": CHANCE}]}]})
        for t in tables:
            mid = f"journal_{n}_" + t.replace(":", "_").replace("/", "_")
            write(f"{ROOT}/dernier_moteur/loot_modifiers/{mid}.json", {
                "type": "neoforge:add_table",
                "conditions": [{"condition": "neoforge:loot_table_id", "loot_table_id": t}],
                "table": f"dernier_moteur:inject/journal_{n}"})
            entries.append(f"dernier_moteur:{mid}")
    write(f"{ROOT}/neoforge/loot_modifiers/global_loot_modifiers.json", {"replace": False, "entries": entries})
    print(f"{len(entries)} injections de journaux")


if __name__ == "__main__":
    main()
