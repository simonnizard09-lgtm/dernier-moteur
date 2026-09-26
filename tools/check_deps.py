#!/usr/bin/env python3
"""Vérifie les dépendances des mods du pack packwiz.

Télécharge chaque jar (cache local), lit META-INF/neoforge.mods.toml (et les jars
embarqués jar-in-jar), puis signale :
  - dépendances "required" absentes ou hors plage de version ;
  - mods déclarés "incompatible" présents ensemble.
Usage : python3 tools/check_deps.py [dossier_pack] [dossier_cache]
"""
import io, os, re, sys, tomllib, urllib.parse, urllib.request, zipfile

PACK = sys.argv[1] if len(sys.argv) > 1 else "pack"
CACHE = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser("~/.cache/dm-jars")
os.makedirs(CACHE, exist_ok=True)
UA = {"User-Agent": "dernier-moteur-pack-checker/1.0"}

def fetch(url, name):
    path = os.path.join(CACHE, name)
    if not os.path.exists(path):
        req = urllib.request.Request(url, headers=UA)
        data = urllib.request.urlopen(req, timeout=120).read()
        with open(path, "wb") as f:
            f.write(data)
    return path

def url_of(meta):
    dl = meta.get("download", {})
    if dl.get("url"):
        return dl["url"]
    cf = meta.get("update", {}).get("curseforge")
    if cf:
        fid = cf["file-id"]
        return f"https://mediafilez.forgecdn.net/files/{fid // 1000}/{fid % 1000}/{urllib.parse.quote(meta['filename'])}"
    return None

# --- comparaison de versions façon Maven (approximation suffisante) ---
def vkey(v):
    parts = re.split(r"[.\-+_]", v)
    out = []
    for p in parts:
        for tok in re.findall(r"\d+|[A-Za-z]+", p):
            out.append((1, int(tok), "") if tok.isdigit() else (0, 0, tok.lower()))
    return out

def cmp(a, b):
    ka, kb = vkey(a), vkey(b)
    for x, y in zip(ka, kb):
        if x != y:
            return -1 if x < y else 1
    if len(ka) == len(kb):
        return 0
    rest = (ka[len(kb):] if len(ka) > len(kb) else kb[len(ka):])
    # suffixe alphabétique (beta, pre...) = version plus ancienne
    sign = 1 if len(ka) > len(kb) else -1
    return -sign if rest[0][0] == 0 else sign

def in_range(ver, rng):
    rng = (rng or "").strip()
    if not rng or rng == "*" or ver is None:
        return True
    if rng[0] not in "[(":
        return cmp(ver, rng) >= 0  # version "douce" = minimum
    for part in re.findall(r"[\[\(][^\]\)]*[\]\)]", rng):
        lo_inc, hi_inc = part[0] == "[", part[-1] == "]"
        body = part[1:-1]
        if "," not in body:
            if cmp(ver, body.strip()) == 0:
                return True
            continue
        lo, hi = [x.strip() for x in body.split(",", 1)]
        ok = True
        if lo:
            c = cmp(ver, lo); ok &= c > 0 or (lo_inc and c == 0)
        if hi:
            c = cmp(ver, hi); ok &= c < 0 or (hi_inc and c == 0)
        if ok:
            return True
    return False

