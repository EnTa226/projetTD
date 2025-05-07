
# Lecture manuelle du fichier
with open("common_player_info.csv", encoding="utf-8") as f:
    lines = f.readlines()

# Extraction de l'en-tête (colonnes)
headers = lines[0].strip().split(",")
data = []


# Fonction pour obtenir une taille en cm
def convert_height_to_cm(height_str):
    try:
        feet, inches = map(int, height_str.split("-"))
        return round(feet * 30.48 + inches * 2.54, 2)
    except (ValueError, AttributeError):
        return None


# Parse ligne par ligne
for line in lines[1:]:
    values = line.strip().split(",")

    # Gérer les valeurs contenant des virgules entre guillemets
    while len(values) > len(headers):
        for i in range(len(values) - 1):
            if values[i].startswith('"') and not values[i].endswith('"'):
                values[i] = values[i] + "," + values.pop(i + 1)
                break

    # Crée un dictionnaire pour chaque joueur
    player = {headers[i]: values[i].strip('"') if i < len(values) else ""
              for i in range(len(headers))}
    data.append(player)

# Nettoyage des données
for player in data:
    try:
        player["draft_number"] = int(player["draft_number"])
    except ValueError:
        player["draft_number"] = None

    player["height_cm"] = convert_height_to_cm(player.get("height", ""))


# Fonction pour calculer la moyenne par position
def mean_height_by_position(players, draft_target):
    position_totals = {}
    position_counts = {}

    for p in players:
        if p["draft_number"] == draft_target and p["height_cm"] is not None:
            pos = p["position"]
            position_totals[pos] = position_totals.get(pos, 0) + p["height_cm"]
            position_counts[pos] = position_counts.get(pos, 0) + 1

    return {pos: round(position_totals[pos] / position_counts[pos], 2)
            for pos in position_totals}


# Affichage
print("Taille des No1 de draft (en cm) par poste :")
for pos, avg in mean_height_by_position(data, 1).items():
    print(f"{pos}: {avg} cm")

print("\nTaille des No30 de draft (en cm) par poste :")
for pos, avg in mean_height_by_position(data, 30).items():
    print(f"{pos}: {avg} cm")
