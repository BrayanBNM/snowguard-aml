# 🛡️ SnowGuard AML — Autonomous Risk, Fraud, & Regulatory Intelligence Copilot

Representing the enterprise **Global Capability Center (Vonage India)** at the **Snowflake CoCo CLI Hackathon - GCC Edition**.

---

## 📌 Project Overview
- **Project Name:** SnowGuard AML
- **Track:** Track 1 — Risk, Fraud, and Regulatory Intelligence Copilot
- **Target:** Autonomous, audit-ready regulatory reporting (AML, FinCEN 31 CFR § 1010.314) and real-time smurfing/structuring fraud triage using Snowflake native capabilities.

SnowGuard AML combines structured ledger analysis with unstructured regulatory search into an automated agent harness, providing compliance officers with a three-pane conversational workspace that automatically compiles audit-ready Suspicious Activity Reports (SAR).

---

## 🏛️ System Architecture

1. **Structured Data Engine (Cortex Analyst):** Querying financial transaction ledgers and customer tables. Powered by a Semantic View YAML with pre-defined Verified Queries to ensure absolute mathematical precision and prevent LLM hallucinations.
2. **Unstructured Policy Engine (Cortex Search):** A managed semantic RAG vector engine indexing Bank Secrecy Act and FinCEN regulatory guidelines stored on a secure Snowflake internal stage.
3. **Procedural Memory & Orchestration:** Governed by Snowflake CoCo CLI skills (`skill_*.md`), maintaining a persistent and auditable reasoning trace for compliance review.
4. **User Interface:** Streamlit in Snowflake (SiS) with a high-fidelity 3-pane layout including:
   - **Left Pane:** Real-time Alert Triage Queue.
   - **Center Pane:** Interactive Conversational Triage Canvas (Cortex Copilot Chat & Transaction Ledger).
   - **Right Pane:** Live, dynamically compiled, and exportable regulatory SAR Dossier.

---

## 📂 Project Directory Structure

Our workspace matches the following deployment-ready layout:
```text
snowguard-aml/
├── data/
│   ├── generate_synthetic_data.py   # Standard-library generator with seed-based reproducibility
│   ├── accounts.csv                 # 52 customer account registry containing risk scores and tiers
│   └── transactions.csv             # 852 historical transaction logs containing complex fraud patterns
├── docs/
│   └── fincen_aml_guidelines.md     # Reference statutory text on structuring regulations (31 CFR § 1010.314)
├── semantic_model/
│   └── aml_semantic_model.yaml      # Cortex Analyst YAML model containing verified SQL patterns
├── skills/
│   ├── skill_1_triage.md            # CoCo CLI skill: Structured Transaction Ledger Triage
│   ├── skill_2_policy_check.md      # CoCo CLI skill: Unstructured Regulatory & Policy Check
│   └── skill_sar_dossier.md         # CoCo CLI skill: Suspicious Activity Report Dossier Compiler
├── app/
│   └── streamlit_app.py             # Streamlit App ready for Streamlit in Snowflake (SiS)
└── README.md                        # Documentation and architecture breakdown (This file)
```

---

## 🔍 Injected Structuring Patterns (Synthetic Data Ledger)
Our synthetic data ledger comprises **52 customer accounts** and **852 historical transaction logs**, carefully injected with three complex structuring (smurfing/layering) fraud patterns designed to test our Copilot's detection precision:

1. **James Sterling (ACC_1042):**
   - **Behavior:** Classic Smurfing / Structuring.
   - **Pattern:** Receives 4 separate cash deposits between $9,000 and $9,950 within a 42-hour window (summing to $38,020), which avoids individual triggering of the $10,000 Currency Transaction Report (CTR). This is immediately followed by an outbound wire transfer of $37,500 to a recognized secrecy shell account in the **Cayman Islands (`KY`)**.
2. **Apex Shell Holdings Ltd (ACC_1085):**
   - **Behavior:** Corporate Sub-Threshold Structuring.
   - **Pattern:** Receives 4 daily ACH/check deposits ranging between $9,910 and $9,980. Immediately aggregates and transfers $39,500 out via wire transfer to a corporate registry in **Panama (`PA`)**.
3. **Marcus Vance (ACC_1102):**
   - **Behavior:** Rapid Cash-in Cash-out Layering.
   - **Pattern:** Receives 3 large physical cash deposits (totaling $29,500) within 5 hours, followed immediately by a cash withdrawal of $29,000 inside the 6th hour.

---

## 💻 Local Execution Instructions

To execute this project locally and explore the high-fidelity Streamlit AML Copilot, follow these commands:

### 1. Generate Synthetic Datasets
Ensure your local Python environment is available, then run:
```bash
python E:\snowguard-aml\data\generate_synthetic_data.py
```
This produces `accounts.csv` and `transactions.csv` in your `data/` folder.

### 2. Run the Streamlit Application
Install Streamlit and Pandas (if not already installed), then run:
```bash
pip install streamlit pandas
streamlit run E:\snowguard-aml\app\streamlit_app.py
```
The browser will automatically open the dashboard at `http://localhost:8501`.

---

## ❄️ Snowflake Deployment Pathway

Transitioning this repository to Snowflake Native capabilities is straightforward:

1. **Table Load:** Create `ACCOUNTS` and `TRANSACTIONS` tables inside a Snowflake Database, and copy the CSV datasets in using standard SQL `COPY INTO` commands.
2. **Cortex Analyst:** Upload `aml_semantic_model.yaml` to an internal Snowflake stage, and configure a Cortex Analyst REST API instance referencing this stage.
3. **Cortex Search:** Create an internal stage named `@AML_STAGE`, upload `fincen_aml_guidelines.md` to it, and initialize a Cortex Search service:
   ```sql
   CREATE OR REPLACE CORTEX SEARCH SERVICE fincen_policy_search
     ON file_content
     ATTRIBUTES (relative_path)
     WAREHOUSE = aml_warehouse
     TARGET_STAGE = @AML_STAGE;
   ```
4. **Streamlit in Snowflake (SiS):** Create a new Streamlit app directly inside the Snowflake Snowsight UI and paste the code from `streamlit_app.py`. Modify the data loaders to use `snowflake.snowpark` session queries instead of local `pd.read_csv`, enabling native access to Cortex APIs.
5. **Agent Orchestration (Tasks):** Schedule monthly evaluations using Snowflake Tasks to trigger automated triage pipelines using the skills documented in `/skills/`.
