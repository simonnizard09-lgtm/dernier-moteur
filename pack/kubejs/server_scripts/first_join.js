// Le Dernier Moteur — accueil : Carnet de l'Ingénieur (Patchouli) + Journal n°1, une seule fois.

PlayerEvents.loggedIn(event => {
  const player = event.player
  if (player.stages.has('dm_welcome')) return
  player.stages.add('dm_welcome')

  player.give(Item.of('patchouli:guide_book[patchouli:book="patchouli:carnet"]'))
  player.give('dernier_moteur:journal_1')

  player.tell(Text.gold('Le Moteur s\'est tu.').bold())
  player.tell(Text.gray('Le monde est devenu hostile. Ouvre ton livre de quêtes (touche L par défaut) '
    + 'et le Carnet de l\'Ingénieur pour savoir par où commencer.').italic())
})
