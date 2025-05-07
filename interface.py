import tkinter as tk
from tkinter import scrolledtext
from collections import defaultdict
from datetime import datetime
import csv
import inspect

# === FONCTIONS DE QUESTION ===

def run_question_1():
    import pandas as pd
    from collections import defaultdict
    from datetime import datetime

    # === 1. Charger le fichier CSV avec pandas et filtrer les Playoffs ===
    df = pd.read_csv("game.csv")
    playoffs_df = df[df["season_type"] == "Playoffs"]

    # === 2. Grouper les matchs par saison ===
    seasons = defaultdict(list)
    for _, row in playoffs_df.iterrows():
        seasons[row["season_id"]].append(row)

    # === 3. Trouver le dernier match de chaque saison ===
    champions = []
    for season_id, matches in seasons.items():
        # Trier les matchs par date
        matches.sort(key=lambda x: datetime.strptime(
            x["game_date"], "%Y-%m-%d %H:%M:%S"))
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

    # === 6. Retourner le résultat formaté ===
    output = "Les équipes ayant gagné au moins 3 fois une saison NBA sont :\n"
    for team in top_teams:
        output += f"- {team} ({win_counts[team]} titres)\n"

    return output



# === CODE SOURCE A AFFICHER POUR CHAQUE QUESTION ===

code_question_1 = """import pandas as pd
from collections import defaultdict
from datetime import datetime

# === 1. Charger le fichier CSV avec pandas et filtrer les Playoffs ===
df = pd.read_csv("game.csv")
playoffs_df = df[df["season_type"] == "Playoffs"]

# === 2. Grouper les matchs par saison ===
seasons = defaultdict(list)
for _, row in playoffs_df.iterrows():
    seasons[row["season_id"]].append(row)

# === 3. Trouver le dernier match de chaque saison ===
champions = []
for season_id, matches in seasons.items():
    # Trier les matchs par date
    matches.sort(key=lambda x: datetime.strptime(
        x["game_date"], "%Y-%m-%d %H:%M:%S"))
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
"""

def run_question_2():
    import pandas as pd
    import numpy as np

    # Charger les données
    game = pd.read_csv('game.csv')
    game_reg_season_22_23 = game[(game["season_id"] == 22022)
                                 & (game["season_type"] == "Regular Season")]

    # Ajouter une colonne pour le vainqueur
    game_reg_season_22_23["winner"] = np.where(
        game_reg_season_22_23["wl_home"] == "W",
        game_reg_season_22_23["team_abbreviation_home"],
        game_reg_season_22_23["team_abbreviation_away"]
    )

    # Calculer le ratio de victoires
    total_games = (game_reg_season_22_23['team_abbreviation_home'].value_counts() +
                   game_reg_season_22_23['team_abbreviation_away'].value_counts())
    wins = game_reg_season_22_23['winner'].value_counts()
    ratio = (wins / total_games).reset_index()
    ratio.columns = ['abbreviation', 'Win Ratio']

    # Calculer le nombre total de points marqués par chaque équipe
    points_home = game_reg_season_22_23.groupby('team_abbreviation_home')['pts_home'].sum()
    points_away = game_reg_season_22_23.groupby('team_abbreviation_away')['pts_away'].sum()
    total_points = points_home.add(points_away, fill_value=0)

    # Calculer la moyenne des points marqués par match
    avg_points = (total_points / total_games).reset_index()
    avg_points.columns = ['abbreviation', 'Avg Points']

    # Fusionner les données
    ratio_df = pd.merge(ratio, avg_points, on='abbreviation')
    teams_conferences = pd.read_csv('teams_conferences.csv', sep=';')
    ratio_df = pd.merge(ratio_df, teams_conferences, on='abbreviation')

    # Trier les équipes
    ratio_df = ratio_df.sort_values(by=['Win Ratio', 'Avg Points'], ascending=[False, False])
    ratio_df['Win Ratio'] = ratio_df['Win Ratio'].round(3)
    ratio_df['Avg Points'] = ratio_df['Avg Points'].round(2)

    # Classement conférence Ouest
    classement_west = ratio_df[ratio_df['conf'] == 'W'].copy()
    classement_west['classement'] = classement_west['Win Ratio'].rank(ascending=False, method='first').astype(int)

    # Classement conférence Est
    classement_east = ratio_df[ratio_df['conf'] == 'E'].copy()
    classement_east['classement'] = classement_east['Win Ratio'].rank(ascending=False, method='first').astype(int)

    # Formatage du résultat à retourner
    output = "Classement Conférence Ouest :\n"
    output += classement_west[['classement', 'abbreviation', 'Win Ratio', 'Avg Points']].to_string(index=False)
    output += "\n\nClassement Conférence Est :\n"
    output += classement_east[['classement', 'abbreviation', 'Win Ratio', 'Avg Points']].to_string(index=False)

    return output



