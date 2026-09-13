# SnowGuard AML

SnowGuard AML is a Streamlit prototype for anti-money-laundering (AML) alert triage, structured transaction analysis, policy review, and SAR dossier generation. It was created for the Snowflake Hackathon's Risk, Fraud, and Regulatory Intelligence Copilot track.

> **Prototype notice:** This project uses synthetic data. The generated dossier and the "Approve & File Regulatory SAR" button are demonstration outputs and do not submit a filing to FinCEN.

## Features

- Alert queue for three synthetic high-risk accounts.
- Transaction ledger inspection with Snowflake-backed data when a connection is available.
- Offline demo mode with built-in mock transactions when Snowflake is unavailable.
- Structuring and layering analysis against sub-threshold transactions.
- Policy-review response referencing 31 CFR Sections 1010.314 and 1020.320.
- Optional Snowflake Cortex completion for free-form chat queries.
- SAR-style Markdown dossier preview and download.

## Architecture

1. **Streamlit application:** Provides the alert queue, investigation workspace, transaction ledger, and SAR dossier views.
2. **Structured data:** Reads `RISK_DB.AML_CORE.TRANSACTIONS` when a Snowflake session is available. The repository also includes CSV data for the synthetic dataset.
3. **Semantic model:** `semantic_model/aml_semantic_model.yaml` describes the `ACCOUNTS` and `TRANSACTIONS` tables and includes example structuring and layering queries.
4. **Cortex integration:** When running with a Snowflake session, free-form chat uses `SNOWFLAKE.CORTEX.COMPLETE` with `mistral-large2`. The quick policy action is a local demonstration response; it does not currently query a Cortex Search service.

## Synthetic scenarios

The generator creates 52 account profiles and a synthetic transaction ledger. The three highlighted cases are:

1. **James Sterling (`ACC_1042`) - cash structuring:** Four cash deposits between $9,000 and $10,000 over approximately 42 hours, totaling $38,020, followed by a $37,500 wire to a Cayman Islands counterparty.
2. **Apex Shell Holdings Ltd (`ACC_1085`) - commercial structuring:** Four daily ACH deposits totaling $39,760, followed by a $39,500 wire to Panama.
3. **Marcus Vance (`ACC_1102`) - rapid cash layering:** Three cash deposits totaling $29,500 within five hours, followed by a $29,000 cash withdrawal.

The checked-in `data/transactions.csv` contains the generated ledger used by the prototype. Run the generator to recreate the data if needed.

## Run locally

### 1. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Start the app

```bash
streamlit run app/streamlit_app.py
```

Without Snowflake credentials, the app starts in standalone demo mode using its built-in mock transactions.

## Optional Snowflake connection

For a local Snowflake connection, create `.streamlit/secrets.toml` and provide the credentials supported by your Streamlit Snowflake connection:

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

## Repository layout

```text
snowguard-aml/
├── app/
│   └── streamlit_app.py
├── data/
│   ├── accounts.csv
│   ├── generate_synthetic_data.py
│   └── transactions.csv
├── docs/
│   └── fincen_aml_guidelines.md
├── semantic_model/
│   └── aml_semantic_model.yaml
├── skills/
│   ├── skill_1_triage.md
│   ├── skill_2_policy_check.md
│   └── skill_sar_dossier.md
├── requirements.txt
└── README.md
```

## Regulatory disclaimer

The statutory references and generated narratives are provided for demonstration and testing only. They are not legal advice, do not establish that activity is reportable, and must be reviewed by a qualified compliance professional before use in a real AML program.
