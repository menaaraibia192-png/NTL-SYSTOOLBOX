import os
import sys
from datetime import datetime
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Import des modules
modules_disponibles = {}
try:
    import diagnostic
    modules_disponibles['diagnostic'] = True
except ImportError as e:
    print(f"[AVERTISSEMENT] Module diagnostic.py : {e}")
    modules_disponibles['diagnostic'] = False
try:
    import backup
    modules_disponibles['backup'] = True
except ImportError as e:
    print(f"[AVERTISSEMENT] Module backup.py : {e}")
    modules_disponibles['backup'] = False
try:
    import obsolescence_audit
    modules_disponibles['obsolescence'] = True
except ImportError as e:
    print(f"[AVERTISSEMENT] Module obsolescence_audit.py : {e}")
    modules_disponibles['obsolescence'] = False
class NTLSysToolbox:
    """Menu CLI interactif principal"""
    def __init__(self):
        self.version = "1.0.0"
        self.nom_entreprise = "NordTransit Logistics"
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    def print_header(self):
        print("=" * 80)
        print(f"  NTL-SYSTOOLBOX v{self.version} - {self.nom_entreprise}")
        print("=" * 80)
        print(f"  Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        print("-" * 80)
    def print_menu_principal(self):
        self.clear_screen()
        self.print_header()
        print("\n╔════════════════════════════════════════════════════════════════════════════╗")
        print("║                            MENU PRINCIPAL                                  ║")
        print("╚════════════════════════════════════════════════════════════════════════════╝")
        statut1 = "✓" if modules_disponibles.get('diagnostic') else "✗"
        print(f"\n  [{statut1}] 1. MODULE DIAGNOSTIC")
        print("      • Vérifier services AD/DNS")
        print("      • Tester MySQL")
        print("      • Informations système")
        statut2 = "✓" if modules_disponibles.get('backup') else "✗"
        print(f"\n  [{statut2}] 2. MODULE SAUVEGARDE WMS")
        print("      • Sauvegarde complète base de données")
        statut3 = "✓" if modules_disponibles.get('obsolescence') else "✗"
        print(f"\n  [{statut3}] 3. MODULE AUDIT D'OBSOLESCENCE")
        print("      • Scanner réseau et audit EOL")
        print("\n  [0] QUITTER")
        print("\n" + "=" * 80)
    # ========== MODULE 1 : DIAGNOSTIC ==========
    def menu_diagnostic(self):
        if not modules_disponibles.get('diagnostic'):
            print("\n[!] Module diagnostic non disponible")
            input("\nAppuyez sur Entrée...")
            return
        while True:
            self.clear_screen()
            self.print_header()
            print("\n╔════════════════════════════════════════════════════════════════════════════╗")
            print("║                         MODULE DIAGNOSTIC                                  ║")
            print("╚════════════════════════════════════════════════════════════════════════════╝")
            print("\n  1. Vérifier services AD/DNS (Windows)")
            print("  2. Tester connexion MySQL")
            print("  3. Informations système")
            print("\n  0. Retour menu principal")
            print("\n" + "-" * 80)
            choix = input("\n→ Votre choix : ").strip()
            if choix == "1":
                diagnostic.verifier_ad_dns()
                input("\nAppuyez sur Entrée...")
            elif choix == "2":
                print("\n" + "=" * 80)
                host = input("→ IP serveur MySQL : ").strip()
                user = input("→ Utilisateur : ").strip()
                password = input("→ Mot de passe : ").strip()
                if host and user and password:
                    diagnostic.test_mysql_connection(host, user, password)
                else:
                    print("[!] Tous les champs requis")
                input("\nAppuyez sur Entrée...")
            elif choix == "3":
                diagnostic.get_system_info()
                input("\nAppuyez sur Entrée...")
            elif choix == "0":
                break
            else:
                print("\n[!] Choix invalide")
                input("\nAppuyez sur Entrée...")
    # ========== MODULE 2 : SAUVEGARDE ==========
    def menu_sauvegarde(self):
        if not modules_disponibles.get('backup'):
            print("\n[!] Module backup non disponible")
            input("\nAppuyez sur Entrée...")
            return
        while True:
            self.clear_screen()
            self.print_header()
            print("\n╔════════════════════════════════════════════════════════════════════════════╗")
            print("║                       MODULE SAUVEGARDE WMS                                ║")
            print("╚════════════════════════════════════════════════════════════════════════════╝")
            print("\n  1. Sauvegarde complète")
            print("\n  0. Retour menu principal")
            print("\n" + "-" * 80)
            choix = input("\n→ Votre choix : ").strip()
            if choix == "1":
                print("\n" + "=" * 80)
                confirm = input("→ Lancer la sauvegarde ? (o/n) : ").strip().lower()
                if confirm == 'o':
                    try:
                        backup.main()
                        print("\n[✓] Sauvegarde terminée")
                    except Exception as e:
                        print(f"\n[✗] Erreur : {e}")
                input("\nAppuyez sur Entrée...")
            elif choix == "0":
                break
            else:
                print("\n[!] Choix invalide")
                input("\nAppuyez sur Entrée...")
    # ========== MODULE 3 : OBSOLESCENCE ==========
    def menu_obsolescence(self):
        if not modules_disponibles.get('obsolescence'):
            print("\n[!] Module obsolescence_audit non disponible")
            input("\nAppuyez sur Entrée...")
            return
        obsolescence_audit.menu_principal()
    # ========== BOUCLE PRINCIPALE ==========
    def run(self):
        while True:
            self.print_menu_principal()
            choix = input("→ Votre choix : ").strip()
            if choix == "1":
                self.menu_diagnostic()
            elif choix == "2":
                self.menu_sauvegarde()
            elif choix == "3":
                self.menu_obsolescence()
            elif choix == "0":
                self.clear_screen()
                print("\n" + "=" * 80)
                print(f"  Merci d'avoir utilisé NTL-SysToolbox")
                print("=" * 80 + "\n")
                sys.exit(0)
            else:
                print("\n[!] Choix invalide")
                input("\nAppuyez sur Entrée...")
def main():
    try:
        if not any(modules_disponibles.values()):
            print("\n[ERREUR] Aucun module trouvé !")
            sys.exit(1)
        toolbox = NTLSysToolbox()
        toolbox.run()
    except KeyboardInterrupt:
        print("\n\n[*] Au revoir !")
        sys.exit(0)
if __name__ == "__main__":
    main()