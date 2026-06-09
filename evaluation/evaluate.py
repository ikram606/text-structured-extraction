#!/usr/bin/env python3
"""
Module d'evaluation de la qualite de l'extraction de donnees structurees.

Compare les resultats extraits (output.json) avec la verite terrain (ground_truth.json)
et calcule des metriques de qualite : precision, rappel et F1-score.
"""

import json
import os


def charger_json(chemin):
    """Charge un fichier JSON et retourne son contenu."""
    with open(chemin, 'r', encoding='utf-8') as f:
        return json.load(f)


def correspondance_exacte(extrait, attendu):
    """
    Evalue un champ simple par correspondance exacte.
    Retourne precision=1, rappel=1, f1=1 si correspondance exacte, sinon 0.
    """
    if extrait is None and attendu is None:
        return {"precision": 1.0, "rappel": 1.0, "f1": 1.0}
    if extrait is None or attendu is None:
        return {"precision": 0.0, "rappel": 0.0, "f1": 0.0}

    # Normaliser les espaces pour la comparaison
    extrait_norm = str(extrait).strip().lower()
    attendu_norm = str(attendu).strip().lower()

    if extrait_norm == attendu_norm:
        return {"precision": 1.0, "rappel": 1.0, "f1": 1.0}
    else:
        return {"precision": 0.0, "rappel": 0.0, "f1": 0.0}


def evaluer_liste(extraite, attendue):
    """
    Evalue une liste d'elements (competences, langues sous forme de liste simple).
    Calcule precision et rappel bases sur les elements trouves vs attendus.

    Precision = elements corrects / elements extraits
    Rappel = elements corrects / elements attendus
    """
    if not extraite and not attendue:
        return {"precision": 1.0, "rappel": 1.0, "f1": 1.0}
    if not extraite:
        return {"precision": 0.0, "rappel": 0.0, "f1": 0.0}
    if not attendue:
        return {"precision": 0.0, "rappel": 0.0, "f1": 0.0}

    # Normaliser les elements pour la comparaison
    extraite_norm = set(e.strip().lower() for e in extraite)
    attendue_norm = set(e.strip().lower() for e in attendue)

    # Elements correctement extraits
    corrects = extraite_norm & attendue_norm

    precision = len(corrects) / len(extraite_norm) if extraite_norm else 0.0
    rappel = len(corrects) / len(attendue_norm) if attendue_norm else 0.0

    if precision + rappel > 0:
        f1 = 2 * (precision * rappel) / (precision + rappel)
    else:
        f1 = 0.0

    return {"precision": precision, "rappel": rappel, "f1": f1}


def evaluer_liste_dictionnaires(extraite, attendue, champs_cles):
    """
    Evalue une liste de dictionnaires (experience, formation).
    Compare sur le nombre d'elements et les champs cles.

    Pour chaque element attendu, on cherche le meilleur match dans les
    elements extraits base sur les champs cles.
    """
    if not extraite and not attendue:
        return {"precision": 1.0, "rappel": 1.0, "f1": 1.0}
    if not extraite:
        return {"precision": 0.0, "rappel": 0.0, "f1": 0.0}
    if not attendue:
        return {"precision": 0.0, "rappel": 0.0, "f1": 0.0}

    # Calculer le score de correspondance pour chaque paire
    nb_matches = 0

    # Pour chaque element attendu, chercher un match dans les elements extraits
    extraits_utilises = set()

    for elem_attendu in attendue:
        meilleur_score = 0.0
        meilleur_idx = -1

        for idx, elem_extrait in enumerate(extraite):
            if idx in extraits_utilises:
                continue

            # Calculer le score de correspondance sur les champs cles
            score = 0.0
            nb_champs = 0

            for champ in champs_cles:
                val_attendue = elem_attendu.get(champ, "")
                val_extraite = elem_extrait.get(champ, "")

                if val_attendue and val_extraite:
                    nb_champs += 1
                    if str(val_attendue).strip().lower() == str(val_extraite).strip().lower():
                        score += 1.0

            if nb_champs > 0:
                score_normalise = score / nb_champs
            else:
                score_normalise = 0.0

            if score_normalise > meilleur_score:
                meilleur_score = score_normalise
                meilleur_idx = idx

        if meilleur_score > 0.5:
            nb_matches += 1
            if meilleur_idx >= 0:
                extraits_utilises.add(meilleur_idx)

    precision = nb_matches / len(extraite) if extraite else 0.0
    rappel = nb_matches / len(attendue) if attendue else 0.0

    if precision + rappel > 0:
        f1 = 2 * (precision * rappel) / (precision + rappel)
    else:
        f1 = 0.0

    return {"precision": precision, "rappel": rappel, "f1": f1}


def evaluer_langues(extraites, attendues):
    """
    Evalue la liste des langues (liste de dictionnaires avec langue et niveau).
    Compare sur la langue et le niveau.
    """
    return evaluer_liste_dictionnaires(extraites, attendues, ["langue", "niveau"])


