"""
----------------------------------------------------
COMBAT.PY - Combat et Logique de combat
~~~~~~~~~~~~~~~~~~~~~~
A CONTINUER : 
dans la classe Combat
- mieux faire les calculs d'attaques ?
~~~~~~~~~~~~~~~~~~~~~~
COMMENTAIRES :
j'utilise "#CHANGER" pour dire que cette donnée est temporaire et sera à modifier
j'ai modif un peu pour les attaques mais en vrai jsais pas trop comment ça fonctionne dans le vrai jeu
----------------------------------------------------
"""
from __future__ import annotations

import random
from pokemon import Pokemon, Attaque, type_poison
from instances_pokemons import pokemondispo
from dresseur import Dresseur
from decoration import barre_de_vie, afficher_texte, afficher_cadre
from exceptions import PokemonInexistantError


def demander_nombre(prompt, mini, maxi):
    while True:
        reponse = input(prompt)
        if reponse.isdigit() and mini <= int(reponse) <= maxi:
            return int(reponse)
        print("Choix invalide")


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
        afficher_cadre(f"Equipe de {dresseur.nom}", ["1) Ajouter un pokemon", "2) Retirer un pokemon", "3) Afficher l'inventaire"])
        choix = demander_nombre("-> ", 1, 3)

        if choix == 1:
            afficher_texte("pokemons disponibles :")
            for pkm in pokemondispo:
                print(f'{pkm}')
            pokemon_nom = input("Quel pokemon voulez-vous ajouter ? (Entrez le nom)\n\n-> ").strip()
            pokemon_choisi = next(
                (pkm for pkm in pokemondispo if pkm.nom.casefold() == pokemon_nom.casefold()),
                None,
            )
            if pokemon_choisi is None:
                afficher_texte("ce pokemon n'est pas disponible, vérifiez le nom ou ajoutez-le")
                pokemon_nom = input("Quel pokemon voulez-vous ajouter ? (Entrez le nom)\n\n-> ").strip()
                pokemon_choisi = next((pkm for pkm in pokemondispo if pkm.nom.casefold() == pokemon_nom.casefold()),None)

            if pokemon_choisi is not None:
                dresseur.ajouter_pokemon(pokemon_choisi)
            else:
                afficher_texte("Toujours faux, abandonne l'ajoute plus mdrr.")
            
        elif choix == 2:
            afficher_texte(f'Pokemons de {dresseur.nom} : {dresseur.pokemon}')
            pokemon_nom = input("Quel pokemon voulez-vous retirer ? (Entrez le nom)\n\n-> ").strip()
            pokemon_choisi = next(
                (pkm for pkm in dresseur.pokemon if pkm.nom.casefold() == pokemon_nom.casefold()),
                None,
            )
            if pokemon_choisi is None:
                raise PokemonInexistantError("tu n'as pas ce pokemon.. ):")
            dresseur.retirer_pokemon(pokemon_choisi)

        elif choix == 3:
            if not dresseur.pokemon:
                afficher_texte(f"{dresseur.nom} n'a pas de pokemon dans son inventaire.")
            else:
                afficher_texte(f"\nInventaire de {dresseur.nom} : {dresseur.pokemon}")

        afficher_texte(f"\nTu veux continuer à modifier l'inventaire ?")
        choixcontinuer= input("\n1) Oui\n2) Non\n\n-> ")
        if choixcontinuer == "1":
            self.modifier_inventaire_pokemon(dresseur, pokemon)
        else:
            return

    def choisir_ordre(self, d1:Dresseur, d2:Dresseur):
        p1 = d1.pokemon_actif
        p2 = d2.pokemon_actif

        if p1 is None or p2 is None:
            return d1, d2
        
        if p1.vitesse >= p2.vitesse:
            return d1, d2
        else:
            return d2, d1
        
    def lancer_combat(self):
        if not self.dresseur1.pokemon:
            afficher_cadre(f"\n{self.dresseur1.nom} n'a pas de pokemon pour combattre.",[])
            modifier_inventaire = input(f"Voulez-vous modifier l'inventaire de {self.dresseur1.nom} ? (1) Oui / (2) Non\n\n-> ")
            if modifier_inventaire == "1":
                self.modifier_inventaire_pokemon(self.dresseur1, None)
        if not self.dresseur1.pokemon:
            afficher_texte(f"Combat annulé : {self.dresseur1.nom} n'a pas de pokemon.")
            return
        if not self.dresseur2.pokemon:
            afficher_texte(f"\n{self.dresseur2.nom} n'a pas de pokemon pour combattre.")
            modifier_inventaire = input(f"Voulez-vous modifier l'inventaire de {self.dresseur2.nom} ? (1) Oui / (2) Non\n\n-> ")
            if modifier_inventaire == "1":
                self.modifier_inventaire_pokemon(self.dresseur2, None)
        if not self.dresseur2.pokemon:
            afficher_texte(f"Combat annulé : {self.dresseur2.nom} n'a pas de pokemon.")
            return

        """ determine l'ordre des dresseurs pour le lancement du combat """
        premier_dresseur, deuxieme_dresseur = self.choisir_ordre(self.dresseur1, self.dresseur2)
        self.dresseur_actif = premier_dresseur  # dresseur actif pour le tour
        self.dresseur_suivant = deuxieme_dresseur   # joue au prochain tour

        if self.dresseur_actif.est_bot:
            self.dresseur_actif.pokemon_actif = self.dresseur_actif.pokemon[0]
        if self.dresseur_suivant.est_bot:
            self.dresseur_suivant.pokemon_actif = self.dresseur_suivant.pokemon[0]

        """ Chaque dresseur doit avoir un pokemon actif avant de commencer le combat """
        if self.dresseur_actif.pokemon_actif is None:
            lignes_pokemons = [f"{self.dresseur_actif.nom} n'a pas de pokémon actif."]
            lignes_pokemons.append("")
            
            for i, pkm in enumerate(self.dresseur_actif.pokemon, 1):
                lignes_pokemons.append(f"{i}) {pkm}")
            
            afficher_cadre(f"Pokemons de {self.dresseur_actif.nom}", lignes_pokemons)
            afficher_texte("choisissez un pokemon (avec son numéro attribué) parmi vos pokemons")
            choisir_pokemon = demander_nombre("-> ", 1, len(self.dresseur_actif.pokemon))
            self.dresseur_actif.pokemon_actif = self.dresseur_actif.pokemon[choisir_pokemon - 1]

        if self.dresseur_suivant.pokemon_actif is None:
            lignes_pokemons = [f"{self.dresseur_suivant.nom} n'a pas de pokémon actif."]
            lignes_pokemons.append("")
            
            for i, pkm in enumerate(self.dresseur_suivant.pokemon, 1):
                lignes_pokemons.append(f"{i}) {pkm}")

            afficher_cadre(f"Pokemons de {self.dresseur_suivant.nom}", lignes_pokemons)
            afficher_texte("choisissez un pokemon (avec son numéro attribué) parmi vos pokemons")
            choisir_pokemon2 = demander_nombre("-> ", 1, len(self.dresseur_suivant.pokemon))
            self.dresseur_suivant.pokemon_actif = self.dresseur_suivant.pokemon[choisir_pokemon2 - 1]

    def changer_tour(self):
        """alterne joueur actif et suivant"""
        self.dresseur_actif, self.dresseur_suivant = self.dresseur_suivant, self.dresseur_actif
        self.tour += 1

    def demander_remplacement(self, dresseur):
        if dresseur.est_bot:
            for i in range(len(dresseur.pokemon)):
                if not dresseur.pokemon[i].est_ko():
                    return i
        lignes_ko = []
        for i, pkm in enumerate(dresseur.pokemon, 1):
            statut_pkm = " (KO)" if pkm.est_ko() else f" ({pkm.get_pv()}/{pkm.get_pv_max()} PV)"
            lignes_ko.append(f"{i}) {pkm.nom} Nv.{pkm.niveau}{statut_pkm}")
        afficher_cadre(f"Remplacement - {dresseur.nom}", lignes_ko)
        while True:
            reponse = input("Quel Pokémon envoyer ? (numéro) -> ")
            if not reponse.isdigit() or not 1 <= int(reponse) <= len(dresseur.pokemon):
                print("Choix invalide")
            elif dresseur.pokemon[int(reponse) - 1].est_ko():
                print("ouais nan l'autre est mort")
            else:
                return int(reponse) - 1

    def calculer_degats(self, pkm_attaquant, pkm_defenseur, attaque):
        """Calcul du multiplicateur basé sur le type de l'attaque"""
        mult = pkm_defenseur.nb_degats_recus(attaque.type_attaque.nom)
        degats_de_base = (attaque.degats + (pkm_attaquant.niveau * 2)) / 5
        # faire /6 si les attaques sont tjr trop puissantes
        return int(degats_de_base * mult)

    def attaquer(self):
        """ gestion de l'attaque du pokemon adverse """

        degats_finaux = 0
        if self.dresseur_actif is None or self.dresseur_suivant is None:
            afficher_texte(" Aucun combat actif ")
            return

        pkm_attaquant:Pokemon|None = self.dresseur_actif.pokemon_actif
        pkm_defenseur:Pokemon|None = self.dresseur_suivant.pokemon_actif

        if pkm_attaquant is None or pkm_defenseur is None:
            afficher_texte("pas de pokemon attaquant ou defenseur")
            return

        # Vérifier que le Pokémon a des attaques
        if not pkm_attaquant.attaques:
            afficher_texte(f"{pkm_attaquant.nom} ne connaît aucune attaque !")
            return

        lignes_attaques = []
        for i, atk in enumerate(pkm_attaquant.attaques, 1):
            degats = self.calculer_degats(pkm_attaquant, pkm_defenseur, atk)
            lignes_attaques.append(f"{i}) {atk.nom} ({degats} dégâts, Type: {atk.type_attaque.nom})")

        # Affichage propre dans le cadre
        afficher_cadre(f"Attaques de {pkm_attaquant.nom}", lignes_attaques)

        if self.dresseur_actif.est_bot:
            # prend l'atq avec le plus de degats
            meilleure_attaque = 0
            degats_max = -1
            
            for i in range(len(pkm_attaquant.attaques)):
                attaque_actuelle = pkm_attaquant.attaques[i]
                degats = self.calculer_degats(pkm_attaquant, pkm_defenseur, attaque_actuelle)
                
                if degats > degats_max:
                    degats_max = degats
                    meilleure_attaque = i
    
            choix = meilleure_attaque
        else:
            choix = demander_nombre("Choisissez une attaque (numéro) -> ", 1, len(pkm_attaquant.attaques)) - 1

        if 0 <= choix < len(pkm_attaquant.attaques):
            attaque_choisie:Attaque|None = pkm_attaquant.attaques[choix]

            if random.randint(1, 100) > attaque_choisie.precision:
                afficher_texte(f"\n{pkm_attaquant.nom} utilise {attaque_choisie.nom} mais rate son attaque !")
                return 0

            # Calcul du multiplicateur basé sur le type de l'attaque
            mult = pkm_defenseur.nb_degats_recus(attaque_choisie.type_attaque.nom)
            degats_finaux = self.calculer_degats(pkm_attaquant, pkm_defenseur, attaque_choisie)

            pkm_defenseur.prendre_degats(degats_finaux)
            afficher_texte(f"\n{pkm_attaquant.nom} utilise {attaque_choisie.nom} sur {pkm_defenseur.nom} !")
            
            if attaque_choisie.type_attaque == type_poison:
                if any(
                    type_pokemon.nom in {"Poison", "Acier"}
                    for type_pokemon in pkm_defenseur.types
                ):
                    afficher_texte(f"{pkm_defenseur} ne peut pas etre empoisonné")
                else:
                    pkm_defenseur.statut = "empoisonné"
                    afficher_texte(f"{pkm_defenseur} est empoisonné")

            if attaque_choisie.nom == "Ultrason":
                pkm_defenseur.statut = "confus"
                afficher_texte(f"{pkm_defenseur} est confus")

            mult = pkm_defenseur.nb_degats_recus(attaque_choisie.type_attaque.nom)
            
            if mult > 1.0:
                afficher_texte(random.choice(["Wooooow t'es trop chaud !", "C'est quoi cette attaque de fou là!"]))
            elif mult < 1.0:
                afficher_texte(random.choice(["Pas fou, pas fou...", "Keske tu fais ???", "T'es pas sauvable toi-", "mouais.."]))

            afficher_texte(f"{self.dresseur_actif.nom} attaque {self.dresseur_suivant.nom} avec son {self.dresseur_actif.pokemon_actif} !")
            afficher_texte(f"{pkm_defenseur.nom} subit {degats_finaux} dégâts. (PV de {pkm_defenseur.nom}: {pkm_defenseur.get_pv()}/{pkm_defenseur.get_pv_max()})")
        else:
            afficher_texte("Choix invalide !")
        return degats_finaux

        
    def gestion_tour(self):
        """ gere le gameplay d'un tour pendant un combat """
        
        if self.dresseur_actif is None or self.dresseur_suivant is None:
            afficher_texte(" Aucun dresseur actif ")
            return

        pkm_actif:Pokemon|None = self.dresseur_actif.pokemon_actif
        pkm_adversaire:Pokemon|None = self.dresseur_suivant.pokemon_actif

        if pkm_actif is None or pkm_adversaire is None:
            afficher_texte(" Aucun pokemon actif ")
            return

        if pkm_actif.statut == "empoisonné":
            pkm_actif.appliquer_poison()
            if pkm_actif.est_ko():
                afficher_texte(f"{pkm_actif.nom} succombe au poison !")
                if self.dresseur_actif.tous_ko():
                    return False
                pkm_actif = self.dresseur_actif.pokemon[self.demander_remplacement(self.dresseur_actif)]
                self.dresseur_actif.pokemon_actif = pkm_actif

        if pkm_actif.statut == "confus":
            pkm_actif.appliquer_confusion()
            if pkm_actif.est_ko():
                afficher_texte(f"{pkm_actif.nom} est KO dans sa confusion !")
                if self.dresseur_actif.tous_ko():
                    return False
                pkm_actif = self.dresseur_actif.pokemon[self.demander_remplacement(self.dresseur_actif)]
                self.dresseur_actif.pokemon_actif = pkm_actif
            
        afficher_texte(f"\n    Pokémon actif : {pkm_actif.nom} ({pkm_actif.get_pv()}/{pkm_actif.get_pv_max()} PV)")
        afficher_texte(f"    {barre_de_vie(pkm_actif.get_pv(), pkm_actif.get_pv_max())}\n")
        afficher_texte(f"    Adversaire : {pkm_adversaire.nom} ({pkm_adversaire.get_pv()}/{pkm_adversaire.get_pv_max()} PV)")
        afficher_texte(f"    {barre_de_vie(pkm_adversaire.get_pv(), pkm_adversaire.get_pv_max())}\n")

        if self.dresseur_actif.est_bot:
            choix = "1"   # puis on tombe dans le if choix == "1" existant
        else:
            afficher_cadre(f"TOUR {self.tour} - A {self.dresseur_actif.nom} de jouer", [
                "1) Attaquer",
                "2) Utiliser un objet",
                "3) Changer de pokemon"
            ])
            choix = input("-> ")

        if choix == "1":
            self.attaquer()

        if choix == "2":
            if not self.dresseur_actif.objets:
                afficher_texte("ouais, nan ton tour a servi à rien bahhaha, t'as pas d'objet")
            else:
                afficher_texte("\n-- Objets disponibles --")
                self.dresseur_actif.afficher_objets()

                try:
                    choisir_item = demander_nombre("\nChoisissez un objet (numéro) : ", 1, len(self.dresseur_actif.objets)) - 1
                    if 0 <= choisir_item < len(self.dresseur_actif.objets):
                        objet = self.dresseur_actif.objets[choisir_item]

                        # Si c'est un ItemSoin ou ItemRevive, l'utiliser
                        if hasattr(objet, 'utiliser'):
                            # Choisir sur quel Pokémon utiliser l'objet
                            afficher_texte("\n-- Choisissez un Pokémon --")
                            self.dresseur_actif.afficher_pokemons()
                            choix_pkm = demander_nombre("Sur quel Pokémon ? (numéro) : ", 1, len(self.dresseur_actif.pokemon)) - 1

                            if 0 <= choix_pkm < len(self.dresseur_actif.pokemon):
                                pokemon_cible = self.dresseur_actif.pokemon[choix_pkm]

                                # Utiliser l'objet
                                if objet.utiliser(pokemon_cible):
                                    self.dresseur_actif.retirer_objet(objet)
                                else:
                                    afficher_texte("L'objet n'a pas pu être utilisé.")
                            else:
                                afficher_texte("Choix invalide")
                        else:
                            afficher_texte("Cet objet ne peut pas être utilisé en combat.")
                    else:
                        afficher_texte("Choix invalide")

                except ValueError:
                    afficher_texte("Entrée invalide")


        if choix == "3":
            if self.dresseur_actif.nb_vivants_restants() == 1:
                afficher_texte(f"Vous n'avez pas d'autres pokemons, continuez avec {pkm_actif}")
            else : 
                print(self.dresseur_actif.afficher_pokemons())
                choisir_pokemon = demander_nombre("choisissez un pokemon (avec son numéro attribué) parmi vos pokemons :\n->", 1, len(self.dresseur_actif.pokemon))
                self.dresseur_actif.pokemon_actif = self.dresseur_actif.pokemon[choisir_pokemon - 1]

            self.attaquer()

        if pkm_adversaire.est_ko():
            ko_texte = """
 _______ _______ _______      _     _    _____   
 |______ |______    |         |____/    |     |  
 |______ ______|    |         |    \_ . |_____| .
                                                 
            """
            if pkm_adversaire.image is not None:
                print(f"\n{pkm_adversaire.image}\n")
            afficher_texte(f"\n{pkm_adversaire.nom.upper()}")
            print(ko_texte)  

            # Gain d'xp
            xp_gagnee = 50 * pkm_adversaire.niveau
            pkm_actif.gagner_xp(xp_gagnee)

            if self.dresseur_suivant.tous_ko():
                afficher_texte(f"gg {self.dresseur_actif.nom} !")
                return False  # stop la boucle while
            else:
                choix_nouveau = self.demander_remplacement(self.dresseur_suivant)
                self.dresseur_suivant.pokemon_actif = self.dresseur_suivant.pokemon[choix_nouveau]
                afficher_texte(f"{self.dresseur_suivant.nom} envoie {self.dresseur_suivant.pokemon_actif.nom} !")

        # 2. Alternance des dresseurs pour le tour suivant
        self.dresseur_actif, self.dresseur_suivant = self.dresseur_suivant, self.dresseur_actif
        self.tour += 1
        return True  # Maintient la boucle active
        