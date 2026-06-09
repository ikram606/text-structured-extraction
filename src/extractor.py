"""
Module d'extraction de donnees structurees depuis des textes bruts de CV.

Ce module utilise des expressions regulieres (regex) pour extraire
les informations cles d'un CV au format texte brut.
"""

import re
from typing import Dict, List, Optional


def smart_split_commas(text: str) -> List[str]:
    """
    Split text by commas, but respect parentheses.
    'AWS (S3, SageMaker, EC2), GCP (BigQuery)' -> ['AWS (S3, SageMaker, EC2)', 'GCP (BigQuery)']
    """
    items = []
    depth = 0
    current = []
    for char in text:
        if char == '(':
            depth += 1
            current.append(char)
        elif char == ')':
            depth -= 1
            current.append(char)
        elif char == ',' and depth == 0:
            items.append(''.join(current).strip())
            current = []
        elif char == ';' and depth == 0:
            items.append(''.join(current).strip())
            current = []
        else:
            current.append(char)
    if current:
        items.append(''.join(current).strip())
    return [item for item in items if item]


def extraire_nom(texte: str) -> Optional[str]:
    """
    Extrait le nom complet depuis le texte du CV.
    Recherche les patterns courants : 'Nom :', 'Name:', ou un nom en majuscules
    en debut de document.
    """
    # Pattern francais : "Nom : Prenom Nom"
    match = re.search(r'(?:Nom|NOM)\s*:\s*(.+)', texte)
    if match:
        return match.group(1).strip()

    # Pattern anglais : "Name: First Last"
    match = re.search(r'(?:Name|NAME)\s*:\s*(.+)', texte)
    if match:
        return match.group(1).strip()

    # Recherche d'un nom en debut de CV (lignes en majuscules ou titre)
    lignes = texte.strip().split('\n')
    for ligne in lignes[:15]:
        ligne = ligne.strip()
        # Ignorer les lignes de decoration
        if re.match(r'^[=\-\s*]+$', ligne) or not ligne:
            continue
        # Ligne avec au moins 2 mots commencant par une majuscule
        if re.match(r'^[A-Z][a-z]+ [A-Z][a-z]+', ligne):
            return ligne.strip()
        # Ligne entierement en majuscules (au moins 2 mots)
        if re.match(r'^[A-Z]{2,}(?: [A-Z]{2,})+$', ligne):
            return ligne.strip().title()

    return None


def extraire_email(texte: str) -> Optional[str]:
    """
    Extrait l'adresse email depuis le texte.
    """
    pattern = r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}'
    match = re.search(pattern, texte)
    if match:
        return match.group(0)
    return None


def extraire_telephone(texte: str) -> Optional[str]:
    """
    Extrait le numero de telephone depuis le texte.
    Gere les formats francais et internationaux.
    """
    patterns = [
        # Format francais : 06 12 34 56 78 ou 06.12.34.56.78
        r'(?:Tel(?:ephone|\.)?|Phone|Mobile)\s*:\s*([\d\s\.\-\+\(\)]+)',
        # Format international : +33 6 12 34 56 78
        r'(\+\d{1,3}[\s\.\-]?\(?\d{1,4}\)?[\s\.\-]?\d{2,3}[\s\.\-]?\d{2,3}[\s\.\-]?\d{2,4})',
        # Format francais sans indicatif
        r'(0[1-9][\s\.\-]?\d{2}[\s\.\-]?\d{2}[\s\.\-]?\d{2}[\s\.\-]?\d{2})',
    ]

    for pattern in patterns:
        match = re.search(pattern, texte)
        if match:
            return match.group(1).strip()
    return None


