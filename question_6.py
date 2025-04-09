import csv
from statistics import mean

# Dictionnaire : poste -> liste des poids
weights_by_position = {}

# Lire le fichier CSV
with open("common_player_info.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row.get("draft_number") == "1":
            position = row.get("position")
            weight_str = row.get("weight")

            if position and weight_str:
                try:
                    weight = float(weight_str)
                except ValueError:
                    continue

                if position not in weights_by_position:
                    weights_by_position[position] = []
                weights_by_position[position].append(weight)

# Affichage des résultats
print("Poids des joueurs draftés en 1ère position par poste :\n")
for position, weights in weights_by_position.items():
    sorted_weights = sorted(weights)
    avg_weight = round(mean(sorted_weights), 1)
    print(f"{position} ({len(weights)} joueurs)")
    print(f"  ➤ Poids triés : {sorted_weights}")
    print(f"  ➤ Moyenne : {avg_weight} lbs\n")

# Option : écriture dans un fichier CSV
save_to_csv = False  # Mets sur True si tu veux sauvegarder

if save_to_csv:
    with open("weights_by_position.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["position", "weights", "average_weight"])
        for position, weights in weights_by_position.items():
            writer.writerow([
                position,
                ";".join(str(w) for w in sorted(weights)),
                round(mean(weights), 1)
            ])
    print("Fichier 'weights_by_position.csv' créé avec succès.")

#les joueurs dont le poids est manquant sont ignorés


# Convertit "6-8" -> 80 pouces
def height_to_inches(height_str):
    try:
        feet, inches = map(int, height_str.split('-'))
        return feet * 12 + inches
    except:
        return None

# Dictionnaire : poste -> liste de tailles (en pouces)
heights_by_position = {}
total_first_picks = 0
kept_players = 0

with open("common_player_info.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row.get("draft_number") == "1":
            total_first_picks += 1
            position = row.get("position")
            height_str = row.get("height")

            if position and height_str:
                height_inches = height_to_inches(height_str)
                if height_inches is not None:
                    kept_players += 1
                    if position not in heights_by_position:
                        heights_by_position[position] = []
                    heights_by_position[position].append(height_inches)

# Affichage
print(f"\nJoueurs draftés #1 : {total_first_picks}")
print(f"Joueurs avec taille connue : {kept_players}\n")
print("Taille (en pouces) des joueurs draftés en 1ère position par poste :\n")

for position, heights in heights_by_position.items():
    sorted_heights = sorted(heights)
    avg_height = round(mean(sorted_heights), 1)
    print(f"{position} ({len(heights)} joueurs)")
    print(f"  ➤ Tailles triées : {sorted_heights}")
    print(f"  ➤ Moyenne : {avg_height} pouces\n")

# Option : sauvegarder dans un fichier CSV
save_to_csv = False  # Mets sur True si tu veux sauvegarder

if save_to_csv:
    with open("heights_by_position.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["position", "heights_inches", "average_height_inches"])
        for position, heights in heights_by_position.items():
            writer.writerow([
                position,
                ";".join(str(h) for h in sorted(heights)),
                round(mean(heights), 1)
            ])
    print("Fichier 'heights_by_position.csv' créé avec succès.")