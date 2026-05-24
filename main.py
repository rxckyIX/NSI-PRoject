import os
from flask import Flask, render_template, send_from_directory, request, redirect, url_for
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



if __name__ == '__main__':
    # Démarrage du serveur web local de développement
    app.run(debug=True)