import csv

def generer_html(csv_path, image_path, output_html_path):
    tableau_r107 = []

    # Lire le fichier CSV et extraire les séances de R1.07
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)  # Lire l'en-tête du fichier CSV
        print(f"Header: {header}")  # Impression de débogage
        for row in reader:
            print(f"Row: {row}")  # Impression de débogage
            if any("R1.07" in cell for cell in row):  # Vérifier si "R1.07" est dans la ligne
                tableau_r107.append(row)

    # Vérifier si des lignes ont été ajoutées
    print(f"Tableau R1.07: {tableau_r107}")  # Impression de débogage

    # Générer le HTML
    html = """<html>
    <head><title>Analyse des Séances</title></head>
    <body>
    <h1>Tableau des séances R1.07</h1>
    <table border='1'>
    <tr><th>Résumé</th><th>Début</th><th>Fin</th><th>Lieu</th></tr>
    """
    for ligne in tableau_r107:
        html += "<tr>"
        for cell in ligne:
            html += f"<td>{cell}</td>"
        html += "</tr>"

    html += f"""
    </table>
    <h1>Graphique des séances</h1>
    <img src='{image_path}' alt='Graphique'>
    </body>
    </html>
    """

    # Écrire le contenu HTML dans un fichier
    print(html)  # Impression du contenu HTML pour vérification
    with open(output_html_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html)

# Exemple d'utilisation
csv_path = 'c:/git/SAE105-1/SAE105/Downloads/SAE 1.05/12/calendrier.csv'
image_path = 'c:/git/SAE105-1/SAE105/Downloads/SAE 1.05/12/image.png'
output_html_path = 'c:/git/SAE105-1/SAE105/Downloads/SAE 1.05/12/seances_r107.html'
generer_html(csv_path, image_path, output_html_path)