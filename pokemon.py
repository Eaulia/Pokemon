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

class Attaque:
    """ sous-classe, attaque qu'un Pokemon peut utiliser"""
    def __init__(self, nom: str, degats: int, type_attaque: Type, precision: int = 100):
        self.nom = nom
        self.degats = degats
        self.type_attaque = type_attaque  # Type de l'attaque (peut être différent du type du Pokémon)
        self.precision = precision  # Pourcentage de réussite (à 100 ne rate jms)


class Pokemon:
    def __init__(self, nom: str, pv_max: int, type1: Type, type2=None):
        self.nom = nom
        self.__pv = pv_max  # pv actuels du pokemon
        self.__pv_max = pv_max
        self.xp = 0
        self.niveau = 1

        self.attaques = []  # Liste d'objets Attaque (max 4)
        self.item = []

        if pv_max <= 0:
            raise PVInvalideError("Les PV max doivent être supérieurs à 0, faut vrmt etre con pour mettre un pv négatif ou nul a son propre pokemon!")

        self.types = [type1]
        if type2:
            self.types.append(type2)

        self.statisque = []


    def __repr__(self):
        return f"{self.nom} Nv.{self.niveau} (PV: {self.get_pv()}/{self.get_pv_max()})"

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

    def apprendre_attaque(self, attaque: Attaque):
        """ Permet au Pokémon d'apprendre une nouvelle attaque (max 4) """
        if len(self.attaques) >= 4:
            print(f"{self.nom} connaît déjà 4 attaques !")
            return False
        self.attaques.append(attaque)
        return True

    def oublier_attaque(self, index: int):
        """ Retire une attaque par son index (0-3) """
        if 0 <= index < len(self.attaques):
            attaque_oubliee = self.attaques.pop(index)
            return f"{self.nom} a oublié {attaque_oubliee.nom}"
        else:
            raise IndexError("Index d'attaque invalide")

    def afficher_attaques(self):
        """ Affiche toutes les attaques du Pokémon """
        if not self.attaques:
            return f"{self.nom} ne connaît aucune attaque !"

        resultat = f"\n-- Attaques de {self.nom} --\n"
        for i, atk in enumerate(self.attaques, 1):
            resultat += f"{i}) {atk.nom} ({atk.degats} dégâts, Type: {atk.type_attaque.nom})\n"
        return resultat

    def xp_requis_prochain_niveau(self) -> int:
        """ Calcule l'XP nécessaire pour atteindre le prochain niveau avec f(x) = (x² + 20x + 200) / 2 (fonction travaillée sur geogebra pour avoir un super simulateur de pokemon!) """
        x = self.niveau
        return int((x**2 + 20 * x + 200) / 2)

    def gagner_xp(self, xp: int):
        """ Ajoute de l'XP et gère la montée de niveau """
        self.xp += xp
        print(f"{self.nom} gagne {xp} XP !")

        # verifier si le Pokémon monte de niveau, max 10.
        while self.xp >= self.xp_requis_prochain_niveau() and self.niveau < 10:
            self.monter_niveau()

    def monter_niveau(self):
        """ Fait monter le Pokémon d'un niveau et augmente ses stats """
        if self.niveau >= 10:
            print(f"{self.nom} est déjà au niveau maximum (10) !")
            return

        # Consommer l'XP nécessaire
        self.xp -= self.xp_requis_prochain_niveau()
        self.niveau += 1

        # Calcul des nouvelles stats (+10% PV, +5% dégâts par niveau)
        ancien_pv_max = self.__pv_max
        nouveau_pv_max = int(self.pv_max_base * (1 + 0.10 * (self.niveau - 1)))

        # Augmenter les PV max et restaurer la différence
        difference_pv = nouveau_pv_max - ancien_pv_max
        self.__pv_max = nouveau_pv_max
        self.__pv += difference_pv  # Restaure les PV gagnés

        # Augmenter les dégâts de toutes les attaques (+5% par niveau)
        for attaque in self.attaques:
            if not hasattr(attaque, 'degats_base'):
                attaque.degats_base = attaque.degats  # Sauvegarder les dégâts de base
            attaque.degats = int(attaque.degats_base * (1 + 0.05 * (self.niveau - 1)))

        print(f"\n{self.nom} monte au niveau {self.niveau} !")
        print(f"PV max : {ancien_pv_max} → {self.__pv_max} (+{difference_pv})")
        if self.attaques:
            print(f"Dégâts des attaques augmentés de 5% !")

        # afficher l'XP restante
        if self.xp >= self.xp_requis_prochain_niveau() and self.niveau < 10:
            print(f"{self.nom} a encore assez d'XP pour monter !")

    def afficher_infos_niveau(self):
        """Affiche les informations de niveau et XP"""
        if self.niveau >= 10:
            return f"{self.nom} - Niveau {self.niveau} (MAX) - {self.get_pv()}/{self.get_pv_max()} PV"
        else:
            xp_requis = self.xp_requis_prochain_niveau()
            return f"{self.nom} - Niveau {self.niveau} - XP: {self.xp}/{xp_requis} - {self.get_pv()}/{self.get_pv_max()} PV"

        

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
# Attaques Normal
charge = Attaque("Charge", 40, type_normal, 100)
vive_attaque = Attaque("Vive-Attaque", 40, type_normal, 100)
griffe = Attaque("Griffe", 40, type_normal, 100)

# Attaques Électrik
eclair = Attaque("Éclair", 40, type_electrik, 100)
etincelle = Attaque("Étincelle", 65, type_electrik, 100)
tonnerre = Attaque("Tonnerre", 90, type_electrik, 70)
cage_eclair = Attaque("Cage-Éclair", 50, type_electrik, 90)

# Lixy (Électrik)
Lixy = Pokemon("Lixy", 60, type_electrik)
Lixy.apprendre_attaque(charge)
Lixy.apprendre_attaque(etincelle)
Lixy.apprendre_attaque(eclair)

# Pikachu (Électrik)
Pikachu = Pokemon("Pikachu", 40, type_electrik)
Pikachu.apprendre_attaque(eclair)
Pikachu.apprendre_attaque(vive_attaque)
Pikachu.apprendre_attaque(tonnerre)
Pikachu.apprendre_attaque(cage_eclair)

pokemondispo = [Lixy, Pikachu]