 NTL-SysToolbox

🌐 Description du projet (FR)

NTL-SysToolbox est un outil en ligne de commande développé en Python dans le cadre d’un projet académique.  
Il est destiné à l’équipe informatique de la société fictive **NordTransit Logistics (NTL)**.

L’outil permet de :

- Diagnostiquer les services critiques (AD/DNS, MySQL, système)  
- Automatiser les sauvegardes de la base de données WMS  
- Réaliser un audit d’obsolescence (fin de support – EOL) du parc informatique  

---

🌐 Project Description (EN)

NTL-SysToolbox is a Python-based command-line tool developed as part of an academic project.  
It is designed for the IT team of the fictional company **NordTransit Logistics (NTL)**.

The tool allows to:

- Diagnose critical services (AD/DNS, MySQL, system health)  
- Automate WMS database backups  
- Perform an end-of-life (EOL) audit of the IT infrastructure  

---

 ⚙️ Prerequisites / Prérequis

- Python 3.8 or higher  
- MySQL client (`mysqldump`)  
- Administrator rights (for AD/DNS checks on Windows)  

---

 🚀 Installation and Execution / Installation et exécution

```bash
git clone https://github.com/menaaraibia192-png/NTL-SYSTOOLBOX.git
cd NTL-SysToolbox
pip install -r requirements.txt
python main.py
🖱️ Usage / Utilisation

The application starts with an interactive menu allowing the user to select:

Diagnostic module

WMS backup module

Obsolescence audit module

The tool generates output files in JSON, TXT, SQL, CSV format.

📁 Project Structure / Structure du projet
NTL-SysToolbox/
│
├─ main.py
├─ diagnostic.py
├─ backup.py
├─ obsolescence_audit.py
├─ inventaire_ntl.csv
├─ requirements.txt
├─ backups/
└─ docs/

⚙️ Configuration

MySQL credentials are defined in the file backup.py:

MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
DB_NAME = "wms_db"

📦 Deliverables / Livrables

Source code (GitHub repository)

Technical and functional documentation

Installation and user manual

Reference obsolescence audit report

👥 Project Team / Équipe du projet

Araibia Menat Allah

Kacou Murielle

Khorchaly Oussama

Djaaloul Bilal

🎓 Academic Context / Contexte académique

Project carried out as part of the training:
Administrateur Systèmes, Réseaux et Bases de Données
Evaluation module: TPRE511 / E6.1

📬 Contact

mena.araibia192@gmail.com
