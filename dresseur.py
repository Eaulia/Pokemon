from pokemon import Pokemon
from items import items_disponibles

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
                    self.pokemon.append(pkm)
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

    def modifier_inventaire_item(self):
        """gère l'ajout, le retrait et l'affichage des objets du dresseur"""
        print(f"\n-- Inventaire d'objets de {self.nom} --")
        choix = input("1) Ajouter un objet\n2) Retirer un objet\n3) Afficher l'inventaire\n-> ")
        
        if choix == "1":
            print("\nObjets disponibles :")
            for i, item in enumerate(items_disponibles, 1):
                print(f"{i}) {item.nom} - {item.description}")
            
            try:
                idx = int(input("Numéro de l'objet à ajouter -> ")) - 1
                if 0 <= idx < len(items_disponibles):
                    objet_choisi = items_disponibles[idx]
                    self.ajouter_objet(objet_choisi)
                    print(f"{objet_choisi.nom} a été ajouté au sac")
                else:
                    print("Numéro invalide.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")

        elif choix == "2":
            if not self.objets:
                print("Le sac est vide..")
                return
            
            self.afficher_objets()
            try:
                idx = int(input("Numéro de l'objet à retirer -> ")) - 1
                if 0 <= idx < len(self.objets):
                    objet_retire = self.objets.pop(idx)
                    print(f"{objet_retire.nom} a été retiré du sac.")
                else:
                    print("Numéro invalide.")
            except ValueError:
                print("Veuillez entrer un nombre valide.")

        elif choix == "3":
            print(f"\nObjets de {self.nom} :")
            self.afficher_objets()

        choixcontinuer = input("\nTu veux continuer à modifier l'inventaire d'objets ?\n1) Oui\n2) Non\n\n-> ")
        if choixcontinuer == "1":
            self.modifier_inventaire_item()