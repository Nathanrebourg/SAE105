def generer_html(tableau_r107, image_path):
    html = """<html>
    <head><title>Analyse des Séances</title></head>
    <body>
    <h1>Tableau des séances R1.07</h1>
    <table border='1'>
    <tr><th>Date</th><th>Durée</th><th>Type</th></tr>
    """
    for ligne in tableau_r107:
        date, duree, type_seance = ligne.split(";")
        html += f"<tr><td>{date}</td><td>{duree}</td><td>{type_seance}</td></tr>"

    html += f"""
    </table>
    <h1>Graphique des séances</h1>
    <img src='{image_path}' alt='Graphique'>
    </body>
    </html>
    """
    with open("resultat.html", "w") as f:
        f.write(html)