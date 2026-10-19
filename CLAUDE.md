# CLAUDE.md — Le Dernier Moteur

Mémo de projet pour les sessions de développement (humain ou IA). À mettre à jour à chaque phase.

## Projet
Modpack solo **Minecraft 1.21.1 / NeoForge / Java 21**, style « expert guidé » :
tech lourde (Create, Immersive Engineering, Mekanism, Industrial Foregoing, AE2), exploration et
boss (Twilight Forest, Cataclysm, YUNG's…), survie difficile (Tough As Nails, Serene Seasons,
mobs renforcés), progression portée par FTB Quests et un lore (« Le Dernier Moteur »).

## Conventions
- **Réutiliser avant de créer** : mod existant > config > KubeJS > datapack > Java custom.
- Pack géré par **packwiz** dans `pack/`. Toujours lancer `packwiz refresh` (depuis `pack/`)
  après avoir modifié un fichier du pack, avant de committer.
- Sources de mods : **Modrinth en priorité**, CurseForge seulement si absent de Modrinth ET
  redistribution tierce autorisée (sinon : section « Ajouts manuels » du README).
- Namespace KubeJS / mod custom : **`dernier_moteur`** (items, blocs, tags, textes).
- Langue : textes joueur (quêtes, lore, lang) en **français** ; `en_us.json` fourni en repli.
- Scripts KubeJS : `pack/kubejs/startup_scripts` (items/blocs), `server_scripts` (recettes,
  tags, loot), `client_scripts` (tooltips), `assets/` + `data/` pour lang, textures, Patchouli.
- Recettes de mods tiers modifiées via `event.custom({...})` (JSON brut) plutôt que des addons
  KubeJS spécifiques : moins de dépendances, plus robuste.
- Un commit + push par phase, sur la branche de dev `claude/clever-ptolemy-twyus4`.

## Décisions (journal)
- **URL du pack** : le README pointe vers `main` (branche par défaut). Tant que la branche de dev
  n'est pas fusionnée, remplacer `main` par le nom de la branche dans la commande de pré-lancement.
- **NeoForge 21.1.251** (dernière 21.1.x au moment de l'init ; Create 6 demande ≥ 21.1.219).
- **CurseForge** seulement pour Twilight Forest et FTB Quests/Library/Teams/Ultimine (absents de Modrinth,
  redistribution autorisée → packwiz-installer les télécharge).
- **EMI + JEI** : EMI est l'interface ; JEI reste installé comme fournisseur de plugins (EMI les
  lit) car Create/IE/TF n'ont parfois que des plugins JEI. Ce n'est pas un doublon fonctionnel
  volontaire : ne pas activer l'interface JEI.
