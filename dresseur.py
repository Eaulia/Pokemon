from pokemon import Pokemon

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