# Liste des mods (151 + le mod custom `dernier_moteur`)

Tous en **1.21.1 NeoForge**, vérifiés par `tools/check_deps.py` (dépendances requises,
incompatibilités déclarées) et par un démarrage réel de serveur NeoForge 21.1.251.
Source : Modrinth, sauf mention **[CF]** (CurseForge, redistribution autorisée).

## Tech (cœur du pack)
| Mod | Rôle |
|---|---|
| Create | Ère 1 (vapeur/mécanique) : énergie cinétique, machines de traitement, trains. |
| Create Crafts & Additions | Pont Create ↔ électricité (FE), fils, moteurs/alternateurs : charnière ère 1 → 2. |
| Create: Connected | Blocs utilitaires Create (pas de nouvelle chaîne de production). |
| Create: Central Kitchen (+ Dragons Plus) | Automatisation Create de Farmer's Delight (nourriture pour la survie). |
| Immersive Engineering | Ère 2 (électricité) et multiblocs lourds de l'ère 3 (haut fourneau amélioré, arc électrique, excavatrice…). |
| Mekanism + Generators | Ère 3 (industrie lourde) : traitement de minerais ×5, chimie, fission/fusion en fin d'ère 4. |
| Industrial Foregoing (+ Titanium) | Ère 4 : automatisation des ressources vivantes (arbres, mobs, laser drill). |
| Applied Energistics 2 (+ GuideME) | Ère 4 : stockage et autocrafting en réseau. |
| Applied Mekanistics | Gaz/chimie Mekanism dans AE2. |

