package fr.derniermoteur;

import fr.derniermoteur.block.EngineCoreBlockEntity;
import fr.derniermoteur.entity.CoreGuardian;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.fml.common.Mod;
import net.neoforged.neoforge.capabilities.Capabilities;
import net.neoforged.neoforge.capabilities.RegisterCapabilitiesEvent;
import net.neoforged.neoforge.event.entity.EntityAttributeCreationEvent;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * Le Dernier Moteur : contenu final du modpack.
 * <ul>
 *   <li>le boss « Gardien du Noyau » ({@link CoreGuardian}) invoqué avec la Clé du Gardien ;</li>
 *   <li>le Moteur, multibloc 5×5×5 piloté par {@link EngineCoreBlockEntity}.</li>
 * </ul>
 * Les fragments du Noyau et les processeurs sont des items KubeJS du pack (même namespace) :
 * ils sont résolus par identifiant à l'exécution, le mod ne dépend donc pas de KubeJS.
 */
@Mod(DernierMoteur.MODID)
public class DernierMoteur {
    public static final String MODID = "dernier_moteur";
    public static final Logger LOGGER = LoggerFactory.getLogger(MODID);

    public DernierMoteur(IEventBus modBus) {
        ModRegistries.register(modBus);
        modBus.addListener(DernierMoteur::registerCapabilities);
        modBus.addListener(DernierMoteur::registerAttributes);
    }

    private static void registerCapabilities(RegisterCapabilitiesEvent event) {
        event.registerBlockEntity(Capabilities.EnergyStorage.BLOCK, ModRegistries.ENGINE_CORE_BE.get(),
                (be, side) -> be.getEnergy());
        event.registerBlockEntity(Capabilities.ItemHandler.BLOCK, ModRegistries.ENGINE_CORE_BE.get(),
                (be, side) -> be.getItems());
    }

    private static void registerAttributes(EntityAttributeCreationEvent event) {
        event.put(ModRegistries.CORE_GUARDIAN.get(), CoreGuardian.createAttributes().build());
    }
}
