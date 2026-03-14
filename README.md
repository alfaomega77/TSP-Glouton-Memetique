# Projet TSP — Voyageur de Commerce

**Méthodes :** Glouton (Plus proche voisin) + Algorithme mémétique (GA + 2-opt)

*Faculté des Sciences Meknès — Université Moulay Ismail*

---

## Description

Ce dépôt contient l’implémentation d’une **heuristique gloutonne** (plus proche voisin) et d’un **algorithme mémétique** (génétique + 2-opt) pour résoudre le problème du voyageur de commerce (TSP), avec comparaison des résultats sur des instances TSPLIB.

## Fichiers du projet

| Fichier | Rôle |
|---------|------|
| `glouton.py` | Chargement des instances TSPLIB + algorithme du plus proche voisin |
| `memetic.py` | Algorithme mémétique (GA + 2-opt) |
| `main.py` | Lance les deux méthodes et génère le tableau comparatif + CSV |

## Prérequis

- **Python 3.7+** (bibliothèque standard uniquement, pas de dépendances externes)

## Instances TSPLIB

1. Création de dossier `instances` à la racine du projet.
2. Téléchargement de au moins 10 fichiers `.tsp` (tailles différentes) sur [TSPLIB](https://softlib.rice.edu/pub/tsplib/tsp/).
3. Placement des instances  dans le dossier `instances/`.

## Exécution

### En local

1. Ouvrant  le  terminal dans le dossier du projet.
2. Lancement de  :

```bash
python main.py
```

Le tableau comparatif s’affiche et le fichier `Tableau_de_resultats_comparatif.csv` est généré.

**Exemple de résultat (exécution dans le terminal) :**

![Résultat après exécution dans le terminal](Screen%20Shot%20terminal.png)

### Sur Google Colab

1. Création d'un nouveau notebook.
2. **Cellule 1** — Upload du code et des instances `.tsp` :

```python
from google.colab import files
uploaded = files.upload()
```

3. **Cellule 2** — Exécution :

```python
import main
main.principale()
```

## Formule du gain

**Gain (%)** = 100 × (Coût_glouton − Coût_méta) / Coût_glouton

---

