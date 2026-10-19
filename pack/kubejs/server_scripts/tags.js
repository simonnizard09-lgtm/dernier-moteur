// Le Dernier Moteur — tags.
//
// Table de décraft (Twilight Forest) : sans ces tags, décrafter un codex rendrait le fragment du
// Noyau qui est resté dans la grille, et décrafter une machine verrouillée rendrait le codex.
// « banned_uncrafting_ingredients » : toute recette contenant ces ingrédients devient indécraftable.

ServerEvents.tags('item', event => {
  event.add('twilightforest:banned_uncrafting_ingredients', [
    '#dernier_moteur:core_fragments',
    '#dernier_moteur:codex',
    'dernier_moteur:guardian_heart'
  ])
  event.add('twilightforest:banned_uncraftables', [
    '#dernier_moteur:codex',
    '#dernier_moteur:core_fragments',
    'dernier_moteur:steam_mechanism',
    'dernier_moteur:galvanic_coil',
    'dernier_moteur:core_alloy',
    'dernier_moteur:core_alloy_block',
    'dernier_moteur:engine_processor'
  ])
})
