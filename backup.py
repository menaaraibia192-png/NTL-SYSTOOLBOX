import subprocess
from datetime import datetime
import os
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
DB_NAME = "wms_db"
def main():
    backup_dir = os.path.join(os.path.dirname(__file__), "backups")
    os.makedirs(backup_dir, exist_ok=True)
    date = datetime.now().strftime("%Y-%m-%d_%H-%M")
    try:
        # SQL dump
        sql = os.path.join(backup_dir, f"wms_{date}.sql")
        subprocess.run(["mysqldump", "-u", MYSQL_USER, f"-p{MYSQL_PASSWORD}", DB_NAME],
                      stdout=open(sql, "w"), stderr=subprocess.PIPE, check=True)
        print(f"✅ SQL: {os.path.basename(sql)}")
        # CSV orders
        csv1 = os.path.join(backup_dir, f"orders_{date}.csv")
        subprocess.run(["mysql", "-u", MYSQL_USER, f"-p{MYSQL_PASSWORD}", DB_NAME, 
                       "-e", "SELECT * FROM orders"],
                      stdout=open(csv1, "w"), stderr=subprocess.PIPE, check=True)
        print(f"✅ CSV: {os.path.basename(csv1)}")
        # CSV products
        csv2 = os.path.join(backup_dir, f"products_{date}.csv")
        subprocess.run(["mysql", "-u", MYSQL_USER, f"-p{MYSQL_PASSWORD}", DB_NAME, 
                       "-e", "SELECT * FROM products"],
                      stdout=open(csv2, "w"), stderr=subprocess.PIPE, check=True)
        print(f"✅ CSV: {os.path.basename(csv2)}")
        return {"success": True}
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return {"success": False, "error": str(e)}
def dump_database(host, user, password, database):
    """Fonction wrapper pour compatibilité avec le menu"""
    global MYSQL_USER, MYSQL_PASSWORD, DB_NAME
    MYSQL_USER = user
    MYSQL_PASSWORD = password
    DB_NAME = database
    return main()
if __name__ == "__main__":
    main()