def rechercher_chaine_dans_fichier(chemin_fichier, chaine_recherche):
    try:
        with open(chemin_fichier, 'r') as fichier:
            for ligne in fichier:
                if chaine_recherche.lower() in ligne.lower(): 
                    print(ligne.strip()) 
    except FileNotFoundError:
        print("Le chemin : ", chemin_fichier," n'a pas été trouvé")
    except IOError:
        print("impossible de lire le fichier")

chemin_fichier = "C:/Users/Admin/Downloads/evenementSAE_15.ics"
chaine_recherche = input("Entrez la chaîne de caractères à rechercher : ")

rechercher_chaine_dans_fichier(chemin_fichier, chaine_recherche)
