import json
import csv
import requests
import os
from datetime import datetime
from typing import Dict, List
# ==================== CONFIGURATION ====================
EOL_DATA_FILE = "eol_database.json"
CSV_FILE = "inventaire_ntl.csv"
API_URL = "https://endoflife.date/api"
# Base de données EOL locale (backup)
EOL_DATABASE = {
    "Windows Server 2008": {"eol_date": "2020-01-14", "categorie": "Windows Server"},
    "Windows Server 2008 R2": {"eol_date": "2020-01-14", "categorie": "Windows Server"},
    "Windows Server 2012": {"eol_date": "2023-10-10", "categorie": "Windows Server"},
    "Windows Server 2012 R2": {"eol_date": "2023-10-10", "categorie": "Windows Server"},
    "Windows Server 2016": {"eol_date": "2027-01-12", "categorie": "Windows Server"},
    "Windows Server 2019": {"eol_date": "2029-01-09", "categorie": "Windows Server"},
    "Windows Server 2022": {"eol_date": "2031-10-14", "categorie": "Windows Server"},
    "Windows 7": {"eol_date": "2020-01-14", "categorie": "Windows Client"},
    "Windows 10": {"eol_date": "2025-10-14", "categorie": "Windows Client"},
    "Windows 11": {"eol_date": "2026-10-10", "categorie": "Windows Client"},
    "Ubuntu 18.04": {"eol_date": "2028-04-30", "categorie": "Linux"},
    "Ubuntu 20.04": {"eol_date": "2030-04-30", "categorie": "Linux"},
    "Ubuntu 22.04": {"eol_date": "2032-04-30", "categorie": "Linux"},
    "CentOS 7": {"eol_date": "2024-06-30", "categorie": "Linux"},
    "CentOS 8": {"eol_date": "2021-12-31", "categorie": "Linux"},
    "VMware ESXi 6.5": {"eol_date": "2022-10-15", "categorie": "Virtualisation"},
    "VMware ESXi 6.7": {"eol_date": "2022-10-15", "categorie": "Virtualisation"},
    "VMware ESXi 7.0": {"eol_date": "2025-04-02", "categorie": "Virtualisation"}
}
# ==================== UTILITAIRES ====================
def print_separator(char="=", length=70):
    print(char * length)
def print_header(title):
    print_separator()
    print(title)
    print_separator()
def calculate_eol_status(eol_date_str: str) -> str:
    if eol_date_str == "N/A":
        return "INCONNU"
    try:
        eol_date = datetime.strptime(eol_date_str, "%Y-%m-%d")
        days = (eol_date - datetime.now()).days
        if days < 0:
            return "NON SUPPORTÉ"
        elif days < 180:
            return "BIENTÔT NON SUPPORTÉ"
        else:
            return "SUPPORTÉ"
    except:
        return "INCONNU"
def detect_os_type(os_version: str) -> str:
    os_lower = os_version.lower()
    if 'windows' in os_lower:
        return 'Windows'
    elif any(x in os_lower for x in ['linux', 'ubuntu', 'centos']):
        return 'Linux/Unix'
    elif any(x in os_lower for x in ['vmware', 'esxi']):
        return 'Virtualisation'
    return 'Inconnu'
