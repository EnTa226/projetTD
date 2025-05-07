import pandas as pd


def convert_height_to_cm(height_str):
    try:
        feet, inches = map(int, height_str.split("-"))
        return round(feet * 30.48 + inches * 2.54, 2)
    except (ValueError, AttributeError):
        return None


df = pd.read_csv("common_player_info.csv")

# Nettoyage / conversion
df["draft_number"] = pd.to_numeric(df["draft_number"], errors="coerce")
df["height_cm"] = df["height"].apply(convert_height_to_cm)

# Filtrage et groupement
draft_1 = df[df["draft_number"] == 1]
mean_heights_1 = draft_1.groupby("position")["height_cm"].mean()

draft_30 = df[df["draft_number"] == 30]
mean_heights_30 = draft_30.groupby("position")["height_cm"].mean()

# Affichage
print("Taille des No1 de draft (en cm) par poste :")
print(mean_heights_1)

print("\nTaille des No30 de draft (en cm) par poste :")
print(mean_heights_30)
