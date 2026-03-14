"""
Fichier 3: Exécute tout (glouton + mémétique sur chaque instance) et génère le tableau.
Utilisation : python main.py   ou   sur Colab : import main puis main.principale()

"""

from pathlib import Path

from glouton import charger_instance, plus_proche_voisin_chrono
from memetic import mementique_tsp_chrono


def obtenir_fichiers_tsp():
    """
    Cherche les fichiers .tsp dans le dossier "instances", puis dans le dossier courant.
    Utile pour Colab où les fichiers sont à la racine.
    """
    repertoire_courant = Path.cwd()
    # D'abord regarder dans le dossier instances
    dossier_instances = repertoire_courant / "instances"
    if dossier_instances.exists():
        fichiers = list(dossier_instances.glob("*.tsp"))
        if len(fichiers) > 0:
            fichiers_tries = sorted(fichiers)
            return fichiers_tries
    # Sinon regarder dans le dossier courant
    fichiers = list(repertoire_courant.glob("*.tsp"))
    if len(fichiers) > 0:
        return sorted(fichiers)
    return []


def executer_une_instance(chemin_ou_contenu):
    """
    Pour une instance : charge le fichier, lance le glouton, lance le mémétique, calcule le gain.
    Retourne un dictionnaire avec tous les résultats.
    """
    matrice, nb_villes, nom = charger_instance(chemin_ou_contenu)

    # Lancer le plus proche voisin (glouton)
    tournee_glouton, cout_glouton, temps_glouton = plus_proche_voisin_chrono(matrice, 0)

    # Choisir la taille de la population et le nombre de générations
    # Paramètres réduits pour que ce soit plus rapide
    if nb_villes < 200:
        taille_population = 15
        nb_generations = 30
    else:
        taille_population = 10
        nb_generations = 20

    # Lancer l'algorithme mémétique
    tournee_mem, cout_mementique, temps_mementique = mementique_tsp_chrono(
        matrice,
        taille_population=taille_population,
        generations=nb_generations
    )

    # Calculer le gain en pourcentage
    if cout_glouton > 0:
        gain_pourcent = 100.0 * (cout_glouton - cout_mementique) / cout_glouton
    else:
        gain_pourcent = 0.0

    # Retourner un dictionnaire avec toutes les infos
    resultat = {
        "instance": nom,
        "taille": nb_villes,
        "cout_glouton": cout_glouton,
        "temps_glouton": temps_glouton,
        "cout_mementique": cout_mementique,
        "temps_mementique": temps_mementique,
        "gain_pourcent": gain_pourcent,
    }
    return resultat


def principale(dico_upload=None):
    """
    Fonction principale : lance les expériences sur toutes les instances et affiche le tableau.
    dico_upload : sur Colab, après files.upload(), on peut passer le dictionnaire ici.
    Sinon, on utilise les fichiers .tsp trouvés dans instances/ ou le dossier courant.
    """
    # Construire la liste des instances à traiter
    taches = []

    if dico_upload is not None:
        # Cas Colab : les fichiers ont été uploadés
        for nom_fichier, contenu in dico_upload.items():
            if nom_fichier.endswith(".tsp"):
                nom_sans_extension = nom_fichier.replace(".tsp", "")
                taches.append((nom_sans_extension, contenu))
    else:
        # Cas normal : chercher les fichiers .tsp
        taches = obtenir_fichiers_tsp()
        if len(taches) == 0:
            print("Aucun fichier .tsp trouvé. Mettez des fichiers .tsp dans le dossier 'instances/' ou à la racine.")
            return

    if len(taches) < 10:
        print("Attention : le projet demande au moins 10 instances. Vous en avez", len(taches))

    # Exécuter chaque instance et stocker les résultats
    resultats = []
    for element in taches:
        try:
            res = executer_une_instance(element)
            resultats.append(res)
            print("  OK", res["instance"], "(n =", res["taille"], ")")
        except ValueError as e:
            # Par exemple : pas de NODE_COORD_SECTION (format non géré)
            print("  Instance ignorée (format non supporté) :", element, "-", e)
            continue

    # Afficher le tableau comparatif
    print("")
    print("=" * 100)
    print("TABLEAU COMPARATIF : Plus proche voisin vs Algorithme mémétique")
    print("=" * 100)
    print("{:<14} {:>6} {:>12} {:>12} {:>12} {:>16} {:>10}".format(
        "Instance", "n", "Coût NN", "Temps NN (s)", "Coût Mémét.", "Temps Mémét. (s)", "Gain (%)"
    ))
    print("-" * 100)

    for res in resultats:
        print("{:<14} {:>6} {:>12} {:>12.4f} {:>12} {:>16.4f} {:>10.2f}".format(
            res["instance"],
            res["taille"],
            res["cout_glouton"],
            res["temps_glouton"],
            res["cout_mementique"],
            res["temps_mementique"],
            res["gain_pourcent"]
        ))
    print("-" * 100)

    # Enregistrer les résultats dans un fichier CSV
    chemin_sortie = Path.cwd() / "Tableau_de_resultats_comparatif.csv"
    fichier_csv = open(chemin_sortie, "w", encoding="utf-8")
    fichier_csv.write("Instance;Taille;Coût_glouton;Temps_glouton_s;Coût_méta;Temps_méta_s;Gain_pct\n")
    for res in resultats:
        ligne = "{};{};{};{:.4f};{};{:.4f};{:.2f}\n".format(
            res["instance"],
            res["taille"],
            res["cout_glouton"],
            res["temps_glouton"],
            res["cout_mementique"],
            res["temps_mementique"],
            res["gain_pourcent"]
        )
        fichier_csv.write(ligne)
    fichier_csv.close()

    print("")
    print("Résultats enregistrés dans :", chemin_sortie)


if __name__ == "__main__":
    principale()
