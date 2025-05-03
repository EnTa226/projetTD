# Quelle est l'équipe ayant eu le plus de joueurs qui ne sont pas arrivé en NBA par la draft ?

import pandas as pd

# On charge le fichier CSV
df = pd.read_csv('common_player_info.csv')

# On garde que les joueurs qui n'ont pas Ã©tÃ© draftÃ©s
# On remarque que la colonne 'draft_year' contient l'annÃ©e de draft ou 'Undrafted'
undrafted_players = df[df['draft_year'] == 'Undrafted']

# On compte le nombre de joueurs "Undrafted" par Ã©quipe ( colone team_name)

undrafted_counts = undrafted_players['team_name'].value_counts()

# Afficher les rÃ©sultats
print(undrafted_counts[0:1])