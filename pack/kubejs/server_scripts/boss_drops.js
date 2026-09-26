// Le Dernier Moteur — chaque gardien vaincu lâche son Fragment du Noyau (100 %) et un journal.
// On utilise l'événement de mort (et non la table de butin) : certains boss (Twilight Forest)
// rangent leur butin dans un coffre, et Cataclysm joue une longue animation de mort.
// L'objet est rendu invulnérable (lave de l'arène d'Ignis, vide de l'End…) et sans expiration.

const GUARDIANS = {
  'mowziesmobs:ferrous_wroughtnaut': { fragment: 'core_fragment_gear', journal: 2, name: 'Rouage' },
  'twilightforest:lich': { fragment: 'core_fragment_spark', journal: 3, name: 'Étincelle' },
  'cataclysm:ignis': { fragment: 'core_fragment_ember', journal: 4, name: 'Braise' },
  'cataclysm:the_harbinger': { fragment: 'core_fragment_storm', journal: 5, name: 'Tempête' },
  'cataclysm:ender_guardian': { fragment: 'core_fragment_void', journal: 6, name: 'Néant' },
  'cataclysm:the_leviathan': { fragment: 'core_fragment_abyss', journal: 7, name: 'Abysse' },
  'dernier_moteur:core_guardian': { fragment: null, journal: 8, name: null }
}

function dropSafe(entity, id) {
  let drop = entity.spawnAtLocation(Item.of(id))
  if (drop) {
    drop.setInvulnerable(true)
    drop.setUnlimitedLifetime()
  }
}

Object.keys(GUARDIANS).forEach(type => {
  const g = GUARDIANS[type]
  EntityEvents.death(type, event => {
    const entity = event.entity
    if (entity.level.isClientSide()) return
    if (g.fragment) dropSafe(entity, `dernier_moteur:${g.fragment}`)
    dropSafe(entity, `dernier_moteur:journal_${g.journal}`)
    if (g.name) {
      event.server.tell(Text.gold(`Le gardien s'effondre. Un Fragment du Noyau — ${g.name} — roule à terre.`).italic())
    }
  })
})
