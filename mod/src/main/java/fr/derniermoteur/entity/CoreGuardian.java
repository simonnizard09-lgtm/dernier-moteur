package fr.derniermoteur.entity;

import net.minecraft.ChatFormatting;
import net.minecraft.core.particles.ParticleTypes;
import net.minecraft.nbt.CompoundTag;
import net.minecraft.network.chat.Component;
import net.minecraft.server.level.ServerBossEvent;
import net.minecraft.server.level.ServerLevel;
import net.minecraft.server.level.ServerPlayer;
import net.minecraft.sounds.SoundEvents;
import net.minecraft.sounds.SoundSource;
import net.minecraft.util.Mth;
import net.minecraft.world.BossEvent;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.effect.MobEffectInstance;
import net.minecraft.world.effect.MobEffects;
import net.minecraft.world.entity.EntityType;
import net.minecraft.world.entity.EquipmentSlot;
import net.minecraft.world.entity.LivingEntity;
import net.minecraft.world.entity.ai.attributes.AttributeSupplier;
import net.minecraft.world.entity.ai.attributes.Attributes;
import net.minecraft.world.entity.ai.goal.FloatGoal;
import net.minecraft.world.entity.ai.goal.LookAtPlayerGoal;
import net.minecraft.world.entity.ai.goal.MeleeAttackGoal;
import net.minecraft.world.entity.ai.goal.RandomLookAroundGoal;
import net.minecraft.world.entity.ai.goal.WaterAvoidingRandomStrollGoal;
import net.minecraft.world.entity.ai.goal.target.HurtByTargetGoal;
import net.minecraft.world.entity.ai.goal.target.NearestAttackableTargetGoal;
import net.minecraft.world.entity.animal.IronGolem;
import net.minecraft.world.entity.monster.Enemy;
import net.minecraft.world.entity.monster.Vex;
import net.minecraft.world.entity.player.Player;
import net.minecraft.world.entity.projectile.SmallFireball;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.minecraft.world.level.Level;
import net.minecraft.world.phys.AABB;
import net.minecraft.world.phys.Vec3;

/**
 * Le Gardien du Noyau : un golem d'alliage noirci, deux fois plus grand qu'un golem de fer.
 * Il réutilise le modèle et les animations du golem de fer (rendu dans {@code CoreGuardianRenderer}).
 *
 * <p>Trois phases selon ses points de vie :</p>
 * <ol>
 *   <li>&gt; 66 % — mêlée pure (projections du golem de fer) ;</li>
 *   <li>33–66 % — salves de boules de feu et invocation de serviteurs (vex) ;</li>
 *   <li>&lt; 33 % — rage : plus rapide, plus fort, ondes de choc au sol et salves plus fréquentes.</li>
 * </ol>
 */
public class CoreGuardian extends IronGolem implements Enemy {
    private static final int MAX_MINIONS = 4;

    private final ServerBossEvent bossEvent = (ServerBossEvent) new ServerBossEvent(
            Component.literal("Le Gardien du Noyau").withStyle(ChatFormatting.GOLD),
            BossEvent.BossBarColor.YELLOW, BossEvent.BossBarOverlay.NOTCHED_10)
            .setDarkenScreen(true);

    private int phase = 1;
    private int volleyCooldown = 80;
    private int summonCooldown = 200;
    private int shockwaveCooldown = 120;

    public CoreGuardian(EntityType<? extends IronGolem> type, Level level) {
        super(type, level);
        this.xpReward = 500;
        this.setPlayerCreated(false);
        this.setPersistenceRequired();
    }

    public static AttributeSupplier.Builder createAttributes() {
        return IronGolem.createAttributes()
                .add(Attributes.MAX_HEALTH, 600.0)
                .add(Attributes.MOVEMENT_SPEED, 0.27)
                .add(Attributes.KNOCKBACK_RESISTANCE, 1.0)
                .add(Attributes.ATTACK_DAMAGE, 20.0)
                .add(Attributes.ARMOR, 16.0)
                .add(Attributes.ARMOR_TOUGHNESS, 6.0)
                .add(Attributes.FOLLOW_RANGE, 48.0)
                .add(Attributes.STEP_HEIGHT, 1.5);
    }

