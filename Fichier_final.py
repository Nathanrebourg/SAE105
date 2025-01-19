import pandas as pd
import os

def detect_file_type(file_path):
    """Détecte le type de fichier à partir de son extension."""
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower()

def load_data(file_path):
    """Charge les données à partir d'un fichier CSV, Excel ou JSON."""
    file_type = detect_file_type(file_path)
    try:
        if file_type == ".csv":
            return pd.read_csv(file_path, sep=None, engine='python')  # Détection automatique du séparateur
        elif file_type in [".xls", ".xlsx"]:
            return pd.read_excel(file_path)
        elif file_type == ".json":
            return pd.read_json(file_path)
        else:
            raise ValueError("Type de fichier non supporté : " + file_type)
    except Exception as e:
        print(f"Erreur lors du chargement du fichier : {e}")
        return None

def generate_html_from_dataframe(df, output_file="output.html"):
    """Génère une page HTML interactive à partir d'un DataFrame."""
    try:
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Tableau des Données</title>
            <style>
                table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                th, td {{
                    border: 1px solid #ddd;
                    padding: 8px;
                }}
                th {{
                    background-color: #f2f2f2;
                    text-align: left;
                }}
                tr:nth-child(even) {{
                    background-color: #f9f9f9;
                }}
            </style>
        </head>
        <body>
            <h1>Tableau des Données</h1>
            {df.to_html(index=False, escape=False)}
        </body>
        </html>
        """
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"Fichier HTML généré : {output_file}")
    except Exception as e:
        print(f"Erreur lors de la génération de la page HTML : {e}")

def main():
    file_path = input("Entrez le chemin du fichier à traiter : ").strip()

    # Charger les données
    df = load_data(file_path)
    if df is None:
        print("Impossible de traiter le fichier. Assurez-vous qu'il est valide et supporté.")
        return

    # Chemins des fichiers de sortie
    html_file = "output.html"

    # Génération de la page HTML
    generate_html_from_dataframe(df, html_file)

if __name__ == "__main__":
    main()
