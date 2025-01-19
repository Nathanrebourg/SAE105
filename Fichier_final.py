import pandas as pd

def load_csv(file_path):
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
        print(f"Erreur lors du chargement du fichier CSV : {e}")
        return None

def load_text(file_path):
    try:
        # Lire le fichier texte en utilisant pandas
        df = pd.read_csv(file_path, sep='\t', header=None)
        return df

    except Exception as e:
        print(f"Erreur lors du chargement du fichier texte : {e}")
        return None

def load_data(file_path):
    if file_path.endswith('.csv'):
        return load_csv(file_path)
    elif file_path.endswith('.txt'):
        return load_text(file_path)
    else:
        print("Format de fichier non supporté. Veuillez fournir un fichier CSV ou texte.")
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
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }
                .container {
                    width: 90%;
                    margin: auto;
                    overflow: hidden;
                }
                table {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    font-size: 18px;
                    text-align: left;
                }
                th, td {
                    padding: 12px;
                    border: 1px solid #ddd;
                }
                th {
                    background-color: #4CAF50;
                    color: white;
                }
                tr:nth-child(even) {
                    background-color: #f2f2f2;
                }
                @media (max-width: 600px) {
                    table, thead, tbody, th, td, tr {
                        display: block;
                    }
                    th {
                        position: absolute;
                        top: -9999px;
                        left: -9999px;
                    }
                    tr {
                        border: 1px solid #ccc;
                    }
                    td {
                        border: none;
                        border-bottom: 1px solid #eee;
                        position: relative;
                        padding-left: 50%;
                    }
                    td:before {
                        content: attr(data-label);
                        position: absolute;
                        left: 0;
                        width: 50%;
                        padding-left: 15px;
                        font-weight: bold;
                        white-space: nowrap;
                    }
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Tableau des séances</h1>
                <table>
                    <thead>
                        <tr>
        """
        # Ajouter les en-têtes de colonnes
        for column in df.columns:
            html_content += f"<th>{column}</th>"
        html_content += "</tr></thead><tbody>"

        # Ajouter les données
        for _, row in df.iterrows():
            html_content += "<tr>"
            for cell, column in zip(row, df.columns):
                html_content += f"<td data-label='{column}'>{cell}</td>"
            html_content += "</tr>"
        
        html_content += """
                    </tbody>
                </table>
            </div>
        </body>
        </html>
        """

        with open(output_html_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"Fichier HTML généré : {output_html_path}")
    except Exception as e:
        print(f"Erreur lors de la génération du HTML : {e}")

def main():
    file_path = input("Entrez le chemin du fichier CSV ou texte à traiter : ").strip()

    # Charger les données
    df = load_data(file_path)
    if df is None:
        print("Impossible de traiter le fichier. Assurez-vous qu'il est valide et supporté.")
        return

    # Sauvegarder les données traitées
    output_file = "output.csv"
    save_data(df, output_file)

    # Chemin du fichier de sortie HTML
    html_file = "output.html"

    # Génération de la page HTML
    generate_html_from_dataframe(df, html_file)

if __name__ == "__main__":
    main()