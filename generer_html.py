# generer_html.py
import os

def normaliser_nom_fichier(titre, date):
    """
    Algorithme de traitement de chaînes (Sanitizer) convertissant le titre et la date
    en un nom de fichier standardisé propre pour le Système d'Exploitation (os).
    Exemple: 'Match Amical' et '2026-05-19' -> 'match_match-amical_2026-05-19.html'
    """
    # Passage en minuscules et substitution des espaces par des tirets
    titre_sain = titre.lower().replace(" ", "-")
    
    # Boucle d'exclusion des caractères spéciaux proscrits par les OS ou perturbants dans une URL
    for caractere in [":", "/", "'", ".", ",", '"', "?", "!", "@", "#", "$", "*"]:
        titre_sain = titre_sain.replace(caractere, "")
        
    return f"match_{titre_sain}_{date}.html"


def creer_page_match(donnees):
    """
    Prend en paramètre le dictionnaire de données validées et écrit physiquement
    la page finale statique sur le disque dur à l'aide d'un gabarit de chaîne (Template).
    """
    # Calcul dynamique sécurisé du nom du fichier grâce à notre fonction algorithmique
    nom_fichier = normaliser_nom_fichier(donnees["titre_match"], donnees["date_match"])
    
    # Formatage de l'encart d'affichage du score collectif
    score_global = f"{donnees['score_notre_equipe']} - {donnees['score_adversaire']}"
    
    # Définition du gabarit de chaîne multi-lignes (f-string) faisant office de moule Markup HTML
    contenu_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{donnees["titre_match"]} - July Verny</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>Fiche de Rencontre Rugby 🏉</h1>
    <h2>Match : {donnees["titre_match"]}</h2>
    <p><strong>Ligue / Compétition :</strong> {donnees["competition"]} | <strong>Date :</strong> {donnees["date_match"]}</p>
    
    <div class="form-container" style="background-color: #ededed; font-size: 1.15em;">
        <p><strong>Équipe Adversaire :</strong> {donnees["adversaire"]}</p>
        <p style="font-size: 2em; margin: 10px 0; font-weight: bold; color: #111;">{score_global}</p>
        <p>Bilan de la confrontation : <strong>{donnees["resultat"]}</strong></p>
    </div>

    <div class="form-container" style="border-left: 5px solid #222; text-align: left;">
        <h3>Performances Individuelles Principales</h3>
        <ul>
            <li><strong>Essais inscrits sur le match (Tries) :</strong> {donnees["essais"]}</li>
            <li><strong>Évaluation de votre ressenti (Rating) :</strong> {donnees["evaluation"]}</li>
        </ul>
    </div>

    <div class="form-container" style="border-left: 5px solid #0066cc; text-align: left;">
        <h3>Données Physiques & Suivi Scientifique Avancé</h3>
        <p style="font-size: 0.8em; color: #666; margin-bottom: 12px;">
            * Les indicateurs suivants sont extraits de capteurs. Ils affichent <strong>N/A</strong> si non mesurés.
        </p>
        <ul>
            <li><strong>Passes ajustées :</strong> {donnees["passes_totales"]}</li>
            <li><strong>Plaquages défensifs :</strong> {donnees["plaquages"]}</li>
            <li><strong>Temps de présence terrain :</strong> {donnees["temps_jeu"]}{" minutes" if donnees["temps_jeu"] != "N/A" else ""}</li>
            <li><strong>Distance totale de course :</strong> {donnees["distance"]}{" km" if donnees["distance"] != "N/A" else ""}</li>
        </ul>
    </div>

    <br>
    <a href="dashboard_rugby.html">⬅ Retour au Dashboard Rugby</a>
</body>
</html>
"""
    
    # Processus d'écriture physique sur le disque dur (Operating System) via open() en mode 'w'
    # L'argument encoding='utf-8' évite les corruptions de caractères sur les accents (ex: 'Défaite')
    with open(nom_fichier, 'w', encoding='utf-8') as fichier_html:
        fichier_html.write(contenu_html)
        
    print(f"[JAMstack Generator] Fiche de match matérialisée sur le disque : {nom_fichier}")