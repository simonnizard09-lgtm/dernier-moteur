// Contrôle automatique (CI) — copié dans server_scripts par tools/ci/boot_test.sh, jamais livré au joueur.
// Vérifie recettes-portes, quêtes et drops des gardiens, écrit "CI RESULT OK|FAIL" puis arrête le serveur.
let CI_FAILS = []
function ciCheck(server) {
  let rm = server.recipeManager
  let ours = 0
  rm.getRecipes().forEach(h => { if (String(h.id()).startsWith('dernier_moteur:')) ours++ })
  if (ours < 25) CI_FAILS.push('recettes dernier_moteur=' + ours)
  ;['immersiveengineering:crafting/hammer', 'mekanism:steel_casing', 'ae2:network/blocks/inscribers', 'ae2:network/blocks/controller']
    .forEach(id => { if (rm.byKey(id).isPresent()) CI_FAILS.push('recette non verrouillée ' + id) })
  let qf = Java.loadClass('dev.ftb.mods.ftbquests.quest.ServerQuestFile').INSTANCE
  let nq = 0
  qf.getAllChapters().forEach(c => nq += c.getQuests().size())
  if (nq < 200) CI_FAILS.push('quêtes=' + nq)
  console.info('CI recettes=' + ours + ' quêtes=' + nq)
  let lvl = server.overworld(), sp = lvl.getSharedSpawnPos()
  let bosses = ['mowziesmobs:ferrous_wroughtnaut', 'twilightforest:lich', 'cataclysm:ignis', 'cataclysm:the_harbinger',
    'cataclysm:ender_guardian', 'cataclysm:the_leviathan', 'dernier_moteur:core_guardian']
  bosses.forEach((b, i) => server.runCommandSilent(`execute in minecraft:overworld run summon ${b} ${sp.x + i * 8} ${sp.y + 2} ${sp.z + 30}`))
  server.scheduleInTicks(20, () => {
    bosses.forEach(b => server.runCommandSilent(`kill @e[type=${b}]`))
    server.scheduleInTicks(80, () => {
      let drops = []
      lvl.getAllEntities().forEach(en => {
        if (String(en.type) == 'minecraft:item') drops.push(String(en.item.id))
      })
      ;['gear', 'spark', 'ember', 'storm', 'void', 'abyss'].forEach(f => {
        if (drops.indexOf('dernier_moteur:core_fragment_' + f) < 0) CI_FAILS.push('fragment manquant ' + f)
      })
      if (drops.indexOf('dernier_moteur:guardian_heart') < 0) CI_FAILS.push('coeur du gardien manquant')
      console.info('CI RESULT ' + (CI_FAILS.length ? 'FAIL ' + CI_FAILS.join(' ; ') : 'OK'))
      server.runCommandSilent('stop')
    })
  })
}
ServerEvents.loaded(e => e.server.scheduleInTicks(40, () => ciCheck(e.server)))
