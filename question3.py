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

print(best_team, best_ratio)

# On veut au minimum 30 matchs joués

eligible_teams = total_games[total_games >= 30].index

filtered_wins = total_wins[eligible_teams]
filtered_games = total_games[eligible_teams]
win_ratio = (filtered_wins / filtered_games).dropna()

# Pour les équipes avec plus de 30 matchs
best_team = win_ratio.idxmax()
best_ratio = win_ratio.max()

print(best_team, best_ratio)

# L'équipe avec le meilleur ratio de victoire est les Lakers de Los Angeles
