"""
----------------------------------------------------
COMBAT.PY - Combat et Logique de combat
~~~~~~~~~~~~~~~~~~~~~~
A CONTINUER : 
dans la classe Combat
- Dans gestion_tour(), le choix 2 sur les objets pas bien fait
~~~~~~~~~~~~~~~~~~~~~~
COMMENTAIRES :
j'utilise "#CHANGER" pour dire que cette donnée est temporaire et sera à modifier
----------------------------------------------------
"""
import random
from pokemon import Dresseur, Lixy, Pikachu, pokemondispo
from items import Fraise
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
            print(f'pokemons disponibles : {pokemondispo}')
            pokemon = input("Quel pokemon voulez-vous ajouter ? (Entrez le nom)\n\n-> ")
            if pokemon not in str(pokemondispo):
                raise PokemonInexistantError("ce pokemon n'est pas disponible, vérifiez le nom ou ajoutez-le")
            for pkm in pokemondispo:
                if str(pkm.nom) == pokemon:
                    dresseur.ajouter_pokemon(pkm)
            
        elif choix == "2":
            print(f'Pokemons de {dresseur.nom} : {dresseur.pokemon}')
            pokemon = input("Quel pokemon voulez-vous retirer ? (Entrez le nom)\n\n-> ")
            if pokemon not in str(dresseur.pokemon):
                raise PokemonInexistantError("tu n'as pas ce pokemon.. ):")
            for pkm in pokemondispo:
                if str(pkm.nom) == pokemon:
                    dresseur.retirer_pokemon(pkm)

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
            choisir_pokemon = int(input(f"choisissez un pokemon (avec son numéro attribué) parmi vos pokemons\n\n-> "))
            self.dresseur_actif.pokemon_actif = self.dresseur_actif.pokemon[choisir_pokemon -1]    # -1 pour l'index de la liste

        if self.dresseur_suivant.pokemon_actif is None:
            print(f"{self.dresseur_suivant.nom} n'a pas de pokemon actif pour combattre.")
            print(f"-- Pokemons de {self.dresseur_suivant.nom} --")
            for i, pkm in enumerate(self.dresseur_suivant.pokemon, 1):
                print(f"{i}) {pkm}")
            choisir_pokemon2 = int(input(f"choisissez un pokemon (avec son numéro attribué) parmi vos pokemons\n\n-> "))
            self.dresseur_suivant.pokemon_actif = self.dresseur_suivant.pokemon[choisir_pokemon2 - 1]    # -1 pour l'index de la liste

    def changer_tour(self):
        """alterne joueur actif et suivant"""
        self.dresseur_actif, self.dresseur_suivant = self.dresseur_suivant, self.dresseur_actif
        self.tour += 1

    def attaquer(self):
        """attaque le pokemon adverse"""
        if self.dresseur_actif is None or self.dresseur_suivant is None:
            print(" Aucun combat actif ")
            return
        
        pkm_attaquant = self.dresseur_actif.pokemon_actif
        pkm_defenseur = self.dresseur_suivant.pokemon_actif

        if pkm_attaquant is None or pkm_defenseur is None :
            print("pas de pokemon attaquant ou defenseur")
            return

        print(f"\n-- Attaques de {pkm_attaquant.nom} --")
        print(f"1) {pkm_attaquant.atk1} ({pkm_attaquant.dgt1} dégâts)")
        print(f"2) {pkm_attaquant.atk2} ({pkm_attaquant.dgt2} dégâts)")
        
        choix = input("Choisissez une attaque (1 ou 2) : ")
        if choix == "1":
            nom_atk, degats_base = pkm_attaquant.atk1, pkm_attaquant.dgt1
        else:
            nom_atk, degats_base = pkm_attaquant.atk2, pkm_attaquant.dgt2

        # Calcul du multiplicateur basé sur le type principal de l'attaquant
        type_atk = pkm_attaquant.types[0].nom
        mult = pkm_defenseur.nb_degats_recus(type_atk)
        degats_finaux = int(degats_base * mult)

        pkm_defenseur.prendre_degats(degats_finaux)
        print(f"\n{pkm_attaquant.nom} utilise {nom_atk} sur {pkm_defenseur.nom} !")
        if mult > 1.0:
            print("Wooooow t'es trop chaud !")
        elif mult < 1.0:
            print(random.choice(["Pas fou, pas fou...", "Keske tu fais ???", "T'es pas sauvable toi-", "mouais.."]))

        print(f"{self.dresseur_actif.nom} attaque {self.dresseur_suivant.nom} avec son {self.dresseur_actif.pokemon_actif} !")
        print(f"{pkm_defenseur.nom} subit {degats_finaux} dégâts. (PV : {pkm_defenseur.get_pv()}/{pkm_defenseur.get_pv_max()})")
        
    def gestion_tour(self):
        """ gere le gameplay d'un tour pendant un combat """
        
        if self.dresseur_actif is None or self.dresseur_suivant is None:
            print(" Aucun dresseur actif ")
            return

        pkm_actif = self.dresseur_actif.pokemon_actif
        pkm_adversaire = self.dresseur_suivant.pokemon_actif

        if pkm_actif is None or pkm_adversaire is None:
            print(" Aucun pokemon actif ")
            return

        print(f"\n\n======== TOUR {self.tour} =========")
        print(f"A {self.dresseur_actif.nom} de jouer")
        print(f"Pokémon actif : {pkm_actif.nom} ({pkm_actif.get_pv()}/{pkm_actif.get_pv_max()} PV)")
        print(f"Adversaire : {pkm_adversaire.nom} ({pkm_adversaire.get_pv()}/{pkm_adversaire.get_pv_max()} PV)")

        choix = input(f"\n1) Attaquer\n2) Utiliser un objet\n3) Changer de pokemon\n\n-> ")
        if choix == "1":
            self.attaquer()

        if choix == "2":
            if not self.dresseur_actif.objets:
                print("ouais, nan ton tour a servi à rien bahhaha")
            else:
                print(self.dresseur_actif.afficher_objets())
                choisir_item = int(input((f"Choisissez un objet (avec son numéro attribué) :\n\n->"))) - 1 #-1 pour l'index
                objet = self.dresseur_actif.objets[choisir_item]
                pkm_actif.soigner(20)
                self.dresseur_actif.retirer_objet(objet)
                print(f"Objet a été utilisé sur {self.dresseur_actif.pokemon_actif}")

            
        if choix == "3":
            choisir_pokemon = int(input(f"choisissez un pokemon (avec son numéro attribué) parmi vos pokemons :\n->"))
            print(self.dresseur_actif.afficher_pokemons())
            self.dresseur_actif.pokemon_actif = self.dresseur_actif.pokemon[choisir_pokemon - 1]

        if pkm_adversaire.est_ko():
            print(f"\n{pkm_adversaire.nom} est KO !")
            if self.dresseur_suivant.tous_ko():
                print(f"gg {self.dresseur_actif.nom} !")
                return False  # Arrête la boucle while
            else:
                # Force l'adversaire à choisir un autre Pokémon
                pass

        # 2. Alternance des dresseurs pour le tour suivant
        self.dresseur_actif, self.dresseur_suivant = self.dresseur_suivant, self.dresseur_actif
        self.tour += 1
        return True  # Maintient la boucle active