## Addons Create (ajoutés à la demande : « tous les mods Create »)
58 addons majeurs et maintenus, compatibles Create 6 / NeoForge 1.21.1, chargés ensemble sur le
serveur de test : Create: Copycats+, Create Aeronautics, Create Big Cannons, Create Slice & Dice, Create: Diesel Generators, Create: Enchantment Industry, Create: Bells & Whistles, Create: Design n' Decor, Create Jetpack, Create Ore Excavation, Create Goggles, Create: Framed, Create Contraption Terminals, Create: Power Loader, Steam 'n' Rails Neoforge, Create Encased, Create Railways Navigator, Create: Bits 'n' Bobs, Create: Pattern Schematics, Create: TFMG Community Edition, Create: Trading floor, Create: Structures Arise, Create: Numismatics, Create: Power Grid, Create: Hypertubes, Create Nuclear, Create: Blocks & Bogies, Sophisticated Backpacks Create Integration, Create: Escalated, Create: Extended Wrenches, Create Sifting, Create: Components and Additions, Create: Ender Transmission, Create Mechanical Spawner, Create Mechanical Extruder, Create: Storage [Neo/Forge], Create: Shuffle Filter, Create More: Parallel Pipes, Create: Garnished, Create Confectionery, Create: Sound of Steam, Create: Mobile Packages, Create Train Parts, Create: Enchantable Machinery, EMI: Create Schematics, Create: Integrated Farming, Create Cafe, Create Ratatouille, Create Train Utilities (Create Train Doors), Create Horse Power, Create: Metallurgy, Create: Ironworks, Create: Deep Dark, Create: Tracks+, Create: Pantographs & Wires, Create: Winery, Create: Transmission!, Create: Electro Energetics.
Dépendances tirées automatiquement : Sable (physique d'Aeronautics), Ritchie's Projectile Library,
DragonLib, Azimuth API, Struts, Mechanicals Lib, Tom's Simple Storage (pour Contraption Terminals).

Volontairement **non ajoutés** (sur ~400 addons Create recensés sur Modrinth) :
| Catégorie | Exemples | Raison |
|---|---|---|
| Incompatible / introuvable | Create: New Age | Exige la bibliothèque `esl`, introuvable sur Modrinth et CurseForge. |
| Remplacé | Create: The Factory Must Grow | Incompatible avec Bits 'n' Bobs (≤ 1.2.2) → **TFMG Community Edition** à la place. |
| Télécharge des exécutables | Create: Harmonics | Au premier lancement, propose d'installer yt-dlp et FFmpeg (lecture de musique YouTube) : programmes externes hors du pack. Retiré. |
| Sans usage | KubeJS Create | Le pack écrit ses recettes en JSON brut ; l'addon ne faisait qu'ajouter des avertissements. |
| Compat pour des mods absents | Ars Creo, Cobblemon, CC:C Bridge, Rechiseled: Create, Storage Drawers compat, Vampirism… | Le mod cible n'est pas dans le pack. |
| Casse la difficulté | Renewable Netherite/Diamonds/Brass, Simple Ore Doubling, Easy Stone Generators, Overpowered, Creator Sword… | Contraire au style « expert ». |
| Doublon de structures | Integrated Dungeons and Structures, Integrated Stronghold | Font doublon avec YUNG's (forteresses). |
| Alpha / abandonné / gadget | longue traîne (< 1 000 téléchargements, versions alpha, « deprecated ») | Risque de plantage sans apport. |

## Exploration et boss
| Mod | Rôle |
|---|---|
| The Twilight Forest **[CF]** | Chaîne de boss principale de l'ère 1 à 3 (Naga → Lich → Hydre → Ur-Ghast…). |
| L_Ender's Cataclysm (+ Lionfish API, Curios) | Gardiens de fin (Ignis, Harbinger, Leviathan, Ender Guardian…) : ères 3-4. |
| Mowzie's Mobs (+ GeckoLib) | Mini-boss d'exploration (Ferrous Wroughtnaut = « gardien mécanique » de l'ère 1). |
| Aquamirae (+ Fragmentum) | Biome glacé et boss marin (Capitaine Cornelia) : annexe exploration. |
| YUNG's (API + 11 modules) | Structures vanilla repensées (donjons, mines, forteresses…). |
| When Dungeons Arise | Grands donjons (le « mod de donjons » du pack). |
| Dungeons and Taverns | Structures et tavernes supplémentaires (cartes d'exploration). |
| Terralith | Génération de terrain plus variée. |
| Explorer's Compass / Nature's Compass | Trouver structures et biomes (quêtes d'exploration guidées). |
| Artifacts | Butin de donjon (équipement passif). |
| Waystones (+ Balm) | Téléportation (coût en XP) pour limiter les allers-retours vides. |
| Sophisticated Backpacks (+ Core) | Sacs à dos évolutifs. |

## Survie
| Mod | Rôle |
|---|---|
| Tough As Nails (+ GlitchCore) | Soif et température. |
| Serene Seasons | Saisons (cultures, température). |
| Improved Mobs (+ TenshiLib) | Mobs plus dangereux avec le temps (configuré pour ne pas casser les machines ni voler). |
| Farmer's Delight | Nourriture variée. |
| AppleSkin | Affichage faim/saturation. |
| Corpse | Tombe à la mort (pas de perte d'objets injuste). |

## Guidage et scripts
| Mod | Rôle |
|---|---|
| FTB Quests (+ FTB Library, FTB Teams, Architectury) **[CF]** | Arbre de quêtes. |
| Patchouli | Journaux de lore (« Carnets de l'Ingénieur »). |
| EMI (+ EMI Loot) | Visionneuse de recettes principale (arbre de recettes, butins). |
| JEI (+ MezzConfig) | Utilisé **comme bibliothèque** : EMI affiche les plugins JEI des mods qui n'ont que celui-ci. Voir décision dans CLAUDE.md. |
| KubeJS (+ Rhino, Better Advanced Tooltips) | Items de lore, recettes, tags, butins. |
| Polymorph | Choix en cas de conflit de recettes. |
| FTB Ultimine **[CF]** | Minage en veine (touche ` par défaut). |
| Almost Unified | Unification des minerais/lingots entre Create, IE, Mekanism… |

## Performances / QoL / rendu
| Mod | Rôle |
|---|---|
| Sodium, Iris | Rendu rapide + shaders. |
| Iris & Oculus Flywheel Compat | Machines Create visibles et éclairées sous shaders. |
| ModernFix, FerriteCore, Entity Culling, ImmediatelyFast | Performances / mémoire. |
| Kotlin for Forge, Fzzy Config | Bibliothèques (EMI Loot). |
| Jade | Infos du bloc visé. |
| Xaero's Minimap + World Map | Carte. |
| Simple Backups | Sauvegardes auto (toutes les 60 min, 8 conservées). |
| Mouse Tweaks, Controlling (+ Searchables), Clumps | Confort. |
| spark | Profilage. |
| Crash Assistant | Fenêtre d'aide en cas de crash (logs faciles à copier). |
| Distant Horizons | **Optionnel, activé par défaut** ; génère lui-même le terrain lointain. |

## Shaderpacks
Complementary Reimagined (principal), BSL (alternative), MakeUp Ultra Fast (léger).

## Écartés (et pourquoi)
| Mod | Raison |
|---|---|
| Tom's Storage, Functional Storage | Doublons du stockage AE2. |
| Mekanism Tools / Additions | Hors sujet, doublons d'équipement. |
| Cold Sweat | Doublon de Tough As Nails. |
| Deeper and Darker, Alex's Mobs, Alex's Caves | Pas de version 1.21.1 NeoForge. |
| Lithium | Pris en charge par NeoForge mais bénéfice faible ici ; écarté par prudence (mixins nombreux). |
| Chunky | Retiré : sa présence fait verrouiller par DH son générateur de terrain lointain (horizon vide). DH génère lui-même. |
| Colorwheel | Même fonction que Iris Flywheel Compat (un seul des deux). |
