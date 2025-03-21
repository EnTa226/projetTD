import pandas as pd

# Lire le fichier CSV
df = pd.read_csv('tableaux/common_player_info.csv', delimiter=',', quotechar='|')

# Afficher les premières lignes du DataFrame pour vérifier
print(df.head())
