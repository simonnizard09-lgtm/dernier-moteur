#!/usr/bin/env python3
"""Génère les quêtes FTB du pack.

Usage (depuis la racine du dépôt) :
    python3 tools/quests/build.py [--dump chemin/dump_registries.json]

--dump : fichier produit par un script KubeJS de dump (items, entités, structures,
advancements). Si fourni, chaque identifiant utilisé dans les quêtes est vérifié ; le script
échoue si un identifiant est inconnu (hors identifiants du mod custom, listés dans MOD_IDS).
"""
import argparse, json, os, shutil, sys

sys.path.insert(0, os.path.dirname(__file__))
from lib import Chapter, Double, Long, hid, snbt, stack  # noqa: E402
import content  # noqa: E402

OUT = "pack/config/ftbquests/quests"

# Identifiants fournis par le mod custom dernier_moteur (absents d'un dump sans le mod)
MOD_IDS = {
    "items": {"dernier_moteur:guardian_key", "dernier_moteur:guardian_heart",
              "dernier_moteur:engine_casing", "dernier_moteur:engine_core"},
    "entities": {"dernier_moteur:core_guardian"},
    "advancements": {"dernier_moteur:engine_ignited"},
}


def layout(ch):
    """Placement automatique : profondeur de dépendance -> x, rang -> y."""
    by_key = {q.key: q for q in ch.quests}
    depth = {}

    def d(q, seen=()):
        if q.key in depth:
            return depth[q.key]
        local = [by_key[x] for x in q.deps if x in by_key]
        depth[q.key] = 0 if not local else 1 + max(d(p, seen + (q.key,)) for p in local)
        return depth[q.key]

    for q in ch.quests:
        d(q)
    cols = {}
    for q in ch.quests:
        cols.setdefault(depth[q.key], []).append(q)
    for c, qs in cols.items():
        n = len(qs)
        for i, q in enumerate(qs):
            if q.x is None:
                q.x = c * 2.0
            if q.y is None:
                q.y = (i - (n - 1) / 2) * 1.6


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dump")
    args = ap.parse_args()

    known = None
    if args.dump:
        d = json.load(open(args.dump))
        known = {k: set(v) | MOD_IDS.get(k, set()) for k, v in d.items()}

    errors = []

    def check(kind, ident, where):
        if known is None:
            return
        if ident not in known.get(kind, set()):
            errors.append(f"{where}: {kind[:-1]} inconnu {ident}")

    chapters = content.CHAPTERS
    groups = content.GROUPS
    lang = {}

    # identifiants
    qid = {}
    for ch in chapters:
        ch.id = hid("chapter", ch.key)
        for q in ch.quests:
            qid[f"{ch.key}:{q.key}"] = hid("quest", ch.key, q.key)
    gid = {g: hid("group", g) for g, _ in groups}

    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(f"{OUT}/chapters")
    os.makedirs(f"{OUT}/lang")

    for g, title in groups:
        lang[f"chapter_group.{gid[g]}.title"] = title

    total = 0
    for order, ch in enumerate(chapters):
        layout(ch)
        check("items", ch.icon, f"chapitre {ch.key}")
        lang[f"chapter.{ch.id}.title"] = ch.title
        if ch.subtitle:
            lang[f"chapter.{ch.id}.chapter_subtitle"] = [ch.subtitle]
        quests = []
        for q in ch.quests:
            where = f"{ch.key}:{q.key}"
            full = qid[where]
            deps = []
            for dep in q.deps:
                ref = dep if ":" in dep and dep.split(":")[0] in {c.key for c in chapters} else f"{ch.key}:{dep}"
                if ref not in qid:
                    errors.append(f"{where}: dépendance inconnue {dep}")
                    continue
                deps.append(qid[ref])
            tasks = []
            for i, t in enumerate(q.tasks):
                tid = hid("task", ch.key, q.key, str(i))
                kind = t[0]
                if kind == "item":
                    _, ident, count, comps = t
                    check("items", ident, where)
                    task = {"id": tid, "type": "item", "item": stack(ident, 1, comps)}
                    if count > 1:
                        task["count"] = Long(count)
                elif kind == "kill":
                    check("entities", t[1], where)
                    task = {"id": tid, "type": "kill", "entity": t[1], "value": Long(t[2])}
                elif kind == "dimension":
                    check("dimensions", t[1], where)
                    task = {"id": tid, "type": "dimension", "dimension": t[1]}
                elif kind == "structure":
                    check("structures", t[1], where)
                    task = {"id": tid, "type": "structure", "structure": t[1]}
                elif kind == "advancement":
                    check("advancements", t[1], where)
                    task = {"id": tid, "type": "advancement", "advancement": t[1], "criterion": ""}
                elif kind == "checkmark":
                    task = {"id": tid, "type": "checkmark"}
                else:
                    raise ValueError(kind)
                tasks.append(task)
            if not tasks:
                errors.append(f"{where}: aucune tâche")
            rewards = []
            for i, r in enumerate(q.rewards):
                rid = hid("reward", ch.key, q.key, str(i))
                if r[0] == "item":
                    _, ident, count, comps = r
                    check("items", ident, where)
                    rewards.append({"id": rid, "type": "item", "item": stack(ident, count, comps)})
                elif r[0] == "xp":
                    rewards.append({"id": rid, "type": "xp", "xp": r[1]})
            quest = {"id": full, "x": Double(q.x), "y": Double(q.y), "tasks": tasks}
            if deps:
                quest["dependencies"] = deps
            if rewards:
                quest["rewards"] = rewards
            if q.icon:
                check("items", q.icon, where)
                quest["icon"] = stack(q.icon)
            if q.shape:
                quest["shape"] = q.shape
            if q.size:
                quest["size"] = Double(q.size)
            if q.optional:
                quest["optional"] = True
            quests.append(quest)
            lang[f"quest.{full}.title"] = q.title
            if q.subtitle:
                lang[f"quest.{full}.quest_subtitle"] = q.subtitle
            if q.desc:
                lang[f"quest.{full}.quest_desc"] = list(q.desc)
            total += 1
        data = {
            "id": ch.id,
            "filename": ch.key,
            "group": gid[ch.group] if ch.group else "",
            "icon": stack(ch.icon),
            "order_index": order,
            "default_quest_shape": "",
            "default_hide_dependency_lines": False,
            "quest_links": [],
            "quests": quests,
        }
        with open(f"{OUT}/chapters/{ch.key}.snbt", "w", encoding="utf-8") as f:
            f.write(snbt(data) + "\n")

    with open(f"{OUT}/chapter_groups.snbt", "w", encoding="utf-8") as f:
        f.write(snbt({"chapter_groups": [{"id": gid[g]} for g, _ in groups]}) + "\n")

    with open(f"{OUT}/data.snbt", "w", encoding="utf-8") as f:
        f.write(snbt({
            "version": 13,
            "default_reward_team": False,
            "default_consume_items": False,
            "default_autoclaim_rewards": "disabled",
            "default_quest_shape": "circle",
            "default_quest_disable_jei": False,
            "emergency_items_cooldown": 300,
            "drop_loot_crates": False,
            "disable_gui": False,
            "grid_scale": Double(0.5),
            "pause_game": False,
            "lock_message": "",
            "progression_mode": "flexible",
            "detection_delay": 20,
        }) + "\n")

    with open(f"{OUT}/lang/en_us.snbt", "w", encoding="utf-8") as f:
        f.write(snbt(lang) + "\n")

    print(f"{len(chapters)} chapitres, {total} quêtes écrites dans {OUT}")
    if errors:
        print("\n".join("ERREUR " + e for e in errors))
        sys.exit(1)


if __name__ == "__main__":
    main()
