# app.py
from flask import Blueprint, Flask, request, render_template, redirect, url_for
import csv
import generer_html
import os

# Initialisation de l'instance Flask pour la capture des flux formulaires
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard_rugby.html')
def dashboard_rugby():
    return render_template('dashboard_rugby.html')

@app.route('/dashboard_football.html')
def dashboard_football():
    return render_template('dashboard_football.html')

@app.route('/dashboard_basketball.html')
def dashboard_basketball():
    return render_template('dashboard_basketball.html')

@app.route('/formrugby.html')
def form_rugby():
    return render_template('formrugby.html')

@app.route('/formfootball.html')
def form_football():
    return render_template('formfootball.html')

@app.route('/formbasketball.html')
def form_basketball():
    return render_template('formbasketball.html')

# --- PARTIE DATA  ---
import re

def evaluer_champ_optionnel(donnees_brutes, cle_dictionnaire, type_cible=int):
    """Retourne la valeur convertie si elle est renseignée, sinon la chaîne 'N/A'."""
    valeur_texte = donnees_brutes.get(cle_dictionnaire, "").strip()
    if valeur_texte == "":
        return "N/A"
    return type_cible(valeur_texte)


def normaliser_lien_video(lien):
    """
    Nettoie le lien et convertit les URLs YouTube (standards, courtes ou HTML complet)
    en liens d'intégration 'embed' valides pour un <iframe>.
    Extrait automatiquement l'URL si l'utilisateur a collé un tag <iframe> complet.
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

    return lien_nettoye

# ===== RUGBY =====
def valider_et_filtrer_donnees_rugby(donnees_brutes):
    """
    Prend en entrée le dictionnaire brut issu de request.form.
    Structure les champs obligatoires sous les bons types et applique la valeur
    par défaut 'N/A' aux métriques scientifiques optionnelles si elles sont vides.
    """
    # Structuration du dictionnaire propre (Table de hachage)
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

def enregistrer_dans_csv_rugby(donnees_finales):
    """
    Persiste les informations extraites dans la table performances_rugby.csv.
    L'usage du mode='a' permet l'écriture séquentielle sans écrasement.
    """
    output_dir = os.path.join('templates', 'matches', 'rugby')
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

@app.route('/upload_rugby', methods=['POST'])
def receptionner_formulaire_rugby():
    """
    Point de contact de l'API interceptant l'envoi du formulaire de saisie rugby.
    Supervise la validation, le stockage et instancie l'écriture du fichier HTML de match.
    """
    # 1. Traitement des types et des valeurs par défaut
    donnees_propres = valider_et_filtrer_donnees_rugby(request.form)
    
    # 2. Sauvegarde de la performance dans la table persistante
    enregistrer_dans_csv_rugby(donnees_propres)
    
    # 3. Activation du Générateur JAMstack pour créer la page de match autonome
    nom_fichier = generer_html.creer_page_match_rugby(donnees_propres)
    return redirect(url_for('voir_match', sport='rugby', nom_match=nom_fichier))

# ===== FOOTBALL =====
def valider_et_filtrer_donnees_football(donnees_brutes):
    """
    Validation et structuration des données pour le football.
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

def enregistrer_dans_csv_football(donnees_finales):
    """
    Persiste les informations extraites dans la table performances_football.csv.
    """
    output_dir = os.path.join('templates', 'matches', 'football')
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

@app.route('/upload_football', methods=['POST'])
def receptionner_formulaire_football():
    """
    Point de contact de l'API interceptant l'envoi du formulaire de saisie football.
    Supervise la validation, le stockage et instancie l'écriture du fichier HTML de match.
    """
    # 1. Traitement des types et des valeurs par défaut
    donnees_propres = valider_et_filtrer_donnees_football(request.form)
    
    # 2. Sauvegarde de la performance dans la table persistante
    enregistrer_dans_csv_football(donnees_propres)
    
    # 3. Activation du Générateur JAMstack pour créer la page de match autonome
    nom_fichier = generer_html.creer_page_match_football(donnees_propres)
    return redirect(url_for('voir_match', sport='football', nom_match=nom_fichier))


# ===== BASKETBALL =====
def valider_et_filtrer_donnees_basketball(donnees_brutes):
    """
    Validation et structuration des données pour le basketball.
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

def enregistrer_dans_csv_basketball(donnees_finales):
    """
    Persiste les informations extraites dans la table performances_basketball.csv.
    """
    output_dir = os.path.join('templates', 'matches', 'basketball')
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


@app.route('/upload_basketball', methods=['POST'])
def receptionner_formulaire_basketball():
    """
    Point de contact de l'API interceptant l'envoi du formulaire de saisie basketball.
    Supervise la validation, le stockage et instancie l'écriture du fichier HTML de match.
    """
    # 1. Traitement des types et des valeurs par défaut
    donnees_propres = valider_et_filtrer_donnees_basketball(request.form)
    
    # 2. Sauvegarde de la performance dans la table persistante
    enregistrer_dans_csv_basketball(donnees_propres)
    
    # 3. Activation du Générateur JAMstack pour créer la page de match autonome
    nom_fichier = generer_html.creer_page_match_basketball(donnees_propres)
    return redirect(url_for('voir_match', sport='basketball', nom_match=nom_fichier))
    
  
