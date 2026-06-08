# Extraction de donnees structurees depuis des textes bruts

## Sujet

Ce projet a pour objectif d'extraire automatiquement des informations structurees
a partir de CV (curriculum vitae) au format texte brut. Les informations extraites
sont organisees sous forme de donnees JSON exploitables.

## Objectif du projet

- Lire des fichiers texte bruts contenant des CV (francais et anglais)
- Identifier et extraire les informations cles : nom, email, telephone,
  competences, experience professionnelle, formation et langues
- Structurer ces informations en format JSON
- Demontrer l'utilisation d'expressions regulieres (regex) pour le traitement
  de texte en Python

## Installation

```bash
# Cloner le depot
git clone <url-du-depot>
cd text-structured-extraction

# (Optionnel) Creer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Installer les dependances (optionnel, pour les fonctionnalites avancees)
pip install -r requirements.txt
```

## Execution

Le script principal fonctionne uniquement avec la bibliotheque standard Python
(pas de dependances externes requises) :

```bash
python main.py
```

Les resultats sont sauvegardes dans `results/output.json`.

## Structure du projet

```
text-structured-extraction/
├── README.md                    # Ce fichier
├── data/
│   ├── cv1.txt                  # CV fictif en francais (data scientist)
│   ├── cv2.txt                  # CV fictif en francais (ingenieur logiciel)
│   └── cv3.txt                  # CV fictif en anglais (ML engineer)
├── notebooks/
│   └── demo_extraction.ipynb    # Notebook de demonstration
├── src/
│   ├── __init__.py
│   └── extractor.py            # Module principal d'extraction
├── main.py                      # Point d'entree du programme
├── requirements.txt             # Dependances Python
└── results/
    └── .gitkeep                 # Dossier pour les resultats
```

## Exemple de resultat

```json
{
  "nom": "Marie Dupont",
  "email": "marie.dupont@email.fr",
  "telephone": "06 12 34 56 78",
  "competences": ["Python", "R", "SQL", "Scikit-learn", "TensorFlow"],
  "experience_professionnelle": [
    {
      "periode": "Janvier 2022 - Present",
      "poste": "Data Scientist Senior",
      "entreprise": "DataTech Solutions, Paris",
      "description": ["Developpement de modeles de machine learning..."]
    }
  ],
  "formation": [
    {
      "periode": "2019 - 2021",
      "diplome": "Master Data Science et Intelligence Artificielle",
      "etablissement": "Universite Paris-Saclay, Orsay"
    }
  ],
  "langues": [
    {"langue": "Francais", "niveau": "Langue maternelle"},
    {"langue": "Anglais", "niveau": "Courant (TOEIC 945)"}
  ]
}
```

## Approche technique

Le projet utilise les **expressions regulieres** (`re`) de Python pour :

1. **Detection de sections** : identifier les blocs (formation, experience, etc.)
   grace aux en-tetes et separateurs
2. **Extraction de patterns** : capturer les emails, numeros de telephone et
   noms avec des motifs regex specifiques
3. **Parsing structure** : analyser le contenu de chaque section pour extraire
   les informations detaillees

## Ameliorations possibles

- **spaCy NER** : utiliser la reconnaissance d'entites nommees pour detecter
  automatiquement les noms, lieux et organisations
- **Transformers (Hugging Face)** : utiliser des modeles pre-entraines comme
  CamemBERT pour une meilleure comprehension du texte francais
- **Parsing PDF** : ajouter la lecture de CV au format PDF avec PyPDF2 ou pdfplumber
- **Interface web** : creer une interface avec Flask ou Streamlit pour
  telecharger et analyser des CV
- **Base de donnees** : stocker les resultats dans une base SQLite ou PostgreSQL
- **Evaluation** : ajouter des metriques de precision/rappel sur un jeu de
  donnees annote

## Auteur

Projet realise dans le cadre d'un cours universitaire.