def extraire_competences(texte: str) -> List[str]:
    """
    Extrait la liste des competences techniques depuis le texte.
    """
    competences = []

    # Recherche de la section competences
    # Pattern 0: Section between separator lines (more specific, try first)
    # This avoids matching "SKILLS" in body text like "PROFESSIONAL SUMMARY"
    patterns_section = [
        r'[-=]+\s*\n\s*(?:COMPETENCES?\s*TECHNIQUES?|COMPETENCES?\s*CLES?|COMPETENCES?|SKILLS|TECHNICAL\s+SKILLS|CORE\s+COMPETENCIES|KEY\s+SKILLS).*?\n\s*[-=]+\s*\n([\s\S]*?)(?:\n\s*[-=]{2,}|\n\n[-=]|$)',
        r'(?:COMPETENCES?\s*TECHNIQUES?|COMPETENCES?\s*CLES?|COMPETENCES?|SKILLS|TECHNICAL\s+SKILLS|CORE\s+COMPETENCIES|KEY\s+SKILLS)\s*[-:]*\s*\n([\s\S]*?)(?:\n\s*\n[-=]{2,}|\n[-=]{2,}|$)',
    ]

    section = None
    for pattern in patterns_section:
        match = re.search(pattern, texte, re.IGNORECASE)
        if match:
            section = match.group(1)
            break

    if section:
        # Extraire les competences depuis la section
        lignes = section.strip().split('\n')
        for ligne in lignes:
            ligne = ligne.strip()
            if not ligne or re.match(r'^[-=]+$', ligne):
                break
            # Ligne avec "Categorie : comp1, comp2, comp3"
            match_cat = re.match(r'^(.+?)\s*:\s*(.+)$', ligne)
            if match_cat:
                items = smart_split_commas(match_cat.group(2))
                competences.extend([item.strip() for item in items if item.strip()])
            # Ligne avec tiret "- competence"
            elif ligne.startswith('-'):
                competences.append(ligne.lstrip('- ').strip())
            # Ligne with bullet point
            elif ligne.startswith('\u2022'):
                competences.append(ligne.lstrip('\u2022 ').strip())

    return competences


# Month names for date patterns (French and English)
MONTHS_FR = r'(?:Janvier|Fevrier|Mars|Avril|Mai|Juin|Juillet|Aout|Septembre|Octobre|Novembre|Decembre)'
MONTHS_EN = r'(?:January|February|March|April|May|June|July|August|September|October|November|December)'
MONTHS_ALL = r'(?:Janvier|Fevrier|Mars|Avril|Mai|Juin|Juillet|Aout|Septembre|Octobre|Novembre|Decembre|January|February|March|April|May|June|July|August|September|October|November|December)'


def extraire_experience(texte: str) -> List[Dict[str, str]]:
    """
    Extrait les experiences professionnelles depuis le texte.
    Retourne une liste de dictionnaires avec periode, poste, entreprise et description.
    """
    experiences = []

    # Recherche de la section experience
    patterns_section = [
        r'[-=]+\s*\n\s*(?:EXPERIENCE[S]?\s*PROFESSIONNELLE[S]?|WORK\s*EXPERIENCE|PROFESSIONAL\s*EXPERIENCE|PROFESSIONAL\s*BACKGROUND|PARCOURS\s*PROFESSIONNEL|CAREER\s*HISTORY|EMPLOYMENT\s*HISTORY).*?\n\s*[-=]+\s*\n([\s\S]*?)(?:\n\s*[-=]{2,}\s*\n\s*[A-Z]|\Z)',
        r'(?:EXPERIENCE[S]?\s*PROFESSIONNELLE[S]?|WORK\s*EXPERIENCE|PROFESSIONAL\s*EXPERIENCE|PROFESSIONAL\s*BACKGROUND|PARCOURS\s*PROFESSIONNEL|CAREER\s*HISTORY|EMPLOYMENT\s*HISTORY)\s*[-:]*\s*\n([\s\S]*?)(?:\n\s*[-=]{2,}\s*\n\s*[A-Z]|\Z)',
    ]

    section = None
    for pattern in patterns_section:
        match = re.search(pattern, texte, re.IGNORECASE)
        if match:
            section = match.group(1)
            break

    if section:
        # Pattern pour detecter le debut d'une experience
        # Supports both French and English month names
        month_pattern = MONTHS_ALL
        exp_pattern = (
            r'(?:^|\n)\s*(' + month_pattern + r'\.?\s+\d{4}\s*-\s*(?:' + month_pattern + r'\.?\s+\d{4}|[Pp]resent|[Aa]ctuel))\s*:\s*(.+?)(?=\n\s*' + month_pattern + r'\.?\s+\d{4}\s*-|\Z)'
        )

        matches = re.finditer(exp_pattern, section, re.DOTALL)
        for match in matches:
            periode = match.group(1).strip()
            contenu = match.group(2).strip()
            lignes = contenu.split('\n')

            poste = lignes[0].strip() if lignes else ""
            entreprise = ""
            description = []

            for ligne in lignes[1:]:
                ligne_clean = ligne.strip()
                if not ligne_clean:
                    continue
                # Detecter l'entreprise
                match_ent = re.match(
                    r'(?:Entreprise|Societe|Company|Startup)\s*:\s*(.+)',
                    ligne_clean
                )
                if match_ent:
                    entreprise = match_ent.group(1).strip()
                elif ligne_clean.startswith('-'):
                    description.append(ligne_clean.lstrip('- ').strip())
                elif not entreprise and not ligne_clean.startswith(('Responsabilites', '-')):
                    # Potentiellement le nom de l'entreprise
                    if re.match(r'^[A-Z]', ligne_clean) and len(ligne_clean) < 100:
                        entreprise = ligne_clean

            experience = {
                "periode": periode,
                "poste": poste,
                "entreprise": entreprise,
                "description": description
            }
            experiences.append(experience)

    return experiences


