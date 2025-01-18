def extraire_r107(tableau_csv, groupe):
    resultats = []
    for ligne in tableau_csv:
        champs = ligne.split(";")
        if "R1.07" in champs[5] and groupe in champs[8]:
            resultats.append(f"{champs[1]};{champs[3]};{champs[4]}")
    return resultats

tableau_csv = convertir_calendrier_ics_en_csv("calendrier.ics")
seances_r107 = extraire_r107(tableau_csv, "A1")
for ligne in seances_r107:
    print(ligne)
