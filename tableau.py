import pandas as pd

# Lire le fichier CSV en ignorant les lignes avec des erreurs
infos_joueurs = pd.read_csv('tableaux/common_player_info.csv', delimiter=',')

print(infos_joueurs)
infos_joueurs.to_excel('tableaux/infos_joueurs.xlsx', index=False)