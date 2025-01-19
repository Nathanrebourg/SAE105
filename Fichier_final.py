import pandas as pd

def load_data(file_path):
    try:
        # Lire le fichier CSV en morceaux (chunks) avec low_memory=False
        chunksize = 10000  # Nombre de lignes par morceau
        chunks = pd.read_csv(file_path, sep=';', chunksize=chunksize, on_bad_lines='skip', low_memory=False)

        # Initialiser une liste pour stocker les morceaux
        data_list = []

        # Traiter chaque morceau
        for chunk in chunks:
            data_list.append(chunk)

        # Combiner tous les morceaux en un seul DataFrame
        df = pd.concat(data_list, ignore_index=True)
        return df

    except Exception as e:
        print(f"Erreur lors du chargement du fichier : {e}")
        return None

def save_data(df, output_file):
    """Génère un fichier CSV à partir d'un DataFrame."""
    try:
        df.to_csv(output_file, index=False, sep=';', encoding='utf-8')
        print(f"Fichier CSV généré : {output_file}")
    except Exception as e:
        print(f"Erreur lors de la génération du CSV : {e}")

def generate_html_from_dataframe(df, output_html_path):
    """Génère une page HTML à partir d'un DataFrame."""
    try:
        html_content = """
        <html>
        <head>
            <title>Analyse des Séances</title>
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
            <h1>Tableau des séances</h1>
            <table>
                <tr>
        """
        # Ajouter les en-têtes de colonnes
        for column in df.columns:
            html_content += f"<th>{column}</th>"
        html_content += "</tr>"

        # Ajouter les données
        for _, row in df.iterrows():
            html_content += "<tr>"
            for cell in row:
                html_content += f"<td>{cell}</td>"
            html_content += "</tr>"
        
        html_content += """
            </table>
        </body>
        </html>
        """

        with open(output_html_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"Fichier HTML généré : {output_html_path}")
    except Exception as e:
        print(f"Erreur lors de la génération du HTML : {e}")

def main():
    file_path = input("Entrez le chemin du fichier CSV à traiter : ").strip()

    # Charger les données
    df = load_data(file_path)
    if df is None:
        print("Impossible de traiter le fichier. Assurez-vous qu'il est valide et supporté.")
        return

    # Sauvegarder les données traitées
    output_file = "output.csv"
    save_data(df, output_file)

    # Chemins des fichiers de sortie
    html_file = "output.html"

    # Génération de la page HTML
    generate_html_from_dataframe(df, html_file)

if __name__ == "__main__":
    main()