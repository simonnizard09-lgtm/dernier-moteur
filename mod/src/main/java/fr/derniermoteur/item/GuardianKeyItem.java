package fr.derniermoteur.item;

import fr.derniermoteur.ModRegistries;
import fr.derniermoteur.entity.CoreGuardian;
import net.minecraft.ChatFormatting;
import net.minecraft.core.BlockPos;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.world.InteractionResult;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.item.Item;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.TooltipFlag;
import net.minecraft.world.item.context.UseOnContext;
import net.minecraft.world.phys.AABB;

import java.util.List;

/** Clé du Gardien : clic droit sur le sol pour invoquer le Gardien du Noyau (consommée). */
public class GuardianKeyItem extends Item {
    public GuardianKeyItem(Properties props) {
        super(props);
    }

    @Override
    public InteractionResult useOn(UseOnContext ctx) {
        if (!(ctx.getLevel() instanceof ServerLevel level)) {
            return InteractionResult.SUCCESS;
        }
        Player player = ctx.getPlayer();
        BlockPos spawn = ctx.getClickedPos().relative(ctx.getClickedFace());
        // Un seul gardien à la fois dans les environs
        if (!level.getEntitiesOfClass(CoreGuardian.class, new AABB(spawn).inflate(64)).isEmpty()) {
            if (player != null) {
                player.displayClientMessage(Component.literal("Le Gardien du Noyau est déjà éveillé.")
                        .withStyle(ChatFormatting.RED), true);
            }
            return InteractionResult.FAIL;
        }
        CoreGuardian guardian = ModRegistries.CORE_GUARDIAN.get().create(level);
        if (guardian == null) {
            return InteractionResult.FAIL;
        }
        guardian.moveTo(spawn.getX() + 0.5, spawn.getY(), spawn.getZ() + 0.5, ctx.getRotation() + 180f, 0f);
        if (!level.noCollision(guardian)) {
            if (player != null) {
                player.displayClientMessage(Component.literal("Il faut plus de place : le Gardien est immense.")
                        .withStyle(ChatFormatting.RED), true);
            }
            return InteractionResult.FAIL;
        }
        level.addFreshEntity(guardian);
        level.sendParticles(ParticleTypes.EXPLOSION_EMITTER, guardian.getX(), guardian.getY() + 1, guardian.getZ(), 1, 0, 0, 0, 0);
        level.playSound(null, spawn, SoundEvents.WITHER_SPAWN, SoundSource.HOSTILE, 2f, 0.5f);
        level.getServer().getPlayerList().broadcastSystemMessage(
                Component.literal("« Montre-moi que tu mérites le Noyau. »").withStyle(ChatFormatting.GOLD, ChatFormatting.ITALIC), false);
        if (player != null && !player.getAbilities().instabuild) {
            ctx.getItemInHand().shrink(1);
        }
        return InteractionResult.CONSUME;
    }

    @Override
    public void appendHoverText(ItemStack stack, TooltipContext ctx, List<Component> tooltip, TooltipFlag flag) {
        tooltip.add(Component.translatable("item.dernier_moteur.guardian_key.desc").withStyle(ChatFormatting.GRAY, ChatFormatting.ITALIC));
    }
}