    @Override
    protected void registerGoals() {
        this.goalSelector.addGoal(0, new FloatGoal(this));
        this.goalSelector.addGoal(1, new MeleeAttackGoal(this, 1.0, true));
        this.goalSelector.addGoal(6, new WaterAvoidingRandomStrollGoal(this, 0.6));
        this.goalSelector.addGoal(7, new LookAtPlayerGoal(this, Player.class, 16.0f));
        this.goalSelector.addGoal(8, new RandomLookAroundGoal(this));
        this.targetSelector.addGoal(1, new HurtByTargetGoal(this));
        this.targetSelector.addGoal(2, new NearestAttackableTargetGoal<>(this, Player.class, false));
    }

    @Override
    public boolean canAttackType(EntityType<?> type) {
        return true;
    }

    @Override
    public boolean removeWhenFarAway(double distance) {
        return false;
    }

    @Override
    public boolean causeFallDamage(float distance, float multiplier, DamageSource source) {
        return false;
    }

    // ------------------------------------------------------------------ phases

    @Override
    protected void customServerAiStep() {
        super.customServerAiStep();
        float ratio = getHealth() / getMaxHealth();
        bossEvent.setProgress(ratio);

        int newPhase = ratio > 0.66f ? 1 : ratio > 0.33f ? 2 : 3;
        if (newPhase > phase) {
            enterPhase(newPhase);
        }

        LivingEntity target = getTarget();
        if (target == null || !target.isAlive()) {
            return;
        }
        if (phase >= 2 && --volleyCooldown <= 0) {
            fireVolley(target);
            volleyCooldown = phase == 3 ? 50 : 90;
        }
        if (phase >= 2 && --summonCooldown <= 0) {
            summonMinions();
            summonCooldown = phase == 3 ? 260 : 360;
        }
        if (phase == 3 && --shockwaveCooldown <= 0) {
            shockwave();
            shockwaveCooldown = 140;
        }
    }

    private void enterPhase(int newPhase) {
        phase = newPhase;
        ServerLevel server = (ServerLevel) level();
        if (phase == 2) {
            bossEvent.setColor(BossEvent.BossBarColor.RED);
            announce("Le Gardien ouvre ses soupapes. Des flammes jaillissent de ses flancs !");
            server.playSound(null, blockPosition(), SoundEvents.BLAZE_SHOOT, SoundSource.HOSTILE, 3f, 0.5f);
            summonCooldown = 20;
        } else if (phase == 3) {
            bossEvent.setColor(BossEvent.BossBarColor.PURPLE);
            announce("Le Gardien ne retient plus rien. Le sol tremble.");
            addEffect(new MobEffectInstance(MobEffects.MOVEMENT_SPEED, Integer.MAX_VALUE, 1, false, false));
            addEffect(new MobEffectInstance(MobEffects.DAMAGE_BOOST, Integer.MAX_VALUE, 1, false, false));
            server.playSound(null, blockPosition(), SoundEvents.WITHER_SPAWN, SoundSource.HOSTILE, 3f, 0.6f);
        }
        server.sendParticles(ParticleTypes.EXPLOSION_EMITTER, getX(), getY() + 2, getZ(), 2, 0.5, 0.5, 0.5, 0);
    }

    private void announce(String text) {
        Component msg = Component.literal(text).withStyle(ChatFormatting.GOLD, ChatFormatting.ITALIC);
        for (ServerPlayer p : bossEvent.getPlayers()) {
            p.sendSystemMessage(msg);
        }
    }

    private void fireVolley(LivingEntity target) {
        int shots = phase == 3 ? 5 : 3;
        Vec3 origin = new Vec3(getX(), getY() + getBbHeight() * 0.75, getZ());
        for (int i = 0; i < shots; i++) {
            Vec3 dir = new Vec3(target.getX() - origin.x, target.getY(0.5) - origin.y, target.getZ() - origin.z)
                    .normalize()
                    .add(getRandom().triangle(0, 0.12), getRandom().triangle(0, 0.08), getRandom().triangle(0, 0.12));
            SmallFireball ball = new SmallFireball(level(), this, dir.normalize());
            ball.setPos(origin.x + dir.x * 1.5, origin.y, origin.z + dir.z * 1.5);
            level().addFreshEntity(ball);
        }
        level().playSound(null, blockPosition(), SoundEvents.BLAZE_SHOOT, SoundSource.HOSTILE, 2f, 0.7f);
    }