code_question_2 = """import tkinter as tk
from tkinter import scrolledtext
import inspect
import sys

# --- Classe pour rediriger les print() ---
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)

    def flush(self):
        pass

# --- Fenêtre Tkinter générique ---
def open_window(titre, fonction, code, besoin_annee=False):
    win = tk.Toplevel()
    win.title(titre)
    win.geometry("700x600")

    # --- Affichage du code source ---
    tk.Label(win, text="Code de la question :", font=("Arial", 12, "bold")).pack(pady=5)
    text_code = scrolledtext.ScrolledText(win, height=15, wrap="word")
    text_code.insert(tk.END, code)
    text_code.configure(state="disabled")
    text_code.pack(fill="both", expand=True, padx=10)

    # --- Zone de résultat ---
    tk.Label(win, text="Résultat :", font=("Arial", 12, "bold")).pack(pady=5)
    result_text = scrolledtext.ScrolledText(win, height=8, wrap="word")
    result_text.configure(state="disabled")
    result_text.pack(fill="both", expand=False, padx=10)

    # --- Helpers internes ---
    def run_with_arg():
        annee = entry.get()
        try:
            sig = inspect.signature(fonction)
            if len(sig.parameters) == 2:
                fonction(annee, result_text)
            else:
                res = fonction(annee)
                result_text.configure(state="normal")
                result_text.delete("1.0", tk.END)
                if res is not None:
                    result_text.insert(tk.END, res)
                result_text.configure(state="disabled")
        except Exception as e:
            result_text.configure(state="normal")
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Erreur : {e}")
            result_text.configure(state="disabled")

    def run_direct():
        try:
            sig = inspect.signature(fonction)
            result_text.configure(state="normal")
            result_text.delete("1.0", tk.END)

            # --- Redirection stdout vers interface ---
            old_stdout = sys.stdout
            sys.stdout = TextRedirector(result_text)

            if len(sig.parameters) == 1:
                fonction(result_text)
            else:
                res = fonction()
                if res is not None:
                    print(res)

            sys.stdout = old_stdout
            result_text.configure(state="disabled")
        except Exception as e:
            sys.stdout = old_stdout
            result_text.configure(state="normal")
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Erreur : {e}")
            result_text.configure(state="disabled")

    # --- Choix d'exécution selon besoin année ---
    if besoin_annee:
        tk.Label(win, text="Entrez une année (ex: 2005) :").pack(pady=5)
        entry = tk.Entry(win)
        entry.pack(pady=5)
        btn = tk.Button(win, text="Exécuter", command=run_with_arg)
    else:
        btn = tk.Button(win, text="Exécuter", command=run_direct)
    btn.pack(pady=10)

"""

code_question_2bis = '''
# Fonction pour lire un fichier CSV et retourner les données
# sous forme de liste de dictionnaires
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

# Convertir les dates en tuples (année, mois, jour)
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
    points[game['team_abbreviation_home']] = points.get(
        game['team_abbreviation_home'], 0) + float(game['pts_home'])
    points[game['team_abbreviation_away']] = points.get(
        game['team_abbreviation_away'], 0) + float(game['pts_away'])

# Calculer la moyenne de points marqués par match
moy_points = {team: points[team] / total_games[team] for team in points}

# Convertir les données de conférence en dictionnaire pour un accès rapide
teams_conferences = {team['abbreviation']: team['conf']
                     for team in teams_conferences_data}

# Ajouter les informations de conférence aux ratios
ratio_with_conference = [{'abbreviation': team, 'Win Ratio': ratio[team],
                          'Points en moyenne': moy_points[team],
                          'conf': teams_conferences[team]} for team in ratio]


# Fonction pour trier les équipes par ratio de victoires, par moyenne de points
def sort_by_win_ratio_and_points(teams):
    return sorted(teams, key=lambda x: (x['Win Ratio'],
                                        x['Points en moyenne']),
                  reverse=True)


# Trier les équipes
ratio_with_conference = sort_by_win_ratio_and_points(ratio_with_conference)


# Fonction pour ajouter le classement
def add_ranking(teams):
    rank = 1
    for team in teams:
        team['classement'] = rank
        rank += 1


# Classement conférence Ouest
classement_west = [team for team
                   in ratio_with_conference if team['conf'] == 'W']
add_ranking(classement_west)
print("Classement Conférence Ouest:")
for team in classement_west:
    print(
        f"{team['classement']}: {team['abbreviation']} - Win Ratio: "
        f"{team['Win Ratio']:.3f} - "
        f"Points en moyenne: {team['Points en moyenne']:.2f}"
    )


# Classement conférence Est
classement_east = [
    team for team in ratio_with_conference if team['conf'] == 'E']
add_ranking(classement_east)
print("\nClassement Conférence Est:")
for team in classement_east:
    print(
        f"{team['classement']}: {team['abbreviation']} - Win Ratio: "
        f"{team['Win Ratio']:.3f} - "
        f"Points en moyenne: {team['Points en moyenne']:.2f}"
    )
'''

def run_question_2bis():
    def read_csv(file_path, delimiter=','):
        with open(file_path, 'r') as f:
            lines = f.readlines()
        headers = lines[0].strip().split(delimiter)
        return [dict(zip(headers, line.strip().split(delimiter))) for line in lines[1:]]

    def parse_date(date_str):
        date = date_str.split(' ')[0]
        y, m, d = map(int, date.split('-'))
        return (y, m, d)

    game_data = read_csv('game.csv')
    teams_conf = read_csv('teams_conferences.csv', delimiter=';')

    for game in game_data:
        game['game_date'] = parse_date(game['game_date'])

    debut = (2022, 10, 18)
    fin = (2023, 4, 12)

    season_games = [g for g in game_data if debut <= g['game_date'] <= fin and g['season_type'] == 'Regular Season']

    total_games = {}
    wins = {}
    points = {}

    for g in season_games:
        home, away = g['team_abbreviation_home'], g['team_abbreviation_away']
        total_games[home] = total_games.get(home, 0) + 1
        total_games[away] = total_games.get(away, 0) + 1

        if g['wl_home'] == 'W':
            wins[home] = wins.get(home, 0) + 1
        else:
            wins[away] = wins.get(away, 0) + 1

        points[home] = points.get(home, 0) + float(g['pts_home'])
        points[away] = points.get(away, 0) + float(g['pts_away'])

    confs = {team['abbreviation']: team['conf'] for team in teams_conf}

    teams = []
    for team in wins:
        ratio = wins[team] / total_games[team]
        avg_pts = points[team] / total_games[team]
        teams.append({'abbr': team, 'ratio': ratio, 'avg_pts': avg_pts, 'conf': confs[team]})

    teams.sort(key=lambda x: (x['ratio'], x['avg_pts']), reverse=True)

    output = ""
    rank = 1
    output += "Conférence Ouest :\n"
    for t in [t for t in teams if t['conf'] == 'W']:
        output += f"{rank}. {t['abbr']} - Ratio: {t['ratio']:.3f}, Moy. points: {t['avg_pts']:.2f}\n"
        rank += 1

    rank = 1
    output += "\nConférence Est :\n"
    for t in [t for t in teams if t['conf'] == 'E']:
        output += f"{rank}. {t['abbr']} - Ratio: {t['ratio']:.3f}, Moy. points: {t['avg_pts']:.2f}\n"
        rank += 1

    return output



