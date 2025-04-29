import pandas as pd

# Charger les données
game = pd.read_csv('game.csv', sep=',')

# Convertir la colonne season_id en chaîne de caractères si nécessaire
game['season_id'] = game['season_id'].astype(str)

# Filtrer les données pour la saison 2005
game2005 = game[game["season_id"] == "22005"]

# Vérifier si game2005 contient des données
if game2005.empty:
    print("Aucune donnée trouvée pour la saison 22005.")
else:
    # Compter le nombre de matchs pour chaque équipe à domicile
    home_counts = game2005['team_abbreviation_home'].value_counts()

    # Compter le nombre de matchs pour chaque équipe à l'extérieur
    away_counts = game2005['team_abbreviation_away'].value_counts()

    # Additionner les comptages pour obtenir le nombre total de matchs pour chaque équipe
    total_counts = home_counts.add(away_counts, fill_value=0)

    # Calculer la somme des pourcentages de réussite à trois points pour chaque équipe à domicile
    home_fg3_pct = game2005.groupby('team_abbreviation_home')['fg3_pct_home'].sum()

    # Calculer la somme des pourcentages de réussite à trois points pour chaque équipe à l'extérieur
    away_fg3_pct = game2005.groupby('team_abbreviation_away')['fg3_pct_away'].sum()

    # Additionner les sommes des pourcentages de réussite à trois points
    total_fg3_pct = home_fg3_pct.add(away_fg3_pct, fill_value=0)

    # Calculer la moyenne des pourcentages de réussite à trois points pour chaque équipe
    reussite_3 = total_fg3_pct / total_counts

    # Convertir le résultat en DataFrame pour une meilleure lisibilité
    reussite_3_df = reussite_3.reset_index()
    reussite_3_df.columns = ['team_abbreviation', 'reussite_3']

    # Trier le DataFrame par la colonne 'reussite_3' dans l'ordre décroissant
    reussite_3_df_sorted = reussite_3_df.sort_values(by='reussite_3', ascending=False)

    # Réinitialiser l'index pour qu'il soit dans l'ordre
    reussite_3_df_sorted = reussite_3_df_sorted.reset_index(drop=True)

    print(reussite_3_df_sorted)


