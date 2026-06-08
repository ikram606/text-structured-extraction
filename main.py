"""
Script principal pour l'extraction de donnees structurees depuis des CV bruts.

Ce script lit tous les fichiers CV dans le dossier data/, extrait les
informations structurees et sauvegarde les resultats en JSON.

Usage :
    python main.py
"""

import json
import os
from pathlib import Path

from src.extractor import extraire_donnees_cv


def charger_cvs(dossier: str = "data") -> dict:
    """
    Charge tous les fichiers texte depuis le dossier specifie.

    Args:
        dossier: Chemin vers le dossier contenant les fichiers CV.

    Returns:
        Dictionnaire {nom_fichier: contenu_texte}
    """
    cvs = {}
    chemin = Path(dossier)

    if not chemin.exists():
        print(f"Erreur : le dossier '{dossier}' n'existe pas.")
        return cvs

    for fichier in sorted(chemin.glob("*.txt")):
        with open(fichier, "r", encoding="utf-8") as f:
            cvs[fichier.name] = f.read()

    return cvs


def afficher_resume(nom_fichier: str, donnees: dict) -> None:
    """
    Affiche un resume des donnees extraites d'un CV.
    """
    print(f"\n{'='*60}")
    print(f"  Fichier : {nom_fichier}")
    print(f"{'='*60}")
    print(f"  Nom        : {donnees.get('nom', 'Non trouve')}")
    print(f"  Email      : {donnees.get('email', 'Non trouve')}")
    print(f"  Telephone  : {donnees.get('telephone', 'Non trouve')}")

    competences = donnees.get('competences', [])
    print(f"  Competences: {len(competences)} extraites")
    if competences:
        # Afficher les 5 premieres
        affichees = competences[:5]
        print(f"               {', '.join(affichees)}")
        if len(competences) > 5:
            print(f"               ... et {len(competences) - 5} autres")

    experiences = donnees.get('experience_professionnelle', [])
    print(f"  Experiences: {len(experiences)} postes")
    for exp in experiences:
        print(f"               - {exp.get('poste', '')} ({exp.get('periode', '')})")

    formations = donnees.get('formation', [])
    print(f"  Formations : {len(formations)} diplomes")
    for form in formations:
        print(f"               - {form.get('diplome', '')} ({form.get('periode', '')})")

    langues = donnees.get('langues', [])
    print(f"  Langues    : {len(langues)} langues")
    for langue in langues:
        print(f"               - {langue.get('langue', '')}: {langue.get('niveau', '')}")


def main():
    """
    Fonction principale : charge les CVs, extrait les donnees et sauvegarde les resultats.
    """
    print("=" * 60)
    print("  EXTRACTION DE DONNEES STRUCTUREES DEPUIS DES CV")
    print("=" * 60)

    # Charger les CVs
    cvs = charger_cvs("data")

    if not cvs:
        print("\nAucun fichier CV trouve dans le dossier data/")
        return

    print(f"\n{len(cvs)} fichier(s) CV trouve(s) dans data/")

    # Extraire les donnees de chaque CV
    resultats = {}
    for nom_fichier, contenu in cvs.items():
        donnees = extraire_donnees_cv(contenu)
        resultats[nom_fichier] = donnees
        afficher_resume(nom_fichier, donnees)

    # Sauvegarder les resultats en JSON
    dossier_resultats = Path("results")
    dossier_resultats.mkdir(exist_ok=True)

    chemin_sortie = dossier_resultats / "output.json"
    with open(chemin_sortie, "w", encoding="utf-8") as f:
        json.dump(resultats, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"  Resultats sauvegardes dans : {chemin_sortie}")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
