#python pur : 


team_points = {}


with open("other_stats.csv", "r", encoding="utf-8") as f:
    next(f)  # Sauter l'en-tête
    for line in f:
        data = line.strip().split(",")  # Séparer les valeurs
        
        # Extraire les informations nécessaires
        team_home = data[3]  # Abréviation équipe domicile
        team_away = data[16] # Abréviation équipe extérieur
        
        # Points à additionner
        pts_home = int(data[5]) + int(data[6]) + int(data[7])  # Raquette + Seconde chance + Contre-attaque
        pts_away = int(data[18]) + int(data[19]) + int(data[20])  # Raquette + Seconde chance + Contre-attaque

        # Ajouter les points au total de chaque équipe
        team_points[team_home] = team_points.get(team_home, 0) + pts_home
        team_points[team_away] = team_points.get(team_away, 0) + pts_away

# Trouver l'équipe avec le plus de points
top_team = max(team_points, key=team_points.get)
top_points = team_points[top_team]

# Afficher le résultat
print(f"L'équipe avec le plus de points cumulés est {top_team} avec {top_points} points.")

#pd : 

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

# Afficher le résultat