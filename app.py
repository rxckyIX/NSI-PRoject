# app.py
from flask import Flask, request
import csv
import generer_html

# Initialisation de l'instance Flask pour la capture des flux formulaires
app = Flask(__name__)

# --- PARTIE DATA (Rôle de Trudon) ---

def valider_et_filtrer_donnees(donnees_brutes):
    """
    Prend en entrée le dictionnaire brut issu de request.form.
    Structure les champs obligatoires sous les bons types et applique la valeur
    par défaut 'N/A' aux métriques scientifiques optionnelles si elles sont vides.
    """
    def evaluer_champ_optionnel(cle_dictionnaire, type_cible=int):
        """Retourne la valeur convertie si elle est renseignée, sinon la chaîne 'N/A'."""
        valeur_texte = donnees_brutes.get(cle_dictionnaire, "").strip()
        if valeur_texte == "":
            return "N/A"
        return type_cible(valeur_texte)

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
        
        "passes_totales": evaluer_champ_optionnel("passes", int),
        "plaquages": evaluer_champ_optionnel("plaquages", int),
        "temps_jeu": evaluer_champ_optionnel("temps_jeu", int),
        "distance": evaluer_champ_optionnel("distance", float)
    }
    return donnees_traitees


# --- PARTIE BACK-END (Rôle de Jason) ---

def enregistrer_dans_csv(donnees_finales):
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


# --- ROUTAGE DES REQUÊTES (Rôle de Jason) ---

@app.route('/upload_rugby', methods=['POST'])
def receptionner_formulaire_rugby():
    """
    Point de contact de l'API interceptant l'envoi du formulaire de saisie.
    Supervise la validation, le stockage et instancie l'écriture du fichier HTML de match.
    """
    # 1. Traitement des types et des valeurs par défaut (Trudon)
    donnees_propres = valider_et_filtrer_donnees(request.form)
    
    # 2. Sauvegarde de la performance dans la table persistante par Jason
    enregistrer_dans_csv(donnees_propres)
    
    # 3. Activation du Générateur JAMstack pour créer la page de match autonome
    generer_html.creer_page_match(donnees_propres)
    
    # 4. CORRECTIF ARCHITECTURE NSI : Renvoyer un code HTTP 204 (No Content)
    # Le navigateur comprend que l'action est validée et reste sur formrugby.html
    # sans provoquer de redirection brisée ni d'erreur 404.
    return '', 204


if __name__ == '__main__':
    # Démarrage du serveur web local de développement
    app.run(debug=True)