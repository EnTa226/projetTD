import csv
from collections import defaultdict

# Dictionnaire pour stocker les équipes par joueur
player_teams = defaultdict(set)

# Lecture du fichier CSV
with open("common_player_info.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        player_name = row["player_name"]
        team_name = row["team_name"]

        if team_name:  # éviter les lignes vides
            player_teams[player_name].add(team_name)

# Trouver le joueur avec le plus d'équipes
most_teams_player = max(player_teams.items(), key=lambda x: len(x[1]))
most_teams_name = most_teams_player[0]
most_teams_count = len(most_teams_player[1])

# Résultat
print(f"Le joueur ayant joué pour le plus d'équipes est {most_teams_name} avec {most_teams_count} équipes différentes.")
