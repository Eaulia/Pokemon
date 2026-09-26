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
from pokemon import Dresseur


class Combat:
    """ Combat 1v1 entre 2 dresseurs - type tour par tour """
    def __init__(self, dresseur1, dresseur2):
        self.dresseur1 = dresseur1
        self.dresseur2 = dresseur2
        self.dresseur_actif:Dresseur = None
        self.dresseur_suivant:Dresseur = None
        self.tour = 0

    def modifier_inventaire_pokemon(self, dresseur, pokemon):
        choix = input(f"\n1) Ajouter un pokemon\n2) Retirer un pokemon\n3) Afficher l'inventaire\n\n-> ")
        if choix == "1":
            pokemon = input("Quel pokemon voulez-vous ajouter ? ")
            dresseur.ajouter_pokemon(pokemon)
        elif choix == "2":
            pokemon = input("Quel pokemon voulez-vous retirer ? ")
            dresseur.retirer_pokemon(pokemon)
        elif choix == "3":
            print(f"\nInventaire de {dresseur.nom} : {dresseur.pokemon}")

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
            choisir_pokemon = input(f"{self.dresseur_actif.nom}, choisissez un pokemon (avec son numéro attribué) parmi vos pokemons :\n\n {self.dresseur_actif.ajouter_pokemon()}\n\n->")
            self.dresseur_actif.pokemon_actif = self.dresseur_actif.pokemon[choisir_pokemon - 1]    # -1 pour l'index de la liste

        if self.dresseur_suivant.pokemon_actif is None:
                print(f"{self.dresseur_suivant.nom} n'a pas de pokemon actif pour combattre.")
                choisir_pokemon2 = input(f"{self.dresseur_suivant.nom}, choisissez un pokemon (avec son numéro attribué) parmi vos pokemons :\n\n {self.dresseur_suivant.ajouter_pokemon()}\n\n->")
                self.dresseur_suivant.pokemon_actif = self.dresseur_suivant.pokemon[choisir_pokemon2 - 1]    # -1 pour l'index de la liste

    def gestion_tour(self):
        """ gere le gameplay d'un tour pendant un combat """
        if self.dresseur_actif.pokemon is None:
            print(" Aucun combat actif ")
            
        choix = input(f"\n{self.dresseur_actif.nom}\n\n1) Attaquer\n2) Utiliser un objet\n3) Changer de pokemon\n\n-> ")
        if choix == "1":
            print(f"{self.dresseur_actif.nom} attaque {self.dresseur_suivant.nom} avec son {self.dresseur_actif.pokemon_actif} !")

        if choix == "2":
            pass

        if choix == "3":
            choisir_pokemon = input(f"{self.dresseur_actif.nom}, choisissez un pokemon (avec son numéro attribué) parmi vos pokemons :\n\n {self.dresseur_actif.ajouter_pokemon()}\n\n->")
            self.dresseur_actif.pokemon_actif = self.dresseur_actif.pokemon[choisir_pokemon - 1]

a = Combat(Dresseur("Sacha"), Dresseur("Ondine"))
a.modifier_inventaire_pokemon(a.dresseur1, "Pikachu")