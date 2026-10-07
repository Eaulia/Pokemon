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
- Differentes attaques des pokemons 
dans la classe Dresseur
- Ajouter un pokemon 
- Ajouter et retirer un objet 
- Afficher l'inventaire
~~~~~~~~~~~~~~~~~~~~~~
A CONTINUER : 
dans la classe Pokemon
- Utilisation des objets 
- Systeme de PV avec variables privées
- niveau, hp qui augmente 
- empoisonnement 
- heritage pour les objets par exemple
- Systeme niveau
- Competences acquerissables selon le nv
- Pourcentage de reussite pour les competences
- evolution par pierre d'evo (boutique ou fin ce combat) ou par niveau
- Systeme de soin avec potions →> consomme 1 tour
- EV IV (cf. pokepedia)
- Menu de depart
~~~~~~~~~~~~~~~~~~~~~~
COMMENTAIRES :
: str | None signifie que la variable peut etre un str ou un None
----------------------------------------------------
"""

from exceptions import *

class Type:
    def __init__(self, nom:str, faiblesse : list | None = None, resistance : list | None = None):
        self.nom = nom
        self.faiblesse = faiblesse
        self.resistance = resistance

#que regarder la cote "defender"
#mettre dans faiblesse si marqué 2
#dans resistance si marqué 1/2 (cf energie.png)
# Chaque points faibles et forts pour chaque type de pokemon selon le lore
type_normal = Type("Normal", faiblesse=[], resistance=[])
type_feu = Type("Feu", faiblesse=["Eau", "Sol", "Roche"], resistance=["Feu", "Plante", "Glace", "Insecte", "Acier"])
type_eau = Type("Eau", faiblesse=["Plante", "Électrik"], resistance=["Feu", "Eau", "Glace"])
type_plante = Type("Plante", faiblesse=["Feu", "Glace", "Poison", "Vol", "Insecte"], resistance=["Eau", "Plante", "Sol", "Roche"])
type_electrik = Type("Électrik", faiblesse=["Sol"], resistance=["Électrik", "Vol", "Acier"])
type_vol = Type("Vol", faiblesse=["Électrik", "Glace", "Roche"], resistance=["Plante", "Combat", "Insecte"])
type_sol = Type("Sol", faiblesse=["Eau", "Plante", "Glace"], resistance=["Poison", "Roche"])
type_roche = Type("Roche", faiblesse=["Eau", "Plante", "Combat", "Sol", "Acier"], resistance=["Feu", "Poison", "Normal", "Vol"])

class Pokemon:
    def __init__(self, nom:str, pv_max:int, atk1:str, dgt1:int, atk2:str, dgt2:int, type1, atksp = None, dgtsp = None, type2 = None, item = None):
        self.nom = nom
        self.__pv = pv_max # pv actuels du pokemon
        self.__pv_max = pv_max

        self.atk1 = atk1
        self.dgt1 = dgt1
        self.atk2 = atk2
        self.dgt2 = dgt2
        self.atksp = atksp
        self.dgtsp = dgtsp

        self.item = []

        if pv_max <= 0:
            raise PVInvalideError("Les PV max doivent être supérieurs à 0, faut vrm etre con pour mettre un pv négatif ou nul a son propre pokemon!")
        
        self.types = [type1]
        if type2:
            self.types.append(type2)

        self.statisque = []
        self.attaque = []

    def __repr__(self):
        return f"{self.nom} (PV: {self.get_pv()}/{self.get_pv_max()})"

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
        for t in self.types:
            if t.faiblesse and pokemon.types[0] in t.faiblesse:
                return True
        return False

    def est_resistant_contre(self, pokemon):
        """ retourne True si le pokemon est resistant contre l'autre pokemon et false si rien """
        for t in self.types:
            if t.resistance and pokemon.types[0].nom in t.resistance:
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

class PokemonAttaque(Pokemon):
    def __init__(self, nom: str, pv_max: int, atk1: str, dgt1: int, atk2: str, dgt2: int, type1, atksp=None, dgtsp=None, type2=None):
        super().__init__(nom, pv_max, atk1, dgt1, atk2, dgt2, type1, atksp, dgtsp, type2)
        

class Dresseur:
    def __init__(self, nom:str="Dresseur"):
        self.nom = nom
        self.pokemon = []
        self.objets = []
        self.pokemon_actif = None

    def tous_ko(self) -> bool:
        """True si toute l'equipe est KO"""
        if not self.pokemon:
            return True
        return all(pkm.est_ko() for pkm in self.pokemon)
    
    def ajouter_pokemon(self, pokemon:Pokemon, pokemon2:Pokemon|None = None, pokemon3:Pokemon|None = None):
        """ ajoute pokemon et limite nombre de pokemon à 3 """
        liste = [pokemon, pokemon2, pokemon3]
        for pkm in liste:
            if pkm is not None:
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
        self.objets.append(objet)
        return f'{objet} a été ajouté'

    def retirer_objet(self, objet):
        """ retire objet """
        self.objets.remove(objet)
        return f'{objet} a été retiré'

    def afficher_inventaire(self):
        """ affiche inventaire """
        return f'INVENTAIRE : {self.objets}'

    def afficher_pokemons(self):
        """ affiche les pokemons """
        if not self.pokemon:
            print("Aucun pokémon disponible.")
            return
        
        res = 1
        for pokemon in self.pokemon:
            print(f"{res}) {pokemon}")  # sous la forme : 1) Pikachu    2) Ronflex
            res += 1

    def afficher_objets(self):
        """ affiche les objets """
        if not self.objets:
            print("Aucun objet disponible.")
            return
        
        res = 1
        for objet in self.objets:
            print(f"{res}) {objet.nom}")
            res += 1

# exemple d'utilisation pour obtenir le type d'un pokemon 
Lixy = Pokemon("Lixy", 60, "atk simple", 10, "atk complexe", 30, type_electrik)
Pikachu = Pokemon("Pikachu", 40, "atk simple", 20, "atk complexe", 30, type_electrik)
Chinchidou = Pokemon("Chinchidou", 30, "atk simple", 20, "atk complexe", 30, type_normal)
pokemondispo = [Lixy, Pikachu, Chinchidou]