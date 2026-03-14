"""
Fichier 2 : Algorithme mémétique (Algorithme génétique + recherche locale 2-opt).

"""

import random
import time

from glouton import cout_tournee_cycle, plus_proche_voisin


# ==================== RECHERCHE LOCALE 2-OPT ====================

def echange_2_opt(tournee, i, k):
    """
    Voisin 2-opt : on inverse l'ordre des villes entre la position i et la position k.
    Exemple : [0,1,2,3,4] avec i=1, k=3 donne [0,3,2,1,4]
    """
    nouvelle_tournee = []
    # De 0 à i-1 : on garde pareil
    for pos in range(0, i):
        nouvelle_tournee.append(tournee[pos])
    # De i à k : on met à l'envers
    for pos in range(k, i - 1, -1):
        nouvelle_tournee.append(tournee[pos])
    # De k+1 à la fin : on garde pareil
    for pos in range(k + 1, len(tournee)):
        nouvelle_tournee.append(tournee[pos])
    return nouvelle_tournee


def meilleure_amelioration_2_opt(tournee, matrice):
    """
    On essaie tous les voisins 2-opt. Si un améliore le coût, on le retourne.
    Sinon on retourne la tournée telle quelle.
    """
    nb_villes = len(tournee)
    cout_actuel = cout_tournee_cycle(tournee, matrice)

    for i in range(nb_villes - 1):
        for k in range(i + 1, nb_villes):
            nouvelle_tournee = echange_2_opt(tournee, i, k)
            nouveau_cout = cout_tournee_cycle(nouvelle_tournee, matrice)
            if nouveau_cout < cout_actuel:
                return nouvelle_tournee, nouveau_cout

    return tournee, cout_actuel


def recherche_locale_2_opt(tournee, matrice, max_ameliorations=20):
    """
    On améliore la tournée avec 2-opt tant qu'on peut (ou jusqu'à max_ameliorations fois).
    """
    cout = cout_tournee_cycle(tournee, matrice)
    nb_etapes = 0

    while nb_etapes < max_ameliorations:
        nouvelle_tournee, nouveau_cout = meilleure_amelioration_2_opt(tournee, matrice)
        if nouveau_cout >= cout:
            break
        tournee = nouvelle_tournee
        cout = nouveau_cout
        nb_etapes = nb_etapes + 1

    return tournee, cout


# ==================== ALGORITHME MÉMÉTIQUE ====================

def tournee_aleatoire(nb_villes):
    """Génère une tournée en mélangeant aléatoirement l'ordre des villes."""
    tournee = []
    for i in range(nb_villes):
        tournee.append(i)
    # Mélanger : on échange chaque position avec une position au hasard
    for i in range(nb_villes):
        j = random.randint(0, nb_villes - 1)
        temp = tournee[i]
        tournee[i] = tournee[j]
        tournee[j] = temp
    return tournee


def initialiser_population(matrice, taille_population, nb_gloutons=5):
    """
    Créer la population de départ :
    - Quelques solutions gloutonnes (plus proche voisin en partant de villes différentes)
    - Le reste : des tournées aléatoires
    """
    nb_villes = len(matrice)
    population = []

    nb_gloutons_a_faire = nb_gloutons
    if nb_gloutons_a_faire > nb_villes:
        nb_gloutons_a_faire = nb_villes

    for depart in range(nb_gloutons_a_faire):
        tournee, _ = plus_proche_voisin(matrice, depart=depart)
        population.append(tournee)

    while len(population) < taille_population:
        tournee = tournee_aleatoire(nb_villes)
        population.append(tournee)

    return population


def croisement_ox(parent1, parent2):
    """
    Croisement OX (Order Crossover) : on prend un bout de parent1, on complète avec parent2.
    """
    nb_villes = len(parent1)
    a = random.randint(0, nb_villes - 1)
    b = random.randint(0, nb_villes - 1)
    if a > b:
        temp = a
        a = b
        b = temp
    if a == b:
        b = b + 1
        if b >= nb_villes:
            b = nb_villes - 1
            a = b - 1

    # Le segment entre a et b vient de parent1
    segment = []
    for i in range(a, b):
        segment.append(parent1[i])

    # Le reste vient de parent2 (dans l'ordre, sans les villes déjà dans segment)
    reste = []
    for i in range(nb_villes):
        ville = parent2[i]
        presente = False
        for s in segment:
            if s == ville:
                presente = True
                break
        if not presente:
            reste.append(ville)

    # Enfant = début de reste + segment + fin de reste
    enfant = []
    for i in range(a):
        enfant.append(reste[i])
    for i in range(len(segment)):
        enfant.append(segment[i])
    for i in range(a, len(reste)):
        enfant.append(reste[i])
    return enfant[:nb_villes]


