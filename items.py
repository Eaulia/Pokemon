"""
----------------------------------------------------
ITEMS.PY - Combat et Logique de combat
~~~~~~~~~~~~~~~~~~~~~~
A CONTINUER : 
- items pour l'histoire tm/hm competences
~~~~~~~~~~~~~~~~~~~~~~
COMMENTAIRES :
- c'est pas du tout bien fait bahhaha
----------------------------------------------------
"""

from exceptions import *

class Items:
    def __init__(self, nom:str) -> None:
        self.nom = nom

class ItemConsommables:
    # baies
    def __init__(self, nom:str) -> None:
        self.nom = nom
        self.disponible = True

class ItemSoin(ItemConsommables):
    def __init__(self, nom: str, qteSoin: int) -> None:
        super().__init__(nom)
        self.qteSoin = qteSoin

class ItemCompetence(Items):
    def __init__(self, nom: str, nomCompetence:str) -> None:
        super().__init__(nom)

"""
class ItemPokeball(Items):
    #Capturer un pkm 
    def __init__(self, nom: str) -> None:
        super().__init__(nom)

class ItemEvolution(Items):
    def __init__(self, nom: str) -> None:
        super().__init__(nom)
"""
Fraise = ItemSoin("Fraise", 20)