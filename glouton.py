"""
Fichier 1 : Glouton (Plus proche voisin) + chargement des instances TSPLIB.

"""

import math
import time
from pathlib import Path


# ==================== CHARGEMENT D'UNE INSTANCE .tsp ====================

def charger_instance(chemin_ou_contenu):
    """
    Charge un fichier .tsp et calcule la matrice des distances entre les villes.
    Retourne (matrice, nb_villes, nom).
    """
    # --- Lire le contenu du fichier ---
    if isinstance(chemin_ou_contenu, (tuple, list)) and len(chemin_ou_contenu) == 2:
        # Cas Colab : (nom, contenu)
        nom = chemin_ou_contenu[0]
        texte = chemin_ou_contenu[1]
        if isinstance(texte, bytes):
            texte = texte.decode("utf-8", errors="ignore")
    else:
        # Cas normal : chemin vers le fichier
        chemin = Path(chemin_ou_contenu)
        if not chemin.exists():
            raise FileNotFoundError("Fichier non trouvé : " + str(chemin))
        nom = chemin.stem
        fichier = open(chemin, "r", encoding="utf-8", errors="ignore")
        texte = fichier.read()
        fichier.close()

    lignes = texte.split("\n")

    # --- Lire la dimension et le type de distance ---
    dimension = None
    type_arete = "EUC_2D"
    indice_coord = -1

    for i in range(len(lignes)):
        ligne = lignes[i].strip()
        if ligne.startswith("DIMENSION"):
            partie_apres_deux_points = ligne.split(":")[1]
            dimension = int(partie_apres_deux_points.strip())
        elif ligne.startswith("EDGE_WEIGHT_TYPE"):
            partie_apres_deux_points = ligne.split(":")[1]
            type_arete = partie_apres_deux_points.strip()
        # Certaines instances peuvent avoir des espaces ou des variantes autour du mot
        elif "NODE_COORD_SECTION" in ligne:
            indice_coord = i
            break

    if indice_coord < 0:
        raise ValueError("Pas de NODE_COORD_SECTION dans le fichier")

    # --- Lire les coordonnées de chaque ville ---
    coordonnees = []
    for i in range(indice_coord + 1, len(lignes)):
        ligne = lignes[i].strip()
        if "EOF" in ligne or ligne == "":
            break
        parties = ligne.split()
        if len(parties) >= 3:
            x = float(parties[1])
            y = float(parties[2])
            coordonnees.append((x, y))

    if dimension is not None and len(coordonnees) > dimension:
        coordonnees = coordonnees[:dimension]

    nb_villes = len(coordonnees)

    # --- Calculer la matrice des distances ---
    # matrice[i][j] = distance entre la ville i et la ville j (symétrique)
    matrice = []
    for i in range(nb_villes):
        ligne = [0] * nb_villes
        matrice.append(ligne)

    for i in range(nb_villes):
        for j in range(i + 1, nb_villes):
            # Distance entre ville i et ville j
            x1, y1 = coordonnees[i][0], coordonnees[i][1]
            x2, y2 = coordonnees[j][0], coordonnees[j][1]
            if type_arete == "ATT":
                r = math.sqrt(((x1 - x2) ** 2 + (y1 - y2) ** 2) / 10.0)
                if r > int(r):
                    d = int(r) + 1
                else:
                    d = int(r)
            else:
                d = round(math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2))
            matrice[i][j] = d
            matrice[j][i] = d

    return matrice, nb_villes, nom


# ==================== PLUS PROCHE VOISIN (GLOUTON) ====================

def cout_tournee_cycle(tournee, matrice):
    """
    Calcule le coût total d'une tournée (distance totale).
    La tournée est un cycle : on revient à la ville de départ.
    """
    if len(tournee) < 2:
        return 0
    cout = 0
    # Distance entre chaque ville consécutive
    for i in range(len(tournee) - 1):
        ville_a = tournee[i]
        ville_b = tournee[i + 1]
        cout = cout + matrice[ville_a][ville_b]
    # Retour à la ville de départ
    cout = cout + matrice[tournee[-1]][tournee[0]]
    return cout


def plus_proche_voisin(matrice, depart=0):
    """
    Algorithme du plus proche voisin :
    1. On part de la ville 'depart'.
    2. À chaque étape, on va vers la ville non visitée la plus proche.
    3. À la fin, on revient à la ville de départ.
    Retourne (tournée, coût).
    """
    nb_villes = len(matrice)

    # Liste des villes pas encore visitées (sauf la ville de départ)
    non_visitees = []
    for i in range(nb_villes):
        if i != depart:
            non_visitees.append(i)

    # On commence par la ville de départ
    tournee = [depart]
    ville_actuelle = depart

    # Tant qu'il reste des villes à visiter
    while len(non_visitees) > 0:
        # Chercher la ville non visitée la plus proche de ville_actuelle
        distance_min = None
        ville_plus_proche = None
        for j in non_visitees:
            d = matrice[ville_actuelle][j]
            if distance_min is None or d < distance_min:
                distance_min = d
                ville_plus_proche = j

        # Aller à cette ville
        tournee.append(ville_plus_proche)
        non_visitees.remove(ville_plus_proche)
        ville_actuelle = ville_plus_proche

    cout = cout_tournee_cycle(tournee, matrice)
    return tournee, cout


def plus_proche_voisin_chrono(matrice, depart=0):
    """
    Même chose que plus_proche_voisin, mais on mesure aussi le temps d'exécution.
    Retourne (tournée, coût, temps_en_secondes).
    """
    temps_debut = time.perf_counter()
    tournee, cout = plus_proche_voisin(matrice, depart)
    temps_fin = time.perf_counter()
    duree = temps_fin - temps_debut
    return tournee, cout, duree