def mutation_echange(tournee):
    """Mutation : on échange deux villes choisies au hasard."""
    nb_villes = len(tournee)
    i = random.randint(0, nb_villes - 1)
    j = random.randint(0, nb_villes - 1)
    while j == i:
        j = random.randint(0, nb_villes - 1)
    # Copie de la tournée
    nouvelle = []
    for k in range(nb_villes):
        nouvelle.append(tournee[k])
    nouvelle[i] = tournee[j]
    nouvelle[j] = tournee[i]
    return nouvelle


def selection_tournoi(population, matrice, k=3):
    """
    Sélection par tournoi : on prend k individus au hasard, on garde le meilleur (coût le plus bas).
    """
    nb_pop = len(population)
    if k > nb_pop:
        k = nb_pop

    # Choisir k indices au hasard
    indices = []
    while len(indices) < k:
        idx = random.randint(0, nb_pop - 1)
        deja_pris = False
        for i in indices:
            if i == idx:
                deja_pris = True
                break
        if not deja_pris:
            indices.append(idx)

    # Trouver celui qui a le plus petit coût
    meilleur_idx = indices[0]
    meilleur_cout = cout_tournee_cycle(population[meilleur_idx], matrice)

    for idx in indices:
        c = cout_tournee_cycle(population[idx], matrice)
        if c < meilleur_cout:
            meilleur_cout = c
            meilleur_idx = idx

    # Retourner une copie de la tournée gagnante
    resultat = []
    for i in range(len(population[meilleur_idx])):
        resultat.append(population[meilleur_idx][i])
    return resultat


def mementique_tsp(matrice, taille_population=30, generations=80, prob_croisement=0.8, prob_mutation=0.2, elitisme=2):
    """
    Algorithme mémétique :
    1. Créer une population (glouton + aléatoire)
    2. Améliorer chaque individu avec 2-opt
    3. Répéter : sélection, croisement, mutation, 2-opt, garder les meilleurs
    Retourne (meilleure_tournée, meilleur_coût).
    """
    random.seed()
    nb_villes = len(matrice)

    # Population initiale
    population = initialiser_population(matrice, taille_population)
    for i in range(len(population)):
        population[i], _ = recherche_locale_2_opt(population[i], matrice)

    # Trouver la meilleure tournée actuelle
    meilleure_tournee = []
    for i in range(len(population[0])):
        meilleure_tournee.append(population[0][i])
    meilleur_cout = cout_tournee_cycle(meilleure_tournee, matrice)

    for idx in range(1, len(population)):
        c = cout_tournee_cycle(population[idx], matrice)
        if c < meilleur_cout:
            meilleur_cout = c
            meilleure_tournee = []
            for i in range(len(population[idx])):
                meilleure_tournee.append(population[idx][i])

    # Boucle des générations
    for gen in range(generations - 1):
        # Trier la population par coût (du meilleur au pire)
        couts = []
        for i in range(len(population)):
            c = cout_tournee_cycle(population[i], matrice)
            couts.append((i, c))
        for i in range(len(couts)):
            for j in range(i + 1, len(couts)):
                if couts[j][1] < couts[i][1]:
                    temp = couts[i]
                    couts[i] = couts[j]
                    couts[j] = temp

        # Nouvelle population : garder les meilleurs (élitisme)
        nouvelle_population = []
        nb_elites = elitisme
        if nb_elites > len(population):
            nb_elites = len(population)
        for i in range(nb_elites):
            copie = []
            for j in range(len(population[0])):
                copie.append(population[couts[i][0]][j])
            nouvelle_population.append(copie)

        # Compléter avec des enfants
        while len(nouvelle_population) < taille_population:
            parent1 = selection_tournoi(population, matrice)
            parent2 = selection_tournoi(population, matrice)

            if random.random() < prob_croisement:
                enfant = croisement_ox(parent1, parent2)
            else:
                enfant = []
                for i in range(len(parent1)):
                    enfant.append(parent1[i])

            if random.random() < prob_mutation:
                enfant = mutation_echange(enfant)

            enfant, _ = recherche_locale_2_opt(enfant, matrice)
            nouvelle_population.append(enfant)

        population = nouvelle_population

        # Mettre à jour la meilleure solution si on a trouvé mieux
        for i in range(len(population)):
            c = cout_tournee_cycle(population[i], matrice)
            if c < meilleur_cout:
                meilleur_cout = c
                meilleure_tournee = []
                for j in range(len(population[i])):
                    meilleure_tournee.append(population[i][j])

    return meilleure_tournee, meilleur_cout


def mementique_tsp_chrono(matrice, taille_population=30, generations=80, **kwargs):
    """
    Même chose que mementique_tsp, mais on mesure le temps d'exécution.
    Retourne (tournée, coût, temps_en_secondes).
    """
    temps_debut = time.perf_counter()
    tournee, cout = mementique_tsp(matrice, taille_population=taille_population, generations=generations, **kwargs)
    temps_fin = time.perf_counter()
    duree = temps_fin - temps_debut
    return tournee, cout, duree
