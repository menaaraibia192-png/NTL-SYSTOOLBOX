
## 📋 Description

NTL-SysToolbox is an integrated command-line utility designed for NordTransit Logistics' IT team to:

✅ **Diagnose** critical infrastructure services (AD/DNS, MySQL, system health)  
✅ **Automate** warehouse management system (WMS) database backups  
✅ **Audit** end-of-life (EOL) status across the IT infrastructure

**Context:** SME logistics company with 4-person IT team, 240+ employees, 24/7 operations requiring minimal maintenance windows.

---

## 🚀 Quick Start

### Prerequisites

- **Python** 3.8+ (tested with 3.14.2)
- **MySQL Client** (for backup module)
- **Administrator rights** (for AD/DNS checks on Windows)

### Installation

```bash
# Clone repository
git clone https://github.com/your-org/NTL-SysToolbox.git
cd NTL-SysToolbox

# Install dependencies
pip install -r requirements.txt

# Run
python main.py
```

### First Run

```
════════════════════════════════════════════════════════════════════════════════
  NTL-SYSTOOLBOX v1.0.0 - NordTransit Logistics
════════════════════════════════════════════════════════════════════════════════

  [✓] 1. MODULE DIAGNOSTIC
  [✓] 2. MODULE SAUVEGARDE WMS
  [✓] 3. MODULE AUDIT D'OBSOLESCENCE
  [0] QUITTER

→ Your choice: _
```

---

## 📦 Repository Structure

```
NTL-SysToolbox/
│
├── main.py                          # CLI entry point with interactive menu
├── diagnostic.py                    # Module 1: Infrastructure diagnostics
├── backup.py                        # Module 2: WMS database backup
├── obsolescence_audit.py            # Module 3: EOL audit
│
├── inventaire_ntl.csv               # Network inventory (input data)
├── requirements.txt                 # Python dependencies
├── README.md                        # This file
│
├── backups/                         # Auto-created backup directory
├── docs/                            # Technical documentation
│   ├── Dossier_Technique.pdf
│   ├── Manuel_Installation.pdf
│   └── Rapport_Audit_Reference.txt
│
└── examples/                        # Sample outputs
    ├── ad_dns_result.json
    ├── mysql_result.json
    └── rapport_obsolescence_sample.txt
```

---

## 🔧 Modules Overview

### 1. Diagnostic Module (`diagnostic.py`)

**Purpose:** Verify operational status of critical services at headquarters.

**Features:**
- ✅ Active Directory / DNS services check (Windows only)
- ✅ MySQL WMS database connectivity test
- ✅ System metrics (CPU, RAM, disk, uptime) - Windows & Linux

**Outputs:** JSON files with structured data + return codes (0=OK, 1=FAIL)

**Example:**
```bash
# Via menu: 1 → 2 (Test MySQL)
→ MySQL host: 192.168.10.21
→ User: root
→ Password: ****

✔ MySQL connection successful
📄 JSON saved: mysql_result.json
```

---

### 2. Backup Module (`backup.py`)

**Purpose:** Ensure existence, integrity, and traceability of WMS database exports.

**Features:**
- ✅ Full SQL dump (`mysqldump`)
- ✅ CSV export of critical tables (orders, products)
- ✅ Timestamped files (ISO 8601 format)

**Outputs:** `backups/` directory with SQL + CSV files

**Example:**
```bash
# Via menu: 2 → 1 (Full backup)
→ Start backup? (y/n): y

✅ SQL: wms_2026-01-04_14-30.sql
✅ CSV: orders_2026-01-04_14-30.csv
✅ CSV: products_2026-01-04_14-30.csv

[✓] Backup completed
```

---

### 3. EOL Audit Module (`obsolescence_audit.py`)

**Purpose:** Identify systems approaching/past end-of-support to prioritize upgrades.

**Features:**
- ✅ Load network inventory from CSV
- ✅ Filter by network range (CIDR, range, single IP)
- ✅ EOL status calculation (UNSUPPORTED, SOON, SUPPORTED, UNKNOWN)
- ✅ Dual-format reports (JSON + human-readable TXT)

**EOL Database:** Built-in (Windows Server, Ubuntu, CentOS, VMware ESXi) - updated Dec 2024

**Example:**
```bash
# Via menu: 3 → 4 (Generate full report)

[+] JSON report: rapport_obsolescence_2026-01-04_14-35-12.json
[+] TXT report: rapport_obsolescence_2026-01-04_14-35-12.txt

STATISTICS:
- UNSUPPORTED: 3 (URGENT ACTION REQUIRED)
- SOON: 2 (PLAN Q1-Q2 2026)
- SUPPORTED: 4
- UNKNOWN: 2 (MANUAL AUDIT NEEDED)
```

---

## 🛠️ Configuration

### MySQL Credentials (backup module)

Edit `backup.py` lines 5-7:

```python
MYSQL_USER = "root"              # ← Change if different
MYSQL_PASSWORD = "root"          # ← Change if different
DB_NAME = "wms_db"               # ← Change if different
```


