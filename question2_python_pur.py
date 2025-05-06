# Fonction pour lire un fichier CSV et retourner les données sous forme de liste de dictionnaires
def read_csv(file_path, delimiter=','):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    headers = lines[0].strip().split(delimiter)
    data = []
    for line in lines[1:]:
        values = line.strip().split(delimiter)
        data.append(dict(zip(headers, values)))
    return data

# Fonction pour convertir une date en tuple (année, mois, jour)
def parse_date(date_str):
    date_part = date_str.split(' ')[0]  # Prendre seulement la partie date
    year, month, day = map(int, date_part.split('-'))
    return year, month, day

# Lire les données des fichiers CSV
game_data = read_csv('game.csv')
teams_conferences_data = read_csv('teams_conferences.csv', delimiter=';')

# Convertir les dates en tuples (année, mois, jour) pour comparaison
for game in game_data:
    game['game_date'] = parse_date(game['game_date'])

# Filtrer les données pour la saison régulière 2022-2023
debut_saison_22_23 = (2022, 10, 18)
fin_saison_22_23 = (2023, 4, 12)

game_reg_season_22_23 = [
    game for game in game_data
    if debut_saison_22_23 <= game['game_date'] <= fin_saison_22_23
    and game['season_type'] == 'Regular Season'
]

# Compter le nombre total de matchs joués par chaque équipe
total_games = {}
for game in game_reg_season_22_23:
    total_games[game['team_abbreviation_home']] = total_games.get(
        game['team_abbreviation_home'], 0) + 1
    total_games[game['team_abbreviation_away']] = total_games.get(
        game['team_abbreviation_away'], 0) + 1

# Compter le nombre de victoires par équipe
wins = {}
for game in game_reg_season_22_23:
    winner = (
        game['team_abbreviation_home']
        if game['wl_home'] == 'W'
        else game['team_abbreviation_away']
    )
    wins[winner] = wins.get(winner, 0) + 1

# Calculer le ratio de victoires
ratio = {team: wins[team] / total_games[team] for team in wins}

# Calculer le nombre total de points marqués par chaque équipe
points = {}
for game in game_reg_season_22_23:
    points[game['team_abbreviation_home']] = points.get(game['team_abbreviation_home'], 0) + float(game['pts_home'])
    points[game['team_abbreviation_away']] = points.get(game['team_abbreviation_away'], 0) + float(game['pts_away'])

# Calculer la moyenne des points marqués par match
avg_points = {team: points[team] / total_games[team] for team in points}

# Convertir les données de conférence en dictionnaire pour un accès rapide
teams_conferences = {team['abbreviation']: team['conf'] for team in teams_conferences_data}

# Ajouter les informations de conférence aux ratios
ratio_with_conference = [{'abbreviation': team, 'Win Ratio': ratio[team], 'Avg Points': avg_points[team], 'conf': teams_conferences[team]} for team in ratio]

# Fonction pour trier les équipes par ratio de victoires décroissant, puis par moyenne de points décroissante
def sort_by_win_ratio_and_points(teams):
    return sorted(teams, key=lambda x: (x['Win Ratio'], x['Avg Points']), reverse=True)

# Trier les équipes
ratio_with_conference = sort_by_win_ratio_and_points(ratio_with_conference)

# Fonction pour ajouter le classement
def add_ranking(teams):
    rank = 1
    for team in teams:
        team['classement'] = rank
        rank += 1

# Classement conférence Ouest
classement_west = [team for team in ratio_with_conference if team['conf'] == 'W']
add_ranking(classement_west)
print("Classement Conférence Ouest:")
for team in classement_west:
    print(f"{team['classement']}: {team['abbreviation']} - Win Ratio: {team['Win Ratio']:.3f} - Avg Points: {team['Avg Points']:.2f}")

# Classement conférence Est
classement_east = [team for team in ratio_with_conference if team['conf'] == 'E']
add_ranking(classement_east)
print("\nClassement Conférence Est:")
for team in classement_east:
    print(f"{team['classement']}: {team['abbreviation']} - Win Ratio: {team['Win Ratio']:.3f} - Avg Points: {team['Avg Points']:.2f}")
