
def lire_csv_sans_package(nom_fichier):
    with open(nom_fichier, "r", encoding="utf-8") as f:
        lignes = f.readlines()  # Lire toutes les lignes du fichier
    return [ligne.strip().split(",") for ligne in lignes]  # Nettoyer et séparer par virgule

# Exemple d'utilisation :
nom_fichier = "team.csv"  
donnees = lire_csv_sans_package(nom_fichier)
print(donnees)
