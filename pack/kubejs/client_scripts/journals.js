// Le Dernier Moteur — clic droit sur un Journal d'ingénieur : ouvre sa page dans le Carnet.
//
// Côté CLIENT volontairement : l'API serveur de Patchouli (openBookEntry(ServerPlayer, …))
// déconnecte le joueur si l'entrée est introuvable côté client. Ici on vérifie que l'entrée
// existe dans le livre chargé ; sinon on ouvre simplement le Carnet et on journalise la liste
// des entrées connues (logs/kubejs/client.log) pour le diagnostic.
// Patchouli ne construit le contenu du livre qu'à sa première ouverture : si l'entrée est absente,
// on force la construction (reloadContents) avant d'ouvrir la page.
// ATTENTION : event.cancel() interrompt le handler (KubeJS 7) → toujours l'appeler en dernier.

let $PatchouliAPI = Java.loadClass('vazkii.patchouli.api.PatchouliAPI')
let $BookRegistry = Java.loadClass('vazkii.patchouli.common.book.BookRegistry')
let $RL = Java.loadClass('net.minecraft.resources.ResourceLocation')
let CARNET_ID = $RL.parse('patchouli:carnet')

ItemEvents.rightClicked(event => {
  let m = String(event.item.id).match(/^dernier_moteur:journal_(\d)$/)
  if (!m) return
  try {
    let entryId = $RL.parse('patchouli:journaux/journal_' + m[1])
    let book = $BookRegistry.INSTANCE.books.get(CARNET_ID)
    let contents = book ? book.getContents() : null
    // Contenu pas encore construit (Patchouli le charge souvent à la première ouverture du livre) :
    // on le construit maintenant, comme le fait Patchouli (BookRegistry → reloadContents(level, false)).
    if (book && (!contents || !contents.entries.containsKey(entryId))) {
      book.reloadContents(event.player.level, false)
      contents = book.getContents()
    }
    if (contents && !contents.isErrored() && contents.entries.containsKey(entryId)) {
      $PatchouliAPI.get().openBookEntry(CARNET_ID, entryId, 0)
    } else {
      let known = []
      if (contents) contents.entries.keySet().forEach(k => known.push(String(k)))
      console.warn('Journal ' + entryId + ' introuvable dans le Carnet même après rechargement (book=' + !!book
        + ', errored=' + (contents ? contents.isErrored() : 'n/a') + ', entrées=' + known.join(', ') + ')')
      $PatchouliAPI.get().openBookGUI(CARNET_ID)
    }
  } catch (err) {
    console.error('Ouverture du Carnet impossible : ' + err)
  }
  event.cancel()
})
