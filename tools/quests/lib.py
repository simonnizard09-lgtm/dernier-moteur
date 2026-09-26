"""Mini-DSL de génération FTB Quests (2101.x, Minecraft 1.21.1).

Chaque quête est déclarée en Python ; le générateur écrit :
  config/ftbquests/quests/data.snbt
  config/ftbquests/quests/chapter_groups.snbt
  config/ftbquests/quests/chapters/<chapitre>.snbt
  config/ftbquests/quests/lang/en_us.snbt   (textes, format « translation keys » de FTB Quests 21.x)
Les identifiants hexadécimaux sont dérivés d'un hash stable de la clé : régénérer ne casse pas
la progression d'une sauvegarde existante tant que les clés ne changent pas.
"""
import hashlib, json, os

ALL_IDS = set()


def hid(*parts):
    # FTB Quests lit les IDs comme des long signés : bit de poids fort à 0 obligatoire,
    # sinon l'objet reçoit un nouvel ID au chargement (dépendances et textes perdus).
    def mk(seed):
        return "%016X" % (int(hashlib.sha1(seed.encode()).hexdigest()[:16], 16) & 0x7FFFFFFFFFFFFFFF)
    h = mk("/".join(parts))
    # FTB Quests réserve 0 et 1 ; on évite aussi les collisions accidentelles
    while h in ALL_IDS or int(h, 16) < 2:
        h = mk(h + "x")
    ALL_IDS.add(h)
    return h


# ---------------------------------------------------------------- SNBT
def snbt(v, ind=0):
    pad = "\t" * ind
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, Long):
        return f"{v.v}L"
    if isinstance(v, Double):
        return f"{v.v}d"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return f"{v}d"
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, list):
        if not v:
            return "[ ]"
        inner = "\n".join("\t" * (ind + 1) + snbt(x, ind + 1) for x in v)
        return "[\n" + inner + "\n" + pad + "]"
    if isinstance(v, dict):
        if not v:
            return "{ }"
        lines = []
        for k in sorted(v):
            key = k if k.replace("_", "").isalnum() else json.dumps(k)
            lines.append("\t" * (ind + 1) + f"{key}: {snbt(v[k], ind + 1)}")
        return "{\n" + "\n".join(lines) + "\n" + pad + "}"
    raise TypeError(v)


class Long:
    def __init__(self, v): self.v = int(v)


class Double:
    def __init__(self, v): self.v = float(v)


# ---------------------------------------------------------------- tâches / récompenses
def item(id, count=1, components=None):
    return ("item", id, count, components)


def kill(entity, n=1):
    return ("kill", entity, n)


def dim(d):
    return ("dimension", d)


def struct(s):
    return ("structure", s)


def adv(a):
    return ("advancement", a)


def check():
    return ("checkmark",)


def xp(n):
    return ("xp", n)


class Quest:
    def __init__(self, key, title, icon=None, tasks=(), deps=(), desc=(), rewards=(),
                 subtitle=None, shape=None, size=None, optional=False, x=None, y=None):
        self.key, self.title, self.icon = key, title, icon
        self.tasks, self.deps, self.desc = list(tasks), list(deps), list(desc)
        self.rewards, self.subtitle = list(rewards), subtitle
        self.shape, self.size, self.optional = shape, size, optional
        self.x, self.y = x, y


class Chapter:
    def __init__(self, key, title, icon, group, subtitle=None, quests=()):
        self.key, self.title, self.icon, self.group = key, title, icon, group
        self.subtitle, self.quests = subtitle, list(quests)


def stack(id, count=1, components=None):
    d = {"id": id, "count": count}
    if components:
        d["components"] = components
    return d
