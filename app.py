# app.py
from flask import Flask, request, redirect
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
    
    Structure de données : Table de hachage / Dictionnaire Python (NSI Chapitre 07).
    """
    def evaluer_champ_optionnel(cle_dictionnaire, type_cible=int):
        """
        Algorithme de programmation défensive (Trudon) :
        Nettoie les espaces et remplace les vides par 'N/A'.
        """
        valeur_texte = donnees_brutes.get(cle_dictionnaire, "").strip()
        if valeur_texte == "":
            return "N/A" # Injection de la chaîne par défaut
        return type_cible(valeur_texte)

    # Création du dictionnaire relationnel propre nettoyé (sans clé pseudo)
    donnees_traitees = {
        # Blocs obligatoires validés explicitement par type
        "titre_match": donnees_brutes.get("titre_match"),
        "competition": donnees_brutes.get("competition"),
        "adversaire": donnees_brutes.get("adversaire"),
        "date_match": donnees_brutes.get("date_match"),
        "score_notre_equipe": int(donnees_brutes.get("score_notre_equipe", 0)),
        "score_adversaire": int(donnees_brutes.get("score_adversaire", 0)),
        "resultat": donnees_brutes.get("resultat"),
        "essais": int(donnees_brutes.get("essais", 0)),
        "evaluation": donnees_brutes.get("evaluation"),
        
        # Filtrage algorithmique des métriques facultatives Complexes
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
    L'usage du mode='a' (append) garantit l'écriture séquentielle sans écrasement.
    
    Contrainte NSI obligatoires : argument encoding='utf-8' et newline=''.
    """
    # newline='' neutralise les sauts de lignes fantômes entre Windows (\r\n) et Linux (\n)
    with open('performances_rugby.csv', mode='a', newline='', encoding='utf-8') as fichier_csv:
        scripteur = csv.writer(fichier_csv)
        # Écriture de la ligne aplatie correspondante
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
    Supervise le traitement Data, la persistance CSV et lance le générateur.
    """
    # 1. Appel du dictionnaire relationnel de Trudon pour typage et filtrage des 'N/A'
    donnees_propres = valider_et_filtrer_donnees(request.form)
    
    # 2. Sauvegarde de la performance dans la table persistante par Jason
    enregistrer_dans_csv(donnees_propres)
    
    # 3. Réveil du robot de build JAMstack pour compiler la fiche de match autonome
    generer_html.creer_page_match(donnees_propres)
    
    # 4. Redirection finale de l'utilisateur vers son Dashboard général fixe
    return redirect('dashboard_rugby.html')


if __name__ == '__main__':
    # Démarrage du serveur local de développement Flask avec debugger actif
    app.run(debug=True)