import pandas as pd

file_path = "test.csv"
output_file_path = "test_with_headers.csv"

# Lire un petit échantillon pour vérifier le nombre de colonnes
sample = pd.read_csv(file_path, sep=';', header=None, nrows=5)
print(sample.head())
print(f"Number of columns: {len(sample.columns)}")

# Définir les noms de colonnes en fonction du nombre de colonnes dans le fichier CSV
# Ajustez le nombre de colonnes en fonction de votre fichier CSV
column_names = ["Date", "Intitulé", "Type", "Professeur", "Groupe", "Durée", "Ressource", "Col8", "Col9", "Col10", "Col11", "Col12"]

# Lire le fichier CSV en morceaux (chunks) avec low_memory=False
chunksize = 10000  # Nombre de lignes par morceau
chunks = pd.read_csv(file_path, sep=';', header=None, chunksize=chunksize, on_bad_lines='skip', low_memory=False)

# Initialiser une variable pour vérifier si c'est le premier morceau
is_first_chunk = True

# Traiter chaque morceau
for chunk in chunks:
    # Vérifier le nombre de colonnes dans le chunk
    print(f"Chunk columns: {len(chunk.columns)}")
    
    # Attribuer des noms de colonnes si le nombre de colonnes correspond
    if len(chunk.columns) == len(column_names):
        chunk.columns = column_names
    else:
        print("Mismatch in number of columns. Skipping this chunk.")
        continue
    
    # Écrire le DataFrame dans un fichier CSV
    chunk.to_csv(output_file_path, mode='a', index=False, sep=';', header=is_first_chunk)
    
    # Après le premier morceau, ne plus écrire les en-têtes
    is_first_chunk = False

print("Traitement terminé et fichier CSV généré.")