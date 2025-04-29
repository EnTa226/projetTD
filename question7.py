import pandas as pd
import matplotlib.pyplot as plt

# Fonction de conversion de la taille en cm
def convert_height_to_cm(height_str):
    try:
        feet, inches = map(int, height_str.split("-"))
        return round(feet * 30.48 + inches * 2.54, 2)
    except:
        return None

# Chargement des données
df = pd.read_csv("common_player_info.csv")

# Conversion des tailles
df["height_cm"] = df["height"].apply(convert_height_to_cm)

# Suppression des lignes avec tailles manquantes ou poste manquant
df_clean = df.dropna(subset=["height_cm", "position"])

# Création du boxplot
plt.figure(figsize=(10, 6))
df_clean.boxplot(column="height_cm", by="position")
plt.title("Répartition des tailles (en cm) des joueurs par poste")
plt.suptitle("")  # Supprime le titre automatique "Boxplot grouped by position"
plt.xlabel("Poste")
plt.ylabel("Taille (cm)")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()

# Affichage
plt.show()
