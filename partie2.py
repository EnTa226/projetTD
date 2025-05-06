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

# Configuration
plt.figure(figsize=(16, 8))
ax = plt.gca()

palette = {0: 'b', 1: 'g', 2: 'y', 3: 'r'}

for cluster in df['Cluster'].unique():
    subset = df[df['Cluster'] == cluster]
    plt.scatter(subset['Win Ratio'], [1]*len(subset),
                c=palette[cluster], s=100,
                label=f'Cluster {cluster}', alpha=0.8)

plt.xticks(np.arange(0.15, 0.75, 0.05), fontsize=10)
plt.xlim(0.15, 0.75)  # comprends toutes les valeurs des ratios de win

for _, row in df.iterrows():
    plt.text(row['Win Ratio'], 1.015, row['abbreviation'],
             ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.text(row['Win Ratio'], 0.985, f"{row['Win Ratio']:.3f}",
             ha='center', va='top', fontsize=8, color='gray')

# Titre et labels
plt.title('Classement des équipes par ratio de victoire avec clustering',
          pad=20, fontsize=14)
plt.xlabel('Win Ratio', fontsize=12)
plt.yticks([])  # Masque l'axe Y
plt.grid(axis='x', linestyle='--', alpha=0.4)

# Légende
legend = plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12),
                    ncol=4, frameon=False, fontsize=11)
for handle in legend.legend_handles:
    handle.set_sizes([60])


plt.tight_layout()
plt.show()
