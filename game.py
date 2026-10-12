"""
----------------------------------------------------
COMBAT.PY - Combat et Logique de combat
~~~~~~~~~~~~~~~~~~~~~~
A CONTINUER : 
- Inventaire du menu principal
----------------------------------------------------
"""

from combat import Combat
from pokemon import Lixy, Pikachu, Smogo
from dresseur import Dresseur

class Game:
    def __init__(self):
        self.d1 = Dresseur("Sacha")
        self.d2 = Dresseur("Ondine")
        self.a = Combat(self.d1, self.d2)

    def run(self):
        #Creation dresseur et ajout pkm
        
        self.d1.ajouter_pokemon(Lixy)
        self.d2.ajouter_pokemon(Smogo)
        self.d2.ajouter_pokemon(Pikachu)

        #Combat
        self.a.lancer_combat()

        while not self.a.dresseur1.tous_ko() and not self.a.dresseur2.tous_ko() :
            combat_actif = self.a.gestion_tour()
            if not combat_actif:
                break

        if self.a.dresseur1.tous_ko():
            print(f"\nVictoire pour {self.a.dresseur2.nom} !")
        elif self.a.dresseur2.tous_ko():
            print(f"\nVictoire pour {self.a.dresseur1.nom} !")

    def menu_principal(self):
        """ affiche le menu principal """
        while True:
            print("\n=== POKÉMON ===")
            print("1) Lancer un combat")
            print("2) Gérer les pokémons")
            print("3) Gérer l'inventaire")
            print("4) Quitter")
            choix = input("-> ")

            if choix == "1":
                self.run()  # Lance le combat
            elif choix == "2":
                self.a.modifier_inventaire_pokemon(self.a.dresseur1, Lixy)
                self.a.modifier_inventaire_pokemon(self.a.dresseur2, Pikachu)
            elif choix == "3":
                Dresseur.modifier_inventaire_item(self.a.dresseur1)
                Dresseur.modifier_inventaire_item(self.a.dresseur2)
            elif choix == "4":
                print("A jamaiiiis !! ;D")
                break