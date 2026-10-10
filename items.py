"""
----------------------------------------------------
ITEMS.PY - Combat et Logique de combat
~~~~~~~~~~~~~~~~~~~~~~
A CONTINUER : 
- items pour l'histoire tm/hm competences
~~~~~~~~~~~~~~~~~~~~~~
COMMENTAIRES :
- c'est pas du tout bien fait bahhaha
----------------------------------------------------
"""

from exceptions import *

class Items:
    def __init__(self, nom: str, description: str = "") -> None:
        self.nom = nom
        self.description = description

class ItemConsommable(Items):
    """Items qui disparaissent après utilisation"""
    def __init__(self, nom: str, description: str = "") -> None:
        super().__init__(nom, description)
        self.disponible = True

class ItemSoin(ItemConsommable):
    """Items qui soignent les PV"""
    def __init__(self, nom: str, qte_soin: int, description: str = "") -> None:
        super().__init__(nom, description)
        self.qte_soin = qte_soin

    def utiliser(self, pokemon):
        """Utilise l'item sur un Pokemon"""
        if pokemon.est_ko():
            print(f"{pokemon.nom} est KO et ne peut pas etre soigné avec cet objet")
            return False

        pv_avant = pokemon.get_pv()
        pokemon.soigner(self.qte_soin)
        pv_apres = pokemon.get_pv()
        pv_soignes = pv_apres - pv_avant

        print(f"{pokemon.nom} récupère {pv_soignes} PV grace à {self.nom} !")
        return True

class ItemRevive(ItemConsommable):
    """Items qui réaniment un Pokémon KO"""
    def __init__(self, nom: str, pourcent_pv: int, description: str = "") -> None:
        super().__init__(nom, description)
        self.pourcent_pv = pourcent_pv  # Pourcentage de PV restaurés

    def utiliser(self, pokemon):
        """Réanime un Pokémon KO"""
        if not pokemon.est_ko():
            print(f"{pokemon.nom} n'est pas KO !")
            return False

        pv_restaures = int(pokemon.get_pv_max() * self.pourcent_pv / 100)
        pokemon.set_pv(pv_restaures)
        print(f"{pokemon.nom} revient au combat avec {pv_restaures} PV !")
        return True

class ItemBoost(ItemConsommable):
    """Items qui boostent temporairement les stats"""
    def __init__(self, nom: str, type_boost: str, valeur: int, description: str = "") -> None:
        super().__init__(nom, description)
        self.type_boost = type_boost  # "attaque", "defense", etc.
        self.valeur = valeur



"""
class ItemPokeball(Items):
    #Capturer un pkm 
    def __init__(self, nom: str) -> None:
        super().__init__(nom)

class ItemEvolution(Items):
    def __init__(self, nom: str) -> None:
        super().__init__(nom)
"""
Fraise = ItemSoin("Fraise", 20)
# Potions
potion = ItemSoin("Potion", 20, "Restaure 20 PV")
super_potion = ItemSoin("Super Potion", 50, "Restaure 50 PV")
hyper_potion = ItemSoin("Hyper Potion", 100, "Restaure 100 PV")
potion_max = ItemSoin("Potion Max", 999, "Restaure tous les PV")

# Baies (heal)
baie_oran = ItemSoin("Baie Oran", 10, "Restaure 10 PV")
baie_sitrus = ItemSoin("Baie Sitrus", 30, "Restaure 30 PV")

# Items de réa
rappel = ItemRevive("Rappel", 50, "Réanime un Pokémon KO avec 50% PV")
rappel_max = ItemRevive("Rappel Max", 100, "Réanime un Pokémon KO avec tous ses PV")

# Tous les items disponibles
items_disponibles = [
    potion, super_potion, hyper_potion, potion_max,
    baie_oran, baie_sitrus,
    rappel, rappel_max
]