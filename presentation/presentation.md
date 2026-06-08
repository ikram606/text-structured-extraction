# Extraction de donnees structurees depuis des textes bruts

**Projet NLP - Traitement de texte**

Auteur : [Votre nom]

Date : 2025

---

## Problematique

### Contexte

- Les CV sont souvent disponibles en **format texte brut**, non structure
- Les informations importantes sont noyees dans du texte libre
- Le traitement manuel est **couteux en temps** et source d'erreurs

### Probleme

> Comment extraire automatiquement les informations cles depuis un CV en texte brut ?

### Objectif

Transformer du **texte brut** en **donnees JSON structurees**, exploitables par des systemes informatiques.

---

## Approche technique

### Methode

- Extraction par **expressions regulieres** (regex)
- Aucune dependance externe requise

### Langage et outils

- **Python 3** (librairie standard uniquement)
- Module `re` pour les expressions regulieres
- Module `json` pour la sortie structuree

### Champs extraits

| Champ | Description |
|-------|-------------|
| Nom | Nom complet du candidat |
| Email | Adresse email |
| Telephone | Numero de telephone |
| Competences | Liste des competences techniques |
| Experience | Postes occupes avec details |
| Formation | Diplomes et etablissements |
| Langues | Langues parlees et niveaux |

### Pipeline de traitement

```
Lecture fichier .txt → Detection de sections → Extraction par regex → Export JSON
```

---

## Architecture du projet

### Structure des fichiers

```
text-structured-extraction/
├── data/
│   ├── cv1.txt          # CV en francais (Data Scientist)
│   ├── cv2.txt          # CV en francais (Ingenieur Logiciel)
│   └── cv3.txt          # CV en anglais (ML Engineer)
├── src/
│   └── extractor.py     # Module principal d'extraction
├── notebooks/
│   └── demo_extraction.ipynb  # Demonstration interactive
├── results/
│   └── output.json      # Resultats de l'extraction
├── main.py              # Point d'entree du programme
├── requirements.txt     # Dependances du projet
└── README.md            # Documentation
```

### Role de chaque composant

- **data/** : Fichiers CV bruts servant de donnees d'entree (3 CV de test)
- **src/extractor.py** : Logique d'extraction (regex, detection de sections)
- **main.py** : Orchestration du pipeline complet
- **results/** : Sortie JSON structuree
- **notebooks/** : Demonstration et exploration interactive

### Donnees de test

- **cv1.txt** : Marie Dupont - Data Scientist (FR)
- **cv2.txt** : Thomas Martin - Ingenieur Logiciel (FR)
- **cv3.txt** : Sarah Johnson - ML Engineer (EN)

---

## Demonstration / Resultats

### AVANT : Texte brut du CV

```
==============================
CURRICULUM VITAE
==============================

Nom : Marie Dupont
Email : marie.dupont@email.fr
Telephone : 06 12 34 56 78

------------------------------
COMPETENCES
------------------------------
Langages de programmation : Python, R, SQL, Scala
Machine Learning : Scikit-learn, TensorFlow, PyTorch
...
```

### APRES : JSON structure

```json
{
  "nom": "Marie Dupont",
  "email": "marie.dupont@email.fr",
  "telephone": "06 12 34 56 78",
  "competences": ["Python", "R", "SQL", "Scala",
                  "Scikit-learn", "TensorFlow", "PyTorch", ...],
  "experience_professionnelle": [
    {
      "periode": "Janvier 2022 - Present",
      "poste": "Data Scientist Senior",
      "entreprise": "Societe DataTech Solutions, Paris"
    }
  ],
  "formation": [...],
  "langues": [{"langue": "Francais", "niveau": "Langue maternelle"}, ...]
}
```

### Resultats

- **3 CV traites avec succes**
- **Tous les champs extraits correctement**
- Support des formats francais et anglais

---

## Limites et ameliorations

### Limites actuelles

- Depend fortement du **format du CV** (sections bien delimitees)
- Les regex sont **fragiles** si la structure varie significativement
- Pas de gestion des CV en PDF ou en image
- Difficulte avec les formats atypiques ou creatifs

### Ameliorations possibles

| Amelioration | Technologie | Benefice |
|-------------|-------------|----------|
| Reconnaissance d'entites nommees (NER) | spaCy, Stanza | Extraction plus robuste |
| Modeles pre-entraines | CamemBERT, BERT | Comprehension du contexte |
| OCR | Tesseract, EasyOCR | Support PDF et images |
| Classification de sections | Transformers | Detection automatique des rubriques |
| Interface web | Flask, Streamlit | Facilite d'utilisation |

---

## Conclusion

### Resume

- Solution **fonctionnelle** basee sur Python standard (pas de dependances externes)
- Extraction reussie de 7 champs structures depuis des CV bruts
- Pipeline simple et reproductible : texte brut vers JSON

### Points forts

- Leger et portable (aucune installation requise)
- Code lisible et maintenable
- Facilement extensible a d'autres types de documents

### Perspectives

- Integration dans un workflow de recrutement automatise
- Extension vers d'autres formats de documents (lettres de motivation, fiches de poste)

### Code disponible sur GitHub

**Questions ?**
