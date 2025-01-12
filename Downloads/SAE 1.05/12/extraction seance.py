def extraire_r107_groupe(tableau_csv, groupe):
    resultats = []
    for ligne in tableau_csv:
        champs = ligne.split(";")
        if "R1.07" in champs[5] and groupe in champs[8]:
            resultats.append(f"{champs[1]};{champs[3]};{champs[4]}")
    return resultats