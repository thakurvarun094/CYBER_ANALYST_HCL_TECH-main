# File-Integrity Verification Dashboard
**Cyber Analyst Project | HCL Internship Submission**


**Institution:** ABES Engineering College  
**Scan Date:** 2026-11-22  
**Repository:** [https://github.com/thakurvarun094/CYBER_ANALYST_HCL_TECH.git]

---

## 📌 Project Overview
The **File-Integrity Verification Dashboard** is an enterprise-grade cybersecurity monitoring solution designed to detect unauthorized modifications, deletions, and file tampering across critical system paths. 

Using baseline cryptographic hash comparisons (SHA-256 prefixes) alongside change approval reconciliation, this project distinguishes legitimate, authorized operational changes from malicious adversary techniques such as unauthorized configuration tampering, persistence mechanisms, and remote code execution (RCE).

> **Key Security Insight:**  
> *Hash comparison shows THAT a file changed, not WHETHER it is bad — match each change to approved change records.*

---

## 📂 Project Structure
```text
CYBER_PROJECT/
├── dashboard/
│   └── index.html             # Standalone interactive dark-mode FIM dashboard (Chart.js)
├── dataset/
│   ├── fim_results.csv        # FIM scan records (CSV)
│   └── fim_results.json       # Structured scan records (JSON)
├── screenshots/
│   ├── dashboard_full.png     # Full-page screenshot of the dashboard
│   ├── dashboard_charts.png   # Cropped view of Status and Risk charts
│   └── dashboard_table.png    # Cropped view of detailed audit table
├── video/
│   ├── project_walkthrough.mp4  # High-definition video demonstration of the dashboard
│   └── project_walkthrough.webm # WebM recording format
├── Project_Submission.pdf     # Consolidated formal project submission report
└── README.md                  # Project documentation
```

---

## 📊 Summary of FIM Findings
- **Total Monitored Files:** 7
- **OK (Unmodified / Baseline Intact):** 2 files
- **MODIFIED:** 3 files (1 Approved change `CHG-101`, 1 Unapproved config change, 1 Malicious RCE script)
- **DELETED:** 1 file (`db.conf` - potential evasion or tampering)
- **ADDED:** 1 file (`.hidden_update.sh` - stealth persistence / reverse shell)
- **High-Risk Critical Alerts:** 2 (`backup.sh` injected curl-bash RCE, `.hidden_update.sh` backdoor)

---

## 🚀 How to Open and View the Dashboard
1. Clone or download this repository.
2. Navigate to the `dashboard/` directory.
3. Open `index.html` directly in any modern web browser (Google Chrome, Microsoft Edge, Firefox, etc.).
   ```bash
   # On Windows (PowerShell):
   Start-Process ./dashboard/index.html
   ```
4. The dashboard is fully self-contained and loads styled KPI metrics, Chart.js donut and bar visualizations, and a detailed audit breakdown.

---

## 📜 Formal Submission PDF
The comprehensive final project document is available as `Project_Submission.pdf` in the root of the repository, containing:
1. Formal title page with institutional credentials.
2. Complete dataset audit table with security analysis and baseline hash tracking.
3. Full dashboard UI visual captures.
4. Repository reference links.
