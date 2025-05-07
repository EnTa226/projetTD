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
    game_reg_season_22_23["team_abbreviation_away"])

# Calculer le ratio de victoires
total_games = (game_reg_season_22_23['team_abbreviation_home'].value_counts() +
               game_reg_season_22_23['team_abbreviation_away'].value_counts())
wins = game_reg_season_22_23['winner'].value_counts()
ratio = (wins / total_games).reset_index()
ratio.columns = ['abbreviation', 'Win Ratio']

# Calculer le nombre total de points marqués par chaque équipe
# On s'intéresse aux points marqués pour régler les problèmes d'égalité
points_home = game_reg_season_22_23.groupby(
    'team_abbreviation_home')['pts_home'].sum()
points_away = game_reg_season_22_23.groupby(
    'team_abbreviation_away')['pts_away'].sum()
total_points = points_home.add(points_away, fill_value=0)

# Calculer la moyenne des points marqués par match
avg_points = (total_points / total_games).reset_index()
avg_points.columns = ['abbreviation', 'Avg Points']

# Joindre les DataFrames ratio et avg_points sur la colonne 'abbreviation'
ratio_df = pd.merge(ratio, avg_points, on='abbreviation')

# Charger le fichier teams_conferences.csv
teams_conferences = pd.read_csv('teams_conferences.csv', sep=';')

# Joindre ratio_df et teams_conferences sur la colonne 'abbreviation'
ratio_df = pd.merge(ratio_df, teams_conferences, on='abbreviation')

# Trier les équipes par ratio de victoires, puis par moyenne de points
ratio_df = ratio_df.sort_values(by=['Win Ratio', 'Avg Points'],
                                ascending=[False, False])

# Arrondir les colonnes 'Win Ratio' et 'Avg Points'
ratio_df['Win Ratio'] = ratio_df['Win Ratio'].round(3)
ratio_df['Avg Points'] = ratio_df['Avg Points'].round(2)

# Classement conférence Ouest
classement_west = ratio_df[ratio_df['conf'] == 'W'].copy()
classement_west['classement'] = classement_west['Win Ratio'].rank(
    ascending=False, method='first').astype(int)
print("Classement Conférence Ouest:")
print(classement_west.to_string(index=False))

# Classement conférence Est
classement_east = ratio_df[ratio_df['conf'] == 'E'].copy()
classement_east['classement'] = classement_east['Win Ratio'].rank(
    ascending=False, method='first').astype(int)
print("Classement Conférence Est:")
print(classement_east.to_string(index=False))
