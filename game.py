from combat import Combat
from pokemon import Dresseur, Lixy, Pikachu, Chinchidou

class Game:
    def __init__():
        pass

    def run(self):
        #Creation dresseur et ajout pkm
        d1 = Dresseur("Sacha")
        d2 = Dresseur("Ondine")
        
        d1.ajouter_pokemon(Lixy)
        d2.ajouter_pokemon(Pikachu)

        #Combat
        #a.modifier_inventaire_pokemon(a.dresseur1, Lixy)
        #a.modifier_inventaire_pokemon(a.dresseur2, Pikachu)
        a = Combat(d1, d2)
        a.lancer_combat()

        while not a.dresseur1.tous_ko() and not a.dresseur2.tous_ko() :
            combat_actif = a.gestion_tour()
            if not combat_actif:
                break

        if a.dresseur1.tous_ko():
            print(f"\nVictoire pour {a.dresseur2.nom} !")
        elif a.dresseur2.tous_ko():
            print(f"\nVictoire pour {a.dresseur1.nom} !")