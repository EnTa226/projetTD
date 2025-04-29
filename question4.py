import pandas as pd

# Charger les données
game = pd.read_csv('game.csv', sep=',')
game = game.dropna(subset=['fg3_pct_home', 'fg3_pct_away'])

print(game.head())

# Convertir la colonne season_id en chaîne de caractères
game['season_id'] = game['season_id'].astype(str)

# Déterminer l'année qui nous intéresse
annee = input("Entrez l'année de la saison à partir de 1979 (ex: 2005) : ")

# Filtrer les données pour l'année spécifiée
game_annee = game[game["season_id"].str.contains(annee)]
if game_annee.empty:
    print(f"Aucune donnée trouvée pour la saison {annee},"
          f" surement parce que la NBA ne documentait toujours pas la réussite aux trois points")
else:
    # Compter le nombre de matchs pour chaque équipe à domicile
    home_counts = game_annee['team_abbreviation_home'].value_counts()

    # Compter le nombre de matchs pour chaque équipe à l'extérieur
    away_counts = game_annee['team_abbreviation_away'].value_counts()

    # Additionner les comptages pour obtenir le nombre total de matchs pour chaque équipe
    total_counts = home_counts.add(away_counts, fill_value=0)

    # Calculer la somme des pourcentages de réussite à trois points pour chaque équipe à domicile
    home_fg3_pct = game_annee.groupby('team_abbreviation_home')['fg3_pct_home'].sum()

    # Calculer la somme des pourcentages de réussite à trois points pour chaque équipe à l'extérieur
    away_fg3_pct = game_annee.groupby('team_abbreviation_away')['fg3_pct_away'].sum()

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
    
    # Charger les données à partir du fichier CSV
    team_csv = pd.read_csv('team.csv')

    # Créer un dictionnaire pour mapper les abréviations aux noms complets
    team_dict = team_csv.set_index('abbreviation')['full_name'].to_dict()

    # Fonction pour obtenir le nom complet de l'équipe à partir de son abréviation
    def get_full_name(abbreviation):
        return team_dict.get(abbreviation, "Équipe non trouvée")

    print(f"L'équipe avec le plus de réussite aux trois points sont les {get_full_name(reussite_3_df_sorted.iloc[0]['team_abbreviation'])} "
        f"avec un pourcentage de {reussite_3_df_sorted.iloc[0]['reussite_3']:.2f}.")