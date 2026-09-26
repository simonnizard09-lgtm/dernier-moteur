package fr.derniermoteur.block;

import fr.derniermoteur.DernierMoteur;
import fr.derniermoteur.ModRegistries;
import net.minecraft.ChatFormatting;
import net.minecraft.advancements.AdvancementHolder;
import net.minecraft.core.BlockPos;
import net.minecraft.core.Direction;
import net.minecraft.core.HolderLookup;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.core.registries.BuiltInRegistries;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.MutableComponent;
import net.minecraft.network.protocol.game.ClientboundSetSubtitleTextPacket;
import net.minecraft.network.protocol.game.ClientboundSetTitleTextPacket;
import net.minecraft.network.protocol.game.ClientboundSetTitlesAnimationPacket;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionHand;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.level.block.entity.BlockEntity;
import net.minecraft.world.level.block.state.BlockState;
import net.neoforged.neoforge.energy.EnergyStorage;
import net.neoforged.neoforge.items.ItemStackHandler;

import java.util.List;

/**
 * Cœur logique du Moteur : réserve d'énergie, emplacements des pièces du Noyau,
 * vérification du multibloc et séquence de fin.
 */
public class EngineCoreBlockEntity extends BlockEntity {
    /** Réserve d'énergie à remplir avant l'allumage (FE). */
    public static final int ENERGY_CAPACITY = 100_000_000;
    /** Débit d'entrée maximal (FE/tick) : ~2,5 s minimum avec une source infinie. */
    public static final int MAX_RECEIVE = 2_000_000;

    /** Pièces exigées : identifiant (item KubeJS ou du mod) et quantité. */
    public record Requirement(ResourceLocation id, int count, String label) {
        Item item() {
            return BuiltInRegistries.ITEM.get(id);
        }
    }

    public static final List<Requirement> REQUIREMENTS = List.of(
            req("core_fragment_gear", 1, "Fragment du Noyau — Rouage"),
            req("core_fragment_spark", 1, "Fragment du Noyau — Étincelle"),
            req("core_fragment_ember", 1, "Fragment du Noyau — Braise"),
            req("core_fragment_storm", 1, "Fragment du Noyau — Tempête"),
            req("core_fragment_void", 1, "Fragment du Noyau — Néant"),
            req("core_fragment_abyss", 1, "Fragment du Noyau — Abysse"),
            req("guardian_heart", 1, "Cœur du Gardien"),
            req("engine_processor", 4, "Processeur du Moteur"));

    private static Requirement req(String path, int count, String label) {
        return new Requirement(ResourceLocation.fromNamespaceAndPath(DernierMoteur.MODID, path), count, label);
    }

    /** Réserve du Moteur : reçoit de l'énergie tant qu'il n'est pas allumé, ne la rend jamais. */
    public final class EngineEnergy extends EnergyStorage {
        EngineEnergy() {
            super(ENERGY_CAPACITY, MAX_RECEIVE, 0);
        }

        @Override
        public int receiveEnergy(int toReceive, boolean simulate) {
            if (ignited) {
                return 0;
            }
            int received = super.receiveEnergy(toReceive, simulate);
            if (received > 0 && !simulate) {
                setChanged();
            }
            return received;
        }

        void drainAll() {
            energy = 0;
        }
    }

    private final EngineEnergy energy = new EngineEnergy();

    private final ItemStackHandler items = new ItemStackHandler(REQUIREMENTS.size()) {
        @Override
        public boolean isItemValid(int slot, ItemStack stack) {
            if (ignited) {
                return false;
            }
            Item item = REQUIREMENTS.get(slot).item();
            return item != Items.AIR && stack.is(item);
        }

        @Override
        public int getSlotLimit(int slot) {
            return REQUIREMENTS.get(slot).count();
        }

        @Override
        public ItemStack extractItem(int slot, int amount, boolean simulate) {
            return ItemStack.EMPTY; // les pièces déposées ne ressortent pas par automatisation
        }

        @Override
        protected void onContentsChanged(int slot) {
            setChanged();
        }
    };

