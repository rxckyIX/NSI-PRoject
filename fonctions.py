import csv
import os
import re


def normaliser_nom_fichier(titre, date):
    """
    Objectif principal : Convertir le titre et la date en un nom de fichier standardisé.
    
    Entrée(s) :
        - titre (str) : Titre brut du match.
        - date (str) : Date du match sous format texte.
        
    Sortie(s) :
        - (str) : Nom du fichier formaté, sans espaces ni caractères spéciaux.
    """
    titre_sain = titre.lower().replace(" ", "-")
    for caractere in [":", "/", "'", ".", ",", '"', "?", "!", "@", "#", "$", "*"]:
        titre_sain = titre_sain.replace(caractere, "")
    return f"match_{titre_sain}_{date}"


def evaluer_champ_optionnel(donnees_brutes, cle_dictionnaire, type_cible=int):
    """
    Objectif principal : Convertir un champ optionnel s'il existe, sinon renvoyer "N/A".
    
    Entrée(s) :
        - donnees_brutes (dict) : Données issues du formulaire (request.form).
        - cle_dictionnaire (str) : La clé à extraire.
        - type_cible (type) : Le type attendu (int par défaut).
        
    Sortie(s) :
        - (type_cible ou str) : La valeur convertie ou la chaîne "N/A".
    """
    valeur_texte = donnees_brutes.get(cle_dictionnaire, "").strip()
    if valeur_texte == "":
        return "N/A"
    return type_cible(valeur_texte)


def normaliser_lien_video(lien):
    """
    Objectif principal : Convertir toute URL YouTube ou iframe en un lien 'embed' pur.
    
    Entrée(s) :
        - lien (str) : Lien brut de la vidéo ou bloc HTML iframe.
        
    Sortie(s) :
        - (str) : URL compatible pour intégration, ou "N/A" si vide.
    """
    lien_nettoye = lien.strip()
    if lien_nettoye == "":
        return "N/A"

    # 1. Si l'utilisateur a collé un bloc HTML <iframe> complet, on extrait l'URL du 'src'.
    # src=["\'] : cherche l'attribut src suivi de guillemets simples ou doubles.
    # ([^"\']+) : capture tout le texte jusqu'au prochain guillemet (l'URL elle-même).
    iframe_match = re.search(r'src=["\']([^"\']+)["\']', lien_nettoye)
    if iframe_match:
        lien_nettoye = iframe_match.group(1) # On ne conserve que l'URL pure extraite du code HTML.

    # 2. Identification de l'identifiant unique de la vidéo YouTube (11 caractères).
    # (?:v=|youtu\.be/|embed/) : cherche un de ces 3 motifs sans le mémoriser.
    # ([A-Za-z0-9_-]{11}) : capture précisément l'ID de 11 caractères qui suit.
    match = re.search(r'(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})', lien_nettoye)
    
    if match:
        # Si un ID est trouvé, on reconstruit une URL d'intégration propre.
        return f"https://www.youtube.com/embed/{match.group(1)}"

    # Si aucun ID YouTube n'est détecté mais que c'est déjà un lien embed connu (ex: Vimeo), on le garde.
    if 'youtube.com/embed/' in lien_nettoye or 'player.vimeo.com/video/' in lien_nettoye:
        return lien_nettoye

    # Si le lien n'a aucun format valide reconnu, on l'invalide pour éviter de casser l'iframe.
    return "N/A"


# ===== RUGBY =====
def valider_et_filtrer_donnees_rugby(donnees_brutes):
    """
    Objectif principal : Extraire et nettoyer les données du formulaire de rugby.
    
    Entrée(s) :
        - donnees_brutes (dict) : Dictionnaire brut des requêtes.
        
    Sortie(s) :
        - (dict) : Dictionnaire contenant les données sécurisées et typées.
    """
    donnees_traitees = {
        "titre_match": donnees_brutes.get("titre_match"),
        "competition": donnees_brutes.get("competition"),
        "adversaire": donnees_brutes.get("adversaire"),
        "date_match": donnees_brutes.get("date_match"),
        "score_notre_equipe": int(donnees_brutes.get("score_notre_equipe", 0)),
        "score_adversaire": int(donnees_brutes.get("score_adversaire", 0)),
        "resultat": donnees_brutes.get("resultat"),
        "essais": int(donnees_brutes.get("essais", 0)),
        "evaluation": donnees_brutes.get("evaluation"),
        "video_url": normaliser_lien_video(donnees_brutes.get("video_url", "")),
        
        "passes_totales": evaluer_champ_optionnel(donnees_brutes, "passes", int),
        "plaquages": evaluer_champ_optionnel(donnees_brutes, "plaquages", int),
        "temps_jeu": evaluer_champ_optionnel(donnees_brutes, "temps_jeu", int),
        "distance": evaluer_champ_optionnel(donnees_brutes, "distance", float)
    }
    return donnees_traitees


def enregistrer_dans_csv_rugby(donnees_finales, username):
    """
    Objectif principal : Sauvegarder les données de rugby dans le fichier CSV de l'utilisateur.
    
    Entrée(s) :
        - donnees_finales (dict) : Données validées à sauvegarder.
        - username (str) : Nom d'utilisateur de la session.
        
    Sortie(s) :
        - Aucune. Modifie le fichier CSV physiquement.
    """
    output_dir = os.path.join('templates', 'matches', 'rugby', username)
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, 'performances_rugby.csv')
    with open(file_path, mode='a', newline='', encoding='utf-8') as fichier_csv:
        scripteur = csv.writer(fichier_csv)
        scripteur.writerow([
            donnees_finales["titre_match"],
            donnees_finales["competition"],
            donnees_finales["adversaire"],
            donnees_finales["date_match"],
            donnees_finales["score_notre_equipe"],
            donnees_finales["score_adversaire"],
            donnees_finales["resultat"],
            donnees_finales["essais"],
            donnees_finales["evaluation"],
            donnees_finales["video_url"],
            donnees_finales["passes_totales"],
            donnees_finales["plaquages"],
            donnees_finales["temps_jeu"],
            donnees_finales["distance"]
        ])


