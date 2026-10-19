#!/usr/bin/env bash
# Test de démarrage du pack sur un serveur NeoForge headless.
# Usage : tools/ci/boot_test.sh   (depuis la racine du dépôt ; WORK=dossier de travail, défaut .ci/)
# Échoue si : dépendance manquante, plantage, erreur de script KubeJS, ou contrôle CI en échec.
# Mods exclus du serveur : ceux marqués side=client, et Improved Mobs (+ TenshiLib) qui fait planter
# Cataclysm sur serveur DÉDIÉ uniquement (voir CLAUDE.md) — sans effet en solo.
set -euo pipefail
ROOT=$(pwd)
WORK=${WORK:-$ROOT/.ci}
mkdir -p "$WORK/jars" "$WORK/server"

echo "== Dépendances"
python3 tools/check_deps.py pack "$WORK/jars"

NEO=$(python3 -c "import tomllib;print(tomllib.load(open('pack/pack.toml','rb'))['versions']['neoforge'])")
cd "$WORK/server"
if [ ! -f run.sh ]; then
  echo "== Installation de NeoForge $NEO"
  curl -sSfLo installer.jar "https://maven.neoforged.net/releases/net/neoforged/neoforge/$NEO/neoforge-$NEO-installer.jar"
  java -jar installer.jar --install-server . > installer.out 2>&1
fi
rm -rf mods world logs crash-reports kubejs config patchouli_books
mkdir -p mods
python3 - "$ROOT/pack" "$WORK/jars" mods <<'PY'
import os, shutil, sys, tomllib
pack, jars, dest = sys.argv[1:]
for f in sorted(os.listdir(f"{pack}/mods")):
    m = tomllib.load(open(f"{pack}/mods/{f}", "rb"))
    if m.get("side", "both") == "client" or f.startswith(("improved-mobs", "tenshilib")):
        continue
    shutil.copy(f"{jars}/{m['filename']}", dest)
PY
cp -r "$ROOT/pack/kubejs" "$ROOT/pack/config" "$ROOT/pack/patchouli_books" .
cp "$ROOT/tools/ci/ci_check.js" kubejs/server_scripts/zz_ci_check.js
echo "eula=true" > eula.txt
printf 'online-mode=false\nspawn-protection=0\n' > server.properties
echo "-Xmx${CI_XMX:-6G}" > user_jvm_args.txt

echo "== Démarrage ($(ls mods | wc -l) mods)"
set +e
timeout "${CI_TIMEOUT:-1500}" ./run.sh nogui > run.log 2>&1
code=$?
set -e

fail=0
grep -E 'Done \(' run.log || { echo "ÉCHEC : le serveur n'a pas fini de démarrer (code $code)"; fail=1; }
if ls crash-reports/*.txt >/dev/null 2>&1; then echo "ÉCHEC : rapport de crash"; head -60 crash-reports/*.txt; fail=1; fi
grep -h 'Loaded .* scripts' logs/kubejs/*.log || true
if grep -hE 'Loaded [0-9]+/[0-9]+ KubeJS .* scripts .* with [1-9][0-9]* errors' logs/kubejs/*.log; then
  echo "ÉCHEC : erreurs de scripts KubeJS"; grep -h 'ERROR' logs/kubejs/*.log | head -30; fail=1
fi
if grep -h 'failed recipes' run.log | grep -vE 'with 0 failed'; then echo "ÉCHEC : recettes KubeJS en échec"; fail=1; fi
grep -h 'CI RESULT' logs/kubejs/server.log || { echo "ÉCHEC : contrôle CI non exécuté"; fail=1; }
grep -q 'CI RESULT OK' logs/kubejs/server.log || fail=1
[ $fail -eq 0 ] && echo "== Test de démarrage : OK" || { echo "== Test de démarrage : ÉCHEC"; tail -40 run.log; }
exit $fail