## 📊 Sample Outputs

### Diagnostic JSON (mysql_result.json)

```json
{
  "test": "mysql",
  "timestamp": "2026-01-04-14-30-25",
  "host": "192.168.10.21",
  "status": "success",
  "return_code": 0
}
```

### EOL Audit Report (excerpt)

```
================================================================================
UNSUPPORTED COMPONENTS (URGENT)
================================================================================

• Hyperviseur-Lille
  IP: 192.168.10.5
  OS: VMware ESXi 6.5
  EOL: 2022-10-15
  RISK: No vendor support, unpatched vulnerabilities
  ACTION: Migrate to ESXi 7.0+ (Q1 2026)

• PC-Quai-WH1-01
  IP: 192.168.20.101
  OS: Windows 7
  EOL: 2020-01-14
  RISK: Critical security exposure (EternalBlue, BlueKeep)
  ACTION: Replace hardware + Windows 11 (URGENT)
```

---

## 🧪 Testing

### Unit Tests Performed

**Diagnostic:**
- ✅ AD/DNS check on Windows Server 2019
- ✅ MySQL connection to WMS-DB (192.168.10.21)
- ✅ System metrics on Windows 11 & Ubuntu 20.04

**Backup:**
- ✅ Full SQL dump (5 tables, 10 records)
- ✅ CSV exports (orders, products)
- ✅ Restore test (`mysql < backup.sql`)

**Audit:**
- ✅ CSV inventory load (11 components)
- ✅ Network filtering (CIDR, range, single IP)
- ✅ EOL status calculation (3 UNSUPPORTED, 2 SOON)
- ✅ Report generation (JSON + TXT)



---

## 🌍 Internationalization

### English Summary

**NTL-SysToolbox** is a Python-based CLI utility developed for NordTransit Logistics, a French logistics SME operating a headquarters and 3 warehouses in Hauts-de-France region.

**Context:** 240+ employees, 24/7 warehouse operations, 4-person IT team with tight maintenance windows (night-only interventions).

**Objectives:**
1. **Rapid diagnostics** of critical services (AD/DNS, MySQL WMS) to minimize downtime
2. **Automated backups** of the warehouse management system database (zero data loss tolerance)
3. **EOL audit** to anticipate end-of-support systems and prioritize upgrades

**Key Features:**
- ✅ Modular architecture (3 independent modules)
- ✅ Cross-platform (Windows/Linux)
- ✅ Structured outputs (JSON) for monitoring integration (Zabbix)
- ✅ Human-readable reports (TXT) for management
- ✅ Interactive CLI menu (no prior knowledge required)

**Technical Stack:**
- Python 3.14.2
- Libraries: `psutil`, `mysql-connector-python`
- Tools: `mysqldump`, Windows `sc.exe`

**Deliverables:**
- ✅ Source code (Git repository)
- ✅ Technical & functional documentation
- ✅ Installation & user manual
- ✅ Reference EOL audit execution

**Business Value:**
- **Time savings:** 15min → 2min for infrastructure diagnostics
- **Zero backup omissions:** Automated nightly tasks
- **Proactive planning:** 6-12 months visibility on obsolescence

**Deployment Status:** Production-ready (January 2026)

---

## 🚧 Roadmap

### Version 1.1 (Q1 2026)

- [ ] Externalize credentials (`.env` file + `python-dotenv`)
- [ ] Backup rotation (auto-delete > 30 days)
- [ ] Integrity verification (SHA256 checksums)
- [ ] Centralized logging (Syslog/Zabbix)

### Version 2.0 (Q3-Q4 2026)

- [ ] REST API mode (Zabbix integration)
- [ ] Automatic network scan (replace CSV with Nmap)
- [ ] Enhanced OS detection (SSH/RDP bannering)
- [ ] Backup encryption (GPG)
- [ ] Email alerting (critical components unsupported)

---

## 🤝 Contributing

**Project Team:**
- Araibia Menat Allah
- Kacou Murielle
- Khorchaly Oussama
- Djaaloul Bilal

**Contact:** mena.araibia192@gmail.com

**Contribution Guidelines:**
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-module`)
3. Commit changes (`git commit -m 'Add new diagnostic check'`)
4. Push to branch (`git push origin feature/new-module`)
5. Open a Pull Request

---



## 🏆 Acknowledgments

**Client:** NordTransit Logistics (NTL)  
**Academic Program:** Administrateur Systèmes, Réseaux et Bases de Données (ASRBD)  
**Evaluation Block:** E6.1 - Concevoir et tester des solutions applicatives  
**Submission Date:** January 5, 2026  
**Oral Defense:** January 9, 2026
---

## 📞 Support & Contact

**Issues:** [GitHub Issues](https://github.com/your-org/NTL-SysToolbox/issues)  
**Email:** mena.araibia192@gmail.com 
**Documentation:** `/docs` directory in repository

---

**Built with ❤️ for NordTransit Logistics IT Team**