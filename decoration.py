"""
----------------------------------------------------
DECORATION.PY - Decorations 
----------------------------------------------------
"""
from __future__ import annotations

import sys
import time

class Couleurs:
    RESET = "\033[0m" # couleur normale
    GRAS = "\033[1m"
    GRIS = "\033[90m"
    ROUGE = "\033[91m"
    VERT = "\033[92m"
    JAUNE = "\033[93m"
    BLEU = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BLANC = "\033[97m"
    ORANGE = "\033[38;5;208m"

def barre_de_vie(pv, pv_max, taille=20):
    """Affichage de la barre de vie"""
    # calcul cases pleines
    cases_pleines = pv * taille // pv_max

    # Si vivant une case pleine minimum
    if pv > 0 and cases_pleines == 0:
        cases_pleines = 1

    cases_vides = taille - cases_pleines
    pourcentage = pv * 100 // pv_max

    if pourcentage > 50:
        couleur = Couleurs.VERT
    elif pourcentage > 20:
        couleur = Couleurs.JAUNE
    else:
        couleur = Couleurs.ROUGE

    partie_pleine = couleur + "░" * cases_pleines + Couleurs.RESET
    partie_vide = Couleurs.GRIS + "░" * cases_vides + Couleurs.RESET   

    return partie_pleine + partie_vide

def afficher_texte(texte, delai=0.02):
    """affiche texte caractere par caractere"""
    for caractere in texte:
        sys.stdout.write(caractere)
        sys.stdout.flush()
        time.sleep(delai)
    print()

def afficher_texte_rapide(texte, delai=0.01):
    """affiche texte caractere par caractere"""
    for caractere in texte:
        sys.stdout.write(caractere)
        sys.stdout.flush()
        time.sleep(delai)
    print()

def afficher_cadre(titre: str, lignes: list[str]):
    """Affiche un cadre"""
    largeur = 58
    print("    ╔" + "═" * (largeur + 2) + "╗")
    print(f"    ║ ▼ {titre.center(largeur - 4)} ▼ ║")
    print("    ╠" + "═" * (largeur + 2) + "╣")
    for ligne in lignes:
        print(f"    ║  {ligne.ljust(largeur)}║")
    print("    ╚" + "═" * (largeur + 2) + "╝")