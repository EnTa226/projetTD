# Dans un premier temps avec pandas:

import pandas as pd

# Charger le fichier CSV
fichier = "game.csv"
df = pd.read_csv(fichier)

# Afficher les premières lignes pour comprendre la structure des données
df.head()

# Compter les victoires et le nombre total de matchs pour chaque équipe
home_wins = df[df["wl_home"] == "W"].groupby(
    "team_name_home")["wl_home"].count()

away_wins = df[df["wl_home"] == "L"].groupby(
    "team_name_away")["wl_home"].count()

total_wins = home_wins.add(away_wins, fill_value=0)

# Compter le nombre total de matchs joués par chaque équipe
home_games = df.groupby("team_name_home")["wl_home"].count()
away_games = df.groupby("team_name_away")["wl_home"].count()
total_games = home_games.add(away_games, fill_value=0)

# Calculer le ratio de victoires
win_ratio = (total_wins / total_games).dropna()

# Trouver l'équipe avec le meilleur ratio
best_team = win_ratio.idxmax()
best_ratio = win_ratio.max()

best_team, best_ratio

# Dictionnaires pour stocker les victoires et matchs joués
win_counts = {}
game_counts = {}


# Ouvrir et lire le fichier ligne par ligne
with open("game.csv", "r", encoding="utf-8") as file:
    # Lire l'en-tête pour identifier les indices des colonnes
    header = file.readline().strip().split(",")
    team_home_idx = header.index("team_name_home")
    team_away_idx = header.index("team_name_away")
    wl_home_idx = header.index("wl_home")

    # Lire chaque ligne du fichier CSV
    for line in file:
        columns = line.strip().split(",")

        # Récupérer les noms des équipes et le résultat du match
        team_home = columns[team_home_idx]
        team_away = columns[team_away_idx]
        wl_home = columns[wl_home_idx]

        # Initialiser les compteurs si l'équipe
        # n'existe pas encore dans les dictionnaires
        if team_home not in win_counts:
            win_counts[team_home] = 0
            game_counts[team_home] = 0
        if team_away not in win_counts:
            win_counts[team_away] = 0
            game_counts[team_away] = 0

        # Mettre à jour le nombre de matchs joués
        game_counts[team_home] += 1
        game_counts[team_away] += 1

        # Mettre à jour le nombre de victoires
        if wl_home == "W":
            win_counts[team_home] += 1
        else:
            win_counts[team_away] += 1

# Calculer les ratios de victoire
win_ratios = {team: win_counts[team] / game_counts[team]
              for team in win_counts if game_counts[team] > 0}

# Trouver l'équipe avec le meilleur ratio
best_team = max(win_ratios, key=win_ratios.get)
best_ratio = win_ratios[best_team]

print(best_team, best_ratio)

# On remarque que la meilleure équipe trouvé est le Barcelone FC, qui
# n'est pas une équipe de la NBA. Il s'agissait d'un match d'exibition.
# Ainsi on rajoute une condition pour ne pas prendre en compte les matchs
# d'exibition. On considère qu'une équipe doit ainsi apparaitre dans plus de
# 30 matchs de la base de donné.


# Calculer les ratios de victoire
win_ratios = {team: win_counts[team] / game_counts[team]
              for team in win_counts if game_counts[team] > 30}

# Trouver l'équipe avec le meilleur ratio
best_team = max(win_ratios, key=win_ratios.get)
best_ratio = win_ratios[best_team]

print(best_team, best_ratio)

# L'équipe avec le meilleur ratio de victoire est les Lakers de Los Angeles
