# SnowGuard AML Copilot
## Autonomous Risk, Fraud, & Regulatory Intelligence Copilot • Powered by Snowflake Cortex

SnowGuard AML Copilot is an enterprise-grade Streamlit application designed for compliance investigators, risk teams, and financial crime auditors. Built for the Snowflake Hackathon (Risk, Fraud, and Regulatory Intelligence Copilot track), it accelerates alert triage, isolates sub-threshold structuring patterns, verifies FinCEN regulatory requirements, and synthesizes audit-ready Suspicious Activity Reports (Form SAR-1020).

The application features a hybrid resilience architecture: it queries Snowflake Cortex LLM (llama3.1-8b) live via native SQL functions when connected, and falls back seamlessly to an internal deterministic compliance engine if offline.

## Key Capabilities

- 🚨 Active Alert Queue & Suspect Triage: Instant multi-account triage across high-risk typologies including smurfing, commercial shell layering, and branch hopping.  
- 🧠 Snowflake Cortex Autonomous Copilot: Live conversational investigative agent powered by SNOWFLAKE.CORTEX.COMPLETE running llama3.1-8b to reason across transactional logs  and FinCEN statutes.  
- 🛡️ Hardened Compliance Guardrail Filter: Employs defensive legal framing and refusal-interceptor logic to eliminate LLM safety false positives on legitimate regulatory queries.  
- 📊 Dual-Engine Connectivity: Compatible with native Streamlit in Snowflake (SiS) via get_active_session(), direct local connector driver (snowflake-connector-python), and st.connection("snowflake").  
- ⚡ Live Status Telemetry: Dynamic header and sidebar status indicators providing real-time engine visibility (● ONLINE / ● OFFLINE).  
- 📁 Form SAR-1020 Dossier Compiler: Compiles complete, FinCEN-compliant Suspicious Activity Reports with subject profiles, transaction audit tables, and legal narrative justifications ready for Markdown export.

## System Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                 Streamlit Presentation Layer                │
│       Alert Queue  •  Cortex Copilot  •  SAR Dossier        │
└──────────────┬───────────────────────────────┬──────────────┘
               │                               │
      [Cortex LLM Pipeline]            [Data & Fallback]
               ▼                               ▼
┌─────────────────────────────┐ ┌─────────────────────────────┐
│  Snowflake Cortex Engine    │ │  Synthetic Compliance Core  │
│  - llama3.1-8b Completion   │ │  - Deterministic Math Engine│
│  - Automated SQL Ingestion  │ │  - Statutory Rules Cache    │
│  - Guardrail Interception   │ │  - Zero-Fail Mock Ledger    │
└──────────────┬──────────────┘ └──────────────┬──────────────┘
               │                               │
               └───────────────┬───────────────┘
                               ▼
               ┌───────────────────────────────┐
               │    Unified Snowflake Engine   │
               │   Snowpark / Connector Driver │
               │     RISK_DB.AML_CORE Schema   │
               └───────────────────────────────┘
```

## Highlighted Investigation Scenarios

The copilot includes three pre-loaded, high-priority audit typologies:  
1. James Sterling (ACC_1042) — Personal Checking  
    - Typology: Smurfing / Structured Cash Evasion + Cayman Layering.  
    - Pattern: 4 cash deposits under the $10,000 threshold within 42 hours ($38,020 total) followed by an immediate $37,500 outbound international wire to a Cayman Islands entity.  
    - Governing Rule: 31 CFR § 1010.314 (Structuring Transactions to Evade CTR Reporting).  
2. Apex Shell Holdings Ltd (ACC_1085) — Business Checking  
    - Typology: Commercial Velocity Structuring & Outbound Offshore Sweep.  
    - Pattern: Rapid ACH aggregation totaling $39,760 from shell counter-parties over 48 hours, immediately funneled into an outbound cross-border wire to Banco Panama
    - Governing Rule: 31 CFR § 1020.320 (Reports by Banks of Suspicious Transactions).  
3. Marcus Vance (ACC_1102) — Personal Savings  
    - Typology: Same-Day Branch Hopping & Velocity Layering.  
    - Pattern: 3 sequential cash deposits executed across different branch locations within 4 hours ($26,500 aggregate) to evade single-teller CTR scrutiny.  
    - Governing Rule: 31 CFR § 1010.314 (Aggregated Branch Structuring).  


## Getting Started

### Prerequisites
- Python: Standard 64-bit installer (Python 3.10 or Python 3.11 from python.org).
- **Note for Windows users:** Avoid the Windows Store sandboxed package (WindowsApps) to prevent reparse-point and socket initialization errors.

### 1. Clone & Set Up Environment

```bash
git clone https://github.com/your-org/snowguard-aml.git
cd snowguard-aml

# Recommended: Python 3.11 virtual environment
py -3.11 -m venv venv
venv\Scripts\activate  # On macOS/Linux: source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Launch Application (Standalone Demo Mode)

Without Snowflake credentials, SnowGuard starts immediately in Standalone Zero-Fail Mode:

```bash
streamlit run app/streamlit_app.py
```

## Snowflake Connection Setup (Live Online Mode)

To enable live Snowflake Cortex LLM reasoning and direct warehouse querying:
1. Create a secrets file at .streamlit/secrets.toml:
```bash
mkdir .streamlit
touch .streamlit/secrets.toml
```

2. Add your Snowflake connection parameters:

```toml
[connections.snowflake]
account = "YOUR_ACCOUNT"
user = "YOUR_USERNAME"
password = "YOUR_PASSWORD"
role = "YOUR_ROLE"
warehouse = "AML_WH"
database = "RISK_DB"
schema = "AML_CORE"
```
Do not commit this file or expose credentials in source control. The app expects the `ACCOUNTS` and `TRANSACTIONS` tables in `RISK_DB.AML_CORE`.

3. Re-launch Streamlit:
```bash
streamlit run app/streamlit_app.py
```

## Repository Structure

```text
snowguard-aml/
├── .streamlit/
│   └── secrets.toml              # Snowflake connection credentials (local)
├── app/
│   └── streamlit_app.py          # Primary Streamlit application & Cortex copilot
├── data/
│   ├── accounts.csv              # Synthetic account profiles
│   ├── generate_synthetic_data.py# Generator script for AML transaction ledger
│   └── transactions.csv          # Raw ledger records
├── docs/
│   └── fincen_aml_guidelines.md  # FinCEN & BSA reference documentation
├── semantic_model/
│   └── aml_semantic_model.yaml   # Cortex Analyst semantic definitions
├── skills/
│   ├── skill_1_triage.md         # Copilot triage specifications
│   ├── skill_2_policy_check.md   # BSA/FinCEN statutory rules
│   └── skill_sar_dossier.md      # SAR narrative assembly templates
├── requirements.txt              # Production dependency specifications
└── README.md
```

## Regulatory Disclaimer

This application is a software prototype developed for hackathon and demonstration purposes. The accounts, transactions, and scenarios are entirely synthetic. Generated SAR filings and statutory assessments are for testing and evaluation only, do not constitute legal advice, and do not submit live filings to FinCEN or law enforcement. Production deployments require review by qualified compliance and legal personnel.
