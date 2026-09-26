// Le Dernier Moteur — infobulles de lore et d'usage.

const LORE = {
  core_fragment_gear: ['Arraché au Ferrous Wroughtnaut.', 'Il tourne encore, lentement, sans axe.'],
  core_fragment_spark: ['Arraché à la Liche du Crépuscule.', 'Une étincelle prisonnière crépite à l\'intérieur.'],
  core_fragment_ember: ['Arraché à Ignis, le forgeron des âmes.', 'Chaud au toucher, même au fond de l\'eau.'],
  core_fragment_storm: ['Arraché au Harbinger de l\'usine ancienne.', 'On y entend gronder un orage lointain.'],
  core_fragment_void: ['Arraché à l\'Ender Guardian.', 'La lumière s\'y perd sans jamais ressortir.'],
  core_fragment_abyss: ['Arraché au Léviathan des cités englouties.', 'Il pèse le poids de toute la mer.'],
  codex_spark: ['Ère II — Électricité.', 'Reste dans la grille quand il sert de catalyseur.'],
  codex_forge: ['Ère III — Industrie lourde.', 'Reste dans la grille quand il sert de catalyseur.'],
  codex_automaton: ['Ère IV — Automatisation avancée.', 'Reste dans la grille quand il sert de catalyseur.'],
  steam_mechanism: ['Composant de l\'ère I (Create).'],
  galvanic_coil: ['Composant de l\'ère II (IE + Crafts & Additions).'],
  core_alloy: ['Composant de l\'ère III (Mekanism).'],
  engine_processor: ['Composant de l\'ère IV (AE2).', 'Le Moteur en réclame quatre.']
}

const JOURNALS = [
  'Le jour où le Moteur s\'est tu.',
  'Notes sur les gardiens de fer.',
  'La tour de la Liche.',
  'La forge des âmes.',
  'L\'usine ancienne.',
  'Au-delà de l\'End.',
  'Les cités englouties.',
  'Le dernier gardien.'
]

ItemEvents.modifyTooltips(event => {
  Object.keys(LORE).forEach(id => {
    event.add(`dernier_moteur:${id}`, LORE[id].map(line => Text.gray(line).italic()))
  })
  for (let i = 1; i <= 8; i++) {
    event.add(`dernier_moteur:journal_${i}`, [
      Text.gray(JOURNALS[i - 1]).italic(),
      Text.darkGray('À lire dans le Carnet de l\'Ingénieur.')
    ])
  }
  event.add('#dernier_moteur:core_fragments', [Text.gold('Fragment du Noyau — requis par le Moteur.')])
})
