# 🐍 Python Data Structures Labs


## 📋 Description

Ce repository contient les 4 travaux pratiques (TPs) réalisés dans le cadre du module
**Fondamentaux des Structures de Données en Python**. Chaque TP est une application
Python complète couvrant différents aspects de la programmation et des structures de données.

## 📁 Structure du Repository

```
python-data-structures-labs/
│
├── TP1_Gestion_Etudiants/       # TP1 — Gestion des étudiants
│   ├── main.py
│   ├── etudiants.json
│   └── etudiants_export.txt
│
├── TP2_Systeme_Bancaire/        # TP2 — Système bancaire simplifié
│   ├── main.py
│   └── comptes.json
│
├── TP3_Gestion_bibliotheque/    # TP3 — Gestion de bibliothèque
│   ├── main.py
│   ├── interface.py
│   └── bibliotheque.json
│
├── TP4_Analyse_Donnees/         # TP4 — Analyse de données
│   ├── main.py
│   ├── analyse.py
│   └── ventes.csv
│
├── .gitignore
└── README.md
```

---

## 🔬 Travaux Pratiques

### TP1 — Gestion des Étudiants

Application de gestion complète des étudiants avec persistance des données.

**Fonctionnalités :**
- ➕ Ajouter un étudiant avec ses notes (5 matières)
- 📋 Afficher la liste complète
- 🔍 Rechercher par nom ou prénom
- ✏️ Modifier les informations
- 🗑️ Supprimer avec confirmation
- 📊 Calculer la moyenne générale de la classe
- 🏆 Afficher le classement avec mentions
- 💾 Exporter les résultats en fichier texte

**Technologies :** `json` `os`

---

### TP2 — Système Bancaire Simplifié
Mini système bancaire avec gestion des comptes et historique des opérations.

**Fonctionnalités :**
- 🏦 Création de compte
- 💰 Dépôt
- 💸 Retrait (solde jamais négatif)
- 🔄 Virement entre comptes
- 📈 Consultation du solde
- 📜 Historique des opérations

**Technologies :** `json` `os` `datetime`

---

### TP3 — Gestion d'une Bibliothèque
Application de gestion de bibliothèque avec interface graphique tkinter.

**Fonctionnalités :**
- 📚 Ajouter un livre (ISBN unique)
- 📋 Catalogue complet avec statut de disponibilité
- 🔍 Recherche multicritère (titre, auteur, ISBN, disponibilité)
- 📤 Emprunt avec horodatage automatique
- 📥 Retour avec mise à jour de l'historique
- 📊 Statistiques détaillées (livre populaire, top emprunteurs)
- 🖥️ Interface graphique professionnelle (tkinter)

**Technologies :** `tkinter` `json` `datetime` `os`

---

### TP4 — Analyse de Données et Tableaux de Bord

Mini-projet d'analyse de données commerciales avec visualisations graphiques.

**Fonctionnalités :**
- 📂 Import et traitement de données CSV avec pandas
- 💹 Calcul du chiffre d'affaires total
- 🏆 Identification du produit le plus vendu
- 📅 Mois le plus rentable
- 🔝 Top 5 des meilleures ventes
- 📊 Histogramme CA par produit
- 📈 Courbe évolution CA par mois
- 🥧 Diagramme circulaire répartition des ventes
- 📉 Barres horizontales Top 5 ventes

**Technologies :** `pandas` `matplotlib` `os`

---

## 🚀 Installation et Exécution

### Prérequis
```bash
Python 3.12+
pip 24.2+
```

### Installation des dépendances
```bash
# TP4 uniquement
pip install pandas matplotlib
```

### Lancer les TPs
```bash
# TP1
cd TP1_Gestion_Etudiants
python main.py

# TP2
cd TP2_Systeme_Bancaire
python main.py

# TP3 — Console
cd TP3_Gestion_bibliotheque
python main.py

# TP3 — Interface graphique
cd TP3_Gestion_bibliotheque
python interface.py

# TP4
cd TP4_Analyse_Donnees
python main.py
```

---

## 🛠️ Technologies Utilisées

| Technologie | Version | Utilisation |
|---|---|---|
| Python | 3.12.7 | Langage principal |
| pandas | 2.x | Analyse de données (TP4) |
| matplotlib | 3.x | Visualisation graphique (TP4) |
| tkinter | Standard | Interface graphique (TP3) |
| JSON | Standard | Persistance des données |

---

## 👨‍💻 Auteur

**Rida Khouaja**  
Élève Ingénieur — Génie Informatique  
Faculté des Sciences et Techniques Errachidia  
Université Moulay Ismail — 2025/2026
