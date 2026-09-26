// Le Dernier Moteur — items et blocs de lore (namespace dernier_moteur)
// Les noms sont en français directement (pack francophone) ; les descriptions sont dans
// client_scripts/tooltips.js. Textures : kubejs/assets/dernier_moteur/textures/ (tools/gen_textures.py).

const FRAGMENTS = [
  ['core_fragment_gear', 'Fragment du Noyau — Rouage'],
  ['core_fragment_spark', 'Fragment du Noyau — Étincelle'],
  ['core_fragment_ember', 'Fragment du Noyau — Braise'],
  ['core_fragment_storm', 'Fragment du Noyau — Tempête'],
  ['core_fragment_void', 'Fragment du Noyau — Néant'],
  ['core_fragment_abyss', 'Fragment du Noyau — Abysse']
]

const CODEX = [
  ['codex_spark', "Codex de l'Étincelle"],
  ['codex_forge', 'Codex de la Forge'],
  ['codex_automaton', "Codex de l'Automate"]
]

StartupEvents.registry('item', event => {
  FRAGMENTS.forEach(([id, name]) => {
    event.create(`dernier_moteur:${id}`)
      .displayName(name)
      .maxStackSize(1)
      .rarity('epic')
      .glow(true)
      .fireResistant(true)
      .tag('dernier_moteur:core_fragments')
  })

  CODEX.forEach(([id, name]) => {
    event.create(`dernier_moteur:${id}`)
      .displayName(name)
      .maxStackSize(1)
      .rarity('rare')
      .glow(true)
      .tag('dernier_moteur:codex')
  })

  // Composants d'ère
  event.create('dernier_moteur:steam_mechanism').displayName('Mécanisme à vapeur').rarity('uncommon')
  event.create('dernier_moteur:incomplete_steam_mechanism')
    .displayName('Mécanisme à vapeur inachevé')
    .texture('dernier_moteur:item/steam_mechanism')
    .maxStackSize(1)
  event.create('dernier_moteur:galvanic_coil').displayName('Bobine galvanique').rarity('uncommon')
  event.create('dernier_moteur:core_alloy').displayName('Alliage du Noyau').rarity('rare')
    .tag('c:ingots').tag('c:ingots/core_alloy')
  event.create('dernier_moteur:engine_processor').displayName('Processeur du Moteur').rarity('epic')

  // Journaux d'ingénieur (lore, lisibles via l'infobulle et le Carnet Patchouli)
  for (let i = 1; i <= 8; i++) {
    event.create(`dernier_moteur:journal_${i}`)
      .displayName(`Journal d'ingénieur n°${i}`)
      .maxStackSize(1)
      .rarity('uncommon')
      .tag('dernier_moteur:journals')
  }
})

StartupEvents.registry('block', event => {
  event.create('dernier_moteur:core_alloy_block')
    .displayName("Bloc d'alliage du Noyau")
    .soundType('metal')
    .hardness(6.0)
    .resistance(12.0)
    .requiresTool(true)
    .tagBlock('minecraft:mineable/pickaxe')
    .tagBlock('minecraft:needs_iron_tool')
    .tagBoth('c:storage_blocks')
    .tagBoth('c:storage_blocks/core_alloy')
})