# ==================== CLASSE PRINCIPALE ====================
class ObsolescenceAuditor:
    def __init__(self, use_api=False):
        self.use_api = use_api
        self.eol_db = EOL_DATABASE
        self.timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    def load_csv(self) -> List[Dict]:
        """Charge l'inventaire CSV"""
        try:
            with open(CSV_FILE, 'r', encoding='utf-8') as f:
                return [
                    {
                        "ip": row.get('ip', 'N/A'),
                        "nom": row.get('nom', 'N/A'),
                        "os_version": row.get('os_version', 'Inconnu'),
                        "os_detected": detect_os_type(row.get('os_version', ''))
                    }
                    for row in csv.DictReader(f)
                ]
        except FileNotFoundError:
            print(f"[!] Fichier {CSV_FILE} introuvable")
            return []
    def filter_network(self, inventory: List[Dict], network_range: str) -> List[Dict]:
        """Filtre l'inventaire selon la plage réseau"""
        if '/' in network_range:
            base = '.'.join(network_range.split('/')[0].split('.')[:-1])
            return [c for c in inventory if c['ip'].startswith(base)]
        elif '-' in network_range:
            parts = network_range.split('-')
            base = '.'.join(parts[0].split('.')[:-1])
            start, end = int(parts[0].split('.')[-1]), int(parts[1])
            return [c for c in inventory if c['ip'].startswith(base) and 
                    start <= int(c['ip'].split('.')[-1]) <= end]
        return [c for c in inventory if c['ip'] == network_range]
    def get_eol_versions(self, search_term: str = None) -> Dict:
        """Récupère les versions EOL (filtrées ou toutes)"""
        if not search_term:
            return self.eol_db
        search_lower = search_term.lower()
        categories = {
            'linux': 'Linux',
            'windows': ['Windows Server', 'Windows Client'],
            'vmware': 'Virtualisation',
            'esxi': 'Virtualisation'
        }
        target = categories.get(search_lower)
        if target:
            target = [target] if isinstance(target, str) else target
            return {k: v for k, v in self.eol_db.items() if v.get('categorie') in target}
        return {k: v for k, v in self.eol_db.items() if search_lower in k.lower()}
    def analyze_inventory(self) -> List[Dict]:
        """Analyse l'inventaire CSV et ajoute les infos EOL"""
        inventory = self.load_csv()
        return [
            {
                "nom": item['nom'],
                "ip": item['ip'],
                "os_version": item['os_version'],
                "date_eol": self.eol_db.get(item['os_version'], {"eol_date": "N/A"})["eol_date"],
                "statut": calculate_eol_status(
                    self.eol_db.get(item['os_version'], {"eol_date": "N/A"})["eol_date"]
                )
            }
            for item in inventory
        ]
    def generate_report(self, components: List[Dict]) -> str:
        """Génère les rapports JSON et TXT"""
        if not components:
            print("[!] Aucune donnée à analyser")
            return ""
        stats = {
            "non_supportes": sum(1 for c in components if c['statut'] == 'NON SUPPORTÉ'),
            "bientot": sum(1 for c in components if c['statut'] == 'BIENTÔT NON SUPPORTÉ'),
            "supportes": sum(1 for c in components if c['statut'] == 'SUPPORTÉ'),
            "inconnus": sum(1 for c in components if c['statut'] == 'INCONNU')
        }
        # JSON
        json_file = f"rapport_obsolescence_{self.timestamp}.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump({
                "date_audit": datetime.now().isoformat(),
                "total_composants": len(components),
                "statistiques": stats,
                "composants": components
            }, f, indent=2, ensure_ascii=False)
        # TXT
        txt_file = f"rapport_obsolescence_{self.timestamp}.txt"
        with open(txt_file, 'w', encoding='utf-8') as f:
            f.write("="*80 + "\n")
            f.write("RAPPORT D'AUDIT D'OBSOLESCENCE - NordTransit Logistics\n")
            f.write("="*80 + "\n\n")
            f.write(f"Date: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            f.write(f"Total: {len(components)} composants\n\n")
            f.write("STATISTIQUES\n" + "-"*80 + "\n")
            for key, label in [
                ('non_supportes', 'NON SUPPORTÉS'),
                ('bientot', 'BIENTÔT NON SUPPORTÉS'),
                ('supportes', 'SUPPORTÉS'),
                ('inconnus', 'INCONNUS')
            ]:
                f.write(f"{label:<30} {stats[key]}\n")
            # Sections par statut
            for status, title in [
                ('NON SUPPORTÉ', 'COMPOSANTS NON SUPPORTÉS (URGENT)'),
                ('BIENTÔT NON SUPPORTÉ', 'BIENTÔT NON SUPPORTÉS (PLANIFIER)'),
                ('INCONNU', 'STATUT INCONNU (AUDIT NÉCESSAIRE)')
            ]:
                filtered = [c for c in components if c['statut'] == status]
                if filtered:
                    f.write(f"\n{'='*80}\n{title}\n{'='*80}\n")
                    for c in filtered:
                        f.write(f"\n• {c['nom']}\n  IP: {c['ip']}\n  OS: {c['os_version']}\n  EOL: {c['date_eol']}\n")
        print(f"\n[+] Rapport JSON: {json_file}")
        print(f"[+] Rapport TXT: {txt_file}")
        return json_file
# ==================== MENU INTERACTIF ====================
def menu_principal():
    print_header("MODULE D'AUDIT D'OBSOLESCENCE - Configuration")
    print("\n1. Mode LOCAL (base intégrée - recommandé)")
    print("2. Mode API (endoflife.date - nécessite Internet)")
    mode = input("\n→ Choix [1] : ").strip() or "1"
    use_api = mode == "2"
    if use_api:
        try:
            requests.get("https://endoflife.date", timeout=3)
            print("[✓] Mode API activé")
        except:
            print("[✗] Échec - Mode LOCAL activé")
            use_api = False
    auditor = ObsolescenceAuditor(use_api=use_api)
    while True:
        print_header(f"MODULE D'AUDIT - {'API' if use_api else 'LOCAL'}")
        print("\n1. Lister composants réseau")
        print("2. Lister versions EOL")
        print("3. Analyser inventaire CSV")
        print("4. Générer rapport complet")
        print("0. Retour\n")
        print_separator("-")
        choix = input("\n→ Choix : ").strip()
        if choix == "1":
            print_header("COMPOSANTS RÉSEAU")
            print("\nExemples: 192.168.10.0/24 | 192.168.10.21 | 192.168.10.1-50")
            plage = input("\n→ Plage : ").strip()
            if plage:
                inventory = auditor.load_csv()
                components = auditor.filter_network(inventory, plage)
                if components:
                    print(f"\n{len(components)} composant(s)\n")
                    print(f"{'Nom':<20} {'IP':<18} {'OS':<15} {'Version'}")
                    print_separator("-")
                    for c in components:
                        print(f"{c['nom']:<20} {c['ip']:<18} {c['os_detected']:<15} {c['os_version']}")
                else:
                    print("\n[!] Aucun composant trouvé")
        elif choix == "2":
            print_header("VERSIONS EOL")
            search = input("\n→ Recherche (linux/windows/vmware) : ").strip()
            versions = auditor.get_eol_versions(search if search else None)
            if versions:
                print(f"\n{len(versions)} version(s)\n")
                for os_ver, info in list(versions.items())[:15]:
                    statut = calculate_eol_status(info['eol_date'])
                    print(f"• {os_ver:<40} EOL: {info['eol_date']:<12} [{statut}]")
            else:
                print("\n[!] Aucune version trouvée")
        elif choix == "3":
            results = auditor.analyze_inventory()
            if results:
                print(f"\n{len(results)} composant(s) analysé(s)\n")
                for r in results:
                    print(f"• {r['nom']:<20} {r['os_version']:<30} [{r['statut']}]")
        elif choix == "4":
            if not os.path.exists(CSV_FILE):
                print(f"\n[!] Fichier {CSV_FILE} introuvable")
            else:
                results = auditor.analyze_inventory()
                if results:
                    auditor.generate_report(results)
        elif choix == "0":
            print("\n[*] Retour au menu principal")
            break
        else:
            print("\n[!] Choix invalide")
        input("\nAppuyez sur Entrée...")
if __name__ == "__main__":
    menu_principal()