def evaluer_cv(resultat, verite):
    """
    Evalue l'extraction d'un CV complet en comparant chaque champ.
    Retourne un dictionnaire avec les scores par champ.
    """
    scores = {}

    # Champs simples : correspondance exacte
    for champ in ["nom", "email", "telephone"]:
        val_extraite = resultat.get(champ, None)
        val_attendue = verite.get(champ, None)
        scores[champ] = correspondance_exacte(val_extraite, val_attendue)

    # Competences : liste simple
    comp_extraites = resultat.get("competences", [])
    comp_attendues = verite.get("competences", [])
    scores["competences"] = evaluer_liste(comp_extraites, comp_attendues)

    # Experience professionnelle : liste de dictionnaires
    exp_extraites = resultat.get("experience_professionnelle", [])
    exp_attendues = verite.get("experience_professionnelle", [])
    scores["experience_professionnelle"] = evaluer_liste_dictionnaires(
        exp_extraites, exp_attendues, ["periode", "poste", "entreprise"]
    )

    # Formation : liste de dictionnaires
    form_extraites = resultat.get("formation", [])
    form_attendues = verite.get("formation", [])
    scores["formation"] = evaluer_liste_dictionnaires(
        form_extraites, form_attendues, ["periode", "diplome", "etablissement"]
    )

    # Langues : liste de dictionnaires
    lang_extraites = resultat.get("langues", [])
    lang_attendues = verite.get("langues", [])
    scores["langues"] = evaluer_langues(lang_extraites, lang_attendues)

    return scores


def calculer_score_global(resultats_evaluation):
    """
    Calcule le score global moyen sur tous les CV et tous les champs.
    """
    total_precision = 0.0
    total_rappel = 0.0
    total_f1 = 0.0
    nb_mesures = 0

    for cv_name, scores in resultats_evaluation.items():
        for champ, metriques in scores.items():
            total_precision += metriques["precision"]
            total_rappel += metriques["rappel"]
            total_f1 += metriques["f1"]
            nb_mesures += 1

    if nb_mesures > 0:
        return {
            "precision_moyenne": total_precision / nb_mesures,
            "rappel_moyen": total_rappel / nb_mesures,
            "f1_moyen": total_f1 / nb_mesures
        }
    else:
        return {
            "precision_moyenne": 0.0,
            "rappel_moyen": 0.0,
            "f1_moyen": 0.0
        }


def afficher_tableau_recapitulatif(resultats_evaluation, score_global):
    """
    Affiche un tableau recapitulatif des scores par CV et par champ.
    """
    champs = ["nom", "email", "telephone", "competences",
              "experience_professionnelle", "formation", "langues"]

    # En-tete
    print("\n" + "=" * 90)
    print("RAPPORT D'EVALUATION DE LA QUALITE DE L'EXTRACTION")
    print("=" * 90)

    # Tableau par CV
    for cv_name in sorted(resultats_evaluation.keys()):
        scores = resultats_evaluation[cv_name]
        print(f"\n--- {cv_name} ---")
        print(f"{'Champ':<30s} {'Precision':>10s} {'Rappel':>10s} {'F1-Score':>10s}")
        print("-" * 62)

        for champ in champs:
            if champ in scores:
                m = scores[champ]
                print(f"{champ:<30s} {m['precision']:>10.2f} {m['rappel']:>10.2f} {m['f1']:>10.2f}")

    # Score global
    print("\n" + "=" * 90)
    print("SCORE GLOBAL")
    print("=" * 90)
    print(f"  Precision moyenne : {score_global['precision_moyenne']:.4f}")
    print(f"  Rappel moyen      : {score_global['rappel_moyen']:.4f}")
    print(f"  F1-Score moyen    : {score_global['f1_moyen']:.4f}")
    print("=" * 90)


def generer_rapport(resultats_evaluation, score_global):
    """
    Genere le rapport d'evaluation au format JSON.
    """
    rapport = {
        "description": "Rapport d'evaluation de la qualite de l'extraction de donnees structurees depuis des CV",
        "methodologie": {
            "champs_simples": "Correspondance exacte (precision/rappel = 1 ou 0)",
            "listes": "Precision = elements corrects / elements extraits, Rappel = elements corrects / elements attendus",
            "listes_dictionnaires": "Correspondance sur les champs cles (periode, poste, entreprise pour experience; periode, diplome, etablissement pour formation)"
        },
        "resultats_par_cv": resultats_evaluation,
        "score_global": score_global
    }
    return rapport


def main():
    """Fonction principale d'evaluation."""

    # Determiner le repertoire de base du projet
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.dirname(script_dir)

    # Chemins des fichiers
    chemin_resultats = os.path.join(project_dir, "results", "output.json")
    chemin_verite = os.path.join(script_dir, "ground_truth.json")
    chemin_rapport = os.path.join(script_dir, "rapport_evaluation.json")

    # Charger les donnees
    print("Chargement des resultats extraits...")
    resultats = charger_json(chemin_resultats)

    print("Chargement de la verite terrain...")
    verite_terrain = charger_json(chemin_verite)

    # Evaluer chaque CV
    print("Evaluation en cours...\n")
    resultats_evaluation = {}

    for cv_name in sorted(verite_terrain.keys()):
        if cv_name in resultats:
            resultats_evaluation[cv_name] = evaluer_cv(
                resultats[cv_name], verite_terrain[cv_name]
            )
        else:
            print(f"  ATTENTION : {cv_name} absent des resultats extraits")

    # Calculer le score global
    score_global = calculer_score_global(resultats_evaluation)

    # Afficher le tableau recapitulatif
    afficher_tableau_recapitulatif(resultats_evaluation, score_global)

    # Generer et sauvegarder le rapport
    rapport = generer_rapport(resultats_evaluation, score_global)

    with open(chemin_rapport, 'w', encoding='utf-8') as f:
        json.dump(rapport, f, ensure_ascii=False, indent=2)

    print(f"\nRapport sauvegarde dans : {chemin_rapport}")


if __name__ == "__main__":
    main()
