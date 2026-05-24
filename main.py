from flask import Flask, render_template, send_from_directory
from fonctions import fonctions, request, render_template, redirect, url_for

# Initialisation de l'instance Flask pour la capture des flux formulaires
app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
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

@app.route('/<nom_match>')
def voir_match(nom_match):
    # On cherche le fichier .html correspondant au nom dans l'URL
    return send_from_directory('.', f"{nom_match}.html")



if __name__ == '__main__':
    # Démarrage du serveur web local de développement
    app.run(debug=True)