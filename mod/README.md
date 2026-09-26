# Mod `dernier_moteur`

Contenu final du modpack (NeoForge 21.1.x, Minecraft 1.21.1, Java 21).

| Objet | ID | Rôle |
|---|---|---|
| Gardien du Noyau | `dernier_moteur:core_guardian` | Boss (600 PV, 3 phases : mêlée → boules de feu + vex → rage + ondes de choc). Lâche le Cœur du Gardien et une étoile du Nether. |
| Clé du Gardien | `dernier_moteur:guardian_key` | Clic droit au sol : invoque le Gardien (un seul à la fois dans 64 blocs). |
| Cœur du Gardien | `dernier_moteur:guardian_heart` | Pièce exigée par le Moteur. |
| Boîtier du Moteur | `dernier_moteur:engine_casing` | 97 blocs forment la coque 5×5×5. |
| Contrôleur du Moteur | `dernier_moteur:engine_core` | Centre d'une face. Reçoit 100 M FE (2 M FE/t max) et les pièces : 6 fragments du Noyau, Cœur du Gardien, 4 processeurs du Moteur. Clic droit : état ; accroupi : allumage. |

Les fragments et processeurs sont des items **KubeJS** du pack (même namespace), résolus par ID à
l'exécution : le mod se charge sans KubeJS, mais le Moteur ne peut alors pas être complété.
Les recettes des objets du mod sont dans `pack/kubejs/server_scripts/recipes_progression.js`.

Allumage : titre et messages de fin, jour + ciel clair, effets bénéfiques, particules, et
l'advancement `dernier_moteur:engine_ignited` (utilisé par la dernière quête).

## Compiler
```
cd mod
./gradlew build        # -> build/libs/dernier_moteur-<version>.jar
```
Textures : `python3 tools/gen_mod_textures.py` (depuis la racine du dépôt).
