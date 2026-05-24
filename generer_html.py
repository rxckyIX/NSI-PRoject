# generer_html.py
import os
def normaliser_nom_fichier(titre, date):
    """
    Algorithme de traitement de chaînes convertissant le titre et la date
    en un nom de fichier standardisé dénué de caractères spéciaux et d'espaces.
    """
    titre_sain = titre.lower().replace(" ", "-")
    for caractere in [":", "/", "'", ".", ",", '"', "?", "!", "@", "#", "$", "*"]:
        titre_sain = titre_sain.replace(caractere, "")
    return f"match_{titre_sain}_{date}"


def creer_page_match_rugby(donnees):
    """
    Prend en paramètre le dictionnaire de données validées et écrit physiquement
    la page finale statique sur le disque dur.
    """
    # Calcul dynamique du nom du fichier
    nom_fichier = normaliser_nom_fichier(donnees["titre_match"], donnees["date_match"])
    
    # Agrégation du score collectif
    score_global = f"{donnees['score_notre_equipe']} - {donnees['score_adversaire']}"
    video_section = ""
    if donnees.get("video_url") and donnees["video_url"] != "N/A":
        video_section = f"""
    <section style=\"margin: 30px 0;\">
        <h2>Vidéo du match</h2>
        <iframe src=\"{donnees['video_url']}\" width=\"100%\" height=\"480\" frameborder=\"0\" allowfullscreen loading=\"lazy\"></iframe>
    </section>
"""
    
    # Définition du gabarit HTML structurel (Moule Markup de Lambert)
    contenu_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{donnees["titre_match"]} - July Verny</title>
    <link rel="stylesheet" href="/static/style.css">
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

    {video_section}

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
    
    # Écriture physique sur le disque dur
    with open(f"matches/rugby/{nom_fichier}.html", 'w', encoding='utf-8') as fichier_html:
        # CORRECTION DU BUG : Utilisation de la variable correcte 'contenu_html'
        fichier_html.write(contenu_html)

    return nom_fichier


def creer_page_match_football(donnees):
    """
    Prend en paramètre le dictionnaire de données validées football et écrit physiquement
    la page finale statique sur le disque dur.
    """
    nom_fichier = normaliser_nom_fichier(donnees["titre_match"], donnees["date_match"])
    score_global = f"{donnees['score_notre_equipe']} - {donnees['score_adversaire']}"
    video_section = ""
    if donnees.get("video_url") and donnees["video_url"] != "N/A":
        video_section = f"""
    <section style=\"margin: 30px 0;\">
        <h2>Vidéo du match</h2>
        <iframe src=\"{donnees['video_url']}\" width=\"100%\" height=\"480\" frameborder=\"0\" allowfullscreen loading=\"lazy\"></iframe>
    </section>
"""

    contenu_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{donnees["titre_match"]} - July Verny</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>Fiche de Rencontre Football ⚽</h1>
    <h2>Match : {donnees["titre_match"]}</h2>
    <p><strong>Compétition :</strong> {donnees["competition"]} | <strong>Date :</strong> {donnees["date_match"]}</p>

    <div class="form-container" style="background-color: #ededed; font-size: 1.15em;">
        <p><strong>Adversaire :</strong> {donnees["adversaire"]}</p>
        <p style="font-size: 2em; margin: 10px 0; font-weight: bold; color: #111;">{score_global}</p>
        <p>Résultat : <strong>{donnees["resultat"]}</strong></p>
    </div>

    {video_section}

    <div class="form-container" style="border-left: 5px solid #00aa00; text-align: left;">
        <h3>Statistique Individuelle</h3>
        <ul>
            <li><strong>Buts marqués :</strong> {donnees["buts"]}</li>
            <li><strong>Évaluation du match :</strong> {donnees["evaluation"]}</li>
        </ul>
    </div>

    <div class="form-container" style="border-left: 5px solid #0066cc; text-align: left;">
        <h3>Données Scientifiques & Physiques</h3>
        <p style="font-size: 0.8em; color: #666; margin-bottom: 12px;">* Ces indicateurs affichent <strong>N/A</strong> si non mesurés.</p>
        <ul>
            <li><strong>Passes décisives :</strong> {donnees["passes_decisives"]}</li>
            <li><strong>Temps de jeu :</strong> {donnees["temps_jeu"]}{" minutes" if donnees["temps_jeu"] != "N/A" else ""}</li>
            <li><strong>Distance parcourue :</strong> {donnees["distance"]}{" km" if donnees["distance"] != "N/A" else ""}</li>
        </ul>
    </div>

    <br>
    <a href="dashboard_football.html">⬅ Retour au Dashboard Football</a>
