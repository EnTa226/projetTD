
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
