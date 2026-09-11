# Skill: Suspicious Activity Report (SAR) Dossier Compiler

## Objective
Automatically compile an audit-ready, legally citeable Suspicious Activity Report (SAR) dossier that incorporates structured transactional history, automated policy verification, and a high-fidelity narrative.

## Dossier Output Structure

### I. SAR Reference Details
- **Filing Date:** [System Date]
- **Filing Institution:** SnowGuard AML Intelligence Engine (GCC Core)
- **Primary Violation Category:** Structuring / Transaction evasion (31 CFR § 1010.314)
- **Filing Threshold Category:** Suspicious Activity > $5,000 with suspicious intent

### II. Suspect Profile
- **Account ID:** [Account Number]
- **Customer Name:** [Customer Legal Name / Entity]
- **Account Type:** [Checking / Savings / Business Checking]
- **Customer Risk Score:** [Risk Score / 1.00]
- **Customer Country:** [Country of Domicile]

### III. Structured Transaction Audit Log
*(Chronologically ordered list of structured transactions)*
| Transaction ID | Timestamp | Type | Method | Amount (USD) | Counterparty Account | Counterparty Country |
|----------------|-----------|------|--------|--------------|----------------------|----------------------|
| [TXN_ID]       | [Time]    | [Type]| [Method]| $[Amount]   | [Counterparty]       | [Country]            |

### IV. Policy Reference & Red Flag Alignment
- **Statutory Violation:** 31 CFR § 1010.314 (Evading Currency Transaction Reports)
- **Statutory Guidance Source:** FinCEN Bank Secrecy Act Regulations
- **Triggered Red Flag Checklist:**
  - [x] Sub-threshold Cash Deposits ($9,000 - $9,990)
  - [x] High-frequency Clustering (within 48-72 hours)
  - [x] Rapid Consolidating Wire Outflows (Layering)
  - [x] High-Risk Jurisdiction Ingress/Egress (Cayman Islands, Panama, Switzerland)

### V. SAR Narrative (Filing Packet)
"Between **[Start Date]** and **[End Date]**, the account of **[Customer Name]** (Account ID: **[Account ID]**) exhibited highly suspicious cash structuring and layering patterns that strongly indicate an intent to evade federal reporting thresholds under **31 CFR § 1010.314**.

Specifically, the suspect executed **[Number of Deposits]** consecutive deposits totaling **$[Total Deposit Amount]**, with each individual transaction strategically priced between **$[Min Deposit]** and **$[Max Deposit]** to remain immediately below the **$10,000 Currency Transaction Report (CTR)** filing threshold. These deposits occurred within a narrow **[Time Diff]**-hour window, bypassing normal business frequencies.

Immediately following these deposits, on **[Wire Date]**, a sum of **$[Wire Amount]** was wired out of the account to counterparty **[Counterparty Account]** in **[Counterparty Country]** (a recognized secrecy jurisdiction), leaving a nominal account balance. 

This transactional choreography—rapid sub-threshold cash intake combined with immediate offshore evacuation—demonstrates classic layering behavior. Extensive automated policy reviews confirm this pattern lacks an apparent lawful or commercial purpose, and has been flagged as a primary candidate for a formal regulatory Suspicious Activity Report (SAR) filing."

## Compilation Procedure
1. Receive inputs from `skill_1_triage.md` (structured transactions, timestamps, amounts, counterparties) and `skill_2_policy_check.md` (red flags triggered, legal citations, policy summaries).
2. Format the transaction log into a clean Markdown table.
3. Automatically calculate minimum and maximum sub-threshold deposits, time differences, and totals.
4. Populate the SAR Narrative template, ensuring all bracketed variables are precisely resolved with the audited facts.
5. Provide a one-click copyable or downloadable SAR Dossier text block within the user interface.
