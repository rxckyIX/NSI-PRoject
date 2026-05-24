import os
from flask import Flask, render_template, send_from_directory, request, redirect, url_for

# Initialisation de l'instance Flask pour la capture des flux formulaires
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/dashboard_rugby.html')
def dashboard_rugby():
    # List only files in the rugby folder
    matches = [f for f in os.listdir('matches/rugby') if f.endswith('.html')]
    return render_template('dashboard_rugby.html', matches=matches)

@app.route('/football')
def dashboard_football():
    matches = [f for f in os.listdir('matches/football') if f.endswith('.html')]
    return render_template('dashboard_football.html', matches=matches)

@app.route('/basketball')
def dashboard_basketball():
    matches = [f for f in os.listdir('matches/basketball') if f.endswith('.html')]
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

@app.route('/view/<sport>/<nom_match>')
def voir_match(sport, nom_match):
    """Sert dynamiquement les rapports de match stockés dans les sous-dossiers."""
    return send_from_directory(os.path.join('matches', sport), f"{nom_match}.html")



if __name__ == '__main__':
    # Démarrage du serveur web local de développement
    app.run(debug=True)