def extraire_formation(texte: str) -> List[Dict[str, str]]:
    """
    Extrait les formations/diplomes depuis le texte.
    """
    formations = []

    # Recherche de la section formation
    patterns_section = [
        r'[-=]+\s*\n\s*(?:FORMATION|EDUCATION).*?\n\s*[-=]+\s*\n([\s\S]*?)(?:\n\s*[-=]{2,}\s*\n\s*[A-Z]|\Z)',
        r'(?:FORMATION|EDUCATION)\s*[-:]*\s*\n([\s\S]*?)(?:\n\s*[-=]{2,}\s*\n\s*[A-Z]|\Z)',
    ]

    section = None
    for pattern in patterns_section:
        match = re.search(pattern, texte, re.IGNORECASE)
        if match:
            section = match.group(1)
            break

    if section:
        # Pattern pour les formations : "Annees : Diplome\n    Etablissement"
        form_pattern = r'(\d{4}\s*-\s*\d{4}|\d{4})\s*:\s*(.+?)(?=\n\s*\d{4}\s*[-:]|\Z)'
        matches = re.finditer(form_pattern, section, re.DOTALL)

        for match in matches:
            periode = match.group(1).strip()
            contenu = match.group(2).strip()
            lignes = contenu.split('\n')

            diplome = lignes[0].strip() if lignes else ""
            etablissement = ""

            for ligne in lignes[1:]:
                ligne_clean = ligne.strip()
                if ligne_clean and not ligne_clean.startswith('-'):
                    # Premiere ligne non vide apres le diplome = etablissement
                    if not etablissement:
                        etablissement = ligne_clean
                    break

            formations.append({
                "periode": periode,
                "diplome": diplome,
                "etablissement": etablissement
            })

    return formations


def extraire_langues(texte: str) -> List[Dict[str, str]]:
    """
    Extrait les langues et niveaux depuis le texte.
    """
    langues = []

    # Recherche de la section langues
    patterns_section = [
        r'[-=]+\s*\n\s*(?:LANGUES?|LANGUAGES?).*?\n\s*[-=]+\s*\n([\s\S]*?)(?:\n\s*[-=]{2,}\s*\n\s*[A-Z]|\Z)',
        r'(?:LANGUES?|LANGUAGES?)\s*[-:]*\s*\n([\s\S]*?)(?:\n\s*[-=]{2,}\s*\n\s*[A-Z]|\Z)',
    ]

    section = None
    for pattern in patterns_section:
        match = re.search(pattern, texte, re.IGNORECASE)
        if match:
            section = match.group(1)
            break

    if section:
        lignes = section.strip().split('\n')
        for ligne in lignes:
            ligne = ligne.strip()
            if not ligne or re.match(r'^[-=]+$', ligne):
                break
            # Pattern "Langue : Niveau"
            match_langue = re.match(r'^[•\-]?\s*(.+?)\s*:\s*(.+)$', ligne)
            if match_langue:
                langues.append({
                    "langue": match_langue.group(1).strip(),
                    "niveau": match_langue.group(2).strip()
                })

    return langues


def extraire_donnees_cv(texte: str) -> Dict:
    """
    Fonction principale qui extrait toutes les donnees structurees d'un CV.

    Args:
        texte: Le contenu brut du CV au format texte brut.

    Returns:
        Un dictionnaire contenant toutes les informations extraites.
    """
    return {
        "nom": extraire_nom(texte),
        "email": extraire_email(texte),
        "telephone": extraire_telephone(texte),
        "competences": extraire_competences(texte),
        "experience_professionnelle": extraire_experience(texte),
        "formation": extraire_formation(texte),
        "langues": extraire_langues(texte),
    }