def run_question_3():
    import pandas as pd

    # Partie pandas
    fichier = "game.csv"
    df = pd.read_csv(fichier)

    home_wins = df[df["wl_home"] == "W"].groupby("team_name_home")["wl_home"].count()
    away_wins = df[df["wl_home"] == "L"].groupby("team_name_away")["wl_home"].count()
    total_wins = home_wins.add(away_wins, fill_value=0)

    home_games = df.groupby("team_name_home")["wl_home"].count()
    away_games = df.groupby("team_name_away")["wl_home"].count()
    total_games = home_games.add(away_games, fill_value=0)

    win_ratio = (total_wins / total_games).dropna()
    best_team_pandas = win_ratio.idxmax()
    best_ratio_pandas = win_ratio.max()

    # Partie en lecture brute ligne par ligne
    win_counts = {}
    game_counts = {}

    with open("game.csv", "r", encoding="utf-8") as file:
        header = file.readline().strip().split(",")
        team_home_idx = header.index("team_name_home")
        team_away_idx = header.index("team_name_away")
        wl_home_idx = header.index("wl_home")

        for line in file:
            columns = line.strip().split(",")

            team_home = columns[team_home_idx]
            team_away = columns[team_away_idx]
            wl_home = columns[wl_home_idx]

            if team_home not in win_counts:
                win_counts[team_home] = 0
                game_counts[team_home] = 0
            if team_away not in win_counts:
                win_counts[team_away] = 0
                game_counts[team_away] = 0

            game_counts[team_home] += 1
            game_counts[team_away] += 1

            if wl_home == "W":
                win_counts[team_home] += 1
            else:
                win_counts[team_away] += 1

    # Avec filtrage > 30 matchs
    win_ratios_filtered = {
        team: win_counts[team] / game_counts[team]
        for team in win_counts if game_counts[team] > 30
    }

    best_team_filtered = max(win_ratios_filtered, key=win_ratios_filtered.get)
    best_ratio_filtered = win_ratios_filtered[best_team_filtered]

    output = (
        f"Résultat avec pandas :\n"
        f" - Meilleure équipe : {best_team_pandas} ({best_ratio_pandas:.3f})\n\n"
        f"Résultat avec condition de > 30 matchs) :\n"
        f" - Meilleure équipe : {best_team_filtered} ({best_ratio_filtered:.3f})"
    )

    return output  # <-- obligatoire



code_q3_pur="""# Dictionnaires pour stocker les victoires et matchs joués
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

        # Initialiser les compteurs si l'équipe n'existe pas
        # encore dans les dictionnaires
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
# On ne prend en compte que les équipes ayant joué plus de 30 matchs
win_ratios = {team: win_counts[team] / game_counts[team]
              for team in win_counts if game_counts[team] >= 30}

# Trouver l'équipe avec le meilleur ratio
best_team = max(win_ratios, key=win_ratios.get)
best_ratio = win_ratios[best_team]

print(best_team, best_ratio)


# L'équipe avec le meilleur ratio de victoire est les Lakers de Los Angeles
"""

def run_question_3_bis():
    win_counts = {}
    game_counts = {}

    with open("game.csv", "r", encoding="utf-8") as file:
        header = file.readline().strip().split(",")
        team_home_idx = header.index("team_name_home")
        team_away_idx = header.index("team_name_away")
        wl_home_idx = header.index("wl_home")

        for line in file:
            columns = line.strip().split(",")
            if len(columns) <= max(team_home_idx, team_away_idx, wl_home_idx):
                continue  # skip lignes incomplètes

            team_home = columns[team_home_idx]
            team_away = columns[team_away_idx]
            wl_home = columns[wl_home_idx]

            for team in (team_home, team_away):
                if team not in win_counts:
                    win_counts[team] = 0
                    game_counts[team] = 0

            game_counts[team_home] += 1
            game_counts[team_away] += 1

            if wl_home == "W":
                win_counts[team_home] += 1
            elif wl_home == "L":
                win_counts[team_away] += 1

    # Ne garder que les équipes ayant joué au moins 30 matchs
    win_ratios = {
        team: win_counts[team] / game_counts[team]
        for team in win_counts if game_counts[team] > 30
    }

    best_team = max(win_ratios, key=win_ratios.get)
    best_ratio = win_ratios[best_team]

    return f"L'équipe avec le meilleur ratio de victoire est : {best_team} ({best_ratio:.2%})"

code_question_3_bis="""# Dans un premier temps avec pandas:

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

# L'équipe avec le meilleur ratio de victoire est les Lakers de Los Angeles"""


