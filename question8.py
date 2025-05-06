import pandas as pd
import matplotlib.pyplot as plt

# Charger le DataFrame
draft = pd.read_csv('draft_history.csv')
draft = draft[draft['season'] >= 1984]  # Filtrer les saisons à partir de 1984
draft = draft.dropna(subset=['organization'])

# Compter le nombre de joueurs draftés par an
annual_counts = draft.groupby('season').size()

# Convertir le résultat en DataFrame pour plus de lisibilité
annual_counts_df = annual_counts.reset_index(name='count')
annual_counts_df

# Filtrer les joueurs dont le organization_type est "Other Team/Club"
# et dont le nom de l'organisation contient des parenthèses,
# mais pas "G League" ni "IBL"
draft_stranger = draft[
    (draft['organization_type'] == 'Other Team/Club') &
    (draft['organization'].str.contains(r'\(')) &
    # Utiliser r'\(' pour échapper la parenthèse
    (~draft['organization'].str.contains('IBL')) &
    (~draft['organization'].str.contains('G League'))
    # Filtrer les organisations contenant "G League"
]

# Grouper par année (colonne 'season') et compter les occurrences
strangers_annual_counts = draft_stranger.groupby('season').size()

# Convertir le résultat en DataFrame pour plus de lisibilité
strangers_annual_counts_df = strangers_annual_counts.reset_index(name='count')

# Fusionner les deux DataFrames pour aligner les années
merged_df = pd.merge(annual_counts_df, strangers_annual_counts_df,
                     on='season', how='left', suffixes=('_total', '_stranger'))

# Calculer le ratio
merged_df['ratio'] = (merged_df['count_stranger'] / merged_df['count_total']
                      ) * 100
merged_df

# Tracer un graphique en barres des occurrences par année
plt.figure(figsize=(12, 8))
plt.bar(merged_df['season'], merged_df['ratio'], color='skyblue')
plt.title('Proportion de joueurs étrangers draftés par année')
plt.xlabel('Année')
plt.ylabel('Part de joueurs étrangers (%)')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