def read_mods_toml(z, depth=0):
    """Retourne ([(modId, version)], {modId: [deps]}) pour un jar et ses jars embarqués."""
    mods, deps = [], {}
    for n in ("META-INF/neoforge.mods.toml", "META-INF/mods.toml"):
        if n in z.namelist():
            raw = z.read(n).decode("utf-8", "replace")
            try:
                t = tomllib.loads(raw)
            except Exception as e:
                print(f"   ! toml illisible ({e})")
                break
            ver_manifest = None
            if "META-INF/MANIFEST.MF" in z.namelist():
                m = re.search(r"Implementation-Version:\s*(\S+)", z.read("META-INF/MANIFEST.MF").decode("utf-8", "replace"))
                ver_manifest = m.group(1) if m else None
            for m in t.get("mods", []):
                v = str(m.get("version", ""))
                if "${" in v:
                    v = ver_manifest
                mods.append((m["modId"], v))
            for k, lst in t.get("dependencies", {}).items():
                deps.setdefault(k, []).extend(lst if isinstance(lst, list) else [])
            break
    for n in z.namelist():
        if n.startswith("META-INF/jarjar/") and n.endswith(".jar") and depth < 3:
            try:
                sub = zipfile.ZipFile(io.BytesIO(z.read(n)))
                m2, d2 = read_mods_toml(sub, depth + 1)
                mods += m2
                for k, v in d2.items():
                    deps.setdefault(k, []).extend(v)
            except zipfile.BadZipFile:
                pass
    return mods, deps

def main():
    provided = {"minecraft": "1.21.1", "neoforge": None, "java": "21"}
    packtoml = tomllib.load(open(os.path.join(PACK, "pack.toml"), "rb"))
    provided["neoforge"] = packtoml["versions"].get("neoforge")
    alldeps, owner, optional = {}, {}, set()
    moddir = os.path.join(PACK, "mods")
    for f in sorted(os.listdir(moddir)):
        if not f.endswith(".pw.toml"):
            continue
        meta = tomllib.load(open(os.path.join(moddir, f), "rb"))
        if meta.get("option", {}).get("optional"):
            optional.add(f)
        url = url_of(meta)
        if not url:
            print(f"?? pas d'URL pour {f}")
            continue
        try:
            path = fetch(url, meta["filename"])
        except Exception as e:
            print(f"!! téléchargement impossible {f}: {e}")
            continue
        try:
            z = zipfile.ZipFile(path)
        except zipfile.BadZipFile:
            print(f"!! jar invalide {f}")
            continue
        mods, deps = read_mods_toml(z)
        if not mods:
            print(f"   (pas de mods.toml : {f})")
        for mid, v in mods:
            if mid not in provided or provided[mid] is None:
                provided[mid] = v
            owner.setdefault(mid, f)
        for k, lst in deps.items():
            alldeps.setdefault(k, []).extend((f, d) for d in lst)
    problems = 0
    for mid, lst in alldeps.items():
        if mid not in owner and mid not in ("minecraft", "neoforge"):
            continue
        for src, d in lst:
            dep = d.get("modId")
            typ = str(d.get("type", "required" if d.get("mandatory", False) else "optional")).lower()
            side = str(d.get("side", "BOTH")).upper()
            rng = d.get("versionRange", "")
            if dep in ("minecraft", "neoforge", "java", "forge"):
                if dep == "minecraft" and typ == "required" and not in_range("1.21.1", rng):
                    print(f"~~ {mid} ({src}) annonce minecraft {rng} (à surveiller)")
                if dep == "neoforge" and typ == "required" and not in_range(provided["neoforge"], rng):
                    print(f"XX {mid} demande neoforge {rng} (pack: {provided['neoforge']})"); problems += 1
                continue
            if typ == "required":
                if dep not in provided:
                    print(f"XX {mid} ({src}) REQUIERT {dep} {rng} [{side}] — absent"); problems += 1
                elif not in_range(provided[dep], rng):
                    print(f"~~ {mid} requiert {dep} {rng}, trouvé {provided[dep]} (vérifier)")
            elif typ == "incompatible" and dep in provided:
                if in_range(provided[dep], rng):
                    print(f"XX {mid} INCOMPATIBLE avec {dep} {rng} (présent {provided[dep]}) : {d.get('reason','')}"); problems += 1
    print(f"\n{len(owner)} modIds fournis, {problems} problème(s) bloquant(s).")
    return problems

if __name__ == "__main__":
    sys.exit(1 if main() else 0)
