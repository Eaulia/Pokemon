"""
----------------------------------------------------
POKEMON.PY - Pokemons et Dresseurs
~~~~~~~~~~~~~~~~~~~~~~
FAITS :
dans la classe Type
- Avoir 1 ou 2 types par Pokemon
- Type Electrique
dans la classe Pokemon
- afficher les types
- calculer les degats reçus
dans la classe Dresseur
- Ajouter un pokemon 
- Ajouter et retirer un objet 
- Afficher l'inventaire
~~~~~~~~~~~~~~~~~~~~~~
A CONTINUER : 
dans la classe Pokemon
- Differentes attaques des pokemons 
- Ajouter les autres types (Normal, Feu, Eau, Herbe)
- Creer les erreurs
- Utilisation des objets 
- Systeme de PV avec variables privées
~~~~~~~~~~~~~~~~~~~~~~
COMMENTAIRES :
----------------------------------------------------
"""

from exceptions import *

# Chaque points faibles et forts pour chaque type de pokemon selon le lore
types_pokemon = {
    "Feu": {
        "faiblesse": ["Eau", "Sol", "Roche"],
        "resistance": ["Feu", "Plante", "Glace", "Insecte", "Acier"]
    },
    "Eau": {
        "faiblesse": ["Plante", "Électrik"],
        "resistance": ["Feu", "Eau", "Glace"]
    },
    "Plante": {
        "faiblesse": ["Feu", "Glace", "Poison", "Vol", "Insecte"],
        "resistance": ["Eau", "Plante", "Sol", "Roche"]
    },
    "Électrik": {
        "faiblesse": ["Sol"],
        "resistance": ["Électrik", "Vol", "Acier"]
    },
    "Vol": {
        "faiblesse": ["Électrik", "Glace", "Roche"],
        "resistance": ["Plante", "Combat", "Insecte"]
    },
    "Sol": {
        "faiblesse": ["Eau", "Plante", "Glace"],
        "resistance": ["Poison", "Roche"]
    },
    "Roche": {
        "faiblesse": ["Eau", "Plante", "Combat", "Sol", "Acier"],
        "resistance": ["Feu", "Poison", "Normal", "Vol"]
    }
}

class Type:
    def __init__(self, nom:str, faiblesse = None, resistance = None):
        self.nom = nom
        self.faiblesse = faiblesse
        self.resistance = resistance

#que regarder la cote "defender"
#mettre dans faiblesse si marqué 2
#dans resistance si marqué 1/2 (cf energie.png)
type_electrique = Type("Electrique", faiblesse=[], resistance=["Electrique"])

class Pokemon:
    def __init__(self, nom:str, pv_max:int, type1, type2 = None):
        self.nom = nom
        self.__pv = pv_max # pv actuels du pokemon
        self.__pv_max = pv_max
        if pv_max <= 0:
            raise PVInvalideError("Les PV max doivent être supérieurs à 0, faut vrm etre con pour mettre un pv négatif ou nul a son propre pokemon!")
        
        self.types = [type1]
        if type2:
            self.types.append(type2)

        self.statisque = []
        self.attaque = []

    # getter et setter pour les attr privés
    def get_pv(self):
        return self.__pv

    def get_pv_max(self):
        return self.__pv_max

    def set_pv(self, value):
        """ setter avec gestion d'erreur pour respecter les bornes pv min et max """
        if value > self.__pv_max:
            raise PVInvalideError("Les PV doivent être compris entre 0 et le PV max du pokemon")
        if value < 0:
            self.__pv = 0
        else:
            self.__pv = value

    def est_ko(self):
        return self.__pv <=0  # pas besoin de condition

    def afficher_types(self):
        """ affiche les types du pokemon """
        liste = [t.nom for t in self.types]
        return f'les types de {self.nom} sont : {liste}'

    def nb_degats_recus(self, type_attaquant) -> float :
        """ calcule les degats recus en prenant compte du type de l'attaquant """
        multiplicateur = 1.0
        for t in self.types:
            if type_attaquant in t.faiblesse:
                multiplicateur *= 1.4
            elif type_attaquant in t.resistance:
                multiplicateur *= 0.8
        return multiplicateur

    def est_faible_contre(self, pokemon):
        """ retourne True si le pokemon est faible contre l'autre pokemon et false si rien """
        if types_pokemon.get(self.types[0].nom, {}).get("faiblesse"):
            if pokemon.types[0].nom in types_pokemon[self.types[0].nom]["faiblesse"]:
                return True
        return False

    def est_resistant_contre(self, pokemon):
        """ retourne True si le pokemon est resistant contre l'autre pokemon et false si rien """
        if types_pokemon.get(self.types[0].nom, {}).get("resistance"):
            if pokemon.types[0].nom in types_pokemon[self.types[0].nom]["resistance"]:
                return True
        return False

    def prendre_degats(self, value):
        if self.est_ko():
            raise PokemonKOError(f"{self.nom} est ko et ne peut pas prendre de dégats.")
        # si value est négatif alors on peut ajouter des pv au pokemon au lieu de faire prendre du dégat
        if value < 0:
            value *= -1

        self.set_pv(self.get_pv() - value)  # utilisation du getter pas necessaire ici mais plus propre

    def soigner(self, value):
            if self.est_ko():
                raise PokemonKOError(f"{self.nom} est ko et ne peut pas etre soigné.")
            # si value est négatif alors on peut ajouter des pv au pokemon au lieu de faire prendre du dégat
            if value < 0:
                value *= -1

            # si le heal dépasse les pv max alors on le met a toutes ses vies
            if self.get_pv() + value > self.get_pv_max():
                self.set_pv(self.get_pv_max())
            else:
                self.set_pv(self.get_pv() + value)

class Dresseur:
    def __init__(self, nom:str="Dresseur"):
        self.nom = nom
        self.pokemon = []
        self.objet = []
        self.pokemon_actif = None

    def ajouter_pokemon(self, pokemon:Pokemon):
        """ ajoute pokemon et limite nombre de pokemon à 3 """
        if len(self.pokemon) < 3:
            self.pokemon.append(pokemon)
        else:
            print("tu ne peux pas avoir plus de pokemon :/")

    def retirer_pokemon(self, pokemon:str):
        """ retire pokemon """
        self.pokemon.remove(pokemon)
        return f'{pokemon} a été retiré'

    def ajouter_objet(self, objet):
        """ ajoute objet """
        self.objet.append(objet)
        return f'{objet} a été ajouté'

    def retirer_objet(self, objet):
        """ retire objet """
        self.objet.remove(objet)
        return f'{objet} a été retiré'

    def afficher_inventaire(self):
        """ affiche inventaire """
        return f'INVENTAIRE : {self.objet}'

    def afficher_pokemons(self):
        """ affiche les pokemons """
        res = 1
        for pokemon in self.pokemon:
            print(f"{res}) {pokemon}")  # sous la forme : 1) Pikachu    2) Ronflex
            res += 1

# exemple d'utilisation pour obtenir le type d'un pokemon 
Pokemon1 = Pokemon("Lixy", type_electrique)
print(Pokemon1.afficher_types())
print(Pokemon1.nb_degats_recus("Electrique"))

# exemple d'utilisation pour les objets 
dresseur = Dresseur()
print(dresseur.ajouter_objet("pomme"))
print(dresseur.afficher_inventaire())