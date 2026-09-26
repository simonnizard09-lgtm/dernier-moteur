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
- **CurseForge** seulement pour Twilight Forest et FTB Quests/Library/Teams (absents de Modrinth,
  redistribution autorisée → packwiz-installer les télécharge).
- **EMI + JEI** : EMI est l'interface ; JEI reste installé comme fournisseur de plugins (EMI les
  lit) car Create/IE/TF n'ont parfois que des plugins JEI. Ce n'est pas un doublon fonctionnel
  volontaire : ne pas activer l'interface JEI.
- **Iris 1.8.14-beta** (couplée à Sodium 0.8.x, cf. message d'incompatibilité dans son jar) +
  **Iris Flywheel Compat** pour Create 6 (Flywheel est embarqué dans Create 6).
- **Distant Horizons** : option packwiz `optional=true, default=false`.
- **Improved Mobs** : `Break BlockEntities=false`, `Stealer Chance=0` (pas de destruction de
  machines ni de vol : difficulté oui, frustration non).
- **Cataclysm sur serveur dédié** : ses boss plantent le chargement des tags sur serveur dédié
  (champ `@OnlyIn(CLIENT)` lu par Improved Mobs). Sans effet en solo (serveur intégré). Pour les
  tests serveur headless, retirer Cataclysm.
- **Difficulté vanilla** : non forcée par le pack ; « Difficile » recommandé (README).
- Liste commentée des mods et des écartés : `docs/mods.md`.

## Outils
- `tools/check_deps.py pack <cache>` : télécharge les jars et vérifie dépendances/incompatibilités.
- Test serveur headless : installer NeoForge server (`--install-server`), copier les jars
  `side = both|server`, `./run.sh nogui`, attendre `Done (`. Les erreurs KubeJS sont dans
  `logs/kubejs/server.log`.

## État d'avancement
- [x] Phase 1 — Structure (packwiz, README, CLAUDE.md)
- [x] Phase 2 — Mods + configs (86 mods, serveur de test OK)
- [ ] Phase 3 — Progression (`docs/progression.md`)
- [ ] Phase 4 — KubeJS (items de lore, recettes)
- [ ] Phase 5 — FTB Quests
- [ ] Phase 6 — Mod custom `dernier_moteur`
- [ ] Phase 7 — CI (build + release du mod, intégration packwiz)
- [ ] Phase 8 — Vérification finale
