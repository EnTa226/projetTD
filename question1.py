import pandas as pd
import numpy as np

game_info = pd.read_csv("game_info.csv", delimiter=",")
game = pd.read_csv("game.csv", delimiter=",")
import pandas as pd


game["game_date"] = pd.to_datetime(game["game_date"])

start_date = pd.to_datetime("2022-10-18")
end_date = pd.to_datetime("2023-06-14")


game_filtered = game[(game["game_date"] >= start_date) & (game["game_date"] <= end_date)]
game_sorted = game.sort_values(by="game_date", ascending=False)
game_sorted["winner"] = np.where(game_sorted["wl_home"] == "W",
                                 game_sorted["team_name_home"],
                                 game_sorted["team_name_away"])

winner = game_sorted[["game_date", "winner"]].copy()
#print(f"Le gagnant de la saison 2022-2023 est {winner.iloc[0, 1]}")
print(winner)