import os
import platform
import mysql.connector
from mysql.connector import Error
import psutil
import time
from datetime import datetime, timedelta
import json
import logging
import subprocess
# Configuration logging
logging.basicConfig(
    filename='diagnostic.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
def save_json(filename, data):
    """Sauvegarde JSON dans le dossier du projet"""
    data["timestamp"] = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    print(f"JSON sauvegardé dans {filename}")
# ========== FONCTION 1 : VÉRIFIER AD/DNS ==========
def verifier_ad_dns():
    """Vérifie les services AD/DNS (Windows uniquement)"""
    if platform.system() != "Windows":
        print("\n[!] Fonction disponible uniquement sous Windows")
        return False
    print("\n=== VÉRIFICATION AD/DNS ===\n")
    services = [
        ("NTDS", "Active Directory"),
        ("DNS", "DNS Server")
    ]
    all_ok = True
    services_status = {}
    for service_name, service_desc in services:
        try:
            cmd = ["sc", "query", service_name]
            process = subprocess.run(cmd, capture_output=True, text=True)
            if "RUNNING" in process.stdout:
                print(f"{service_desc} : Actif ✔")
                services_status[service_name] = "running"
            else:
                print(f"{service_desc} : Arrêté ✖")
                services_status[service_name] = "stopped"
                all_ok = False
        except Exception as e:
            print(f"{service_desc} : Erreur ✖ - {e}")
            services_status[service_name] = "error"
            all_ok = False
    success = all_ok
    logging.info(f"AD/DNS → {'OK' if success else 'ECHEC'}")
    # Génération JSON
    data = {
        "test": "ad_dns",
        "services": services_status,
        "status": "success" if success else "failed",
        "return_code": 0 if success else 1
    }
    save_json("ad_dns_result.json", data)
    return success
# ========== FONCTION 2 : TESTER MYSQL ==========
def test_mysql_connection(host, user, password):
    """Test de connexion MySQL"""
    print(f"\nTest de connexion MySQL vers {host}...")    
    try:
        # Tentative de connexion
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        if connection.is_connected():
            print("Connexion MySQL réussie ✔")
            connection.close()
            successmysql = True
            logging.info(f"MySQL {host} → {'OK' if successmysql else 'ECHEC'}")
            data = {
                "test": "mysql",
                "host": host,
                "status": "success" if successmysql else "failed",
                "return_code": 0 if successmysql else 1
            }
            save_json("mysql_result.json", data)
            return True
    except Error as er:
        print(f"Erreur MySQL ✖ : {er}")
        successmysql = False
        logging.info(f"MySQL {host} → {'OK' if successmysql else 'ECHEC'}")
        data = {
            "test": "mysql",
            "host": host,
            "status": "failed",
            "error": str(er),
            "return_code": 1
        }
        save_json("mysql_result.json", data)
        return False
# ========== FONCTION 3 : INFORMATIONS SYSTÈME ==========
def get_system_info():
    """Récupère les informations système"""
    print("Récupération des informations système...\n")
    # CPU %
    cpu = psutil.cpu_percent(interval=1)
    # RAM %
    ram = psutil.virtual_memory().percent
    # Disque %
    disk = psutil.disk_usage('/').percent
    # Uptime
    boot_time = psutil.boot_time()
    uptime_seconds = time.time() - boot_time
    uptime = str(timedelta(seconds=int(uptime_seconds)))
    print(f"CPU utilisé : {cpu}%")
    print(f"RAM utilisée : {ram}%")
    print(f"Espace disque utilisé : {disk}%")
    print(f"Uptime : {uptime}")
    logging.info("Récupération infos système OK")
    # Données JSON
    data = {
        "test": "system_info",
        "cpu_percent": cpu,
        "ram_percent": ram,
        "disk_percent": disk,
        "uptime": uptime,
        "status": "success",
        "return_code": 0
    }
    # Sauvegarde JSON
    save_json("system_info_result.json", data)
    return data