</body>
</html>
"""

    with open(f"matches/football/{nom_fichier}.html", 'w', encoding='utf-8') as fichier_html:
        fichier_html.write(contenu_html)

    print(f"[JAMstack Generator] Fiche de match matérialisée : {nom_fichier}")
    return nom_fichier


def creer_page_match_basketball(donnees):
    """
    Prend en paramètre le dictionnaire de données validées basketball et écrit physiquement
    la page finale statique sur le disque dur.
    """
    nom_fichier = normaliser_nom_fichier(donnees["titre_match"], donnees["date_match"])
    score_global = f"{donnees['score_notre_equipe']} - {donnees['score_adversaire']}"
    video_section = ""
    if donnees.get("video_url") and donnees["video_url"] != "N/A":
        video_section = f"""
    <section style=\"margin: 30px 0;\">
        <h2>Vidéo du match</h2>
        <iframe src=\"{donnees['video_url']}\" width=\"100%\" height=\"480\" frameborder=\"0\" allowfullscreen loading=\"lazy\"></iframe>
    </section>
"""

    contenu_html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{donnees["titre_match"]} - July Verny</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <h1>Fiche de Rencontre Basketball 🏀</h1>
    <h2>Match : {donnees["titre_match"]}</h2>
    <p><strong>Compétition :</strong> {donnees["competition"]} | <strong>Date :</strong> {donnees["date_match"]}</p>

    <div class="form-container" style="background-color: #ededed; font-size: 1.15em;">
        <p><strong>Adversaire :</strong> {donnees["adversaire"]}</p>
        <p style="font-size: 2em; margin: 10px 0; font-weight: bold; color: #111;">{score_global}</p>
        <p>Résultat : <strong>{donnees["resultat"]}</strong></p>
    </div>

    {video_section}

    <div class="form-container" style="border-left: 5px solid #ff6600; text-align: left;">
        <h3>Statistique Individuelle</h3>
        <ul>
            <li><strong>Points marqués :</strong> {donnees["points"]}</li>
            <li><strong>Évaluation du match :</strong> {donnees["evaluation"]}</li>
        </ul>
    </div>

    <div class="form-container" style="border-left: 5px solid #0066cc; text-align: left;">
        <h3>Données Scientifiques & Physiques</h3>
        <p style="font-size: 0.8em; color: #666; margin-bottom: 12px;">* Ces indicateurs affichent <strong>N/A</strong> si non mesurés.</p>
        <ul>
            <li><strong>Passes ajustées :</strong> {donnees["passes_ajustees"]}</li>
            <li><strong>Temps de jeu :</strong> {donnees["temps_jeu"]}{" minutes" if donnees["temps_jeu"] != "N/A" else ""}</li>
            <li><strong>Distance parcourue :</strong> {donnees["distance"]}{" km" if donnees["distance"] != "N/A" else ""}</li>
        </ul>
    </div>

    <br>
    <a href="dashboard_basketball.html">⬅ Retour au Dashboard Basketball</a>
</body>
</html>
"""

    with open(f"matches/basketball/{nom_fichier}.html", 'w', encoding='utf-8') as fichier_html:
        fichier_html.write(contenu_html)

    print(f"[JAMstack Generator] Fiche de match matérialisée : {nom_fichier}")
    return nom_fichier