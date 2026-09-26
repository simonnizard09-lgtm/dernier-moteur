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

## Développement
- Outil : `packwiz` (`go install github.com/packwiz/packwiz@latest`).
- Ajouter un mod : `cd pack && packwiz modrinth add <slug>` (ou `packwiz curseforge add <slug>`).
- Après toute modification de fichiers dans `pack/` : `packwiz refresh`.
