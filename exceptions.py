"""
----------------------------------------------------
EXCEPTIONS.PY - Lever des erreurs
----------------------------------------------------
"""

class PokemonKOError(Exception):
    """ si on tente d'attaquer ou interagir avec un Pokémon K.O."""
    pass

class ObjetIndisponibleError(Exception):
    """ si l'objet n'est pas dans le sac du dresseur."""
    pass

class PVInvalideError(Exception):
    """si modification incohérente des PV."""
    pass

class PokemonInexistantError(Exception):
    """pkm pas dans la base de donnees"""
    pass