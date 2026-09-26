// Le Dernier Moteur — recettes qui imposent la progression (voir docs/progression.md)
//
// Principe : les machines-clés d'une ère demandent le Codex de cette ère comme catalyseur
// (keepIngredient : il reste dans la grille) et/ou le composant fabriqué à l'ère précédente.
// Les recettes des mods tiers sont écrites en JSON brut (event.custom) : pas d'addon KubeJS requis.

const DM = id => `dernier_moteur:${id}`

ServerEvents.recipes(event => {
  // ---------------------------------------------------------------------------
  // Composants d'ère
  // ---------------------------------------------------------------------------

  // Ère I — Mécanisme à vapeur : assemblage séquencé Create sur tôle de laiton
  event.custom({
    type: 'create:sequenced_assembly',
    ingredient: { tag: 'c:plates/brass' },
    loops: 1,
    results: [{ id: DM('steam_mechanism') }],
    transitional_item: { id: DM('incomplete_steam_mechanism') },
    sequence: [
      {
        type: 'create:deploying',
        ingredients: [{ item: DM('incomplete_steam_mechanism') }, { item: 'create:precision_mechanism' }],
        results: [{ id: DM('incomplete_steam_mechanism') }]
      },
      {
        type: 'create:deploying',
        ingredients: [{ item: DM('incomplete_steam_mechanism') }, { item: 'create:electron_tube' }],
        results: [{ id: DM('incomplete_steam_mechanism') }]
      },
      {
        type: 'create:filling',
        ingredients: [
          { item: DM('incomplete_steam_mechanism') },
          { type: 'neoforge:single', amount: 250, fluid: 'minecraft:water' }
        ],
        results: [{ id: DM('incomplete_steam_mechanism') }]
      },
      {
        type: 'create:pressing',
        ingredients: [{ item: DM('incomplete_steam_mechanism') }],
        results: [{ id: DM('incomplete_steam_mechanism') }]
      }
    ]
  }).id(DM('sequenced_assembly/steam_mechanism'))

  // Ère II — Bobine galvanique (IE + Crafts & Additions + Create), gardée par le Codex de l'Étincelle
  event.shaped(Item.of(DM('galvanic_coil'), 2), [
    'SBS',
    'CLC',
    'SKS'
  ], {
    S: '#c:plates/steel',
    B: '#c:plates/brass',
    C: 'createaddition:copper_spool',
    L: 'immersiveengineering:coil_lv',
    K: DM('codex_spark')
  }).keepIngredient(DM('codex_spark')).id(DM('crafting/galvanic_coil'))

  // Ère III — Alliage du Noyau : infuseur métallurgique (acier + obsidienne raffinée)
  event.custom({
    type: 'mekanism:metallurgic_infusing',
    chemical_input: { amount: 40, tag: 'mekanism:refined_obsidian' },
    item_input: { count: 1, tag: 'c:ingots/steel' },
    output: { count: 1, id: DM('core_alloy') },
    per_tick_usage: false
  }).id(DM('metallurgic_infusing/core_alloy'))

  event.shaped(DM('core_alloy_block'), ['AAA', 'AAA', 'AAA'], { A: DM('core_alloy') })
    .id(DM('crafting/core_alloy_block'))
  event.shapeless(Item.of(DM('core_alloy'), 9), [DM('core_alloy_block')])
    .id(DM('crafting/core_alloy_from_block'))

  // Ère IV — Processeur du Moteur : graveur AE2
  event.custom({
    type: 'ae2:inscriber',
    mode: 'press',
    ingredients: {
      top: { item: 'ae2:engineering_processor' },
      middle: { item: DM('core_alloy') },
      bottom: { item: 'ae2:calculation_processor' }
    },
    result: { count: 1, id: DM('engine_processor') }
  }).id(DM('inscriber/engine_processor'))

  // ---------------------------------------------------------------------------
  // Codex (le fragment reste dans la grille)
  // ---------------------------------------------------------------------------
  event.shaped(DM('codex_spark'), [
    ' F ',
    'NBN',
    ' M '
  ], {
    F: DM('core_fragment_gear'),
    N: 'twilightforest:naga_scale',
    B: 'minecraft:book',
    M: DM('steam_mechanism')
  }).keepIngredient(DM('core_fragment_gear')).id(DM('crafting/codex_spark'))

  event.shaped(DM('codex_forge'), [
    'IFI',
    'GBG',
    'SCS'
  ], {
    F: DM('core_fragment_spark'),
    I: 'twilightforest:ironwood_ingot',
    S: 'twilightforest:steeleaf_ingot',
    G: DM('galvanic_coil'),
    B: 'minecraft:book',
    C: 'immersiveengineering:component_steel'
  }).keepIngredient(DM('core_fragment_spark')).id(DM('crafting/codex_forge'))

  event.shaped(DM('codex_automaton'), [
    'E T',
    'IBW',
    ' A '
  ], {
    E: DM('core_fragment_ember'),
    T: DM('core_fragment_storm'),
    I: 'cataclysm:ignitium_ingot',
    W: 'cataclysm:witherite_ingot',
    B: 'minecraft:book',
    A: DM('core_alloy')
  }).keepIngredient(DM('core_fragment_ember')).keepIngredient(DM('core_fragment_storm'))
    .id(DM('crafting/codex_automaton'))

  // ---------------------------------------------------------------------------
  // Ère II — Électricité : gardée par le Codex de l'Étincelle / la bobine galvanique
  // ---------------------------------------------------------------------------
  event.remove({ id: 'immersiveengineering:crafting/hammer' })
  event.shaped('immersiveengineering:hammer', [
    ' IF',
    ' SI',
    'S K'
  ], {
    I: '#c:ingots/iron',
    F: '#c:strings',
    S: '#c:rods/wooden',
    K: DM('codex_spark')
  }).keepIngredient(DM('codex_spark')).id(DM('gate/ie_hammer'))

  event.remove({ id: 'immersiveengineering:crafting/workbench' })
  event.shaped('immersiveengineering:workbench', [
    'iss',
    'cKf'
  ], {
    i: '#c:ingots/iron',
    s: '#immersiveengineering:treated_wood_slab',
    c: 'immersiveengineering:craftingtable',
    f: 'immersiveengineering:treated_fence',
    K: DM('codex_spark')
  }).keepIngredient(DM('codex_spark')).id(DM('gate/ie_workbench'))

  event.remove({ id: 'immersiveengineering:crafting/dynamo' })
  event.shaped('immersiveengineering:dynamo', [
    'rcr',
    'igi'
  ], {
    r: '#c:dusts/redstone',
    c: 'immersiveengineering:component_iron',
    i: '#c:ingots/iron',
    g: DM('galvanic_coil')
  }).id(DM('gate/ie_dynamo'))

  event.remove({ id: 'createaddition:mechanical_crafting/alternator' })
  event.custom({
    type: 'create:mechanical_crafting',
    accept_mirrored: false,
    category: 'misc',
    key: {
      A: { item: 'create:andesite_alloy' },
      I: { tag: 'c:plates/iron' },
      S: { item: 'createaddition:copper_spool' },
      G: { item: DM('galvanic_coil') }
    },
    pattern: ['  A  ', ' ISI ', 'ISGSI', ' ISI ', '  A  '],
    result: { count: 1, id: 'createaddition:alternator' },
    show_notification: false
  }).id(DM('gate/cca_alternator'))

  event.remove({ id: 'createaddition:mechanical_crafting/electric_motor' })
  event.custom({
    type: 'create:mechanical_crafting',
    accept_mirrored: false,
    category: 'misc',
    key: {
      A: { item: 'create:andesite_alloy' },
      B: { tag: 'c:plates/brass' },
      C: { item: 'createaddition:capacitor' },
      S: { item: 'createaddition:copper_spool' },
      G: { item: DM('galvanic_coil') }
    },
    pattern: ['  A  ', ' BSB ', 'BSGSB', ' BCB '],
    result: { count: 1, id: 'createaddition:electric_motor' },
    show_notification: false
  }).id(DM('gate/cca_electric_motor'))

  // ---------------------------------------------------------------------------
  // Ère III — Industrie lourde : gardée par le Codex de la Forge
  // ---------------------------------------------------------------------------
  event.remove({ id: 'mekanism:steel_casing' })
  event.shaped('mekanism:steel_casing', [
    'SGS',
    'OKO',
    'SGS'
  ], {
    S: '#c:ingots/steel',
    G: '#c:glass_blocks/cheap',
    O: '#c:ingots/osmium',
    K: DM('codex_forge')
  }).keepIngredient(DM('codex_forge')).id(DM('gate/mek_steel_casing'))

  event.remove({ id: 'mekanism:metallurgic_infuser' })
  event.shaped('mekanism:metallurgic_infuser', [
    'IFI',
    'OKO',
    'IRI'
  ], {
    I: '#c:ingots/iron',
    F: 'minecraft:furnace',
    O: '#c:ingots/osmium',
    R: '#c:dusts/redstone',
    K: DM('codex_forge')
  }).keepIngredient(DM('codex_forge')).id(DM('gate/mek_metallurgic_infuser'))

  event.remove({ id: 'immersiveengineering:crafting/heavy_engineering' })
  event.shaped(Item.of('immersiveengineering:heavy_engineering', 4), [
    'igi',
    'eKe',
    'igi'
  ], {
    i: '#c:sheetmetals/steel',
    g: 'immersiveengineering:component_steel',
    e: '#c:ingots/electrum',
    K: DM('codex_forge')
  }).keepIngredient(DM('codex_forge')).id(DM('gate/ie_heavy_engineering'))

  // Circuit de contrôle basique : demande un composant électronique IE (établi d'ingénieur)
  event.remove({ id: 'mekanism:control_circuit/basic' })
  event.shaped(Item.of('mekanism:basic_control_circuit', 2), [
    'OEO'
  ], {
    O: '#c:ingots/osmium',
    E: 'immersiveengineering:component_electronic'
  }).id(DM('cross/mek_basic_control_circuit'))

  // ---------------------------------------------------------------------------
  // Ère IV — Automatisation : gardée par le Codex de l'Automate / Processeur du Moteur
  // ---------------------------------------------------------------------------
  event.remove({ id: 'ae2:network/blocks/inscribers' })
  event.shaped('ae2:inscriber', [
    'aba',
    'cKa',
    'aba'
  ], {
    a: '#c:ingots/iron',
    b: 'minecraft:piston',
    c: '#c:ingots/copper',
    K: DM('codex_automaton')
  }).keepIngredient(DM('codex_automaton')).id(DM('gate/ae2_inscriber'))

  event.remove({ id: 'ae2:network/blocks/controller' })
  event.shaped('ae2:controller', [
    'aba',
    'bPb',
    'aba'
  ], {
    a: 'ae2:smooth_sky_stone_block',
    b: 'ae2:fluix_crystal',
    P: DM('engine_processor')
  }).id(DM('gate/ae2_controller'))

  event.remove({ id: 'industrialforegoing:machine_frame_pity' })
  event.shaped('industrialforegoing:machine_frame_pity', [
    'WIW',
    'RKR',
    'WAW'
  ], {
    W: '#minecraft:logs',
    I: '#c:ingots/iron',
    R: '#c:storage_blocks/redstone',
    A: DM('core_alloy'),
    K: DM('codex_automaton')
  }).keepIngredient(DM('codex_automaton')).id(DM('gate/if_machine_frame_pity'))

  event.remove({ id: 'industrialforegoing:ore_laser_base' })
  event.shaped('industrialforegoing:ore_laser_base', [
    'pfp',
    'bmb',
    'gPg'
  ], {
    p: '#c:plastics',
    f: 'minecraft:diamond_pickaxe',
    b: '#c:ores/iron',
    m: '#industrialforegoing:machine_frame/advanced',
    g: '#c:gears/diamond',
    P: DM('engine_processor')
  }).id(DM('gate/if_ore_laser_base'))

  event.remove({ id: 'mekanism:digital_miner' })
  event.shaped('mekanism:digital_miner', [
    'APA',
    'SRS',
    'TXT'
  ], {
    A: '#mekanism:alloys/atomic',
    P: DM('engine_processor'),
    S: 'mekanism:logistical_sorter',
    R: 'mekanism:robit',
    T: 'mekanism:teleportation_core',
    X: 'mekanism:steel_casing'
  }).id(DM('gate/mek_digital_miner'))

  event.remove({ id: 'mekanismgenerators:reactor/controller' })
  event.shaped('mekanismgenerators:fusion_reactor_controller', [
    'CPC',
    'FTF',
    'FFF'
  ], {
    C: '#c:circuits/ultimate',
    P: DM('engine_processor'),
    F: 'mekanismgenerators:fusion_reactor_frame',
    T: 'mekanism:basic_chemical_tank'
  }).id(DM('gate/mekgen_fusion_controller'))

  // ---------------------------------------------------------------------------
  // Épilogue — objets du mod dernier_moteur (seulement si le mod est chargé)
  // ---------------------------------------------------------------------------
  if (Platform.isLoaded('dernier_moteur')) {
    event.shaped(Item.of(DM('engine_casing'), 4), [
      'SAS',
      'ACA',
      'SAS'
    ], {
      S: '#c:plates/steel',
      A: DM('core_alloy'),
      C: 'mekanism:steel_casing'
    }).id(DM('crafting/engine_casing'))

    event.shaped(DM('engine_core'), [
      'BPB',
      'CUC',
      'BPB'
    ], {
      B: DM('core_alloy_block'),
      P: DM('engine_processor'),
      C: DM('engine_casing'),
      U: 'mekanism:ultimate_control_circuit'
    }).id(DM('crafting/engine_core'))

    // Clé du Gardien : les six fragments restent dans la grille
    let FRAGS = ['gear', 'spark', 'ember', 'storm', 'void', 'abyss'].map(f => DM(`core_fragment_${f}`))
    event.shaped(DM('guardian_key'), [
      'GSE',
      'NBP',
      'TVA'
    ], {
      G: FRAGS[0], S: FRAGS[1], E: FRAGS[2], T: FRAGS[3], V: FRAGS[4], A: FRAGS[5],
      N: 'minecraft:nether_star',
      B: DM('core_alloy_block'),
      P: DM('engine_processor')
    }).keepIngredient(FRAGS[0]).keepIngredient(FRAGS[1]).keepIngredient(FRAGS[2])
      .keepIngredient(FRAGS[3]).keepIngredient(FRAGS[4]).keepIngredient(FRAGS[5])
      .id(DM('crafting/guardian_key'))
  }
})
