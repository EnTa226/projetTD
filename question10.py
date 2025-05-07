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
print(
    f"L'équipe avec le plus de points cumulés est {top_team} "
    f"avec {top_points} points."
)
