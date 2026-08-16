# Cybersecurity Automation Portfolio Lab

This repository contains a collection of hands-on cybersecurity projects built in Python, showcasing both application security (defensive patching & CI/CD auditing) and network security (traffic sniffing & analysis) skills.

---

## 🛡️ Project 1: AppSec & DevSecOps Security Automation Lab
A project demonstrating the lifecycle of identifying, exploiting, and remediating classic web application vulnerabilities (aligned with the OWASP Top 10) using both automated security tools and custom exploit scripts.

### Tech Stack & Security Tools
* **Core Application:** Python, Flask, SQLite
* **SAST (Static Analysis):** Semgrep
* **DAST (Dynamic Analysis):** OWASP ZAP (Zed Attack Proxy)
* **Exploitation & Automation:** Python `requests`, custom test runner (`run_dast.py`)

### Vulnerability Coverage & Remediation
1. **SQL Injection (SQLi):** Fixed by migrating raw string-formatted SQL queries to parameterized queries (`?` placeholders).
2. **Cross-Site Scripting (XSS):** Fixed by routing user search queries through Flask's Jinja2 template auto-escaping (`{{ query }}`).
3. **Insecure Direct Object Reference (IDOR):** Secured by implementing Flask-session tracking and enforcing ownership-based authorization checks on profile pages.

---

## 🔌 Project 2: Network Sniffer & Packet Analyzer
A low-level networking tool built to capture, dissect, and audit network traffic in real-time, showcasing how unencrypted protocols expose sensitive credentials.

### Tech Stack & Drivers
* **Language:** Python 3
* **Libraries:** `scapy` (for packet capture and dissection)
* **Underlying Drivers:** Npcap (packet capture library for Windows)

### Capabilities
1. **Multi-Protocol Decoding:** Parses network packets to extract layer details including Source/Destination IP addresses and Port numbers (TCP, UDP, ICMPv6).
2. **Plaintext Credential Auditing:** Extracts and decodes raw payloads (`Raw` layer) to search for insecure patterns (like `username=` or `password=`).
3. **Security Alerts:** Automatically triggers a terminal security warning banner showing the exact unencrypted credentials intercepted on the wire when logging into HTTP sites.

---

## How to Set Up and Run

### 1. Installation
Clone the repository and install dependencies inside a Python virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1   # On Windows
pip install -r requirements.txt
pip install -r network_sniffer/requirements.txt
```

### 2. Run the AppSec Lab
```bash
python app.py
```
* Visit the login page: `http://127.0.0.1:5000/login`
* Run the automated exploit suite: `python exploits/run_dast.py`

### 3. Run the Network Sniffer
*(Requires running the console as Administrator)*
```bash
python network_sniffer/sniffer.py
```
Submit a login attempt on `http://127.0.0.1:5000/login` to see the sniffer capture your credentials in plaintext over the wire!
