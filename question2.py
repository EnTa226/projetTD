import pandas as pd
import numpy as np
#On extrait
game = pd.read_csv('game.csv')
game[ "game_date"] = pd.to_datetime(game["game_date"])
print(game.head())

# on trie les données pour avoir les matchs de saison réguliere 2022 et 2023
debut_saison_22_23 = pd.Timestamp(2022, 10, 18)
fin_saison_22_23 = pd.Timestamp(2023, 4, 12)

game_reg_season_22_23 = game[(game['game_date'] >= debut_saison_22_23 ) & (game['game_date'] <= fin_saison_22_23)
                             & (game["season_type"] == "Regular Season")]
print(game_reg_season_22_23)


#on cherche à compter le nombre de victoires par chaque équipe
#On crée une colonne pour le vainqueur
game_reg_season_22_23["winner"] = np.where(game_reg_season_22_23["wl_home"] == "W",
                                 game_reg_season_22_23["team_abbreviation_home"],
                                 game_reg_season_22_23["team_abbreviation_away"])
print(game_reg_season_22_23.head())

ratio = game_reg_season_22_23.groupby("winner").size() / (game_reg_season_22_23.groupby("team_abbreviation_home").size() + game_reg_season_22_23.groupby("team_abbreviation_away").size())

# Convertir le résultat en DataFrame
ratio_df = ratio.reset_index()

# Renommer les colonnes pour plus de clarté
ratio_df.columns = ['abbreviation', 'Win Ratio']


# Charger le fichier teams_conferences.csv
teams_conferences = pd.read_csv('teams_conferences.csv', sep = ';')

# Joindre les deux DataFrames sur les colonnes 'winner' et 'abbreviation'
ratio_df = pd.merge(ratio_df, teams_conferences, on = 'abbreviation')

# Afficher le résultat
print(ratio_df.head())

ratio_df = ratio_df.sort_values(ascending=False, by = 'Win Ratio')


#classement conférence ouest
classement_west = ratio_df[ratio_df['conf'] == 'W'].copy()

# Ajouter la colonne 'classement' en utilisant .loc
classement_west.loc[:, 'classement'] = classement_west['Win Ratio'].rank(ascending=False, method='first').astype(int)
print(classement_west.to_string(index=False))

#classement conférence est
# Filtrer le DataFrame pour la conférence Est
classement_east = ratio_df[ratio_df['conf'] == 'E'].copy()

# Ajouter la colonne 'classement' en utilisant .loc
classement_east.loc[:, 'classement'] = classement_east['Win Ratio'].rank(ascending=False, method='first').astype(int)

print(classement_east.to_string(index=False))


