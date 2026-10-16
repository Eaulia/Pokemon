"""
----------------------------------------------------
COMBAT.PY - Combat et Logique de combat
~~~~~~~~~~~~~~~~~~~~~~
A CONTINUER : 
- Inventaire du menu principal
COMMENTAIRES : tkt les couleurs c'est la folie quand t'es fatigué 
----------------------------------------------------
"""

from combat import Combat
from pokemon import Lixy, Pikachu, Smogo, Bulbizarre, Nosferapti
from dresseur import Dresseur
from decoration import afficher_texte, Couleurs, afficher_cadre

class Game:
    def __init__(self):
        self.d1 = Dresseur("Sacha")
        self.d2 = Dresseur("Ondine")
        self.a = Combat(self.d1, self.d2)

    def run(self):
        #Creation dresseur et ajout pkm

        self.d1.ajouter_pokemon(Nosferapti)
        self.d1.ajouter_pokemon(Lixy)
        self.d2.ajouter_pokemon(Smogo)
        self.d2.ajouter_pokemon(Pikachu)

        #Combat
        self.a.lancer_combat()

        if self.a.dresseur1.tous_ko() or self.a.dresseur2.tous_ko():
            return

        while not self.a.dresseur1.tous_ko() and not self.a.dresseur2.tous_ko() :
            combat_actif = self.a.gestion_tour()
            if not combat_actif:
                break

        if self.a.dresseur1.tous_ko():
            afficher_texte(f"\nVictoire pour {self.a.dresseur2.nom} !")
            print("\n┗━━━━                                                              ━━━━┛")
            self.d1.soigner_equipe()
            self.d2.soigner_equipe()

        elif self.a.dresseur2.tous_ko():
            afficher_texte(f"\nVictoire pour {self.a.dresseur1.nom} !")
            print("\n┗━━━━                                                              ━━━━┛")
            self.d1.soigner_equipe()
            self.d2.soigner_equipe()

    def menu_principal(self):
        """ affiche le menu principal """
        while True:   
            print("┏━━━━                                                              ━━━━┓")
            print("""
                                                           [0m
[0;36m [0;96m▄[0;96;46m▀[0;36m█[0;90;46m▄[0;36m▀▀▀[0;96;46m▄[0;36m██[0;90m▌[0;36m           [0;96m▄[0;96;46m▀[0;90m▄[0;36m   ▄[0;90m▄[0;36m                                          [0m
[0;96m▐[0;36m██[0;90m▌[0;36m    [0;96m▄[0;96;46m▀[0;36m█[0;90;46m▐[0;36m          [0;96m█[0;36m██[0;90;46m▄[0;90m▌[0;36m [0;96;46m▀[0;36m██[0;90m▌[0;36m                                         [0m
[0;96m▐[0;36m███[0;90;46m▀[0;36m▄▄[0;96;46m▀[0;36m█[0;90;46m▄[0;90m▀[0;36m          [0;96m▐[0;36m██[0;90m▀[0;36m  [0;96m▄[0;36m█[0;90;46m▄[0;90m▀[0;36m    [0;96m▄▄[0;36m▄[0;90m▄[0;36m   [0;96;46m█▀[0;36m▄▄▄[0;90m▄[0;36m  [0;96m▄[0;96;46m▀▀[0;36m▄          [0;96;46m█▀[0;36m▄▄▄[0;96;46m▀▀[0;36m▄ [0m
[0;96m▐[0;36m██[0;90;46m▐[0;36m         [0;96m▄[0;96;46m▀[0;36m██[0;90;46m▀▀[0;90m▄[0;36m [0;96;46m▌[0;36m█[0;96;46m▀[0;36m█[0;96;46m▀▀[0;90;46m▄[0;90m▀[0;36m    [0;96m▄[0;96;46m▀[0;36m█▀▀█[0;90;46m▀[0;90m▄[0;36m [0;96m▐[0;36m█[0;90;46m▄[0;36m▀[0;96;46m▄[0;36m█[0;90m▌[0;36m▄[0;96;46m▀[0;36m██[0;90;46m▐[0;36m  [0;96m▄[0;96;46m▀[0;36m██[0;90;46m▀▀[0;90m▄[0;36m [0;96m▐[0;36m█[0;90;46m▄[0;36m▀[0;96;46m▄[0;36m██[0;90;46m▐[0;36m [0m
[0;96m▐[0;36m██[0;90m▌[0;36m        [0;96m▐[0;36m█[0;90;46m▐[0;90m▀[0;36m  [0;96m▐[0;36m█[0;96m▐[0;36m██[0;90;46m▐[0;96m▀[0;96;46m▄[0;36m██[0;90;46m▀[0;90m▄[0;36m  [0;96m▐[0;36m███▄▄▄█[0;90m▌[0;36m [0;96;46m▌[0;36m██[0;90m▌[0;36m [0;96;46m▌[0;36m██[0;90;46m▐[0;36m [0;96;46m▌[0;36m█[0;90m▌[0;96m▐[0;36m█[0;90;46m▐[0;90m▀[0;36m  [0;96m▐[0;36m█ [0;96;46m▌[0;36m██[0;90m▌[0;36m  [0;96;46m▌[0;36m█[0;90m▌[0m
[0;96m▐[0;36m██[0;90m▌[0;36m        [0;96;46m▌ [0;90;46m▐[0;90m▄[0;36m ▄[0;96;46m▀[0;90;46m▐[0;96;46m▌ [0;36m██[0;90m▌[0;36m [0;96m▀[0;96;46m█ [0;36m█[0;90m▌[0;36m [0;96m▀[0;96;46m▄[0;36m██▀  ▄[0;90m▄[0;96m▐[0;36m██[0;90;46m▐[0;36m  [0;96m▀[0;96;46m▄[0;90;46m▐[0;36m [0;96m▐[0;36m██[0;90m▌[0;96;46m▌ [0;90;46m▐[0;90m▄[0;36m ▄[0;96;46m▀[0;90;46m▐[0;96m▐[0;36m██[0;90;46m▐[0;36m  [0;96m▐[0;36m██[0;90m▌[0m
[0;96m▀[0;36m▀[0;90m▀[0;36m         [0;96m▀[0;96;46m▄[0;36m██[0;90;46m▄▄[0;90m▀[0;36m [0;96m▀[0;96;46m▄[0;36m█[0;90m▀[0;36m   [0;96m▀[0;96;46m▄[0;36m█[0;90;46m▐[0;36m   [0;96m▀[0;96;46m▄▄[0;36m█[0;90;46m▄[0;90m▀[0;36m [0;96m█[0;96;46m▄[0;36m██[0;90;46m█[0;36m     [0;96;46m█▄[0;36m█[0;90;46m▐[0;96m▀[0;96;46m▄[0;36m██[0;90;46m▄▄[0;90m▀[0;36m [0;96m█[0;96;46m▄[0;36m██[0;90;46m█[0;36m [0;96;46m█▄[0;36m█[0;90;46m▐[0m
""")
            print(f"                       {Couleurs.GRIS}par Quentin et Viviane{Couleurs.RESET}\n")
            afficher_cadre("MENU PRINCIPAL", [
                "   1) Lancer un combat",
                "   2) Gérer les pokémons",
                "   3) Gérer l'inventaire",
                "   4) Quitter"
            ])
            
            choix = input("-> ")

            if choix == "1":
                afficher_cadre("Mode de combat", ["1) Joueur vs Joueur", "2) Joueur vs Bot"])
                self.d2.est_bot = (input("-> ") == "2")
                self.run()
                self.d1.pokemon = []
                self.d2.pokemon = []
            elif choix == "2":
                self.a.modifier_inventaire_pokemon(self.a.dresseur1, Lixy)
                self.a.modifier_inventaire_pokemon(self.a.dresseur2, Pikachu)
                print("\n┗━━━━                                                              ━━━━┛")
            elif choix == "3":
                Dresseur.modifier_inventaire_item(self.a.dresseur1)
                Dresseur.modifier_inventaire_item(self.a.dresseur2)
                print("\n┗━━━━                                                              ━━━━┛")
            elif choix == "4":
                print("A jamaiiiis !! 👿\n")
                print("\n┗━━━━                                                              ━━━━┛")
                break