import csv
def mean(l):
    a= 0
    for i in l:
        a += i
    return a / len(l)
# Fonction pour convertir une taille au format "pied-pouce" en centimètres
def convert_height_to_cm(height_str):
    try:
        feet, inches = map(int, height_str.split("-"))
        return round(feet * 30.48 + inches * 2.54, 2)
    except (ValueError, AttributeError):
        return None

# Dictionnaire pour stocker les tailles par poste
heights_by_position = {}
heights_by_position2 = {}

with open("common_player_info.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row.get("draft_number") == "1":
            position = row.get("position")
            height_str = row.get("height")
            height_cm = convert_height_to_cm(height_str)
            if position and height_cm:
                if position not in heights_by_position:
                    heights_by_position[position] = []
                heights_by_position[position].append(height_cm)

with open("common_player_info.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row.get("draft_number") == "30":
            position2 = row.get("position")
            height_str2 = row.get("height")
            height_cm2 = convert_height_to_cm(height_str)
            if position2 and height_cm2:
                if position2 not in heights_by_position2:
                    heights_by_position2[position2] = []
                heights_by_position2[position2].append(height_cm2)
# Afficher les résultats
print("Taille des No1 de draft (en cm) par poste :")
for position, heights in heights_by_position.items():
    print(f"{position} : {mean(heights)}")
print("Taille des No30 de draft (en cm) par poste :")
for position, heights in heights_by_position2.items():
    print(f"{position} : {mean(heights)}")