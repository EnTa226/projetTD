import pandas as pd

# Charger les données
game = pd.read_csv('game.csv', sep=',')
game = game.dropna(subset=['fg3_pct_home', 'fg3_pct_away'])

# Filtrer les données pour ne pas avoir en sorti une équipe qui
# n'est pas une équipe NBA (ex: All-Star, Moscow CSKA, etc.)
game = game[(game['season_type'] == 'Regular Season')
            | (game['season_type'] == 'Playoffs')]

# Convertir la colonne season_id en chaîne de caractères
game['season_id'] = game['season_id'].astype(str)

# Déterminer l'année qui nous intéresse
year = input("Entrez l'année de la saison à partir de 1986 (ex: 2005) : ")

if not year.isdigit() or int(year) < 1986 or int(year) >= 2023:
    print(f"Aucune donnée trouvée pour la saison {year}.")
else:
    game_year = game[game["season_id"].str.contains(year)]
    game_year = game[game["season_id"].str.contains(year)]

    # Compter le nombre de matchs pour chaque équipe à domicile
    home_counts = game_year['team_abbreviation_home'].value_counts()

    # Compter le nombre de matchs pour chaque équipe à l'extérieur
    away_counts = game_year['team_abbreviation_away'].value_counts()

    # Total des matchs joués par équipe
    total_counts = home_counts + away_counts

    # Calculer les pourcentages de réussite
    home_fg3_pct = game_year.groupby('team_abbreviation_home'
                                     )['fg3_pct_home'].sum()
    away_fg3_pct = game_year.groupby('team_abbreviation_away'
                                     )['fg3_pct_away'].sum()
    total_fg3_pct = home_fg3_pct.add(away_fg3_pct, fill_value=0)

    # Moyenne des % de réussite à 3 points
    reussite_3 = total_fg3_pct / total_counts

    # Mise en forme du DataFrame
    reussite_3_df = reussite_3.reset_index()
    reussite_3_df.columns = ['team_abbreviation', 'reussite_3']
    reussite_3_df_sorted = reussite_3_df.sort_values(
        by='reussite_3', ascending=False
    ).reset_index(drop=True)

    # Créer un dictionnaire pour mapper les abréviations aux noms complets
    team_dict = game.set_index(
        'team_abbreviation_home')['team_name_home'].to_dict()

    # Obtenir le nom complet de l'équipe à partir de son abréviation
    def get_full_name(abbreviation):
        return team_dict.get(abbreviation)

    # Afficher l'équipe avec le plus de réussite aux trois points
    top_team_abbreviation = reussite_3_df_sorted.iloc[0]['team_abbreviation']

    print(
        (f"L'équipe avec le plus de réussite aux "
         f"trois points pour la saison {year} "
         f"sont les {get_full_name(top_team_abbreviation)} "
         f"avec un ratio de "
         f"{round(reussite_3_df_sorted.iloc[0]['reussite_3'], 3)}.")
        )
