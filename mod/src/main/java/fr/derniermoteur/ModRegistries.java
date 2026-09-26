package fr.derniermoteur;

import fr.derniermoteur.block.EngineCoreBlock;
import fr.derniermoteur.block.EngineCoreBlockEntity;
import fr.derniermoteur.entity.CoreGuardian;
import fr.derniermoteur.item.GuardianKeyItem;
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.MobCategory;
import net.minecraft.world.item.BlockItem;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Rarity;
import net.minecraft.world.level.block.Block;
import net.minecraft.world.level.block.SoundType;
import net.minecraft.world.level.block.entity.BlockEntityType;
import net.minecraft.world.level.block.state.BlockBehaviour;
import net.minecraft.world.level.material.MapColor;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.neoforge.common.DeferredSpawnEggItem;
import net.neoforged.neoforge.registries.DeferredBlock;
import net.neoforged.neoforge.registries.DeferredHolder;
import net.neoforged.neoforge.registries.DeferredItem;
import net.neoforged.neoforge.registries.DeferredRegister;

public final class ModRegistries {
    private ModRegistries() {}

    public static final DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks(DernierMoteur.MODID);
    public static final DeferredRegister.Items ITEMS = DeferredRegister.createItems(DernierMoteur.MODID);
    public static final DeferredRegister<BlockEntityType<?>> BLOCK_ENTITIES =
            DeferredRegister.create(Registries.BLOCK_ENTITY_TYPE, DernierMoteur.MODID);
    public static final DeferredRegister<EntityType<?>> ENTITIES =
            DeferredRegister.create(Registries.ENTITY_TYPE, DernierMoteur.MODID);
    public static final DeferredRegister<CreativeModeTab> TABS =
            DeferredRegister.create(Registries.CREATIVE_MODE_TAB, DernierMoteur.MODID);

    // --- Blocs du Moteur
    public static final DeferredBlock<Block> ENGINE_CASING = BLOCKS.registerSimpleBlock("engine_casing",
            BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_GRAY).strength(8.0f, 1200.0f)
                    .requiresCorrectToolForDrops().sound(SoundType.NETHERITE_BLOCK));

    public static final DeferredBlock<EngineCoreBlock> ENGINE_CORE = BLOCKS.register("engine_core",
            () -> new EngineCoreBlock(BlockBehaviour.Properties.of().mapColor(MapColor.COLOR_ORANGE)
                    .strength(10.0f, 1200.0f).requiresCorrectToolForDrops().sound(SoundType.NETHERITE_BLOCK)
                    .lightLevel(state -> state.getValue(EngineCoreBlock.LIT) ? 15 : 3)));

    public static final DeferredItem<BlockItem> ENGINE_CASING_ITEM = ITEMS.registerSimpleBlockItem(ENGINE_CASING);
    public static final DeferredItem<BlockItem> ENGINE_CORE_ITEM = ITEMS.registerSimpleBlockItem(ENGINE_CORE,
            new Item.Properties().rarity(Rarity.EPIC));

    public static final DeferredHolder<BlockEntityType<?>, BlockEntityType<EngineCoreBlockEntity>> ENGINE_CORE_BE =
            BLOCK_ENTITIES.register("engine_core",
                    () -> BlockEntityType.Builder.of(EngineCoreBlockEntity::new, ENGINE_CORE.get()).build(null));

    // --- Le Gardien du Noyau
    public static final DeferredHolder<EntityType<?>, EntityType<CoreGuardian>> CORE_GUARDIAN =
            ENTITIES.register("core_guardian", () -> EntityType.Builder.of(CoreGuardian::new, MobCategory.MONSTER)
                    .sized(2.8f, 5.4f).fireImmune().clientTrackingRange(12).build("core_guardian"));

    public static final DeferredItem<GuardianKeyItem> GUARDIAN_KEY = ITEMS.register("guardian_key",
            () -> new GuardianKeyItem(new Item.Properties().stacksTo(1).rarity(Rarity.EPIC).fireResistant()));
    public static final DeferredItem<Item> GUARDIAN_HEART = ITEMS.registerSimpleItem("guardian_heart",
            new Item.Properties().stacksTo(1).rarity(Rarity.EPIC).fireResistant());
    public static final DeferredItem<DeferredSpawnEggItem> CORE_GUARDIAN_SPAWN_EGG = ITEMS.register(
            "core_guardian_spawn_egg", () -> new DeferredSpawnEggItem(CORE_GUARDIAN, 0x2A3236, 0xF07A2A,
                    new Item.Properties()));

    public static final DeferredHolder<CreativeModeTab, CreativeModeTab> TAB = TABS.register("main",
            () -> CreativeModeTab.builder()
                    .title(Component.translatable("itemGroup.dernier_moteur"))
                    .icon(() -> new ItemStack(ENGINE_CORE_ITEM.get()))
                    .displayItems((params, out) -> {
                        out.accept(ENGINE_CASING_ITEM.get());
                        out.accept(ENGINE_CORE_ITEM.get());
                        out.accept(GUARDIAN_KEY.get());
                        out.accept(GUARDIAN_HEART.get());
                        out.accept(CORE_GUARDIAN_SPAWN_EGG.get());
                    })
                    .build());

    public static void register(IEventBus bus) {
        BLOCKS.register(bus);
        ITEMS.register(bus);
        BLOCK_ENTITIES.register(bus);
        ENTITIES.register(bus);
        TABS.register(bus);
    }
}