    private boolean ignited = false;
    private int ticks = 0;

    public EngineCoreBlockEntity(BlockPos pos, BlockState state) {
        super(ModRegistries.ENGINE_CORE_BE.get(), pos, state);
    }

    public EnergyStorage getEnergy() {
        return energy;
    }

    public ItemStackHandler getItems() {
        return items;
    }

    public boolean isIgnited() {
        return ignited;
    }

    // ------------------------------------------------------------------ interaction

    public boolean accepts(ItemStack stack) {
        for (int i = 0; i < REQUIREMENTS.size(); i++) {
            if (items.isItemValid(i, stack) && items.getStackInSlot(i).getCount() < REQUIREMENTS.get(i).count()) {
                return true;
            }
        }
        return false;
    }

    public void insertFromPlayer(Player player, InteractionHand hand) {
        ItemStack held = player.getItemInHand(hand);
        for (int i = 0; i < REQUIREMENTS.size() && !held.isEmpty(); i++) {
            ItemStack rest = items.insertItem(i, held.copy(), false);
            int inserted = held.getCount() - rest.getCount();
            if (inserted > 0) {
                if (!player.getAbilities().instabuild) {
                    held.shrink(inserted);
                }
                player.displayClientMessage(Component.literal("Le Moteur accepte : " + REQUIREMENTS.get(i).label()
                        + " (" + items.getStackInSlot(i).getCount() + "/" + REQUIREMENTS.get(i).count() + ")")
                        .withStyle(ChatFormatting.GOLD), true);
                level.playSound(null, worldPosition, SoundEvents.END_PORTAL_FRAME_FILL, SoundSource.BLOCKS, 1f, 0.8f);
                return;
            }
        }
    }

    private boolean itemsComplete() {
        for (int i = 0; i < REQUIREMENTS.size(); i++) {
            if (items.getStackInSlot(i).getCount() < REQUIREMENTS.get(i).count()) {
                return false;
            }
        }
        return true;
    }

    // ------------------------------------------------------------------ multibloc

    /** Résultat de la vérification de structure. */
    public record Structure(int missingCasings, int blockedInterior, BlockPos firstProblem) {
        boolean formed() {
            return missingCasings == 0 && blockedInterior == 0;
        }
    }

    /**
     * Le contrôleur est au centre d'une face ; le cube 5×5×5 s'étend derrière lui.
     * Coque : 97 boîtiers ; intérieur 3×3×3 : air.
     */
    public Structure checkStructure() {
        Direction facing = getBlockState().getValue(EngineCoreBlock.FACING);
        BlockPos center = worldPosition.relative(facing.getOpposite(), 2);
        int missing = 0, blocked = 0;
        BlockPos first = null;
        for (int dx = -2; dx <= 2; dx++) {
            for (int dy = -2; dy <= 2; dy++) {
                for (int dz = -2; dz <= 2; dz++) {
                    BlockPos p = center.offset(dx, dy, dz);
                    if (p.equals(worldPosition)) {
                        continue;
                    }
                    boolean interior = Math.abs(dx) < 2 && Math.abs(dy) < 2 && Math.abs(dz) < 2;
                    BlockState s = level.getBlockState(p);
                    if (interior) {
                        if (!s.isAir()) {
                            blocked++;
                            if (first == null) first = p;
                        }
                    } else if (!s.is(ModRegistries.ENGINE_CASING.get())) {
                        missing++;
                        if (first == null) first = p;
                    }
                }
            }
        }
        return new Structure(missing, blocked, first);
    }

