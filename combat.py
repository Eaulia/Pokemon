"""
----------------------------------------------------
COMBAT.PY - Combat et Logique de combat
~~~~~~~~~~~~~~~~~~~~~~
A CONTINUER : 
dans la classe Combat
- Systeme d'attaques etc
~~~~~~~~~~~~~~~~~~~~~~
COMMENTAIRES :
j'utilise "#CHANGER" pour dire que cette donnée est temporaire et sera à modifier
----------------------------------------------------
"""
import random
from pokemon import Dresseur, Lixy, Pikachu, pokemondispo
from exceptions import PokemonInexistantError


class Combat:
    """ Combat 1v1 entre 2 dresseurs - type tour par tour """
    def __init__(self, dresseur1: Dresseur, dresseur2: Dresseur):
        self.dresseur1:Dresseur = dresseur1
        self.dresseur2:Dresseur = dresseur2
        self.dresseur_actif: None | Dresseur = None
        self.dresseur_suivant: None | Dresseur = None
        self.tour:int = 0

    def modifier_inventaire_pokemon(self, dresseur, pokemon=None):
        """modifier l'inventaire en boucle"""
        print(f"\n-- Inventaire de {dresseur.nom}--")
        choix = input(f"\n1) Ajouter un pokemon\n2) Retirer un pokemon\n3) Afficher l'inventaire\n\n-> ")
        if choix == "1":
            pokemon = input("Quel pokemon voulez-vous ajouter ? ")
            if pokemon not in pokemondispo:
                raise PokemonInexistantError("ce pokemon n'est pas disponible, vérifiez le nom ou ajoutez-le")
            dresseur.ajouter_pokemon(pokemon)
        elif choix == "2":
            pokemon = input("Quel pokemon voulez-vous retirer ? ")
            dresseur.retirer_pokemon(pokemon)
        elif choix == "3":
            print(f"\nInventaire de {dresseur.nom} : {dresseur.pokemon}")

        print(f"\nTu veux continuer à modifier l'inventaire ?")
        choixcontinuer= input("\n1) Oui\n2) Non\n\n-> ")
        if choixcontinuer == "1":
            self.modifier_inventaire_pokemon(dresseur, pokemon)
        else:
            return

    def lancer_combat(self):
        if self.dresseur1.pokemon is None:
            print(f"{self.dresseur1.nom} n'a pas de pokemon pour combattre.")
        if self.dresseur2.pokemon is None:
            print(f"{self.dresseur2.nom} n'a pas de pokemon pour combattre.")

        """ determine l'ordre des dresseurs pour le lancement du combat """
        premier_dresseur = random.choice([self.dresseur1, self.dresseur2])
        deuxieme_dresseur = self.dresseur1 if premier_dresseur == self.dresseur2 else self.dresseur2
        self.dresseur_actif = premier_dresseur  # dresseur actif pour le tour
        self.dresseur_suivant = deuxieme_dresseur   # joue au prochain tour

        """ Chaque dresseur doit avoir un pokemon actif avant de commencer le combat """
        if self.dresseur_actif.pokemon_actif is None:
            print(f"{self.dresseur_actif.nom} n'a pas de pokemon actif pour combattre.")
            print(f"-- Pokemons de {self.dresseur_actif.nom} --")
            for i, pkm in enumerate(self.dresseur_actif.pokemon, 1):
                print(f"{i}) {pkm}")
            choisir_pokemon = int(input(f"choisissez un pokemon (avec son numéro attribué) parmi vos pokemons"))
            self.dresseur_actif.pokemon_actif = self.dresseur_actif.pokemon[choisir_pokemon -1]    # -1 pour l'index de la liste

        if self.dresseur_suivant.pokemon_actif is None:
            print(f"{self.dresseur_suivant.nom} n'a pas de pokemon actif pour combattre.")
            print(f"-- Pokemons de {self.dresseur_suivant.nom} --")
            for i, pkm in enumerate(self.dresseur_suivant.pokemon, 1):
                print(f"{i}) {pkm}")
            choisir_pokemon2 = int(input(f"choisissez un pokemon (avec son numéro attribué) parmi vos pokemons"))
            self.dresseur_suivant.pokemon_actif = self.dresseur_suivant.pokemon[choisir_pokemon2 - 1]    # -1 pour l'index de la liste

    def gestion_tour(self):
        """ gere le gameplay d'un tour pendant un combat """
        print(self.dresseur_actif, self.dresseur_suivant)
        if self.dresseur_actif is None or self.dresseur_suivant is None:
            print(" Aucun combat actif ")
            return
            
        choix = input(f"\n{self.dresseur_actif.nom}\n\n1) Attaquer\n2) Utiliser un objet\n3) Changer de pokemon\n\n-> ")
        if choix == "1":
            print(f"{self.dresseur_actif.nom} attaque {self.dresseur_suivant.nom} avec son {self.dresseur_actif.pokemon_actif} !")

        if choix == "2":
            pass

        if choix == "3":
            print(f"-- {self.dresseur_actif.nom} --")
            choisir_pokemon = int(input(f"choisissez un pokemon (avec son numéro attribué) parmi vos pokemons :\n->"))
            print(self.dresseur_actif.afficher_pokemons)
            self.dresseur_actif.pokemon_actif = self.dresseur_actif.pokemon[choisir_pokemon - 1]

a = Combat(Dresseur("Sacha"), Dresseur("Ondine"))
a.dresseur1.ajouter_pokemon(Lixy)
a.dresseur2.ajouter_pokemon(Pikachu)
#a.modifier_inventaire_pokemon(a.dresseur1, Lixy)
#a.modifier_inventaire_pokemon(a.dresseur2)
a.lancer_combat()