code_q4 = """import pandas as pd

# Charger les données
game = pd.read_csv('game.csv', sep=',')
game = game.dropna(subset=['fg3_pct_home', 'fg3_pct_away'])

# Filtrer les données pour ne pas avoir en sorti une équipe qui
# n'est pas une équipe NBA (ex: All-Star, Moscow CSKA, etc.)
game = game[(game['season_type'] == 'Regular Season')
            | (game['season_type'] == 'Playoffs')]

# Convertir la colonne season_id en chaîne de caractères
game['season_id'] = game['season_id'].astype(str)

# Déterminer l'année qui nous intéresse
year = input("Entrez l'année de la saison à partir de 1986 (ex: 2005) : ")

if not year.isdigit() or int(year) < 1986 or int(year) >= 2023:
    print(f"Aucune donnée trouvée pour la saison {year}.")
else:
    game_year = game[game["season_id"].str.contains(year)]
    game_year = game[game["season_id"].str.contains(year)]

    # Compter le nombre de matchs pour chaque équipe à domicile
    home_counts = game_year['team_abbreviation_home'].value_counts()

    # Compter le nombre de matchs pour chaque équipe à l'extérieur
    away_counts = game_year['team_abbreviation_away'].value_counts()

    # Total des matchs joués par équipe
    total_counts = home_counts + away_counts

    # Calculer les pourcentages de réussite
    home_fg3_pct = game_year.groupby('team_abbreviation_home'
                                     )['fg3_pct_home'].sum()
    away_fg3_pct = game_year.groupby('team_abbreviation_away'
                                     )['fg3_pct_away'].sum()
    total_fg3_pct = home_fg3_pct.add(away_fg3_pct, fill_value=0)

    # Moyenne des % de réussite à 3 points
    reussite_3 = total_fg3_pct / total_counts

    # Mise en forme du DataFrame
    reussite_3_df = reussite_3.reset_index()
    reussite_3_df.columns = ['team_abbreviation', 'reussite_3']
    reussite_3_df_sorted = reussite_3_df.sort_values(
        by='reussite_3', ascending=False
    ).reset_index(drop=True)

    # Charger les données à partir du fichier CSV
    team_csv = pd.read_csv('team.csv')

    # Créer un dictionnaire pour mapper les abréviations aux noms complets
    team_dict = game.set_index(
        'team_abbreviation_home')['team_name_home'].to_dict()

    # Obtenir le nom complet de l'équipe à partir de son abréviation
    def get_full_name(abbreviation):
        return team_dict.get(abbreviation)

    # Afficher l'équipe avec le plus de réussite aux trois points
    top_team_abbreviation = reussite_3_df_sorted.iloc[0]['team_abbreviation']

    print(
        (f"L'équipe avec le plus de réussite aux "
         f"trois points pour la saison {year} "
         f"sont les {get_full_name(top_team_abbreviation)} "
         f"avec un ratio de "
         f"{round(reussite_3_df_sorted.iloc[0]['reussite_3'], 3)}.")
        )
"""


def run_question_4(annee):
    import pandas as pd
    try:
        annee_int = int(annee)
        if annee_int < 1986 or annee_int >= 2023:
            return f"Aucune donnée trouvée pour la saison {annee}."

        game = pd.read_csv('game.csv', sep=',')
        game = game.dropna(subset=['fg3_pct_home', 'fg3_pct_away'])

        # Filtrage NBA uniquement
        game = game[(game['season_type'] == 'Regular Season') |
                    (game['season_type'] == 'Playoffs')]

        game['season_id'] = game['season_id'].astype(str)
        game_year = game[game['season_id'].str.contains(annee)]

        if game_year.empty:
            return f"Aucune donnée disponible pour la saison {annee}."

        home_counts = game_year['team_abbreviation_home'].value_counts()
        away_counts = game_year['team_abbreviation_away'].value_counts()
        total_counts = home_counts.add(away_counts, fill_value=0)

        home_fg3_pct = game_year.groupby('team_abbreviation_home')['fg3_pct_home'].sum()
        away_fg3_pct = game_year.groupby('team_abbreviation_away')['fg3_pct_away'].sum()
        total_fg3_pct = home_fg3_pct.add(away_fg3_pct, fill_value=0)

        reussite_3 = total_fg3_pct / total_counts
        reussite_3_df = reussite_3.reset_index()
        reussite_3_df.columns = ['team_abbreviation', 'reussite_3']
        reussite_3_df_sorted = reussite_3_df.sort_values(by='reussite_3', ascending=False).reset_index(drop=True)

        # Dictionnaire des noms d'équipe
        team_dict = game.set_index('team_abbreviation_home')['team_name_home'].to_dict()

        top_team_abbr = reussite_3_df_sorted.iloc[0]['team_abbreviation']
        top_team_name = team_dict.get(top_team_abbr, top_team_abbr)
        top_pct = round(reussite_3_df_sorted.iloc[0]['reussite_3'], 3)

        return (f"L'équipe avec le plus de réussite aux "
                f"trois points pour la saison {annee} "
                f"est {top_team_name} avec un ratio de {top_pct}.")

    except Exception as e:
        return f"Erreur lors de l'exécution : {str(e)}"


# Question 5 : équipe avec le plus de matchs gagnés par saison

code_question_5 = '''
# Quelle est l'équipe ayant eu le plus de joueurs qui ne sont pas
# arrivé en NBA par la draft ?

import pandas as pd

# On charge le fichier CSV
df = pd.read_csv('common_player_info.csv')

# On garde que les joueurs qui n'ont pas été draftés
# On remarque que la colonne 'draft_year' contient l'année
# de draft ou 'Undrafted'
undrafted_players = df[df['draft_year'] == 'Undrafted']

# On compte le nombre de joueurs "Undrafted" par équipe ( colone team_name)

undrafted_counts = undrafted_players['team_name'].value_counts()

# Afficher les résultats
print(undrafted_counts[0:1])

# Il s'agit donc de l'équipe des Hawks
'''