    public void sendStatus(ServerPlayer player) {
        if (ignited) {
            player.sendSystemMessage(Component.literal("Le Moteur tourne. Le monde respire.")
                    .withStyle(ChatFormatting.GOLD, ChatFormatting.ITALIC));
            return;
        }
        Structure st = checkStructure();
        player.sendSystemMessage(Component.literal("— État du Moteur —").withStyle(ChatFormatting.GOLD));
        if (st.formed()) {
            player.sendSystemMessage(ok("Structure formée (5×5×5)"));
        } else {
            MutableComponent line = Component.literal("✘ Structure incomplète : ").withStyle(ChatFormatting.RED);
            if (st.missingCasings() > 0) line.append(st.missingCasings() + " boîtier(s) manquant(s) ");
            if (st.blockedInterior() > 0) line.append(st.blockedInterior() + " bloc(s) à retirer de l'intérieur ");
            if (st.firstProblem() != null) {
                BlockPos p = st.firstProblem();
                line.append("(ex. " + p.getX() + " " + p.getY() + " " + p.getZ() + ")");
            }
            player.sendSystemMessage(line);
        }
        int pct = (int) (100L * energy.getEnergyStored() / ENERGY_CAPACITY);
        MutableComponent e = Component.literal(String.format("Énergie : %,d / %,d FE (%d %%)",
                energy.getEnergyStored(), ENERGY_CAPACITY, pct));
        player.sendSystemMessage(energy.getEnergyStored() >= ENERGY_CAPACITY
                ? ok(e.getString()) : ko(e.getString()));
        for (int i = 0; i < REQUIREMENTS.size(); i++) {
            Requirement r = REQUIREMENTS.get(i);
            int have = items.getStackInSlot(i).getCount();
            String text = r.label() + " : " + have + "/" + r.count();
            if (r.item() == Items.AIR) {
                text += " (item introuvable : " + r.id() + ")";
            }
            player.sendSystemMessage(have >= r.count() ? ok(text) : ko(text));
        }
        if (st.formed() && itemsComplete() && energy.getEnergyStored() >= ENERGY_CAPACITY) {
            player.sendSystemMessage(Component.literal("Tout est prêt. Clic droit accroupi pour rallumer le Moteur.")
                    .withStyle(ChatFormatting.GOLD, ChatFormatting.BOLD));
        }
    }

    private static Component ok(String s) {
        return Component.literal("✔ " + s).withStyle(ChatFormatting.GREEN);
    }

    private static Component ko(String s) {
        return Component.literal("✘ " + s).withStyle(ChatFormatting.RED);
    }

    // ------------------------------------------------------------------ allumage

    public void tryIgnite(ServerPlayer player) {
        if (ignited) {
            sendStatus(player);
            return;
        }
        if (!checkStructure().formed() || !itemsComplete() || energy.getEnergyStored() < ENERGY_CAPACITY) {
            player.sendSystemMessage(Component.literal("Le Moteur ne répond pas. Il manque encore quelque chose.")
                    .withStyle(ChatFormatting.RED));
            sendStatus(player);
            return;
        }
        ignite((ServerLevel) level);
    }