    private void summonMinions() {
        ServerLevel server = (ServerLevel) level();
        int existing = server.getEntitiesOfClass(Vex.class, getBoundingBox().inflate(32), v -> v.getOwner() == this).size();
        int toSpawn = Math.min(2, MAX_MINIONS - existing);
        for (int i = 0; i < toSpawn; i++) {
            Vex vex = EntityType.VEX.create(server);
            if (vex == null) {
                continue;
            }
            double angle = getRandom().nextDouble() * Math.PI * 2;
            vex.moveTo(getX() + Math.cos(angle) * 3, getY() + 3, getZ() + Math.sin(angle) * 3, getYRot(), 0);
            vex.setOwner(this);
            vex.setLimitedLife(20 * 40);
            vex.setItemSlot(EquipmentSlot.MAINHAND, new ItemStack(Items.IRON_SWORD));
            vex.setDropChance(EquipmentSlot.MAINHAND, 0f);
            if (getTarget() != null) {
                vex.setTarget(getTarget());
            }
            server.addFreshEntity(vex);
            server.sendParticles(ParticleTypes.SOUL_FIRE_FLAME, vex.getX(), vex.getY(), vex.getZ(), 20, 0.3, 0.3, 0.3, 0.02);
        }
        if (toSpawn > 0) {
            server.playSound(null, blockPosition(), SoundEvents.EVOKER_PREPARE_SUMMON, SoundSource.HOSTILE, 2f, 0.6f);
        }
    }

    private void shockwave() {
        ServerLevel server = (ServerLevel) level();
        AABB area = getBoundingBox().inflate(8, 2, 8);
        for (Player p : server.getEntitiesOfClass(Player.class, area, pl -> !pl.isCreative() && !pl.isSpectator())) {
            if (!p.onGround()) {
                continue; // sauter au bon moment esquive l'onde
            }
            p.hurt(damageSources().mobAttack(this), 12.0f);
            Vec3 push = p.position().subtract(position()).normalize().scale(1.6);
            p.push(push.x, 0.6, push.z);
            p.hurtMarked = true;
        }
        for (int i = 0; i < 48; i++) {
            double a = i * Math.PI * 2 / 48;
            server.sendParticles(ParticleTypes.CAMPFIRE_COSY_SMOKE, getX() + Math.cos(a) * 6, getY() + 0.2,
                    getZ() + Math.sin(a) * 6, 1, 0, 0.05, 0, 0.01);
        }
        server.playSound(null, blockPosition(), SoundEvents.GENERIC_EXPLODE.value(), SoundSource.HOSTILE, 2.5f, 0.5f);
    }

    // ------------------------------------------------------------------ barre de boss

    @Override
    public void startSeenByPlayer(ServerPlayer player) {
        super.startSeenByPlayer(player);
        bossEvent.addPlayer(player);
    }

    @Override
    public void stopSeenByPlayer(ServerPlayer player) {
        super.stopSeenByPlayer(player);
        bossEvent.removePlayer(player);
    }

    @Override
    public void aiStep() {
        super.aiStep();
        if (level().isClientSide && phase >= 1 && tickCount % 4 == 0) {
            level().addParticle(ParticleTypes.SMALL_FLAME, getRandomX(0.6), getY() + getBbHeight() * Mth.nextFloat(getRandom(), 0.3f, 0.9f),
                    getRandomZ(0.6), 0, 0.02, 0);
        }
    }

    // ------------------------------------------------------------------ sauvegarde

    @Override
    public void addAdditionalSaveData(CompoundTag tag) {
        super.addAdditionalSaveData(tag);
        tag.putInt("GuardianPhase", phase);
    }

    @Override
    public void readAdditionalSaveData(CompoundTag tag) {
        super.readAdditionalSaveData(tag);
        phase = Math.max(1, tag.getInt("GuardianPhase"));
        if (hasCustomName()) {
            bossEvent.setName(getDisplayName());
        }
    }
}
