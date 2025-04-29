import tkinter as tk
from tkinter import scrolledtext
from collections import defaultdict
from datetime import datetime
import csv

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


# === FENÊTRE QUESTION DÉDIÉE ===

def open_question_window(title, code_str, run_function):
    question_win = tk.Toplevel()
    question_win.title(title)
    question_win.geometry("1200x900")

    tk.Label(question_win, text=title, font=("Helvetica", 20, "bold")).pack(pady=10)

    code_area = scrolledtext.ScrolledText(question_win, width=140, height=30, font=("Courier", 10), bg="#f0f0f0")
    code_area.insert(tk.END, code_str)
    code_area.config(state="disabled")
    code_area.pack(padx=10, pady=5)

    output_area = scrolledtext.ScrolledText(question_win, width=140, height=12, font=("Courier", 10), bg="#eaffea")
    output_area.insert(tk.END, "Résultat ici...")
    output_area.config(state="disabled")
    output_area.pack(padx=10, pady=10)

    tk.Button(question_win, text="Exécuter le code", font=("Helvetica", 12),
              command=lambda: run_function(output_area)).pack(pady=10)

# === FENÊTRE PRINCIPALE AVEC LE HUB ===

def main_menu():
    root = tk.Tk()
    root.title("Hub d'analyse NBA 🏀")
    root.geometry("600x700")

    tk.Label(root, text="Ici ca répond", font=("Helvetica", 22, "bold")).pack(pady=20)
    tk.Label(root, text="Choisis une question à explorer :", font=("Helvetica", 14)).pack(pady=10)

    for i in range(1, 11):
        if i == 1:
            tk.Button(root,
                  text=f"Question {i}",
                  font=("Helvetica", 13),
                  width=30,
                  command=lambda: open_question_window("Question 1", code_question_1, run_question_1)
                  ).pack(pady=5)
        elif i == 2:
            tk.Button(root,
                  text=f"Question {i}",
                  font=("Helvetica", 13),
                  width=30,
                  command=lambda: open_question_window("Question 2", code_question_2, run_question_2)
                  ).pack(pady=5)
        elif i == 3:
            # Bouton pour la version avec tous les matchs
            tk.Button(root,
                    text="Question 3 - Tous matchs",
                    font=("Helvetica", 13),
                    width=30,
                    command=lambda: open_question_window("Question 3 - Tous matchs", code_q10_part1, run_question_3_part1)
                    ).pack(pady=3)

            # Bouton pour la version filtrée (NBA uniquement)
            tk.Button(root,
                    text="Question 3 - NBA (≥30 matchs)",
                    font=("Helvetica", 13),
                    width=30,
                    command=lambda: open_question_window("Question 3 - NBA", code_q10_part2, run_question_3_part2)
                    ).pack(pady=3)


        elif i == 9:
            tk.Button(root,
                  text=f"Question {i}",
                  font=("Helvetica", 13),
                  width=30,
                  command=lambda: open_question_window("Question 9", code_question_9, run_question_9)
                  ).pack(pady=5)
            
        else:
            tk.Button(root,
                  text=f"Question {i} (à compléter)",
                  font=("Helvetica", 13),
                  width=30,
                  state="disabled"
                  ).pack(pady=5)

    root.mainloop()

# === LANCEMENT ===
main_menu()