def run_question_5(annee):
    import pandas as pd

    # Charger les données
    df = pd.read_csv('common_player_info.csv')

    # Vérification de l'année en tant qu'entier
    try:
        annee = int(annee)
    except ValueError:
        return f"Année invalide : {annee}"

    # Garder les joueurs non draftés
    undrafted_players = df[df['draft_year'] == 'Undrafted']

    # Filtrer par année (dans 'from_year' et 'to_year')
    actifs_cette_annee = undrafted_players[
        (undrafted_players['from_year'] <= annee) & (undrafted_players['to_year'] >= annee)
    ]

    if actifs_cette_annee.empty:
        return f"Aucun joueur non drafté n'était actif en {annee}."

    # Compter les joueurs non draftés par équipe
    undrafted_counts = actifs_cette_annee['team_name'].value_counts()

    top_team = undrafted_counts.idxmax()
    top_count = undrafted_counts.max()

    return (f"En {annee}, l'équipe ayant eu le plus de joueurs non draftés "
            f"était les {top_team} avec {top_count} joueur(s) non drafté(s).")


code_q6 = """
import pandas as pd


def convert_height_to_cm(height_str):
    try:
        feet, inches = map(int, height_str.split("-"))
        return round(feet * 30.48 + inches * 2.54, 2)
    except (ValueError, AttributeError):
        return None


df = pd.read_csv("common_player_info.csv")

# Nettoyage / conversion
df["draft_number"] = pd.to_numeric(df["draft_number"], errors="coerce")
df["height_cm"] = df["height"].apply(convert_height_to_cm)

# Filtrage et groupement
draft_1 = df[df["draft_number"] == 1]
mean_heights_1 = draft_1.groupby("position")["height_cm"].mean()

draft_30 = df[df["draft_number"] == 30]
mean_heights_30 = draft_30.groupby("position")["height_cm"].mean()

# Affichage
print("Taille des No1 de draft (en cm) par poste :")
print(mean_heights_1)

print("\nTaille des No30 de draft (en cm) par poste :")
print(mean_heights_30)
"""


def run_question_6():
    import pandas as pd

    def convert_height_to_cm(height_str):
        try:
            feet, inches = map(int, height_str.split("-"))
            return round(feet * 30.48 + inches * 2.54, 2)
        except (ValueError, AttributeError):
            return None

    df = pd.read_csv("common_player_info.csv")

    # Nettoyage / conversion
    df["draft_number"] = pd.to_numeric(df["draft_number"], errors="coerce")
    df["height_cm"] = df["height"].apply(convert_height_to_cm)

    # Filtrage et groupement
    draft_1 = df[df["draft_number"] == 1]
    mean_heights_1 = draft_1.groupby("position")["height_cm"].mean()

    draft_30 = df[df["draft_number"] == 30]
    mean_heights_30 = draft_30.groupby("position")["height_cm"].mean()

    # Affichage
    print("Taille des No1 de draft (en cm) par poste :")
    print(mean_heights_1)

    print("\nTaille des No30 de draft (en cm) par poste :")
    print(mean_heights_30)

code_q6_bis = """

# Lecture manuelle du fichier
with open("common_player_info.csv", encoding="utf-8") as f:
    lines = f.readlines()

# Extraction de l'en-tête (colonnes)
headers = lines[0].strip().split(",")
data = []


# Fonction pour obtenir une taille en cm
def convert_height_to_cm(height_str):
    try:
        feet, inches = map(int, height_str.split("-"))
        return round(feet * 30.48 + inches * 2.54, 2)
    except (ValueError, AttributeError):
        return None


# Parse ligne par ligne
for line in lines[1:]:
    values = line.strip().split(",")

    # Gérer les valeurs contenant des virgules entre guillemets
    while len(values) > len(headers):
        for i in range(len(values) - 1):
            if values[i].startswith('"') and not values[i].endswith('"'):
                values[i] = values[i] + "," + values.pop(i + 1)
                break

    # Crée un dictionnaire pour chaque joueur
    player = {headers[i]: values[i].strip('"') if i < len(values) else ""
              for i in range(len(headers))}
    data.append(player)

# Nettoyage des données
for player in data:
    try:
        player["draft_number"] = int(player["draft_number"])
    except ValueError:
        player["draft_number"] = None

    player["height_cm"] = convert_height_to_cm(player.get("height", ""))


# Fonction pour calculer la moyenne par position
def mean_height_by_position(players, draft_target):
    position_totals = {}
    position_counts = {}

    for p in players:
        if p["draft_number"] == draft_target and p["height_cm"] is not None:
            pos = p["position"]
            position_totals[pos] = position_totals.get(pos, 0) + p["height_cm"]
            position_counts[pos] = position_counts.get(pos, 0) + 1

    return {pos: round(position_totals[pos] / position_counts[pos], 2)
            for pos in position_totals}


# Affichage
print("Taille des No1 de draft (en cm) par poste :")
for pos, avg in mean_height_by_position(data, 1).items():
    print(f"{pos}: {avg} cm")

print("\nTaille des No30 de draft (en cm) par poste :")
for pos, avg in mean_height_by_position(data, 30).items():
    print(f"{pos}: {avg} cm")
"""

def run_question_6_bis():
    # Lecture manuelle du fichier
    with open("common_player_info.csv", encoding="utf-8") as f:
        lines = f.readlines()

    # Extraction de l'en-tête (colonnes)
    headers = lines[0].strip().split(",")
    data = []

    # Fonction pour obtenir une taille en cm
    def convert_height_to_cm(height_str):
        try:
            feet, inches = map(int, height_str.split("-"))
            return round(feet * 30.48 + inches * 2.54, 2)
        except (ValueError, AttributeError):
            return None

    # Parse ligne par ligne
    for line in lines[1:]:
        values = line.strip().split(",")

        while len(values) > len(headers):
            for i in range(len(values) - 1):
                if values[i].startswith('"') and not values[i].endswith('"'):
                    values[i] = values[i] + "," + values.pop(i + 1)
                    break

        player = {headers[i]: values[i].strip('"') if i < len(values) else ""
                  for i in range(len(headers))}
        data.append(player)

    # Nettoyage des données
    for player in data:
        try:
            player["draft_number"] = int(player["draft_number"])
        except ValueError:
            player["draft_number"] = None

        player["height_cm"] = convert_height_to_cm(player.get("height", ""))

    # Fonction pour calculer la moyenne par position
    def mean_height_by_position(players, draft_target):
        position_totals = {}
        position_counts = {}

        for p in players:
            if p["draft_number"] == draft_target and p["height_cm"] is not None:
                pos = p["position"]
                position_totals[pos] = position_totals.get(pos, 0) + p["height_cm"]
                position_counts[pos] = position_counts.get(pos, 0) + 1

        return {pos: round(position_totals[pos] / position_counts[pos], 2)
                for pos in position_totals}

    # Affichage
    print("Taille des No1 de draft (en cm) par poste :")
    for pos, avg in mean_height_by_position(data, 1).items():
        print(f"{pos}: {avg} cm")

    print("\nTaille des No30 de draft (en cm) par poste :")
    for pos, avg in mean_height_by_position(data, 30).items():
        print(f"{pos}: {avg} cm")


