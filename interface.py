import tkinter as tk
from tkinter import scrolledtext
from collections import defaultdict
from datetime import datetime
import csv
import inspect

# === FONCTIONS DE QUESTION ===

def run_question_1(output_widget):
    try:
        with open("game.csv", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            playoffs_games = [row for row in reader if row["season_type"] == "Playoffs"]

        seasons = defaultdict(list)
        for row in playoffs_games:
            seasons[row["season_id"]].append(row)

        champions = []
        for season_id, matches in seasons.items():
            matches.sort(key=lambda x: datetime.strptime(x["game_date"], "%Y-%m-%d %H:%M:%S"))
            last_game = matches[-1]
            if last_game["wl_home"] == "W":
                winner = last_game["team_abbreviation_home"]
            else:
                winner = last_game["team_abbreviation_away"]
            champions.append(winner)

        win_counts = defaultdict(int)
        for team in champions:
            win_counts[team] += 1

        top_teams = [team for team, count in win_counts.items() if count >= 3]

        result = "Les équipes ayant gagné au moins 3 fois une saison NBA sont :\n"
        for team in top_teams:
            result += f"- {team} ({win_counts[team]} titres)\n"

        output_widget.config(state="normal")
        output_widget.delete("1.0", tk.END)
        output_widget.insert(tk.END, result)
        output_widget.config(state="disabled")
    except Exception as e:
        output_widget.config(state="normal")
        output_widget.delete("1.0", tk.END)
        output_widget.insert(tk.END, f"Erreur : {e}")
        output_widget.config(state="disabled")


# === CODE SOURCE A AFFICHER POUR CHAQUE QUESTION ===

code_question_1 = """import csv
from collections import defaultdict
from datetime import datetime

with open("game.csv", newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    playoffs_games = [row for row in reader if row["season_type"] == "Playoffs"]

seasons = defaultdict(list)
for row in playoffs_games:
    seasons[row["season_id"]].append(row)

champions = []
for season_id, matches in seasons.items():
    matches.sort(key=lambda x: datetime.strptime(x["game_date"], "%Y-%m-%d %H:%M:%S"))
    last_game = matches[-1]

    if last_game["wl_home"] == "W":
        winner = last_game["team_abbreviation_home"]
    else:
        winner = last_game["team_abbreviation_away"]
    champions.append(winner)

win_counts = defaultdict(int)
for team in champions:
    win_counts[team] += 1

top_teams = [team for team, count in win_counts.items() if count >= 3]

print("Les équipes ayant gagné au moins 3 fois une saison NBA sont :")
for team in top_teams:
    print(f"- {team} ({win_counts[team]} titres)")
"""
# Fonction simple qui retourne "feur"
def run_question_2(output_widget):
    try:
        import pandas as pd
        import numpy as np

        game = pd.read_csv('game.csv')
        game["game_date"] = pd.to_datetime(game["game_date"])

        debut_saison_22_23 = pd.Timestamp(2022, 10, 18)
        fin_saison_22_23 = pd.Timestamp(2023, 4, 12)

        game_reg = game[(game['game_date'] >= debut_saison_22_23 ) & (game['game_date'] <= fin_saison_22_23)
                        & (game["season_type"] == "Regular Season")].copy()

        game_reg["winner"] = np.where(game_reg["wl_home"] == "W",
                                      game_reg["team_abbreviation_home"],
                                      game_reg["team_abbreviation_away"])

        ratio = game_reg.groupby("winner").size() / (
            game_reg.groupby("team_abbreviation_home").size() + game_reg.groupby("team_abbreviation_away").size()
        )

        ratio_df = ratio.reset_index()
        ratio_df.columns = ['abbreviation', 'Win Ratio']

        teams_conferences = pd.read_csv('teams_conferences.csv', sep=';')
        ratio_df = pd.merge(ratio_df, teams_conferences, on='abbreviation')
        ratio_df = ratio_df.sort_values(ascending=False, by='Win Ratio')

        classement_west = ratio_df[ratio_df['conf'] == 'W'].copy()
        classement_west['classement'] = classement_west['Win Ratio'].rank(ascending=False, method='first').astype(int)

        classement_east = ratio_df[ratio_df['conf'] == 'E'].copy()
        classement_east['classement'] = classement_east['Win Ratio'].rank(ascending=False, method='first').astype(int)

        result = "=== Conférence OUEST ===\n"
        result += classement_west[['classement', 'abbreviation', 'Win Ratio']].sort_values('classement').to_string(index=False)
        result += "\n\n=== Conférence EST ===\n"
        result += classement_east[['classement', 'abbreviation', 'Win Ratio']].sort_values('classement').to_string(index=False)

        output_widget.config(state="normal")
        output_widget.delete("1.0", tk.END)
        output_widget.insert(tk.END, result)
        output_widget.config(state="disabled")

    except Exception as e:
        output_widget.config(state="normal")
        output_widget.delete("1.0", tk.END)
        output_widget.insert(tk.END, f"Erreur : {e}")
        output_widget.config(state="disabled")

code_question_2 = """import pandas as pd
import numpy as np
game = pd.read_csv('game.csv')
game["game_date"] = pd.to_datetime(game["game_date"])

debut_saison_22_23 = pd.Timestamp(2022, 10, 18)
fin_saison_22_23 = pd.Timestamp(2023, 4, 12)

game_reg_season_22_23 = game[(game['game_date'] >= debut_saison_22_23 ) & (game['game_date'] <= fin_saison_22_23)
                             & (game["season_type"] == "Regular Season")]

game_reg_season_22_23["winner"] = np.where(game_reg_season_22_23["wl_home"] == "W",
                                 game_reg_season_22_23["team_abbreviation_home"],
                                 game_reg_season_22_23["team_abbreviation_away"])

ratio = game_reg_season_22_23.groupby("winner").size() / (game_reg_season_22_23.groupby("team_abbreviation_home").size()
                                                         + game_reg_season_22_23.groupby("team_abbreviation_away").size())

ratio_df = ratio.reset_index()
ratio_df.columns = ['abbreviation', 'Win Ratio']

teams_conferences = pd.read_csv('teams_conferences.csv', sep=';')
ratio_df = pd.merge(ratio_df, teams_conferences, on='abbreviation')
ratio_df = ratio_df.sort_values(ascending=False, by='Win Ratio')

classement_west = ratio_df[ratio_df['conf'] == 'W'].copy()
classement_west['classement'] = classement_west['Win Ratio'].rank(ascending=False, method='first').astype(int)

classement_east = ratio_df[ratio_df['conf'] == 'E'].copy()
classement_east['classement'] = classement_east['Win Ratio'].rank(ascending=False, method='first').astype(int)

print(classement_west.to_string(index=False))
print(classement_east.to_string(index=False))
"""
def run_question_3_part1(output_widget):
    try:
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

        win_ratios = {team: win_counts[team] / game_counts[team] for team in win_counts if game_counts[team] > 0}
        best_team = max(win_ratios, key=win_ratios.get)
        best_ratio = win_ratios[best_team]

        result = f"L'équipe avec le meilleur ratio de victoire (incluant tous les matchs) est :\n\n{best_team} avec un ratio de {best_ratio:.2f}"

        output_widget.config(state="normal")
        output_widget.delete("1.0", tk.END)
        output_widget.insert(tk.END, result)
        output_widget.config(state="disabled")

    except Exception as e:
        output_widget.config(state="normal")
        output_widget.delete("1.0", tk.END)
        output_widget.insert(tk.END, f"Erreur : {e}")
        output_widget.config(state="disabled")

def run_question_3_part2(output_widget):
    try:
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

        win_ratios = {team: win_counts[team] / game_counts[team] for team in win_counts if game_counts[team] >= 30}
        best_team = max(win_ratios, key=win_ratios.get)
        best_ratio = win_ratios[best_team]

        result = f"L'équipe NBA avec le meilleur ratio de victoire est : {best_team}\n"
        result += f"Ratio de victoire : {best_ratio:.2f}"

        output_widget.config(state="normal")
        output_widget.delete("1.0", tk.END)
        output_widget.insert(tk.END, result)
        output_widget.config(state="disabled")

    except Exception as e:
        output_widget.config(state="normal")
        output_widget.delete("1.0", tk.END)
        output_widget.insert(tk.END, f"Erreur : {e}")
        output_widget.config(state="disabled")



code_q4 = """import pandas as pd

# Charger les données
game = pd.read_csv('game.csv', sep=',')
game = game.dropna(subset=['fg3_pct_home', 'fg3_pct_away'])
game['season_id'] = game['season_id'].astype(str)

# Filtrer les données pour une année
game_annee = game[game["season_id"].str.contains(annee)]
if game_annee.empty:
    print(f"Aucune donnée trouvée pour la saison {annee}")
else:
    home_counts = game_annee['team_abbreviation_home'].value_counts()
    away_counts = game_annee['team_abbreviation_away'].value_counts()
    total_counts = home_counts.add(away_counts, fill_value=0)
    home_fg3_pct = game_annee.groupby('team_abbreviation_home')['fg3_pct_home'].sum()
    away_fg3_pct = game_annee.groupby('team_abbreviation_away')['fg3_pct_away'].sum()
    total_fg3_pct = home_fg3_pct.add(away_fg3_pct, fill_value=0)
    reussite_3 = total_fg3_pct / total_counts
    reussite_3_df = reussite_3.reset_index()
    reussite_3_df.columns = ['team_abbreviation', 'reussite_3']
    reussite_3_df_sorted = reussite_3_df.sort_values(by='reussite_3', ascending=False).reset_index(drop=True)

    team_csv = pd.read_csv('team.csv')
    team_dict = team_csv.set_index('abbreviation')['full_name'].to_dict()

    def get_full_name(abbreviation):
        return team_dict.get(abbreviation, "Équipe non trouvée")

    print(f"L'équipe avec le plus de réussite à 3 pts est {get_full_name(reussite_3_df_sorted.iloc[0]['team_abbreviation'])} "
          f"avec {reussite_3_df_sorted.iloc[0]['reussite_3']:.2f}.")
"""
def run_question_4(annee):
    import pandas as pd

    game = pd.read_csv('game.csv', sep=',')
    game = game.dropna(subset=['fg3_pct_home', 'fg3_pct_away'])
    game['season_id'] = game['season_id'].astype(str)
    game_annee = game[game["season_id"].str.contains(annee)]

    if game_annee.empty:
        return f"Aucune donnée trouvée pour la saison {annee}"

    home_counts = game_annee['team_abbreviation_home'].value_counts()
    away_counts = game_annee['team_abbreviation_away'].value_counts()
    total_counts = home_counts.add(away_counts, fill_value=0)
    home_fg3_pct = game_annee.groupby('team_abbreviation_home')['fg3_pct_home'].sum()
    away_fg3_pct = game_annee.groupby('team_abbreviation_away')['fg3_pct_away'].sum()
    total_fg3_pct = home_fg3_pct.add(away_fg3_pct, fill_value=0)
    reussite_3 = total_fg3_pct / total_counts
    reussite_3_df = reussite_3.reset_index()
    reussite_3_df.columns = ['team_abbreviation', 'reussite_3']
    reussite_3_df_sorted = reussite_3_df.sort_values(by='reussite_3', ascending=False).reset_index(drop=True)

    team_csv = pd.read_csv('team.csv')
    team_dict = team_csv.set_index('abbreviation')['full_name'].to_dict()

    def get_full_name(abbreviation):
        return team_dict.get(abbreviation, "Équipe non trouvée")

    result = f"L'équipe avec le plus de réussite à 3 pts est {get_full_name(reussite_3_df_sorted.iloc[0]['team_abbreviation'])} avec {reussite_3_df_sorted.iloc[0]['reussite_3']:.2f}."
    return result

# Question 5 : équipe avec le plus de matchs gagnés par saison

code_question_5 = '''
# Compter les victoires par équipe dans une saison donnée
import pandas as pd

game = pd.read_csv('game.csv')
game['season_id'] = game['season_id'].astype(str)

annee = input("Entrez l'année de la saison (ex: 2005) : ")
games = game[game["season_id"].str.contains(annee)]

# Compter les victoires
home_wins = games[games["pts_home"] > games["pts_away"]]["team_abbreviation_home"].value_counts()
away_wins = games[games["pts_home"] < games["pts_away"]]["team_abbreviation_away"].value_counts()
total_wins = home_wins.add(away_wins, fill_value=0)

# Obtenir l'équipe avec le plus de victoires
max_team = total_wins.idxmax()
max_wins = total_wins[max_team]

print(f"L'équipe avec le plus de victoires est {max_team} avec {int(max_wins)} victoires.")
'''

def run_question_5(annee):
    import pandas as pd

    try:
        game = pd.read_csv("game.csv")
        game['season_id'] = game['season_id'].astype(str)
        games = game[game["season_id"].str.contains(annee)]

        if games.empty:
            return f"Aucune donnée trouvée pour la saison {annee}."

        home_wins = games[games["pts_home"] > games["pts_away"]]["team_abbreviation_home"].value_counts()
        away_wins = games[games["pts_home"] < games["pts_away"]]["team_abbreviation_away"].value_counts()
        total_wins = home_wins.add(away_wins, fill_value=0)

        max_team = total_wins.idxmax()
        max_wins = int(total_wins[max_team])

        return f"L'équipe avec le plus de victoires est {max_team} avec {max_wins} victoires."

    except Exception as e:
        return f"Erreur : {e}"


code_question_7 = '''
# Boxplot des tailles de joueurs par poste
import pandas as pd
import matplotlib.pyplot as plt

def convert_height_to_cm(height_str):
    try:
        feet, inches = map(int, height_str.split("-"))
        return round(feet * 30.48 + inches * 2.54, 2)
    except:
        return None

df = pd.read_csv("common_player_info.csv")
df["height_cm"] = df["height"].apply(convert_height_to_cm)
df_clean = df.dropna(subset=["height_cm", "position"])

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

code_question_8 = '''
# Analyser l'évolution de la proportion de joueurs étrangers draftés depuis 1984
import pandas as pd
import matplotlib.pyplot as plt

draft = pd.read_csv('draft_history.csv')
draft = draft[draft['season'] >= 1984]
draft = draft.dropna(subset=['organization'])

annual_counts = draft.groupby('season').size()
annual_counts_df = annual_counts.reset_index(name='count')

draft_stranger = draft[
    (draft['organization_type'] == 'Other Team/Club') &
    (draft['organization'].str.contains(r'\\(')) &
    (~draft['organization'].str.contains('IBL')) &
    (~draft['organization'].str.contains('G League'))
]

strangers_annual_counts = draft_stranger.groupby('season').size()
strangers_annual_counts_df = strangers_annual_counts.reset_index(name='count')

merged_df = pd.merge(annual_counts_df, strangers_annual_counts_df, on='season', how='left', suffixes=('_total', '_stranger'))
merged_df['ratio'] = (merged_df['count_stranger'] / merged_df['count_total']) * 100

plt.figure(figsize=(12, 8))
plt.bar(merged_df['season'], merged_df['ratio'], color='skyblue')
plt.title('Proportion de joueurs étrangers draftés par année')
plt.xlabel('Année')
plt.ylabel('Part de joueurs étrangers (%)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
'''


def run_question_8():
    import pandas as pd
    import matplotlib.pyplot as plt

    try:
        draft = pd.read_csv('draft_history.csv')
        draft = draft[draft['season'] >= 1984]
        draft = draft.dropna(subset=['organization'])

        annual_counts = draft.groupby('season').size()
        annual_counts_df = annual_counts.reset_index(name='count')

        draft_stranger = draft[
            (draft['organization_type'] == 'Other Team/Club') &
            (draft['organization'].str.contains(r'\(')) &
            (~draft['organization'].str.contains('IBL')) &
            (~draft['organization'].str.contains('G League'))
        ]

        strangers_annual_counts = draft_stranger.groupby('season').size()
        strangers_annual_counts_df = strangers_annual_counts.reset_index(name='count')

        merged_df = pd.merge(
            annual_counts_df, 
            strangers_annual_counts_df, 
            on='season', 
            how='left', 
            suffixes=('_total', '_stranger')
        )

        merged_df['ratio'] = (merged_df['count_stranger'] / merged_df['count_total']) * 100

        plt.figure(figsize=(12, 8))
        plt.bar(merged_df['season'], merged_df['ratio'], color='skyblue')
        plt.title('Proportion de joueurs étrangers draftés par année')
        plt.xlabel('Année')
        plt.ylabel('Part de joueurs étrangers (%)')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        return "Graphique affiché avec succès."

    except Exception as e:
        return f"Erreur : {e}"


code_q10_part1 = """# Version sans filtre (inclut Barcelone FC)
# Dictionnaires pour stocker les victoires et matchs joués
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

win_ratios = {team: win_counts[team] / game_counts[team] for team in win_counts if game_counts[team] > 0}
best_team = max(win_ratios, key=win_ratios.get)
best_ratio = win_ratios[best_team]

print(best_team, best_ratio)
"""

code_q10_part2 = """# Version avec filtre (au moins 30 matchs joués)
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

win_ratios = {team: win_counts[team] / game_counts[team] for team in win_counts if game_counts[team] >= 30}
best_team = max(win_ratios, key=win_ratios.get)
best_ratio = win_ratios[best_team]

print(best_team, best_ratio)
"""

def run_question_9(output_widget):
    try:
        import pandas as pd

        df = pd.read_csv("common_player_info.csv")
        df['jersey'] = df['jersey'].astype(str)
        df = df[df['jersey'].str.isnumeric()]
        df['jersey'] = df['jersey'].astype(int)

        top_jerseys = df['jersey'].value_counts().sort_values(ascending=False)

        result = "Numéro de maillot le plus utilisé par les joueurs :\n"
        result += top_jerseys.head(1).to_string()

        output_widget.config(state="normal")
        output_widget.delete("1.0", tk.END)
        output_widget.insert(tk.END, result)
        output_widget.config(state="disabled")

    except Exception as e:
        output_widget.config(state="normal")
        output_widget.delete("1.0", tk.END)
        output_widget.insert(tk.END, f"Erreur : {e}")
        output_widget.config(state="disabled")

code_question_9 = """import pandas as pd

# Charger le fichier CSV
df = pd.read_csv("common_player_info.csv")

# Convertir la colonne 'jersey' en chaîne de caractères pour utiliser str.isnumeric()
df['jersey'] = df['jersey'].astype(str)

# Filtrer uniquement les valeurs non nulles et numériques
df = df[df['jersey'].str.isnumeric()]

# Convertir les numéros de maillot en entiers
df['jersey'] = df['jersey'].astype(int)

# Compter les occurrences de chaque numéro
top_jerseys = df['jersey'].value_counts().sort_values(ascending=False)

# Afficher les numéros les plus utilisés
print("Numéros de maillot les plus utilisés par les joueurs :")
print(top_jerseys.head(1))
"""
def run_question_10_pure(output_widget):
    try:
        team_points = {}
        with open("other_stats.csv", "r", encoding="utf-8") as f:
            next(f)  # Sauter l'en-tête
            for line in f:
                data = line.strip().split(",")
                team_home = data[3]
                team_away = data[16]
                pts_home = int(data[5]) + int(data[6]) + int(data[7])
                pts_away = int(data[18]) + int(data[19]) + int(data[20])
                team_points[team_home] = team_points.get(team_home, 0) + pts_home
                team_points[team_away] = team_points.get(team_away, 0) + pts_away

        top_team = max(team_points, key=team_points.get)
        top_points = team_points[top_team]
        result = f"L'équipe avec le plus de points cumulés est {top_team} avec {top_points} points."

        output_widget.config(state="normal")
        output_widget.delete("1.0", tk.END)
        output_widget.insert(tk.END, result)
        output_widget.config(state="disabled")
    except Exception as e:
        output_widget.config(state="normal")
        output_widget.delete("1.0", tk.END)
        output_widget.insert(tk.END, f"Erreur : {e}")
        output_widget.config(state="disabled")


def run_question_10_pandas(output_widget):
    try:
        import pandas as pd
        df = pd.read_csv("other_stats.csv")
        df["pts_home_total"] = df.iloc[:, 5] + df.iloc[:, 6] + df.iloc[:, 7]
        df["pts_away_total"] = df.iloc[:, 18] + df.iloc[:, 19] + df.iloc[:, 20]

        points_home = df.groupby(df.columns[3])["pts_home_total"].sum()
        points_away = df.groupby(df.columns[16])["pts_away_total"].sum()

        total_points = points_home.add(points_away, fill_value=0)

        top_team = total_points.idxmax()
        top_points = int(total_points.max())
        result = f"L'équipe avec le plus de points cumulés est {top_team} avec {top_points} points."

        output_widget.config(state="normal")
        output_widget.delete("1.0", tk.END)
        output_widget.insert(tk.END, result)
        output_widget.config(state="disabled")
    except Exception as e:
        output_widget.config(state="normal")
        output_widget.delete("1.0", tk.END)
        output_widget.insert(tk.END, f"Erreur : {e}")
        output_widget.config(state="disabled")

code_q10_pure = '''team_points = {}

with open("other_stats.csv", "r", encoding="utf-8") as f:
    next(f)
    for line in f:
        data = line.strip().split(",")
        team_home = data[3]
        team_away = data[16]
        pts_home = int(data[5]) + int(data[6]) + int(data[7])
        pts_away = int(data[18]) + int(data[19]) + int(data[20])
        team_points[team_home] = team_points.get(team_home, 0) + pts_home
        team_points[team_away] = team_points.get(team_away, 0) + pts_away

top_team = max(team_points, key=team_points.get)
top_points = team_points[top_team]

print(f"L'équipe avec le plus de points cumulés est {top_team} avec {top_points} points.")
'''

code_q10_pandas = '''import pandas as pd

df = pd.read_csv("other_stats.csv")
df["pts_home_total"] = df.iloc[:, 5] + df.iloc[:, 6] + df.iloc[:, 7]
df["pts_away_total"] = df.iloc[:, 18] + df.iloc[:, 19] + df.iloc[:, 20]

points_home = df.groupby(df.columns[3])["pts_home_total"].sum()
points_away = df.groupby(df.columns[16])["pts_away_total"].sum()

total_points = points_home.add(points_away, fill_value=0)

top_team = total_points.idxmax()
top_points = int(total_points.max())

print(f"L'équipe avec le plus de points cumulés est {top_team} avec {top_points} points.")
'''



# === FENÊTRE QUESTION DÉDIÉE ===

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
        res = fonction(annee)
        result_text.configure(state="normal")
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, res)
        result_text.configure(state="disabled")

    def run_direct():
        result_text.configure(state="normal")
        result_text.delete("1.0", tk.END)
        sig = inspect.signature(fonction)
        # si la fonction attend 1 paramètre, on lui passe le widget
        if len(sig.parameters) == 1:
            fonction(result_text)
        else:
            # sinon on récupère son retour (texte ou "")
            res = fonction()
            if res is not None:
                result_text.insert(tk.END, res)
        result_text.configure(state="disabled")

    # --- Choix d'exécution selon qu'on doive saisir une année ---
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
    tk.Button(root, text="Question 1", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 1", run_question_1, code_question_1)).pack(pady=5)

    tk.Button(root, text="Question 2", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 2", run_question_2, code_question_2)).pack(pady=5)

    tk.Button(root, text="Question 3 - Tous matchs", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 3 - Tous matchs", run_question_3_part1, code_q10_part1)).pack(pady=3)

    tk.Button(root, text="Question 3 - NBA (≥30 matchs)", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 3 - NBA", run_question_3_part2, code_q10_part2)).pack(pady=3)

    tk.Button(root, text="Question 4", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 4", run_question_4, code_q4, besoin_annee=True)).pack(pady=5)

    tk.Button(root, text="Question 5", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 5", run_question_5, code_question_5, besoin_annee=True)).pack(pady=5)

    tk.Button(root, text="Question 7", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 7", run_question_7, code_question_7)).pack(pady=5)

    tk.Button(root, text="Question 8", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 8", run_question_8, code_question_8)).pack(pady=5)

    tk.Button(root, text="Question 9", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 9", run_question_9, code_question_9)).pack(pady=5)

    tk.Button(root, text="Question 10 - Python pur", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 10 - Python pur", run_question_10_pure, code_q10_pure)).pack(pady=3)

    tk.Button(root, text="Question 10 - Pandas", font=("Helvetica", 13), width=30,
              command=lambda: open_window("Question 10 - Pandas", run_question_10_pandas, code_q10_pandas)).pack(pady=3)

    root.mainloop()



# === LANCEMENT ===
main_menu()

