package fr.derniermoteur.client;

import fr.derniermoteur.DernierMoteur;
import net.minecraft.client.model.IronGolemModel;
import net.minecraft.client.renderer.RenderType;
import net.minecraft.client.renderer.entity.RenderLayerParent;
import net.minecraft.client.renderer.entity.layers.EyesLayer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.animal.IronGolem;

/** Yeux et cœur de poitrine du Gardien, rendus en pleine lumière (visibles dans le noir). */
public class CoreGuardianGlowLayer extends EyesLayer<IronGolem, IronGolemModel<IronGolem>> {
    private static final RenderType GLOW = RenderType.eyes(
            ResourceLocation.fromNamespaceAndPath(DernierMoteur.MODID, "textures/entity/core_guardian_glow.png"));

    public CoreGuardianGlowLayer(RenderLayerParent<IronGolem, IronGolemModel<IronGolem>> parent) {
        super(parent);
    }

    @Override
    public RenderType renderType() {
        return GLOW;
    }
}
