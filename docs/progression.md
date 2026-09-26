# Progression — Le Dernier Moteur

Document de conception. Il fait foi pour les recettes KubeJS (phase 4) et les quêtes (phase 5).
Tous les identifiants cités existent dans le pack (vérifiés sur le registre d'un serveur de test).

## Principe

- **Quatre ères techniques + un épilogue.** Chaque ère a un mod « moteur » et des mods de soutien.
- **Les portes entre ères sont des boss.** Chaque gardien vaincu lâche un **Fragment du Noyau**
  (item KubeJS, 100 % de chance, ajouté par `EntityEvents.drops`).
- **Les Codex.** Avec un fragment on fabrique le **Codex** de l'ère suivante. Le codex est un
  **catalyseur** : il reste dans la grille (`keepIngredient`) quand on fabrique les machines-clés
  de l'ère. Le fragment, lui, reste aussi dans la grille quand on fabrique un codex : on peut donc
  refaire un codex perdu, et on garde tous les fragments pour le Moteur final.
- **Composants d'ère.** Chaque ère produit un composant (item KubeJS) fabriqué en croisant
  plusieurs mods ; les machines de l'ère suivante le demandent. On ne saute pas d'ère.
- **Jamais de grind vide** : pas de drop à faible pourcentage, pas de quantité absurde. Les drops
  de boss servent aux items uniques (codex, clé du gardien) ; les recettes répétables n'utilisent
  que des ressources automatisables.

## Vue d'ensemble

| Ère | Thème | Mods moteurs | Boss-porte (sortie) | Fragment | Codex débloqué | Composant produit |
|---|---|---|---|---|---|---|
| 0 — Réveil | Survie, premiers outils | Vanilla, TaN, Serene Seasons, Farmer's Delight | — | — | — | — |
| I — Vapeur | Mécanique, vapeur | Create (+ Crafts & Additions côté cinétique) | **Ferrous Wroughtnaut** (Mowzie's) + **Naga** (TF) | Rouage | Codex de l'Étincelle | Mécanisme à vapeur |
| II — Électricité | Courant, acier | Immersive Engineering, Crafts & Additions | **Liche** (TF) | Étincelle | Codex de la Forge | Bobine galvanique |
| III — Industrie lourde | Minerais ×5, alliages, multiblocs | Mekanism (+ Generators), IE lourd | **Ignis** + **The Harbinger** (Cataclysm) | Braise, Tempête | Codex de l'Automate | Alliage du Noyau |
| IV — Automatisation | Réseaux, autocraft, ressources vivantes | AE2 (+ Applied Mekanistics), Industrial Foregoing | **Ender Guardian** + **The Leviathan** (Cataclysm) | Néant, Abysse | Clé du Gardien (6 fragments) | Processeur du Moteur |
| Épilogue | Rallumer le Moteur | Mod `dernier_moteur` | **Le Gardien du Noyau** (boss custom) | Cœur du Gardien | — | Le Moteur (multibloc) |

Boss **optionnels** (chapitre annexe « Boss », récompenses utiles, pas bloquants) : Minoshroom,
Hydre, Chevaliers fantômes, Ur-Ghast, Reine des neiges (TF) ; Netherite Monstrosity, Ancient
Remnant, Maledictus, Scylla (Cataclysm) ; Frostmaw, Umvuthi (Mowzie's) ; Capitaine Cornelia
(Aquamirae).

---

## Ère 0 — Réveil
*« Le Moteur s'est tu. Le vent a changé, l'eau est devenue trouble et les nuits sont pleines de
choses qui n'y étaient pas. »*

- Survivre : soif (gourde, purification de l'eau — Tough As Nails), température (vêtements,
  feux), saisons (Serene Seasons : récoltes selon la saison).
- Premiers outils, abri, nourriture variée (Farmer's Delight).
- Recevoir le **Carnet de l'Ingénieur** (Patchouli) et le **Journal n°1**.
- Mobs renforcés (Improved Mobs) : la difficulté grimpe avec le temps de jeu.
- **Jalon de sortie** : premier alliage d'andésite (Create) → ouverture de l'ère I.

## Ère I — Vapeur (Create)
*« Avant l'électricité, les Ingénieurs faisaient tourner le monde avec de l'eau, du vent et de la
vapeur. Les rouages se souviennent. »*

- Roues à eau, moulins, presse, mixeur, laiton, mécanisme de précision, machine à vapeur.
- Premières automatisations Create (minerais concassés ×1,5, cuisine avec Central Kitchen).
- Exploration : structures YUNG's, premiers donjons, **portail du Crépuscule** (Twilight Forest).
- **Boss-portes** :
  - **Naga** (TF, cour de la Naga) → `twilightforest:naga_scale` (ingrédient du Codex).
  - **Ferrous Wroughtnaut** (Mowzie's, dans les grottes, « gardien mécanique » en armure de fer)
    → **Fragment du Rouage** `dernier_moteur:core_fragment_gear`.
- **Composant produit** : **Mécanisme à vapeur** `dernier_moteur:steam_mechanism`
  (assemblage séquencé Create sur tôle de laiton : mécanisme de précision, tube électronique,
  bouteille d'eau purifiée TaN, pression).
- **Sortie** : **Codex de l'Étincelle** `dernier_moteur:codex_spark`
  = Fragment du Rouage (conservé) + écaille de Naga + mécanisme à vapeur + livre.

## Ère II — Électricité (Immersive Engineering + Crafts & Additions)
*« L'Étincelle fut la deuxième leçon. Les Ingénieurs apprirent à enfermer la foudre dans le cuivre. »*

- Débloqué par le Codex de l'Étincelle (catalyseur) : **marteau d'ingénieur** IE (indispensable
  pour former tous les multiblocs IE), **établi d'ingénieur** IE, **moteur électrique** et
  **alternateur** de Crafts & Additions.
- Four à coke → acier (haut fourneau), fils et câbles, générateurs (dynamo cinétique :
  la vapeur de Create devient électricité), accumulateurs, moulin à eau/à vent IE.
- Exploration : tour de la Liche (TF), labyrinthe du Minoshroom (optionnel).
- **Boss-porte** : **Liche** (TF) → **Fragment de l'Étincelle** `dernier_moteur:core_fragment_spark`.
- **Composant produit** : **Bobine galvanique** `dernier_moteur:galvanic_coil`
  = bobine BT d'IE + bobine de cuivre C&A + tôle de laiton Create + plaques d'acier.
- **Sortie** : **Codex de la Forge** `dernier_moteur:codex_forge`
  = Fragment de l'Étincelle (conservé) + 2 bobines galvaniques + composant d'acier IE
  + lingots de bois de fer et de feuille d'acier (TF) + livre.

## Ère III — Industrie lourde (Mekanism + IE lourd)
*« La Forge fut la troisième leçon : fondre, séparer, recomposer. Le monde entier devint minerai. »*

- Débloqué par le Codex de la Forge : **boîtier en acier** Mekanism (base de toutes ses machines),
  **infuseur métallurgique**, **bloc d'ingénierie lourde** IE (four à arc, excavatrice,
  broyeur IE, raffinerie…).
- Traitement des minerais ×3 puis ×4/×5, alliages, circuits (le **circuit de contrôle basique**
  Mekanism demande désormais un **composant électronique IE**), générateurs Mekanism.
- Exploration : Nether (forgeron d'âmes → **Ignis**), usine ancienne (**The Harbinger**,
  un gardien mécanique au sens propre).
- **Boss-portes** :
  - **Ignis** (Cataclysm) → **Fragment de la Braise** `dernier_moteur:core_fragment_ember`
    (+ `cataclysm:ignitium_ingot`).
  - **The Harbinger** (Cataclysm) → **Fragment de la Tempête** `dernier_moteur:core_fragment_storm`
    (+ `cataclysm:witherite_ingot`).
- **Composant produit** : **Alliage du Noyau** `dernier_moteur:core_alloy`
  (infuseur métallurgique : acier + obsidienne raffinée), et son bloc.
- **Sortie** : **Codex de l'Automate** `dernier_moteur:codex_automaton`
  = Fragments Braise + Tempête (conservés) + lingot d'ignitium + lingot de witherite
  + alliage du Noyau + livre.

## Ère IV — Automatisation avancée (AE2 + Industrial Foregoing)
*« L'Automate fut la dernière leçon : des machines qui fabriquent des machines. C'est ainsi que
fut bâti le Moteur. »*

- Débloqué par le Codex de l'Automate : **graveur** (inscriber) et **contrôleur ME** AE2,
  **cadre de machine** d'Industrial Foregoing.
- Processeurs AE2, autocrafting, stockage ME, chimie Mekanism dans AE2 (Applied Mekanistics),
  ressources vivantes (IF : arbres, mobs, foreuse laser), fission puis fusion Mekanism.
- **Composant produit** : **Processeur du Moteur** `dernier_moteur:engine_processor`
  (graveur AE2 : processeur d'ingénierie + alliage du Noyau + processeur de calcul).
  Demandé par : contrôleur ME, foreuse laser IF, mineur digital et contrôleur de fusion Mekanism.
- Exploration : l'End (citadelle en ruine → **Ender Guardian**), l'océan (cité engloutie →
  **The Leviathan**).
- **Boss-portes** :
  - **Ender Guardian** → **Fragment du Néant** `dernier_moteur:core_fragment_void`.
  - **The Leviathan** → **Fragment de l'Abysse** `dernier_moteur:core_fragment_abyss`.
- **Sortie** : **Clé du Gardien** (item du mod) = les 6 fragments (conservés) + 4 processeurs
  du Moteur + étoile du Nether + bloc d'alliage du Noyau.

## Épilogue — Rallumer le Moteur (mod `dernier_moteur`)
*« Le dernier gardien n'est pas devenu fou. Il attend quelqu'un qui mérite le Noyau. »*

- **Le Gardien du Noyau** : boss custom invoqué avec la Clé du Gardien. Trois phases
  (mêlée → salves de projectiles + invocation de sbires → rage). Lâche le **Cœur du Gardien**.
- **Le Moteur** : multibloc (5×5×5, boîtiers du Moteur + contrôleur central). Il doit recevoir :
  - de l'**énergie** (FE) jusqu'à remplir sa réserve ;
  - les **6 Fragments du Noyau**, le **Cœur du Gardien** et 4 **Processeurs du Moteur**.
  Une fois plein et formé, un clic active le Moteur : message final, effets, fin du pack.

---

## Rôle de chaque mod

| Mod | Ère(s) | Rôle dans la progression |
|---|---|---|
| Create | I → IV | Base mécanique ; assemblage séquencé des composants ; logistique jusqu'à la fin. |
| Create Crafts & Additions | I → II | Transition cinétique ↔ FE ; moteur/alternateur gardés par le Codex de l'Étincelle. |
| Create: Connected, Central Kitchen | I+ | Confort Create, cuisine automatisée (nourriture pour la survie). |
| Immersive Engineering | II → III | Acier, fils, générateurs, multiblocs ; composants électroniques pour Mekanism. |
| Mekanism (+ Generators) | III → IV | Minerais ×5, alliages, circuits, fission/fusion. |
| Industrial Foregoing | IV | Automatisation des ressources vivantes. |
| AE2 (+ Applied Mekanistics) | IV | Stockage/autocrafting ; Processeur du Moteur au graveur. |
| Twilight Forest | I → IV | Chaîne de boss (Naga, Liche = portes) ; matériaux (bois de fer, feuille d'acier). |
| L_Ender's Cataclysm | III → IV | Gardiens : Ignis, Harbinger, Ender Guardian, Leviathan. |
| Mowzie's Mobs | I | Ferrous Wroughtnaut, premier gardien mécanique. |
| Aquamirae, YUNG's, When Dungeons Arise, Dungeons and Taverns, Terralith | toutes | Exploration, butin, journaux de lore. |
| Tough As Nails, Serene Seasons, Improved Mobs, Farmer's Delight | toutes | Survie difficile mais lisible. |
| FTB Quests, Patchouli, EMI | toutes | Guidage, lore, recettes. |
| KubeJS | toutes | Items de lore, codex, composants, recettes, drops de boss. |
| `dernier_moteur` (mod custom) | Épilogue | Gardien du Noyau et Moteur. |

## Items KubeJS (namespace `dernier_moteur`)

| ID | Nom | Obtention |
|---|---|---|
| `core_fragment_gear` | Fragment du Noyau — Rouage | Ferrous Wroughtnaut |
| `core_fragment_spark` | Fragment du Noyau — Étincelle | Liche |
| `core_fragment_ember` | Fragment du Noyau — Braise | Ignis |
| `core_fragment_storm` | Fragment du Noyau — Tempête | The Harbinger |
| `core_fragment_void` | Fragment du Noyau — Néant | Ender Guardian |
| `core_fragment_abyss` | Fragment du Noyau — Abysse | The Leviathan |
| `steam_mechanism` | Mécanisme à vapeur | Create, assemblage séquencé |
| `galvanic_coil` | Bobine galvanique | Établi (IE + C&A + Create) |
| `core_alloy` / `core_alloy_block` | Alliage du Noyau (+ bloc) | Infuseur métallurgique Mekanism |
| `engine_processor` | Processeur du Moteur | Graveur AE2 |
| `codex_spark` / `codex_forge` / `codex_automaton` | Codex d'ère | Établi (fragment conservé) |
| `journal_1` … `journal_8` | Journaux d'ingénieur | Récompenses de quêtes + coffres de structures |

Tag : `dernier_moteur:core_fragments` (les 6 fragments), utilisé par le Moteur et les quêtes.
