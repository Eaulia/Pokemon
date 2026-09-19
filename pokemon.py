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
    def __init__(self, nom:str, type1, type2 = None):
        self.nom = nom
        self.types = [type1]
        if type2:
            self.types.append(type2)
        self.statisque = []
        self.attaque = []

    def afficher_types(self):
        """ affiche les types du pokemon """
        liste = [t.nom for t in self.types]
        return f'les types de {self.nom} sont : {liste}'

    def nb_degats_recus(self, type_attaquant) -> float :
        """ calcule les degats recus en prenant compte du type de l'attaquant """
        multiplicateur = 1.0
        for t in self.types:
            if type_attaquant in t.faiblesse:
                multiplicateur *= 2.0
            elif type_attaquant in t.resistance:
                multiplicateur *= 0.5
        return multiplicateur

class Dresseur:
    def __init__(self):
        self.pokemon = []
        self.objet = []

    def ajouter_pokemon(self, pokemon:str):
        """ ajoute pokemon et limite nombre de pokemon à 3 """
        if len(self.pokemon) < 3:
            self.pokemon.append(pokemon)
        else:
            return "tu ne peux pas avoir plus de pokemon :/"

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

# exemple d'utilisation pour obtenir le type d'un pokemon 
Pokemon1 = Pokemon("Lixy", type_electrique)
print(Pokemon1.afficher_types())
print(Pokemon1.nb_degats_recus("Electrique"))

# exemple d'utilisation pour les objets 
dresseur = Dresseur()
print(dresseur.ajouter_objet("pomme"))
print(dresseur.afficher_inventaire())