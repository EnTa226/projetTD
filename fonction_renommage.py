import csv

def get_full_team_names(file_path):
    abbreviations = {}

    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Domicile
            abbr_home = row["team_abbreviation_home"]
            name_home = row["team_name_home"]
            abbreviations[abbr_home] = name_home

            # Extérieur
            abbr_away = row["team_abbreviation_away"]
            name_away = row["team_name_away"]
            abbreviations[abbr_away] = name_away

    return abbreviations


abbr_to_full = get_full_team_names("game.csv")

# Afficher les résultats
for abbr, full_name in abbr_to_full.items():
    print(f"{abbr} : {full_name}")
