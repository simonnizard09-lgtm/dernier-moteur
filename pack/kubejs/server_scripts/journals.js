// Le Dernier Moteur — clic droit sur un Journal d'ingénieur : ouvre sa page dans le Carnet
// (livre Patchouli externe patchouli:carnet, entrée patchouli:journaux/journal_N).
// Côté serveur : Patchouli envoie au client l'ordre d'ouvrir le livre à la bonne entrée.

let $PatchouliAPI = Java.loadClass('vazkii.patchouli.api.PatchouliAPI')
let $RL = Java.loadClass('net.minecraft.resources.ResourceLocation')
let CARNET_ID = $RL.parse('patchouli:carnet')

ItemEvents.rightClicked(event => {
  let id = String(event.item.id)
  let m = id.match(/^dernier_moteur:journal_(\d)$/)
  if (!m) return
  let player = event.player
  if (!player || player.level.isClientSide()) return
  $PatchouliAPI.get().openBookEntry(player, CARNET_ID, $RL.parse('patchouli:journaux/journal_' + m[1]), 0)
  event.cancel()
})
