# Parc Informatique (API Backend)

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-2.0%2B-informational)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-Unlicensed-lightgrey)](https://choosealicense.com/)

Une application backend en Python/Flask pour gérer l'inventaire et l'affectation d'équipements, les utilisateurs, l'authentification (JWT), et le traitement des réclamations avec notifications par email.

## 🚀 Fonctionnalités principales

- Gestion des **utilisateurs** (CRUD)
- Gestion des **équipements** (CRUD)
- Gestion des **affectations** d'équipements aux utilisateurs
- Gestion des **réclamations** (création, suivi)
- **Authentification JWT** (login / refresh token)
- Envoi d'**emails** (notifications d'affectation / réclamation)
- **Migrations de base de données** avec Alembic

## Prérequis

- Python 3.10+ (recommandé)
- MySQL / MariaDB
- Git (optionnel)

## 🔧 Installation

1. Clonez le dépôt (si nécessaire) :

```bash
git clone <url-du-repo>
cd pi-back
```

2. Créez et activez un environnement virtuel :

```bash
python -m venv venv
# Windows PowerShell
venv\Scripts\Activate.ps1
# Windows CMD
venv\Scripts\activate.bat
# macOS / Linux
source venv/bin/activate
```

3. Installez les dépendances :

```bash
pip install -r requirements.txt
```

## ⚙️ Configuration

Le projet utilise `python-dotenv` pour charger les variables d'environnement depuis un fichier `.env`. Créez un fichier `.env` à la racine du projet avec au moins :

```env
SECRET_KEY=une_chaine_secrete
JWT_SECRET_KEY=une_autre_chaine_secrete
MAIL_USERNAME=votre.email@gmail.com
MAIL_PASSWORD=mot_de_passe_app
```

> **Note** : la connexion MySQL est configurée dans `config.py` (par défaut `root:root@localhost/parc_informatique`). Modifiez-la selon votre configuration.

## 🗄️ Base de données & migrations

1. Créez la base de données MySQL (nommée `parc_informatique` par défaut).
2. Exécutez les migrations :

```bash
flask db upgrade
```

Si la commande `flask` n'est pas disponible, lancez-la via le module `flask` :

```bash
python -m flask db upgrade
```

## ▶️ Lancer l'application

```bash
python app.py
```

L'API sera disponible sur : `http://localhost:5000`

## 📌 Points de terminaison principaux

Les blueprints enregistrés (avec préfixes) :

- `/auth` - Authentification (login, refresh)
- `/utilisateurs` - Gestion des utilisateurs
- `/equipements` - Gestion des équipements
- `/affectations` - Gestion des affectations
- `/reclamations` - Gestion des réclamations

## 🧪 Tests

Aucun framework de test n'est fourni dans ce dépôt, mais vous pouvez ajouter des tests avec `pytest` ou `unittest` selon votre préférence.

## 📝 Structure du projet

- `app.py` - point d'entrée principal
- `config.py` - configuration Flask / Base de données / JWT / mail
- `src/` - code applicatif (controllers, models, services, dao)
- `migrations/` - historiques Alembic

---

## 🌟 Contribution

N'hésitez pas à proposer des améliorations, à corriger des bugs ou à enrichir l'API (pagination, filtrage, gestion des rôles, tests, etc.).
