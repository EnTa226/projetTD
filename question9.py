import pandas as pd

# Charger le fichier CSV
df = pd.read_csv("common_player_info.csv")

# Convertir la colonne 'jersey' en chaîne de caractères pour utiliser str.isnumeric()
df['jersey'] = df['jersey'].astype(str)

# Filtrer uniquement les valeurs non nulles et numériques
df = df[df['jersey'].str.isnumeric()]

# Convertir les numéros de maillot en entiers
df['jersey'] = df['jersey'].astype(int)

# Compter les occurrences de chaque numéro
top_jerseys = df['jersey'].value_counts().sort_values(ascending=False)

# Afficher les numéros les plus utilisés
print("Le numéro de maillot le plus utilisé par les joueurs :")
print(top_jerseys.head(1))
