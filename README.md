# AppSec & DevSecOps Security Automation Lab

This repository contains a hands-on **Application Security (AppSec) & DevSecOps Lab** built in Python. The project demonstrates the lifecycle of identifying, exploiting, and remediating classic web application vulnerabilities (aligned with the OWASP Top 10) using both automated security tools and custom exploit scripts.

## Tech Stack & Security Tools
* **Core Application:** Python, Flask, SQLite
* **SAST (Static Analysis):** Semgrep
* **DAST (Dynamic Analysis):** OWASP ZAP (Zed Attack Proxy)
* **Exploitation & Automation:** Python `requests`, custom test runner (`run_dast.py`)

---

## Lab Features & Vulnerability Coverage

### 1. SQL Injection (SQLi)
* **Vulnerability:** Unsafe SQL queries constructed via Python f-strings, allowing authentication bypass on the login page.
* **Exploit:** `admin' --` payload injected into the username field to comment out the password check.
* **Remediation:** Migrated database queries to use parameterized statements (`?` placeholders).

### 2. Cross-Site Scripting (XSS)
* **Vulnerability:** Reflected XSS on the search page caused by direct concatenation of raw URL query parameters into the HTML response.
* **Exploit:** Injecting HTML/JavaScript payloads (e.g. `<h1>` or `<script>`) directly into the URL parameters.
* **Remediation:** Configured Flask's Jinja2 template engine to auto-escape user input (`{{ query }}`).

### 3. Insecure Direct Object Reference (IDOR)
* **Vulnerability:** Exposure of internal database user IDs in profile URLs (`/profile?id=1`) without session authorization checks.
* **Exploit:** Directly editing the user ID parameter to access other users' private profile details and credentials.
* **Remediation:** Implemented Flask-session state tracking and enforced role-based and owner-based authorization checks.

---

## How to Set Up and Run

### 1. Installation
Clone the repository and install dependencies inside a Python virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1   # On Windows
pip install -r requirements.txt
```

### 2. Start the Target Web Application
```bash
python app.py
```
The server will start locally at `http://127.0.0.1:5000/`.

---

## How to Run Security Scans

### 1. Static Code Analysis (SAST)
We use **Semgrep** to scan the source code for insecure design patterns:
```bash
semgrep scan --config auto
```

### 2. Automated Exploit & Regression Suite (DAST)
We built a custom automated DAST suite to verify vulnerabilities and test patches. Run the test runner:
```bash
python exploits/run_dast.py
```
