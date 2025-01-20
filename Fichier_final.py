import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, request, render_template
import os
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import spacy

nltk.download('vader_lexicon')
nlp = spacy.load("en_core_web_sm")

app = Flask(__name__)

def load_data(file_path):
    """Charge les données à partir d'un fichier CSV ou texte."""
    try:
        return pd.read_csv(file_path)
    except Exception as e:
        print(f"Erreur lors du chargement des données : {e}")
        return None

def save_data(df, output_file):
    """Sauvegarde les données dans un fichier CSV."""
    try:
        df.to_csv(output_file, index=False)
        print(f"Données sauvegardées dans {output_file}")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde des données : {e}")

def generate_graph(df, output_image_path, column_name):
    """Génère un graphique à partir d'un DataFrame."""
    if column_name in df.columns:
        plt.figure(figsize=(10, 6))
        df[column_name].value_counts().plot(kind='bar')
        plt.title(f'Graphique des données pour {column_name}')
        plt.xlabel('Catégories')
        plt.ylabel('Valeurs')
        plt.savefig(output_image_path)
        plt.close()
        print(f"Graphique généré : {output_image_path}")
    else:
        print(f"Erreur : La colonne '{column_name}' n'existe pas dans le DataFrame.")

def generate_html_from_dataframe(df, output_html_path, threats, attacks, errors):
    """Génère une page HTML à partir d'un DataFrame."""
    try:
        html_content = f"""
        <html>
        <head>
            <title>Menaces, Attaques et Erreurs détectées</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }}
                .container {{
                    width: 90%;
                    margin: auto;
                    overflow: hidden;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin: 20px 0;
                    font-size: 18px;
                    text-align: left;
                }}
                th, td {{
                    padding: 12px;
                    border: 1px solid #ddd;
                }}
                th {{
                    background-color: #4CAF50;
                    color: white;
                }}
                tr:nth-child(even) {{
                    background-color: #f2f2f2;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Menaces, Attaques et Erreurs détectées</h1>
        """

        if threats or attacks or errors:
            html_content += "<table><thead><tr><th>Ligne</th><th>Type</th><th>Texte</th><th>Explications</th></tr></thead><tbody>"
            for threat in threats:
                html_content += f"<tr><td>{threat['ligne']}</td><td>Menace</td><td>{threat['texte']}</td><td>{threat['explications']}</td></tr>"
            for attack in attacks:
                html_content += f"<tr><td>{attack['ligne']}</td><td>Attaque</td><td>{attack['texte']}</td><td>{attack['explications']}</td></tr>"
            for error in errors:
                html_content += f"<tr><td>{error['ligne']}</td><td>Erreur</td><td>{error['texte']}</td><td>{error['explications']}</td></tr>"
            html_content += "</tbody></table>"
        else:
            html_content += "<p>Aucune menace, attaque ou erreur détectée.</p>"

        html_content += """
            </div>
        </body>
        </html>
        """

        with open(output_html_path, 'w', encoding='utf-8') as file:
            file.write(html_content)
        print(f"Fichier HTML généré : {output_html_path}")
    except Exception as e:
        print(f"Erreur lors de la génération du HTML : {e}")

def analyze_text(text):
    """Analyse le texte pour détecter des menaces, des attaques et des erreurs."""
    sid = SentimentIntensityAnalyzer()
    sentiment_scores = sid.polarity_scores(text)
    doc = nlp(text)
    threats = []
    attacks = []
    errors = []
    explanations = []

    for token in doc:
        if token.dep_ == 'neg':
            threats.append(token.text)
            explanations.append(f"Le mot '{token.text}' est une négation, ce qui peut indiquer une menace.")
        if token.dep_ == 'dobj' and token.head.dep_ == 'ROOT':
            attacks.append(token.text)
            explanations.append(f"Le mot '{token.text}' est un objet direct de l'action '{token.head.text}', ce qui peut indiquer une attaque.")
        if token.dep_ == 'amod':
            errors.append(token.text)
            explanations.append(f"Le mot '{token.text}' est un modificateur adjectival, ce qui peut indiquer une erreur.")

    return threats, attacks, errors, explanations

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        column_name = request.form.get('column_name')
        if file and column_name:
            df = pd.read_csv(file)
            output_image_path = os.path.join('static', 'output.png')
            generate_graph(df, output_image_path, column_name)
            return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values, image=output_image_path)
    return render_template('index.html')

def main():
    file_path = input("Entrez le chemin du fichier CSV ou texte à traiter : ").strip()

    # Charger les données
    df = load_data(file_path)
    if df is None:
        print("Impossible de traiter le fichier. Assurez-vous qu'il est valide et supporté.")
        return

    # Analyser les données pour détecter des menaces, des attaques et des erreurs
    all_threats = []
    all_attacks = []
    all_errors = []
    for index, row in df.iterrows():
        text = ' '.join(map(str, row.values))
        threats, attacks, errors, explanations = analyze_text(text)
        if threats:
            all_threats.append({'ligne': index + 1, 'texte': ', '.join(threats), 'explications': ', '.join(explanations)})
        if attacks:
            all_attacks.append({'ligne': index + 1, 'texte': ', '.join(attacks), 'explications': ', '.join(explanations)})
        if errors:
            all_errors.append({'ligne': index + 1, 'texte': ', '.join(errors), 'explications': ', '.join(explanations)})
        print(f"Ligne {index + 1} :")
        print(f"Menaces détectées : {', '.join(threats)}")
        print(f"Attaques détectées : {', '.join(attacks)}")
        print(f"Erreurs détectées : {', '.join(errors)}")
        print(f"Explications : {', '.join(explanations)}")

    # Sauvegarder les données traitées
    output_file = "output.csv"
    save_data(df, output_file)

    # Chemin du fichier de sortie HTML
    html_file = "output.html"

    # Génération de la page HTML
    generate_html_from_dataframe(df, html_file, all_threats, all_attacks, all_errors)

if __name__ == "__main__":
    main()
    app.run(debug=True)