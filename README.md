# Extraction de donnees structurees depuis des textes bruts

## Sujet

Ce projet a pour objectif d'extraire automatiquement des informations structurees
a partir de CV (curriculum vitae) au format texte brut. Les informations extraites
sont organisees sous forme de donnees JSON et CSV exploitables.

## Objectifs du projet (NLP)

Ce projet repond a 4 objectifs pedagogiques en Traitement Automatique du Langage (NLP) :

1. **Extraction d'information** : identifier et extraire des entites nommees (noms, emails, telephones) et des structures complexes (experiences, formations) depuis du texte non-structure.
2. **Expressions regulieres** : maitriser les regex Python pour le pattern matching sur des formats de texte varies (francais/anglais, formats heterogenes).
3. **Evaluation quantitative** : mesurer la qualite de l'extraction avec des metriques standard (precision, rappel, F1-score) sur un jeu de donnees annote.
4. **Robustesse** : gerer la diversite des formats de CV reels (ordres de sections variables, separateurs differents, langues multiples).

## Dataset

Le projet utilise un corpus de **20 CVs fictifs** dans le dossier `data/` :

- Mix de CVs en **francais** et en **anglais**
- Professions variees : data science, marketing, sante, finance, ingenierie, design, enseignement, droit, cuisine, etc.
- Formats heterogenes : separateurs (`===`, `---`), labels de sections varies, ordres de sections differents
- Niveaux d'experience : junior, mid-level, senior, executif

## Execution

Le projet fonctionne uniquement avec la **bibliotheque standard Python** (aucune dependance externe) :

```bash
# Extraction des donnees depuis les 20 CVs
python3 main.py

# Evaluation de la qualite (precision, rappel, F1-score)
python3 evaluation/evaluate.py
```

### Sorties

- `results/output.json` : donnees structurees extraites pour chaque CV
- `results/output.csv` : tableau resume (fichier, nom, email, telephone, nombre de competences/experiences/formations/langues)
- `evaluation/rapport_evaluation.json` : rapport detaille avec scores par CV, par champ, et globaux

## Methodologie d'evaluation

L'evaluation compare les resultats extraits avec une verite terrain annotee manuellement (`evaluation/ground_truth.json`).

### Metriques

- **Precision** : proportion d'elements extraits qui sont corrects
- **Rappel** : proportion d'elements attendus qui ont ete extraits
- **F1-score** : moyenne harmonique de la precision et du rappel

### Niveaux d'evaluation

1. **Par champ et par CV** : F1-score pour chaque champ (nom, email, competences, etc.) de chaque CV
2. **Moyenne par champ** : F1-score moyen pour chaque type de champ across tous les CVs
3. **Score global** : F1-score moyen sur tous les champs et tous les CVs
4. **Detection des problemes** : identification des CVs ayant un F1 < 0.8 sur au moins un champ

### Types de comparaison

- Champs simples (nom, email, telephone) : correspondance exacte
- Listes (competences) : intersection des ensembles normalises
- Listes structurees (experience, formation, langues) : correspondance sur champs cles

## Structure du projet

```
text-structured-extraction/
├── README.md                           # Ce fichier
├── requirements.txt                    # Dependances (stdlib uniquement)
├── main.py                             # Point d'entree - extraction et export
├── data/
│   ├── cv1.txt ... cv20.txt            # 20 CVs fictifs (francais/anglais)
├── src/
│   ├── __init__.py
│   └── extractor.py                    # Module principal d'extraction (regex)
├── evaluation/
│   ├── evaluate.py                     # Script d'evaluation F1-score
│   ├── ground_truth.json               # Verite terrain annotee
│   └── rapport_evaluation.json         # Rapport genere (scores detailles)
├── results/
│   ├── output.json                     # Resultats d'extraction (genere)
│   └── output.csv                      # Resume tabulaire (genere)
├── notebooks/
│   └── demo_extraction.ipynb           # Notebook de demonstration
└── presentation/
    └── presentation.md                 # Support de presentation
```

## Approche technique

Le projet utilise les **expressions regulieres** (`re`) de Python pour :

1. **Detection de sections** : identifier les blocs (formation, experience, etc.)
   grace aux en-tetes entre lignes de separateurs (`===`, `---`)
2. **Extraction de patterns** : capturer les emails, numeros de telephone et
   noms avec des motifs regex specifiques
3. **Parsing structure** : analyser le contenu de chaque section pour extraire
   les informations detaillees (dates, postes, entreprises, competences)
4. **Gestion multi-format** : supporter les variantes de nommage de sections
   en francais et anglais, les differents formats de dates, et les styles
   de listes varies

## Exemple de resultat

```json
{
  "nom": "Marie Dupont",
  "email": "marie.dupont@email.fr",
  "telephone": "06 12 34 56 78",
  "competences": ["Python", "R", "SQL", "Scikit-learn", "TensorFlow", "AWS (S3, SageMaker, EC2)"],
  "experience_professionnelle": [
    {
      "periode": "Janvier 2022 - Present",
      "poste": "Data Scientist Senior",
      "entreprise": "DataTech Solutions, Paris"
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

## Auteur

Projet realise dans le cadre d'un cours universitaire.
