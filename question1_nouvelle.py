import csv
from collections import defaultdict
from datetime import datetime

# On stocke uniquement les matchs de Playoffs
with open("game.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    playoffs_games = [row for row in reader if row["season_type"] == "Playoffs"]

# === 2. Grouper les matchs par saison ===
seasons = defaultdict(list)
for row in playoffs_games:
    seasons[row["season_id"]].append(row)

# === 3. Trouver le dernier match de chaque saison ===
champions = []
for season_id, matches in seasons.items():
    # Trier les matchs par date (format avec heure incluse)
    matches.sort(key=lambda x: datetime.strptime(x["game_date"], "%Y-%m-%d %H:%M:%S"))
    last_game = matches[-1]

    # Déterminer le gagnant du dernier match
    if last_game["wl_home"] == "W":
        winner = last_game["team_abbreviation_home"]
    else:
        winner = last_game["team_abbreviation_away"]

    champions.append(winner)

# === 4. Compter les titres pour chaque équipe ===
win_counts = defaultdict(int)
for team in champions:
    win_counts[team] += 1

# === 5. Filtrer les équipes ayant gagné au moins 3 fois ===
top_teams = [team for team, count in win_counts.items() if count >= 3]

# === 6. Afficher le résultat ===
print("Les équipes ayant gagné au moins 3 fois une saison NBA sont :")
for team in top_teams:
    print(f"- {team} ({win_counts[team]} titres)")