    /** Séquence de fin (appelée par {@link #tryIgnite} une fois toutes les conditions réunies). */
    public void ignite(ServerLevel server) {
        ignited = true;
        energy.drainAll();
        for (int i = 0; i < REQUIREMENTS.size(); i++) {
            items.setStackInSlot(i, ItemStack.EMPTY);
        }
        server.setBlock(worldPosition, getBlockState().setValue(EngineCoreBlock.LIT, true), 3);
        setChanged();

        // Le monde se remet d'aplomb : jour, ciel clair.
        if (server.dimension() == Level.OVERWORLD) {
            server.setDayTime(1000);
        }
        server.setWeatherParameters(24000 * 3, 0, false, false);

        double cx = worldPosition.getX() + 0.5, cy = worldPosition.getY() + 0.5, cz = worldPosition.getZ() + 0.5;
        server.sendParticles(ParticleTypes.END_ROD, cx, cy + 2, cz, 400, 3, 3, 3, 0.2);
        server.sendParticles(ParticleTypes.TOTEM_OF_UNDYING, cx, cy + 2, cz, 300, 2, 2, 2, 0.6);
        server.sendParticles(ParticleTypes.FLASH, cx, cy, cz, 5, 0, 0, 0, 0);
        server.playSound(null, worldPosition, SoundEvents.END_PORTAL_SPAWN, SoundSource.BLOCKS, 4f, 0.7f);
        server.playSound(null, worldPosition, SoundEvents.BEACON_ACTIVATE, SoundSource.BLOCKS, 4f, 0.5f);

        AdvancementHolder adv = server.getServer().getAdvancements()
                .get(ResourceLocation.fromNamespaceAndPath(DernierMoteur.MODID, "engine_ignited"));
        for (ServerPlayer p : server.getServer().getPlayerList().getPlayers()) {
            p.connection.send(new ClientboundSetTitlesAnimationPacket(20, 120, 40));
            p.connection.send(new ClientboundSetTitleTextPacket(
                    Component.literal("Le Moteur gronde").withStyle(ChatFormatting.GOLD, ChatFormatting.BOLD)));
            p.connection.send(new ClientboundSetSubtitleTextPacket(
                    Component.literal("Le monde respire à nouveau.").withStyle(ChatFormatting.YELLOW)));
            p.sendSystemMessage(Component.literal(""));
            p.sendSystemMessage(Component.literal("Sous la roche, un grondement sourd reprend, d'abord hésitant, "
                    + "puis régulier, comme un cœur qui se souvient de battre.").withStyle(ChatFormatting.GRAY, ChatFormatting.ITALIC));
            p.sendSystemMessage(Component.literal("Les rivières s'éclaircissent. Le vent retrouve sa douceur. "
                    + "Quelque part, Iléa Vaucor aurait souri.").withStyle(ChatFormatting.GRAY, ChatFormatting.ITALIC));
            p.sendSystemMessage(Component.literal("Merci d'avoir joué au Dernier Moteur.").withStyle(ChatFormatting.GOLD));
            p.addEffect(new MobEffectInstance(MobEffects.REGENERATION, 20 * 60, 1));
            p.addEffect(new MobEffectInstance(MobEffects.ABSORPTION, 20 * 300, 4));
            p.addEffect(new MobEffectInstance(MobEffects.LUCK, 20 * 60 * 20, 1));
            p.addEffect(new MobEffectInstance(MobEffects.HERO_OF_THE_VILLAGE, 20 * 60 * 20, 2));
            p.playNotifySound(SoundEvents.UI_TOAST_CHALLENGE_COMPLETE, SoundSource.MASTER, 1f, 1f);
            if (adv != null) {
                p.getAdvancements().award(adv, "ignited");
            }
        }
        DernierMoteur.LOGGER.info("Le Moteur a été rallumé en {}", worldPosition);
    }

    public static void serverTick(Level level, BlockPos pos, BlockState state, EngineCoreBlockEntity be) {
        if (!be.ignited || !(level instanceof ServerLevel server)) {
            return;
        }
        if (++be.ticks % 40 == 0) {
            Direction facing = state.getValue(EngineCoreBlock.FACING);
            BlockPos c = pos.relative(facing.getOpposite(), 2);
            server.sendParticles(ParticleTypes.END_ROD, c.getX() + 0.5, c.getY() + 3.2, c.getZ() + 0.5,
                    12, 1.5, 0.3, 1.5, 0.02);
            if (be.ticks % 200 == 0) {
                server.playSound(null, pos, SoundEvents.BEACON_AMBIENT, SoundSource.BLOCKS, 1.5f, 0.6f);
            }
        }
    }

    // ------------------------------------------------------------------ sauvegarde

    @Override
    protected void saveAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.saveAdditional(tag, registries);
        tag.put("Energy", energy.serializeNBT(registries));
        tag.put("Items", items.serializeNBT(registries));
        tag.putBoolean("Ignited", ignited);
    }

    @Override
    protected void loadAdditional(CompoundTag tag, HolderLookup.Provider registries) {
        super.loadAdditional(tag, registries);
        if (tag.contains("Energy")) {
            energy.deserializeNBT(registries, tag.get("Energy"));
        }
        if (tag.contains("Items")) {
            items.deserializeNBT(registries, tag.getCompound("Items"));
        }
        ignited = tag.getBoolean("Ignited");
    }
}