code_question_7 = '''
import pandas as pd
import matplotlib.pyplot as plt


def convert_height_to_cm(height_str):
    try:
        feet, inches = map(int, height_str.split("-"))
        return round(feet * 30.48 + inches * 2.54, 2)
    except (ValueError, AttributeError):
        return None


# Chargement des données
df = pd.read_csv("common_player_info.csv")

# Conversion des tailles
df["height_cm"] = df["height"].apply(convert_height_to_cm)

# Suppression des lignes avec tailles manquantes ou poste manquant
df_clean = df.dropna(subset=["height_cm", "position"])

# Création du boxplot
plt.figure(figsize=(10, 6))
df_clean.boxplot(column="height_cm", by="position")
plt.title("Répartition des tailles (en cm) des joueurs par poste")
plt.suptitle("")  # Supprime le titre automatique "Boxplot grouped by position"
plt.xlabel("Poste")
plt.ylabel("Taille (cm)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()


# Display the plot
plt.show()
'''

def run_question_7():
    import pandas as pd
    import matplotlib.pyplot as plt

    def convert_height_to_cm(height_str):
        try:
            feet, inches = map(int, height_str.split("-"))
            return round(feet * 30.48 + inches * 2.54, 2)
        except:
            return None

    try:
        df = pd.read_csv("common_player_info.csv")
        df["height_cm"] = df["height"].apply(convert_height_to_cm)
        df_clean = df.dropna(subset=["height_cm", "position"])

        if df_clean.empty:
            return "Aucune donnée exploitable (vérifiez la colonne 'height' ou 'position')."

        plt.figure(figsize=(10, 6))
        df_clean.boxplot(column="height_cm", by="position")
        plt.title("Répartition des tailles (en cm) des joueurs par poste")
        plt.suptitle("")
        plt.xlabel("Poste")
        plt.ylabel("Taille (cm)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.tight_layout()
        plt.show()

        return "Boxplot affiché avec succès."

    except Exception as e:
        return f"Erreur : {e}"

code_question_8 = """import pandas as pd
import matplotlib.pyplot as plt

# Charger le DataFrame
draft = pd.read_csv('draft_history.csv')
draft = draft[draft['season'] >= 1984]  # Filtrer les saisons à partir de 1984
draft = draft.dropna(subset=['organization'])

# Compter le nombre de joueurs draftés par an
annual_counts = draft.groupby('season').size()

# Convertir le résultat en DataFrame pour plus de lisibilité
annual_counts_df = annual_counts.reset_index(name='count')
annual_counts_df

# Filtrer les joueurs dont le organization_type est "Other Team/Club"
# et dont le nom de l'organisation contient des parenthèses,
# mais pas "G League" ni "IBL"
draft_stranger = draft[
    (draft['organization_type'] == 'Other Team/Club') &
    (draft['organization'].str.contains(r'\(')) &
    # Utiliser r'\(' pour échapper la parenthèse
    (~draft['organization'].str.contains('IBL')) &
    (~draft['organization'].str.contains('G League'))
    # Filtrer les organisations contenant "G League"
]

# Grouper par année (colonne 'season') et compter les occurrences
strangers_annual_counts = draft_stranger.groupby('season').size()

# Convertir le résultat en DataFrame pour plus de lisibilité
strangers_annual_counts_df = strangers_annual_counts.reset_index(name='count')

# Fusionner les deux DataFrames pour aligner les années
merged_df = pd.merge(annual_counts_df, strangers_annual_counts_df,
                     on='season', how='left', suffixes=('_total', '_stranger'))

# Calculer le ratio
merged_df['ratio'] = (merged_df['count_stranger'] / merged_df['count_total']
                      ) * 100
merged_df

# Tracer un graphique en barres des occurrences par année
plt.figure(figsize=(12, 8))
plt.bar(merged_df['season'], merged_df['ratio'], color='skyblue')
plt.title('Proportion de joueurs étrangers draftés par année')
plt.xlabel('Année')
plt.ylabel('Part de joueurs étrangers (%)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()"""


def run_question_8():
    import pandas as pd
    import matplotlib.pyplot as plt

    draft = pd.read_csv('draft_history.csv')
    draft = draft[draft['season'] >= 1984]
    draft = draft.dropna(subset=['organization'])

    annual_counts = draft.groupby('season').size().reset_index(name='count_total')

    draft_stranger = draft[
        (draft['organization_type'] == 'Other Team/Club') &
        (draft['organization'].str.contains(r'\(')) &
        (~draft['organization'].str.contains('IBL')) &
        (~draft['organization'].str.contains('G League'))
    ]
    strangers_annual_counts = draft_stranger.groupby('season').size().reset_index(name='count_stranger')

    merged_df = pd.merge(annual_counts, strangers_annual_counts, on='season', how='left')
    merged_df['count_stranger'] = merged_df['count_stranger'].fillna(0)
    merged_df['ratio'] = (merged_df['count_stranger'] / merged_df['count_total']) * 100

    # Affichage du graphique
    plt.figure(figsize=(12, 8))
    plt.bar(merged_df['season'], merged_df['ratio'], color='skyblue')
    plt.title('Proportion de joueurs étrangers draftés par année')
    plt.xlabel('Année')
    plt.ylabel('Part de joueurs étrangers (%)')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

    return "Le graphique a été affiché avec succès."


def run_question_9():
    import pandas as pd

    # Charger le fichier CSV
    df = pd.read_csv("common_player_info.csv")

    # Convertir la colonne 'jersey' en chaîne de caractères
    df['jersey'] = df['jersey'].astype(str)

    # Filtrer uniquement les valeurs non nulles et numériques
    df = df[df['jersey'].str.isnumeric()]

    # Convertir les numéros de maillot en entiers
    df['jersey'] = df['jersey'].astype(int)

    # Compter les occurrences de chaque numéro
    top_jerseys = df['jersey'].value_counts().sort_values(ascending=False)

    # Afficher les numéros les plus utilisés
    print("Le numéro de maillot le plus utilisé par les joueurs :")
    print(top_jerseys.head(1))


code_question_9 = """import pandas as pd

# Charger le fichier CSV
df = pd.read_csv("common_player_info.csv")

# Convertir la colonne 'jersey' en chaîne de caractères
df['jersey'] = df['jersey'].astype(str)

# Filtrer uniquement les valeurs non nulles et numériques
df = df[df['jersey'].str.isnumeric()]

# Convertir les numéros de maillot en entiers
df['jersey'] = df['jersey'].astype(int)

# Compter les occurrences de chaque numéro
top_jerseys = df['jersey'].value_counts().sort_values(ascending=False)

# Afficher les numéros les plus utilisés
print("Le numéro de maillot le plus utilisé par les joueurs :")
print(top_jerseys.head(1))
"""
def run_question_10_pure():
    team_points = {}

    with open("other_stats.csv", "r", encoding="utf-8") as f:
        next(f)  # Sauter l'en-tête
        for line in f:
            data = line.strip().split(",")

            # Extraire les infos d'équipes
            team_home = data[3]
            team_away = data[16]

            # Points domicile et extérieur
            pts_home = int(data[5]) + int(data[6]) + int(data[7])
            pts_away = int(data[18]) + int(data[19]) + int(data[20])

            team_points[team_home] = team_points.get(team_home, 0) + pts_home
            team_points[team_away] = team_points.get(team_away, 0) + pts_away

    # Trouver l'équipe avec le plus de points
    top_team = max(team_points, key=team_points.get)
    top_points = team_points[top_team]

    print(
        f"L'équipe avec le plus de points cumulés est {top_team} "
        f"avec {top_points} points."
    )



def run_question_10_pandas():
    import pandas as pd

    # Charger le fichier CSV
    df = pd.read_csv("other_stats.csv")

    # Calcul des points domicile (raquette + seconde chance + contre-attaque)
    df["pts_home_total"] = df.iloc[:, 5] + df.iloc[:, 6] + df.iloc[:, 7]

    # Calcul des points extérieur
    df["pts_away_total"] = df.iloc[:, 18] + df.iloc[:, 19] + df.iloc[:, 20]

    # Additionner les points pour chaque équipe (domicile + extérieur)
    points_home = df.groupby(df.columns[3])["pts_home_total"].sum()
    points_away = df.groupby(df.columns[16])["pts_away_total"].sum()

    # Fusionner les deux résultats
    total_points = points_home.add(points_away, fill_value=0)

    # Trouver l'équipe avec le plus de points
    top_team = total_points.idxmax()
    top_points = int(total_points.max())

    print(
        f"L'équipe avec le plus de points cumulés est {top_team} "
        f"avec {top_points} points."
    )


code_q10_pure = '''team_points = {}


with open("other_stats.csv", "r", encoding="utf-8") as f:
    next(f)  # Sauter l'en-tête
    for line in f:
        data = line.strip().split(",")  # Séparer les valeurs

        # Extraire les informations nécessaires
        team_home = data[3]  # Abréviation équipe domicile
        team_away = data[16]  # Abréviation équipe extérieur

        # Points à additionner
        # Raquette + Seconde chance + Contre-attaque
        pts_home = int(data[5]) + int(data[6]) + int(data[7])
        # Raquette + Seconde chance + Contre-attaque
        pts_away = int(data[18]) + int(data[19]) + int(data[20])

        # Ajouter les points au total de chaque équipe
        team_points[team_home] = team_points.get(team_home, 0) + pts_home
        team_points[team_away] = team_points.get(team_away, 0) + pts_away

# Trouver l'équipe avec le plus de points
top_team = max(team_points, key=team_points.get)
top_points = team_points[top_team]

# Afficher le résultat
print(
    f"L'équipe avec le plus de points cumulés est {top_team} "
    f"avec {top_points} points."
)
'''

code_q10_pandas = '''import pandas as pd

# Charger le fichier CSV
df = pd.read_csv("other_stats.csv")

# Calcul des points domicile (raquette + seconde chance + contre-attaque)
df["pts_home_total"] = df.iloc[:, 5] + df.iloc[:, 6] + df.iloc[:, 7]

# Calcul des points extérieur
df["pts_away_total"] = df.iloc[:, 18] + df.iloc[:, 19] + df.iloc[:, 20]

# Additionner les points pour chaque équipe (domicile + extérieur)
points_home = df.groupby(df.columns[3])["pts_home_total"].sum()
points_away = df.groupby(df.columns[16])["pts_away_total"].sum()

# Fusionner les deux résultats
total_points = points_home.add(points_away, fill_value=0)

# Trouver l'équipe avec le plus de points
top_team = total_points.idxmax()
top_points = int(total_points.max())

# Afficher le résultat
print(
    f"L'équipe avec le plus de points cumulés est {top_team} "
    f"avec {top_points} points."
)
'''



# === FENÊTRE QUESTION DÉDIÉE ===

import tkinter as tk
from tkinter import scrolledtext
import inspect
import sys

# --- Classe pour rediriger les print() ---
class TextRedirector:
    def __init__(self, widget):
        self.widget = widget

    def write(self, text):
        self.widget.insert(tk.END, text)
        self.widget.see(tk.END)

    def flush(self):
        pass

# --- Fenêtre Tkinter générique ---
def open_window(titre, fonction, code, besoin_annee=False):
    win = tk.Toplevel()
    win.title(titre)
    win.geometry("700x600")

    # --- Affichage du code source ---
    tk.Label(win, text="Code de la question :", font=("Arial", 12, "bold")).pack(pady=5)
    text_code = scrolledtext.ScrolledText(win, height=15, wrap="word")
    text_code.insert(tk.END, code)
    text_code.configure(state="disabled")
    text_code.pack(fill="both", expand=True, padx=10)

    # --- Zone de résultat ---
    tk.Label(win, text="Résultat :", font=("Arial", 12, "bold")).pack(pady=5)
    result_text = scrolledtext.ScrolledText(win, height=8, wrap="word")
    result_text.configure(state="disabled")
    result_text.pack(fill="both", expand=False, padx=10)

    # --- Helpers internes ---
    def run_with_arg():
        annee = entry.get()
        try:
            sig = inspect.signature(fonction)
            if len(sig.parameters) == 2:
                fonction(annee, result_text)
            else:
                res = fonction(annee)
                result_text.configure(state="normal")
                result_text.delete("1.0", tk.END)
                if res is not None:
                    result_text.insert(tk.END, res)
                result_text.configure(state="disabled")
        except Exception as e:
            result_text.configure(state="normal")
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Erreur : {e}")
            result_text.configure(state="disabled")

    def run_direct():
        try:
            sig = inspect.signature(fonction)
            result_text.configure(state="normal")
            result_text.delete("1.0", tk.END)

            # --- Redirection stdout vers interface ---
            old_stdout = sys.stdout
            sys.stdout = TextRedirector(result_text)

            if len(sig.parameters) == 1:
                fonction(result_text)
            else:
                res = fonction()
                if res is not None:
                    print(res)

            sys.stdout = old_stdout
            result_text.configure(state="disabled")
        except Exception as e:
            sys.stdout = old_stdout
            result_text.configure(state="normal")
            result_text.delete("1.0", tk.END)
            result_text.insert(tk.END, f"Erreur : {e}")
            result_text.configure(state="disabled")

    # --- Choix d'exécution selon besoin année ---
    if besoin_annee:
        tk.Label(win, text="Entrez une année (ex: 2005) :").pack(pady=5)
        entry = tk.Entry(win)
        entry.pack(pady=5)
        btn = tk.Button(win, text="Exécuter", command=run_with_arg)
    else:
        btn = tk.Button(win, text="Exécuter", command=run_direct)
    btn.pack(pady=10)






# === FENÊTRE PRINCIPALE AVEC LE HUB ===

def main_menu():
    root = tk.Tk()
    root.title("Hub d'analyse NBA 🏀")
    root.geometry("600x700")

    tk.Label(root, text="Ici ça répond", font=("Helvetica", 22, "bold")).pack(pady=20)
    tk.Label(root, text="Choisis une question à explorer :", font=("Helvetica", 14)).pack(pady=10)

    # === Boutons des questions ===
    tk.Button(root,
          text="Question 1",
          font=("Helvetica", 13),
          width=30,
          command=lambda: open_window("Question 1", run_question_1, code_question_1)
          ).pack(pady=5)


    tk.Button(root, text="Question 2 pandas", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 2", run_question_2, code_question_2)).pack(pady=5)

    tk.Button(root,
          text="Question 2 python pur",
          font=("Helvetica", 13),
          width=30,
          command=lambda: open_window("Question 2 bis - Classement 2022-2023", run_question_2bis, code_question_2bis)
          ).pack(pady=5)



    tk.Button(root,
          text="Question 3 pandas",
          font=("Helvetica", 13),
          width=30,
          command=lambda: open_window("Question 3 - Meilleur ratio victoire", run_question_3, code_question_3_bis)
          ).pack(pady=5)


    tk.Button(root, text="Question 3 python pur", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 3 - NBA", run_question_3_bis, code_q3_pur)).pack(pady=3)

    tk.Button(root, text="Question 4", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 4", run_question_4, code_q4, besoin_annee=True)).pack(pady=5)

    tk.Button(root, text="Question 5", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 5", run_question_5, code_question_5, besoin_annee=True)).pack(pady=5)

    tk.Button(root, text="Question 6 - pandas", font=("Helvetica", 13), width=30,
          command=lambda: open_window("Question 6", run_question_6, code_q6)).pack(pady=3)

    tk.Button(root, text="Question 6 - python pur", font=("Helvetica", 13), width=30,
          command=lambda: open_window("Question 6", run_question_6_bis, code_q6_bis)).pack(pady=3)


    tk.Button(root, text="Question 7", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 7", run_question_7, code_question_7)).pack(pady=5)

    tk.Button(root, text="Question 8", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 8", run_question_8, code_question_8)).pack(pady=5)

    tk.Button(root, text="Question 9", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 9", run_question_9, code_question_9)).pack(pady=5)

    tk.Button(root, text="Question 10 - Pandas", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 10 - Pandas", run_question_10_pandas, code_q10_pandas)).pack(pady=3)

    tk.Button(root, text="Question 10 - Python pur", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 10 - Python pur", run_question_10_pure, code_q10_pure)).pack(pady=3)



    root.mainloop()



# === LANCEMENT ===
main_menu()

1