# ===== FOOTBALL =====
def valider_et_filtrer_donnees_football(donnees_brutes):
    """
    Objectif principal : Extraire et nettoyer les données du formulaire de football.
    
    Entrée(s) :
        - donnees_brutes (dict) : Dictionnaire brut des requêtes.
        
    Sortie(s) :
        - (dict) : Dictionnaire contenant les données sécurisées et typées.
    """
    donnees_traitees = {
        "titre_match": donnees_brutes.get("titre_match"),
        "competition": donnees_brutes.get("competition"),
        "adversaire": donnees_brutes.get("adversaire"),
        "date_match": donnees_brutes.get("date_match"),
        "score_notre_equipe": int(donnees_brutes.get("score_notre_equipe", 0)),
        "score_adversaire": int(donnees_brutes.get("score_adversaire", 0)),
        "resultat": donnees_brutes.get("resultat"),
        "evaluation": donnees_brutes.get("evaluation"),
        "video_url": normaliser_lien_video(donnees_brutes.get("video_url", "")),
        
        "buts": int(donnees_brutes.get("buts", 0)),
        "passes_decisives": evaluer_champ_optionnel(donnees_brutes, "passes_decisives", int),
        "temps_jeu": evaluer_champ_optionnel(donnees_brutes, "temps_jeu", int),
        "distance": evaluer_champ_optionnel(donnees_brutes, "distance", float)
    }
    return donnees_traitees


def enregistrer_dans_csv_football(donnees_finales, username):
    """
    Objectif principal : Sauvegarder les données de foot dans le CSV de l'utilisateur.
    
    Entrée(s) :
        - donnees_finales (dict) : Données validées à sauvegarder.
        - username (str) : Nom d'utilisateur de la session.
        
    Sortie(s) :
        - Aucune.
    """
    output_dir = os.path.join('templates', 'matches', 'football', username)
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, 'performances_football.csv')
    with open(file_path, mode='a', newline='', encoding='utf-8') as fichier_csv:
        scripteur = csv.writer(fichier_csv)
        scripteur.writerow([
            donnees_finales["titre_match"],
            donnees_finales["competition"],
            donnees_finales["adversaire"],
            donnees_finales["date_match"],
            donnees_finales["score_notre_equipe"],
            donnees_finales["score_adversaire"],
            donnees_finales["resultat"],
            donnees_finales["evaluation"],
            donnees_finales["video_url"],
            donnees_finales["buts"],
            donnees_finales["passes_decisives"],
            donnees_finales["temps_jeu"],
            donnees_finales["distance"]
        ])



# ===== BASKETBALL =====
def valider_et_filtrer_donnees_basketball(donnees_brutes):
    """
    Objectif principal : Extraire et nettoyer les données du formulaire de basketball.
    
    Entrée(s) :
        - donnees_brutes (dict) : Dictionnaire brut des requêtes.
        
    Sortie(s) :
        - (dict) : Dictionnaire contenant les données sécurisées et typées.
    """
    donnees_traitees = {
        "titre_match": donnees_brutes.get("titre_match"),
        "competition": donnees_brutes.get("competition"),
        "adversaire": donnees_brutes.get("adversaire"),
        "date_match": donnees_brutes.get("date_match"),
        "score_notre_equipe": int(donnees_brutes.get("score_notre_equipe", 0)),
        "score_adversaire": int(donnees_brutes.get("score_adversaire", 0)),
        "resultat": donnees_brutes.get("resultat"),
        "evaluation": donnees_brutes.get("evaluation"),
        "video_url": normaliser_lien_video(donnees_brutes.get("video_url", "")),
        
        "points": int(donnees_brutes.get("points", 0)),
        "passes_ajustees": evaluer_champ_optionnel(donnees_brutes, "passes_ajustees", int),
        "temps_jeu": evaluer_champ_optionnel(donnees_brutes, "temps_jeu", int),
        "distance": evaluer_champ_optionnel(donnees_brutes, "distance", float)
    }
    return donnees_traitees


def enregistrer_dans_csv_basketball(donnees_finales, username):
    """
    Objectif principal : Sauvegarder les données basket dans le CSV de l'utilisateur.
    
    Entrée(s) :
        - donnees_finales (dict) : Données validées à sauvegarder.
        - username (str) : Nom d'utilisateur de la session.
        
    Sortie(s) :
        - Aucune.
    """
    output_dir = os.path.join('templates', 'matches', 'basketball', username)
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, 'performances_basketball.csv')
    with open(file_path, mode='a', newline='', encoding='utf-8') as fichier_csv:
        scripteur = csv.writer(fichier_csv)
        scripteur.writerow([
            donnees_finales["titre_match"],
            donnees_finales["competition"],
            donnees_finales["adversaire"],
            donnees_finales["date_match"],
            donnees_finales["score_notre_equipe"],
            donnees_finales["score_adversaire"],
            donnees_finales["resultat"],
            donnees_finales["evaluation"],
            donnees_finales["video_url"],
            donnees_finales["points"],
            donnees_finales["passes_ajustees"],
            donnees_finales["temps_jeu"],
            donnees_finales["distance"]
        ])
    
  