- **Iris 1.8.14-beta** (couplée à Sodium 0.8.x, cf. message d'incompatibilité dans son jar) +
  **Iris Flywheel Compat** pour Create 6 (Flywheel est embarqué dans Create 6).
- **Distant Horizons** : option packwiz `optional=true, default=true` (voulu par l'utilisateur).
  `config/DistantHorizons.toml` fourni : `enableAutoUpdater=false` (sinon DH propose une mise à
  jour qui casse le hash du pack), `generatorPlan="SURFACE_THEN_CHUNKS"`.
- **Chunky retiré** : DH, s'il détecte la classe `org.popcraft.chunky.api.ChunkyAPI`, force sans
  condition `generatorPlan=DISABLED` (verrou API « Distant Horizons / Chunky ») → horizon vide.
- **Journaux** : clic droit → `client_scripts/journals.js` ouvre l'entrée
  `patchouli:journaux/journal_N` côté client, après avoir vérifié qu'elle existe (sinon ouvre le
  Carnet et journalise les entrées connues). **Ne jamais utiliser `openBookEntry(ServerPlayer, …)`** :
  si l'entrée manque côté client, Patchouli déconnecte le joueur (« Failed to open book … entry is null »).
- **Improved Mobs** : `Break BlockEntities=false`, `Stealer Chance=0` (pas de destruction de
  machines ni de vol : difficulté oui, frustration non).
- **Cataclysm sur serveur dédié** : ses boss plantent le chargement des tags sur serveur dédié
  (champ `@OnlyIn(CLIENT)` lu par Improved Mobs). Sans effet en solo (serveur intégré). Pour les
  tests serveur headless, retirer Cataclysm.
- **Difficulté vanilla** : non forcée par le pack ; « Difficile » recommandé (README).
- **Portes d'ère = boss → fragments → codex catalyseurs** (`keepIngredient`) : voir
  `docs/progression.md`. Items KubeJS et mod partagent le namespace `dernier_moteur`
  (le mod ne déclare que Clé du Gardien, Cœur du Gardien, blocs du Moteur, boss).
- **Carnet Patchouli** = livre *externe* `patchouli:carnet` : `pack/patchouli_books/carnet/book.json`
  **et** son contenu dans `pack/patchouli_books/carnet/en_us/{categories,entries}/` (texte FR sous
  en_us = langue de repli). Un livre externe est lu **sur le disque** (`BookContentExternalLoader`),
  jamais dans les resource packs : du contenu dans `kubejs/assets/patchouli/…` est ignoré (livre
  réduit à sa page d'accueil). Généré par `tools/gen_patchouli.py`.
- **Drops de boss** : `EntityEvents.death` + `spawnAtLocation` (invulnérable, sans expiration),
  testé sur les 6 gardiens. Journaux en coffres via Global Loot Modifiers NeoForge (`neoforge:add_table`), 25 %, dans 30 tables
  vanilla + YUNG's, WDA, TF, Nova Structures, Aquamirae, Cataclysm : généré par `tools/gen_loot.py`.
- **Noms d'items KubeJS** en français via `displayName` (pas de fichier lang pour eux).
- **Quêtes générées** par `tools/quests/build.py` (DSL dans `tools/quests/content.py`) : ne pas
  éditer les SNBT à la main, régénérer. Textes dans `quests/lang/en_us.snbt` (FR sous en_us).
  IDs = hash stable de la clé, **bit de poids fort à 0** (FTB lit des long signés, sinon il
  réattribue l'ID et perd dépendances + textes). `--dump` valide chaque ID d'item/entité/structure.
- **Mod custom** (`mod/`, ModDevGradle 2.0.147, package `fr.derniermoteur`) : le Gardien étend
  `IronGolem` pour réutiliser modèle/animations (rendu ×2, texture procédurale originale). Le
  Moteur lit les pièces par ID (`BuiltInRegistries.ITEM`) → pas de dépendance à KubeJS.
- **KubeJS 7** : `event.cancel()` / `success()` / `exit()` **lèvent une exception** et terminent le
  handler → toujours les appeler en dernier.
- **Rhino/KubeJS** : pas de `const` dans un bloc (`if`, boucle) ni pour une variable globale
  réutilisée → « redeclaration of var ». Utiliser `let`.
- **Release du mod** : une release par `mod_version`, jamais republiée (hash figé dans le pack).
  Jar reproductible (`preserveFileTimestamps=false`). Le workflow committe
  `pack/mods/dernier-moteur.pw.toml` sur la branche : faire `git pull` avant de continuer.
- **Addons Create** (demande utilisateur « tous les mods Create ») : 58 addons majeurs ajoutés, la
  règle « pas de doublons » est levée pour eux (Diesel Generators, Power Grid, Electro Energetics,
  TFMG… coexistent avec IE/Mekanism). Les portes d'ère restent sur les machines-clés (codex), donc
  l'énergie précoce ne court-circuite pas la progression. Exclus et raisons : `docs/mods.md`.
  TFMG = **Community Edition** (l'original ≤ 1.2.2 est incompatible avec Bits 'n' Bobs) ;
  Create New Age retiré (dépendance `esl` introuvable) ; KubeJS Create retiré (inutile) ; Create: Harmonics
  retiré (veut télécharger yt-dlp + FFmpeg au lancement). Avant d'ajouter un mod : vérifier qu'il
  ne télécharge rien hors packwiz.
- **FTB Ultimine** (CurseForge, redistribution autorisée).
- **Métaux** : priorités Almost Unified = minecraft, kubejs, create, IE, mekanism, createaddition,
  tfmg, createbigcannons, create_ironworks, createmetallurgy, createnuclear… Un seul minerai généré
  par métal : biome modifier `kubejs/data/dernier_moteur/neoforge/biome_modifier/remove_duplicate_ores.json`
  retire plomb/uranium (Mekanism, Create Nuclear, TFMG), nickel (TFMG), étain (Ironworks). Restent :
  plomb/nickel/uranium/argent/aluminium = IE, étain/osmium/fluorite = Mekanism, zinc = Create.
- **Décraft TF bloqué** pour fragments, codex et composants (`server_scripts/tags.js`), sinon
  décrafter un codex rendrait un fragment.
- **Scan anti-contournement** (oct. 2026) : aucune recette d'addon ne produit une machine verrouillée.
- **.mrpack** : `.github/workflows/mrpack.yml` exporte le pack à chaque push sur main (release
  rolling `pack-latest` + release figée `pack-v<version>` quand `pack/pack.toml` change de version).
  Les mods CurseForge sont embarqués dans l'archive (overrides), les autres référencés par URL.
- **Gardien** (mod 1.1.0) : calque `RenderType.eyes` (yeux + cœur de poitrine lumineux).
- **Identité** : `assets/icon.png` (icône d'instance Prism), splashs du lore
  (`kubejs/assets/minecraft/texts/splashes.txt`). Custom Window Title écarté : jar Fabric étiqueté NeoForge.
- Liste commentée des mods et des écartés : `docs/mods.md`.

## Outils
- `tools/gen_textures.py` : textures 16×16 des items KubeJS (Pillow).
- `tools/quests/build.py --dump <dump.json>` : génère et valide les quêtes FTB.
- `tools/gen_mod_textures.py` : textures du mod.
- `tools/gen_loot.py` : injections des journaux dans les coffres de structures.
- `tools/gen_patchouli.py` : contenu du Carnet + advancements des journaux.
- `tools/check_deps.py pack <cache>` : télécharge les jars et vérifie dépendances/incompatibilités.
- `tools/ci/boot_test.sh` : test de démarrage complet (dépendances, serveur, KubeJS, `tools/ci/ci_check.js`),
  exécuté par `.github/workflows/boot.yml` à chaque changement du pack. Lancer en local avant de pousser.
- Test serveur headless manuel : installer NeoForge server (`--install-server`), copier les jars
  `side = both|server`, `./run.sh nogui`, attendre `Done (`. Les erreurs KubeJS sont dans
  `logs/kubejs/server.log`.

## État d'avancement
- [x] Phase 1 — Structure (packwiz, README, CLAUDE.md)
- [x] Phase 2 — Mods + configs (86 mods à l'origine ; 151 + le mod custom après ajout des addons Create et de FTB Ultimine)
- [x] Phase 3 — Progression (`docs/progression.md`)
- [x] Phase 4 — KubeJS (items de lore, recettes, drops de boss, carnet Patchouli) — validé sur serveur de test
- [x] Phase 5 — FTB Quests (12 chapitres, 262 quêtes dont l'annexe « Ateliers Create », chargées sans perte)
- [x] Phase 6 — Mod custom `dernier_moteur` (compile ; boss, drops, multibloc et allumage testés sur serveur)
- [x] Phase 7 — CI : `mod.yml` (build, release `mod-v<version>`, pw.toml auto-commité), `pack.yml` (cohérence),
  `boot.yml` (démarrage serveur + contrôles)
- [x] Phase 8 — Vérification finale : release `mod-v1.0.0` publiée et référencée par le pack (hash
  vérifié), 0 dépendance manquante (98 modIds), serveur de test avec l'état exact du dépôt :
  0 erreur KubeJS, recettes présentes, 236 quêtes, tous les IDs de quêtes existent (mod inclus),
  boss + Moteur OK. Reste à tester côté client : voir « Points à tester » du README.
- [x] Retours du premier test client (oct. 2026) : DH actif par défaut + générateur fonctionnel,
  updater DH coupé, journaux ouvrables au clic droit (validé en jeu), Carnet complet (validé en jeu),
  fermeture du monde OK. État général revérifié sur serveur : 0 dépendance manquante, 0 erreur
  KubeJS, 27 recettes ajoutées / 15 retirées sans échec, 236 quêtes, 7 boss → fragments, cœur et
  journaux. Erreurs restantes du log = bruit amont (Create Connected « dye_depot », potions de
  When Dungeons Arise, advancements optionnels, slot exemple de Curios), sans effet en jeu.
- [x] Améliorations (oct. 2026, pack 0.2.0) : scan anti-contournement (aucun), décraft TF bloqué,
  unification des métaux + minerais en double retirés, chapitre « Ateliers Create » (262 quêtes),
  journaux dans 30 coffres de structures, CI `boot.yml` (démarrage + contrôles, vert), mod 1.1.0
  (Gardien lumineux), `.mrpack` publié automatiquement, splashs + icône. Reste : équilibrage après
  quelques heures de jeu (retours joueur).
