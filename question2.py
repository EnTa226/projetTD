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