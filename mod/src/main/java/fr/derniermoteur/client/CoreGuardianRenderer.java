package fr.derniermoteur.client;

import com.mojang.blaze3d.vertex.PoseStack;
import fr.derniermoteur.DernierMoteur;
import net.minecraft.client.renderer.entity.EntityRendererProvider;
import net.minecraft.client.renderer.entity.IronGolemRenderer;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.entity.animal.IronGolem;

/** Modèle du golem de fer, texture d'alliage noirci, échelle ×2. */
public class CoreGuardianRenderer extends IronGolemRenderer {
    private static final ResourceLocation TEXTURE =
            ResourceLocation.fromNamespaceAndPath(DernierMoteur.MODID, "textures/entity/core_guardian.png");

    public CoreGuardianRenderer(EntityRendererProvider.Context ctx) {
        super(ctx);
        this.shadowRadius = 1.4f;
    }

    @Override
    public ResourceLocation getTextureLocation(IronGolem entity) {
        return TEXTURE;
    }

    @Override
    protected void scale(IronGolem entity, PoseStack pose, float partialTick) {
        pose.scale(2.0f, 2.0f, 2.0f);
    }
}
