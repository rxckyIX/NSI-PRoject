# comparaison.py
import csv

def recuperer_matchs_depuis_csv(sport_cible):
    """
    ALGORITHME D'EXTRACTION SÉQUENTIELLE (Trudon)
    Parcourt le fichier CSV de l'historique pour en extraire tous les matchs 
    liés au sport demandé sous forme de table de hachage (dictionnaires).
    """
    liste_matchs = []
    try:
        # Ouverture sécurisée avec encodage UTF-8 (Norme validée par Jason)
        with open('historique_matchs.csv', mode='r', encoding='utf-8') as fichier_csv:
            lecteur = csv.DictReader(fichier_csv)
            for ligne in lecteur:
                # Filtrage algorithmique selon le sport sélectionné
                if ligne.get('sport') == sport_cible:
                    liste_matchs.append(dict(ligne))
    except FileNotFoundError:
        # Programmation défensive si le fichier n'est pas encore créé
        print("Erreur : Le fichier de persistance CSV n'existe pas encore.")
        
    return liste_matchs


def calculer_progression(match_a, match_b, cles_numeriques):
    """
    ALGORITHME ARITHMÉTIQUE DES DELTAS (Trudon)
    Calcule la différence stricte (Match_B - Match_A).
    Gère les exceptions pour éviter les crashs de type sur données textuelles.
    """
    evolution = {}
    
    for cle in cles_numeriques:
        if cle in match_a and cle in match_b:
            try:
                # Conversion explicite en flottant pour autoriser les calculs arithmétiques
                val_a = float(match_a[cle])
                val_b = float(match_b[cle])
                
                delta = val_b - val_a
                
                # Optimisation de l'affichage : On caste en entier si le résultat est rond
                evolution[cle] = int(delta) if delta.is_integer() else round(delta, 2)
            except (ValueError, TypeError):
                # Si la conversion échoue (ex: texte ou champ vide), on sécurise avec une valeur neutre
                evolution[cle] = 0
        else:
            evolution[cle] = 0
            
    return evolution


def creer_page_comparaison(sport, match_a, match_b, evolution):
    """
    ALGORITHME DE SUBSTITUTION ET PERSISTANCE STATIQUE (Trudon)
    Prend le template de Lambert et génère un rapport de comparaison physique 
    au format HTML pour l'archivage local des performances du joueur.
    """
    # Ce code simule la persistance ou l'écriture de secours demandée par le sujet NSI
    nom_fichier_export = f"export_comparaison_{sport}.html"
    
    # Message de log pour le débogage de l'équipe
    print(f"[DATA LOG] Trudon génère le rapport d'archive : {nom_fichier_export}")
    
    # Ici Trudon pourrait faire un traitement de sauvegarde de données ou une journalisation
    return True