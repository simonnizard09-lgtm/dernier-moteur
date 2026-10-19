# Le Dernier Moteur

Modpack Minecraft **solo** en **1.21.1 / NeoForge**. Style « expert guidé » : grosses machines
tech, exploration, boss et survie rude, avec une progression très encadrée par les quêtes.

> Une civilisation d'ingénieurs maintenait le monde en vie grâce à une machine planétaire :
> le **Moteur**. Il s'est arrêté, et le monde est devenu hostile. Ses gardiens mécaniques,
> devenus fous, gardent chacun un fragment du Noyau. À toi de retrouver les techniques perdues,
> ère après ère, de vaincre les gardiens puis de rallumer le Moteur.

Le pack est distribué avec [packwiz](https://packwiz.infra.link/) : le dossier `pack/` de ce
dépôt contient le pack, et `packwiz-installer` télécharge ou met à jour les mods à chaque
lancement.

---

## Installation (Prism Launcher)

Prérequis : [Prism Launcher](https://prismlauncher.org/) et **Java 21** (Prism peut le
télécharger tout seul).

1. **Créer l'instance**
   *Ajouter une instance* → *Personnalisé (Custom)* → version **1.21.1** → chargeur de mods
   **NeoForge** (prends la version recommandée ou la dernière 21.1.x ; le pack demande au minimum
   celle indiquée dans `pack/pack.toml`). Nomme l'instance « Le Dernier Moteur ».

2. **Ajouter le bootstrap packwiz**
   Télécharge `packwiz-installer-bootstrap.jar` depuis
   <https://github.com/packwiz/packwiz-installer-bootstrap/releases> (dernière release).
   Clic droit sur l'instance → *Dossier* → ouvre le dossier **`minecraft`** (ou `.minecraft`)
   et place le jar **dedans**.

3. **Commande de pré-lancement**
   *Modifier l'instance* → *Paramètres* → *Commandes personnalisées* → coche la case, puis dans
   **Commande de pré-lancement** colle exactement :

   ```
   "$INST_JAVA" -jar packwiz-installer-bootstrap.jar https://raw.githubusercontent.com/simonnizard09-lgtm/dernier-moteur/main/pack/pack.toml
   ```

   > Pour tester une branche de développement avant fusion dans `main`, remplace `main` par le
   > nom de la branche (ex. `claude/clever-ptolemy-twyus4`).

4. **Mémoire (important)**
   *Modifier l'instance* → *Paramètres* → *Java* → coche *Mémoire* :
   - **Mémoire minimale : 6144 Mo** — **mémoire maximale : 10240 Mo** (recommandé).
   - Avec 32 Go de RAM tu peux monter à **12288 Mo** si tu actives Distant Horizons ou de gros
     shaders. Ne dépasse pas 12 Go : au-delà, le ramasse-miettes devient plus lent.
   - Arguments JVM conseillés (même page, *Arguments JVM*) :

     ```
     -XX:+UseG1GC -XX:+UnlockExperimentalVMOptions -XX:G1NewSizePercent=20 -XX:G1ReservePercent=20 -XX:MaxGCPauseMillis=50 -XX:G1HeapRegionSize=32M
     ```

5. **Lancer.** Au premier démarrage, une fenêtre packwiz télécharge ~90 mods (quelques minutes).
   Elle propose aussi les **mods optionnels** (voir plus bas). Les lancements suivants ne
   téléchargent que les mises à jour.

### Ajouts manuels
Aucun pour l'instant : tous les mods viennent de Modrinth ou de CurseForge avec la
redistribution tierce autorisée, donc `packwiz-installer` les récupère seul. Si un mod doit un
jour être installé à la main, il sera listé ici.

---

## Shaders

Le pack inclut **Sodium** + **Iris** (NeoForge) et **Iris & Oculus Flywheel Compat**, qui permet
aux machines animées de Create (Flywheel) de s'afficher correctement avec les shaders.
Shaderpacks fournis dans `shaderpacks/` :

| Shaderpack | Usage |
|---|---|
| **Complementary Reimagined** | Le « beau » par défaut, très compatible avec les mods. |
| **BSL Shaders** | Alternative classique, rendu plus contrasté. |
| **MakeUp Ultra Fast** | Fallback léger, pour les grosses bases ou les scènes chargées. |

**Activer / changer de shader** : en jeu, *Options* → *Options vidéo* → *Shader Packs…*
(ou touche **O** par défaut) → sélectionne un pack → *Appliquer*. Pour les désactiver, choisis
*(off)*. Tu peux ajouter tes propres packs `.zip` dans le dossier `shaderpacks/` de l'instance
(bouton *Ouvrir le dossier des shaderpacks*).

Conseils :
- Si une machine Create s'affiche mal avec les shaders, essaie un autre shaderpack, ou change de
  backend de rendu Flywheel avec la commande `/flywheel backend` (l'autocomplétion liste les
  choix disponibles).
- **Distant Horizons** est proposé en **mod optionnel désactivé par défaut** (il est compatible
  Sodium/Iris, mais il est gourmand et peu utile en intérieur d'usine). Pour l'activer :
  supprime le fichier `packwiz.json` du dossier `minecraft` de l'instance et relance ; la fenêtre
  des options réapparaît. Avec DH, utilise Complementary ou BSL (ils gèrent les LOD de DH).

---

## Mods optionnels
Proposés par la fenêtre packwiz au premier lancement :
- **Distant Horizons** (désactivé par défaut) — vue lointaine en LOD.

---

## Conseils de départ
- Crée le monde en difficulté **Difficile** (le pack ne la force pas).
- Au premier lancement du monde, tu reçois le **Carnet de l'Ingénieur** et le **Journal n°1** ;
  le livre de quêtes (FTB Quests) s'ouvre avec la touche **L** par défaut.

## Points à tester en jeu en priorité
Ce qui a été vérifié automatiquement (serveur NeoForge de test) : chargement de tous les mods
côté serveur, scripts KubeJS sans erreur, toutes les recettes du pack présentes, drops des 6 gardiens,
236 quêtes chargées par FTB Quests sans perte d'ID, mod `dernier_moteur` (boss, drops, multibloc,
allumage). Ce qui **ne peut être vérifié qu'en jeu (client)**, par ordre de priorité :

1. **Démarrage client** : l'instance se lance (mods client : Sodium, Iris, Iris Flywheel Compat,
   Entity Culling, ImmediatelyFast…) et atteint le menu. En cas de crash, envoie
   `logs/latest.log` (et le fichier de `crash-reports/` s'il existe).
2. **Création d'un monde** : Terralith + YUNG's + When Dungeons Arise + Twilight Forest se
   génèrent sans erreur ; tu reçois le Carnet et le Journal n°1.
3. **Livre de quêtes** : les chapitres ont leurs titres et descriptions en français
   (sinon : problème de fichier de langue FTB), les icônes s'affichent.
4. **Carnet de l'Ingénieur** (Patchouli) : s'ouvre, catégories « Journaux » et « Guide des ères »
   visibles ; le Journal n°2 se déverrouille quand on l'a dans l'inventaire.
5. **Items de lore** : textures et infobulles des fragments, codex, journaux (EMI).
6. **Recettes-portes dans EMI** : marteau IE, boîtier en acier Mekanism, graveur AE2 affichent le
   Codex ; en fabriquer une à la table de craft doit **laisser le Codex dans la grille**.
7. **Shaders** : activer Complementary puis BSL puis MakeUp ; vérifier qu'une machine Create en
   mouvement (roue à eau, presse) s'affiche correctement.
8. **Assemblage séquencé** du Mécanisme à vapeur (Create) et **infusion** de l'Alliage du Noyau
   (Mekanism), recettes écrites en JSON brut.
9. **Boss** : le Gardien du Noyau (œuf d'apparition en créatif) s'affiche (golem noirci ×2), a une
   barre de boss, change de phase (boules de feu, vex, ondes de choc).
10. **Le Moteur** : construire le cube 5×5×5 (97 boîtiers + contrôleur au centre d'une face),
    clic droit = état ; y brancher de l'énergie (câble Mekanism/IE) ; allumage accroupi.
11. **Performances** avec 10 Go : FPS en base Create chargée, avec et sans shaders.
12. **Distant Horizons** (optionnel) : activation via la fenêtre packwiz, cohabitation avec Iris.

Pour tester vite en créatif : `/give @s dernier_moteur:codex_spark`, puis `dernier_moteur:codex_forge`,
`dernier_moteur:codex_automaton` ; les fragments sont `dernier_moteur:core_fragment_<gear|spark|ember|storm|void|abyss>`.

## Liste des mods
Voir [`docs/mods.md`](docs/mods.md) (rôle de chaque mod et mods écartés).

## Structure du dépôt

| Dossier | Contenu |
|---|---|
| `pack/` | Le pack packwiz (`pack.toml`, `index.toml`, `mods/`, `config/`, `kubejs/`, `shaderpacks/`…). |
| `docs/` | Documentation de conception (`progression.md`…). |
| `mod/` | Le mod NeoForge custom `dernier_moteur` (boss final + multibloc du Moteur). |
| `.github/workflows/` | CI : compilation du mod et publication en release. |
| `CLAUDE.md` | Mémo de projet : conventions, décisions, état d'avancement. |

## Mod custom et CI
Le mod `dernier_moteur` (dossier `mod/`, voir [`mod/README.md`](mod/README.md)) apporte le boss
final et le Moteur. La GitHub Action **Mod dernier_moteur** le compile à chaque changement ; au
premier push d'une nouvelle version (`mod_version` dans `mod/gradle.properties`), elle publie le
jar dans une release `mod-v<version>` et ajoute/actualise automatiquement
`pack/mods/dernier-moteur.pw.toml` (URL de la release + sha512). packwiz-installer le télécharge
donc comme n'importe quel autre mod. L'Action **Vérification du pack** contrôle que l'index
packwiz et les quêtes générées sont à jour.

## Développement
- Outil : `packwiz` (`go install github.com/packwiz/packwiz@latest`).
- Ajouter un mod : `cd pack && packwiz modrinth add <slug>` (ou `packwiz curseforge add <slug>`).
- Après toute modification de fichiers dans `pack/` : `packwiz refresh`.
