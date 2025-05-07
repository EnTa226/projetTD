# Comment etablir une grille tarifaire des places de matchs de la NBA ?

# Pour cela on établit des groupes d'équipes ayant des caractéristiques
# similaires afin d'y appliquer des grilles tarifaires similaires.

# Importation des bibliothèques nécessaires

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# Indicateurs de performance: pourcentage de victoire
# On utilise les tables csv créer en question 2,
# classement_east et classement_west

df_1 = pd.read_csv('classement_east.csv', sep=',')
df_2 = pd.read_csv('classement_west.csv', sep=',')

# On concatène les deux DataFrames en un seul
df = pd.concat([df_1, df_2], ignore_index=True)

# On supprime la colonne 'conf' qui n'est pas nécessaire pour le clustering
df = df.drop('conf', axis=1)


# On visualise les données
print(df)

# Il y 30 équipes en tout, on va donc faire du clustering sur ces 30 équipes

# Début du clustering

X = df[['Win Ratio']]  # Garder uniquement les valeurs numériques

print(X)  # pas de NaN ou d'autres problèmes

inertias = []

for n in range(1, 31):  # Calculer les inerties pour n de 1 à 30
    kmeans = KMeans(n_clusters=n, random_state=0)
    kmeans.fit(X)
    inertias.append({'n_clusters': n, 'inertia': kmeans.inertia_})

print(inertias)

# convertir les inerties en DataFrame pour affichage
inertie_df = pd.DataFrame(inertias)

print(inertie_df)

# Tracer la courbe du coude pour effectuer la méthode du coude
plt.figure(figsize=(8, 5))
plt.plot(inertie_df['n_clusters'], inertie_df['inertia'], marker='o')
plt.title("Méthode du coude")
plt.xlabel("Nombre de clusters (k)")
plt.ylabel("Inertie")
plt.grid(True)
plt.show()

# Remplacez par le nombre de clusters optimal, déterminé via méthode du coude
k_optimal = 4

# Appliquer KMeans avec le nombre de clusters optimal, ici 4

kmeans = KMeans(n_clusters=k_optimal, random_state=0)
kmeans.fit(X)
df['Cluster'] = kmeans.labels_
print(df)

# On cherche à visualiser les clusters
plt.close()

plt.close()
# Palette de couleurs pour les clusters
palette = {0: 'b', 1: 'g', 2: 'y', 3: 'r'}


cluster_data = [] # Prépare les données par cluster
for cluster in sorted(df['Cluster'].unique()):
    teams = df[df['Cluster'] == cluster].sort_values(by='Win Ratio', ascending=False)
    team_strs = [f"{row['abbreviation']} ({row['Win Ratio']:.3f})" for _, row in teams.iterrows()]
    cluster_data.append(team_strs)

max_len = max(len(col) for col in cluster_data)
for col in cluster_data:
    while len(col) < max_len:
        col.append("")

# Création du tableau
table_data = list(zip(*cluster_data))  # Transpose pour avoir les équipes en lignes
column_labels = [f"Cluster {c}" for c in sorted(df['Cluster'].unique())]
col_colors = [palette[c] for c in sorted(df['Cluster'].unique())]

fig, ax = plt.subplots(figsize=(14, 6))
ax.axis('off')

table = ax.table(cellText=table_data,
                 colLabels=column_labels,
                 colColours=col_colors,
                 loc='center',
                 cellLoc='center')

table.auto_set_font_size(False)
table.set_fontsize(11)
table.scale(1.2, 1.5)

plt.title('Équipes regroupées par cluster (Win Ratio)', fontsize=14, pad=20)
plt.tight_layout()
plt.show()
