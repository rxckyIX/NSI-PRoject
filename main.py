import os
import comparaison
from flask import Flask, render_template, send_from_directory, request, redirect, url_for
import generer_html
from fonctions_form import (
    valider_et_filtrer_donnees_rugby,
    valider_et_filtrer_donnees_football,
    valider_et_filtrer_donnees_basketball,
    enregistrer_dans_csv_rugby,
    enregistrer_dans_csv_football,
    enregistrer_dans_csv_basketball,
)

# Initialisation de l'instance Flask pour la capture des flux formulaires
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/dashboard_rugby.html')
def dashboard_rugby():
    # List only files in the rugby folder
    matches = [f for f in os.listdir('templates/matches/rugby') if f.endswith('.html')]
    return render_template('dashboard_rugby.html', matches=matches)

@app.route('/football')
def dashboard_football():
    matches = [f for f in os.listdir('templates/matches/football') if f.endswith('.html')]
    return render_template('dashboard_football.html', matches=matches)

@app.route('/basketball')
def dashboard_basketball():
    matches = [f for f in os.listdir('templates/matches/basketball') if f.endswith('.html')]
    return render_template('dashboard_basketball.html', matches=matches)

@app.route('/rugby/form')
def form_rugby():
    return render_template('formrugby.html')

@app.route('/football/form')
def form_football():
    return render_template('formfootball.html')

@app.route('/basketball/form')
def form_basketball():
    return render_template('formbasketball.html')

@app.route('/upload_rugby', methods=['POST'])
def upload_rugby():
    donnees_propres = valider_et_filtrer_donnees_rugby(request.form)
    enregistrer_dans_csv_rugby(donnees_propres)
    nom_fichier = generer_html.creer_page_match_rugby(donnees_propres)
    return redirect(url_for('voir_match', sport='rugby', nom_match=nom_fichier))

@app.route('/upload_football', methods=['POST'])
def upload_football():
    donnees_propres = valider_et_filtrer_donnees_football(request.form)
    enregistrer_dans_csv_football(donnees_propres)
    nom_fichier = generer_html.creer_page_match_football(donnees_propres)
    return redirect(url_for('voir_match', sport='football', nom_match=nom_fichier))

@app.route('/upload_basketball', methods=['POST'])
def upload_basketball():
    donnees_propres = valider_et_filtrer_donnees_basketball(request.form)
    enregistrer_dans_csv_basketball(donnees_propres)
    nom_fichier = generer_html.creer_page_match_basketball(donnees_propres)
    return redirect(url_for('voir_match', sport='basketball', nom_match=nom_fichier))

@app.route('/view/<sport>/<nom_match>')
def voir_match(sport, nom_match):
    """Sert dynamiquement les rapports de match stockés dans les sous-dossiers."""
    return send_from_directory(os.path.join('templates/matches', sport), f"{nom_match}.html")

@app.route('/comparaison', methods=['GET', 'POST'])
def gerer_comparaison():
    """
    Contrôleur principal de l'outil analytique.
    Gère l'aiguillage du flux de données entre l'historique CSV et l'affichage final.
    """
    # Pour ce sprint, le sport cible est configuré par défaut (ex: le rugby)
    sport_actuel = "rugby"
    
    # ----------------------------------------------------------------------
    # CAS INTERCEPTION DU FORMULAIRE (MÉTHODE POST)
    # ----------------------------------------------------------------------
    if request.method == 'POST':
        # CAPTURE MULTIPLE : Récupération des valeurs sous forme de liste Python
        # Contient les identifiants uniques (Titre_Date) des cases cochées chez Lambert
        matchs_selectionnes = request.form.getlist('matchs_choisis')
        
        # PROGRAMMATION DÉFENSIVE : Validation de la contrainte métier (strictement 2 matchs)
        if len(matchs_selectionnes) != 2:
            # Si la contrainte n'est pas respectée, on recharge le formulaire initial
            # en injectant un message d'erreur explicite pour l'expérience utilisateur (UI)
            matchs_disponibles = comparaison.recuperer_matchs_depuis_csv(sport_actuel)
            return render_template(
                'comparaison.html', 
                matchs=matchs_disponibles,
                erreur="Veuillez sélectionner exactement deux matchs pour pouvoir lancer la comparaison."
            )
            
        # EXTRACTION SECURISEE : On récupère l'ensemble des dictionnaires depuis le CSV
        historique_complet = comparaison.recuperer_matchs_depuis_csv(sport_actuel)
        
        # Initialisation des pointeurs pour isoler nos deux fiches cibles
        match_a = None
        match_b = None
        
        # RECHERCHE ALGORITHMIQUE : Association des chaînes d'identifiants aux dictionnaires complets
        for match in historique_complet:
            # Reconstitution de la clé primaire textuelle (Titre_Date)
            identifiant_cible = f"{match['titre_match']}_{match['date_match']}"
            
            if identifiant_cible == matchs_selectionnes[0]:
                match_a = match
            if identifiant_cible == matchs_selectionnes[1]:
                match_b = match

        # Si nos deux entités de données ont été trouvées avec succès dans le CSV
        if match_a and match_b:
            # Spécification des descripteurs numériques sur lesquels l'analyse peut s'exécuter
            cles_numeriques = ["score_notre_equipe", "score_adversaire", "temps_jeu", "distance"]
            if sport_actuel == "rugby":
                cles_numeriques += ["essais", "passes_totales", "plaquages"]
                
            # DELEGATION ALGORITHMIQUE : Trudon prend la main pour calculer les écarts mathématiques
            dictionnaire_deltas = comparaison.calculer_progression(match_a, match_b, cles_numeriques)
            
            # APPEL DE PERSISTANCE SYSTEME : Trudon crée l'archive locale de sauvegarde
            comparaison.creer_page_comparaison(sport_actuel, match_a, match_b, dictionnaire_deltas)
            
            # INJECTION ET RESTITUTION : Envoi des 3 structures de données au template de Lambert
            return render_template(
                'resultat_comparaison.html', 
                match_a=match_a, 
                match_b=match_b, 
                evolution=dictionnaire_deltas
            )

    # ----------------------------------------------------------------------
    # CAS AFFICHAGE INITIAL DE LA PAGE (MÉTHODE GET)
    # ----------------------------------------------------------------------
    # On lit simplement le CSV via le module Data de Trudon pour afficher la liste des choix possibles
    matchs_disponibles = comparaison.recuperer_matchs_depuis_csv(sport_actuel)
    return render_template('comparaison.html', matchs=matchs_disponibles)

if __name__ == '__main__':
    # Démarrage du serveur web local de développement
    app.run(debug=True)