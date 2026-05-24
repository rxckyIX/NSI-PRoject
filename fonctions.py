# app.py
from flask import Blueprint, request, render_template, redirect, url_for
import csv
import generer_html

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

def evaluer_champ_optionnel(donnees_brutes, cle_dictionnaire, type_cible=int):
    """Retourne la valeur convertie si elle est renseignée, sinon la chaîne 'N/A'."""
    valeur_texte = donnees_brutes.get(cle_dictionnaire, "").strip()
    if valeur_texte == "":
        return "N/A"
    return type_cible(valeur_texte)

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
    with open('performances_rugby.csv', mode='a', newline='', encoding='utf-8') as fichier_csv:
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
    return redirect(f"/{nom_fichier}")

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
    with open('performances_football.csv', mode='a', newline='', encoding='utf-8') as fichier_csv:
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
    return redirect(f"/{nom_fichier}")


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
    with open('performances_basketball.csv', mode='a', newline='', encoding='utf-8') as fichier_csv:
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
    return redirect(f"/{nom_fichier}")
    
  
