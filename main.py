import os
import shutil
from flask import Flask, render_template, send_from_directory, request, redirect, url_for, session
import generer_html
from fonctions import (
    valider_et_filtrer_donnees_rugby,
    valider_et_filtrer_donnees_football,
    valider_et_filtrer_donnees_basketball,
    enregistrer_dans_csv_rugby,
    enregistrer_dans_csv_football,
    enregistrer_dans_csv_basketball,
)

# Initialisation de l'instance Flask pour la capture des flux formulaires
app = Flask(__name__)
app.secret_key = "okay"

@app.before_request
def require_login():
    """
    Objectif principal : Intercepter les requêtes pour sécuriser l'accès à l'application.
    
    Entrée(s) : Aucune.
    
    Sortie(s) : 
        - Redirection vers la page de login si non authentifié (sauf login et static).
    """
    allowed_routes = ['login', 'static']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect(url_for('login'))


@app.route('/')
@app.route('/home')
def home():
    """
    Objectif principal : Afficher la page d'accueil.
    Entrée(s) : Aucune.
    Sortie(s) : (HTML) Template 'index.html'.
    """
    return render_template('index.html')


@app.route('/dashboard_rugby.html')
def dashboard_rugby():
    """
    Objectif principal : Afficher le tableau de bord avec les matchs de rugby de l'utilisateur.
    Entrée(s) : Aucune (utilise la session utilisateur).
    Sortie(s) : (HTML) Template 'dashboard_rugby.html' avec la liste de ses matchs.
    """
    username = session['username']
    user_dir = os.path.join('templates/matches/rugby', username)
    
    matches = []
    if os.path.exists(user_dir):
        matches = [f for f in os.listdir(user_dir) if f.endswith('.html')]
        
    return render_template('dashboard_rugby.html', matches=matches)


@app.route('/football')
def dashboard_football():
    """
    Objectif principal : Afficher le tableau de bord des matchs de football.
    Entrée(s) : Aucune.
    Sortie(s) : (HTML) Template 'dashboard_football.html'.
    """
    username = session['username']
    user_dir = os.path.join('templates/matches/football', username)
    
    matches = []
    if os.path.exists(user_dir):
        matches = [f for f in os.listdir(user_dir) if f.endswith('.html')]
        
    return render_template('dashboard_football.html', matches=matches)


@app.route('/basketball')
def dashboard_basketball():
    """
    Objectif principal : Afficher le tableau de bord des matchs de basketball.
    Entrée(s) : Aucune.
    Sortie(s) : (HTML) Template 'dashboard_basketball.html'.
    """
    username = session['username']
    user_dir = os.path.join('templates/matches/basketball', username)
    
    matches = []
    if os.path.exists(user_dir):
        matches = [f for f in os.listdir(user_dir) if f.endswith('.html')]
        
    return render_template('dashboard_basketball.html', matches=matches)


@app.route('/rugby/form')
def form_rugby():
    """Objectif principal : Afficher le formulaire de rugby."""
    return render_template('formrugby.html')


@app.route('/football/form')
def form_football():
    """Objectif principal : Afficher le formulaire de football."""
    return render_template('formfootball.html')


@app.route('/basketball/form')
def form_basketball():
    """Objectif principal : Afficher le formulaire de basketball."""
    return render_template('formbasketball.html')


@app.route('/upload_rugby', methods=['POST'])
def upload_rugby():
    """
    Objectif principal : Traiter le formulaire de rugby, créer le fichier CSV et la page HTML.
    
    Entrée(s) : Aucune (récupère via request.form).
    
    Sortie(s) : 
        - Redirection vers la page du match nouvellement créée.
    """
    donnees_propres = valider_et_filtrer_donnees_rugby(request.form)
    username = session['username']
    enregistrer_dans_csv_rugby(donnees_propres, username)
    nom_fichier = generer_html.creer_page_match_rugby(donnees_propres, username)
    return redirect(url_for('voir_match', sport='rugby', nom_match=nom_fichier))


@app.route('/upload_football', methods=['POST'])
def upload_football():
    """
    Objectif principal : Traiter le formulaire de football, créer CSV et page HTML.
    Entrée(s) : Aucune.
    Sortie(s) : 
        - Redirection vers la page du match.
    """
    donnees_propres = valider_et_filtrer_donnees_football(request.form)
    username = session['username']
    enregistrer_dans_csv_football(donnees_propres, username)
    nom_fichier = generer_html.creer_page_match_football(donnees_propres, username)
    return redirect(url_for('voir_match', sport='football', nom_match=nom_fichier))


@app.route('/upload_basketball', methods=['POST'])
def upload_basketball():
    """
    Objectif principal : Traiter le formulaire de basket, créer CSV et page HTML.
    Entrée(s) : Aucune.
    Sortie(s) : 
        - Redirection vers la page du match.
    """
    donnees_propres = valider_et_filtrer_donnees_basketball(request.form)
    username = session['username']
    enregistrer_dans_csv_basketball(donnees_propres, username)
    nom_fichier = generer_html.creer_page_match_basketball(donnees_propres, username)
    return redirect(url_for('voir_match', sport='basketball', nom_match=nom_fichier))


@app.route('/view/<sport>/<nom_match>')
def voir_match(sport, nom_match):
    """
    Objectif principal : Servir le rapport de match statique d'un utilisateur depuis ses dossiers personnels.
    
    Entrée(s) : 
        - sport (str) : Nom du sport.
        - nom_match (str) : Nom du fichier HTML à récupérer.
        
    Sortie(s) : (Fichier) Le fichier .html matérialisé.
    """
    username = session['username']
    return send_from_directory(os.path.join('templates/matches', sport, username), f"{nom_match}.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Objectif principal : Gérer la connexion d'un utilisateur et créer une session.
    Entrée(s) : Formulaire de connexion.
    Sortie(s) : Redirection vers /user ou affichage du formulaire.
    """
    if request.method == 'POST':
        user=request.form['username']
        session['username'] = user  # Stockage du nom d'utilisateur dans la session
        return redirect(url_for('user'))
    else:
        return render_template('login.html')


@app.route("/user" )
def user():
    """
    Objectif principal : Vérifier l'état de la connexion.
    Entrée(s)/Sortie(s) : Redirection vers home (succès) ou login (échec).
    """
    if 'username' in session:
        user= session['username']
        return redirect(url_for('home'))
    else:
        return redirect (url_for('login'))


@app.route('/logout')
def logout():
    """
    Objectif principal : Détruire la session et purger les dossiers temporaires du disque dur.
    Entrée(s) : Aucune.
    Sortie(s) : Redirection vers la page de login.
    """
    username = session.pop('username', None)
    if username:
        for sport in ['rugby', 'football', 'basketball']:
            user_dir = os.path.join('templates', 'matches', sport, username)
            if os.path.exists(user_dir):
                shutil.rmtree(user_dir)
    return redirect(url_for('login'))






if __name__ == '__main__':
    # Démarrage du serveur web local de développement
    app.run(debug=False)