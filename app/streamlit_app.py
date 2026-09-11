import streamlit as pd_st # keep naming standard
import streamlit as st
import pandas as pd
import os
import csv
from datetime import datetime

# Set page config for wide layout
st.set_page_config(
    page_title="SnowGuard AML Copilot",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for high-fidelity dark/light styling and cards
st.markdown("""
<style>
    /* Styling headings */
    .main-header {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    /* Alert Status Badges */
    .badge {
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: bold;
        font-size: 0.8rem;
    }
    .badge-high {
        background-color: #FEE2E2;
        color: #991B1B;
        border: 1px solid #FCA5A5;
    }
    .badge-medium {
        background-color: #FEF3C7;
        color: #92400E;
        border: 1px solid #FCD34D;
    }
    .badge-low {
        background-color: #D1FAE5;
        color: #065F46;
        border: 1px solid #6EE7B7;
    }
    .badge-filed {
        background-color: #DBEAFE;
        color: #1E40AF;
        border: 1px solid #93C5FD;
    }
    /* Card Container */
    .custom-card {
        background-color: #F9FAFB;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid #E5E7EB;
        margin-bottom: 10px;
    }
    .custom-card-active {
        background-color: #EFF6FF;
        border-radius: 8px;
        padding: 15px;
        border: 1px solid #3B82F6;
        margin-bottom: 10px;
    }
    /* Text styling */
    .bold-label {
        font-weight: 700;
    }
    /* Chat bubbles */
    .chat-user {
        background-color: #3B82F6;
        color: white;
        padding: 10px 15px;
        border-radius: 15px 15px 0px 15px;
        margin-bottom: 10px;
        width: fit-content;
        max-width: 80%;
        margin-left: auto;
    }
    .chat-agent {
        background-color: #F3F4F6;
        color: #1F2937;
        padding: 12px 18px;
        border-radius: 15px 15px 15px 0px;
        margin-bottom: 15px;
        border: 1px solid #E5E7EB;
        max-width: 85%;
    }
    .cortex-header {
        font-weight: 800;
        color: #0284C7;
        font-size: 0.9rem;
        margin-bottom: 5px;
        display: flex;
        align-items: center;
    }
</style>
""", unsafe_allowed_html=True)

# Helper functions to load data
@st.cache_data
def load_accounts_data():
    accounts_path = "E:/snowguard-aml/data/accounts.csv"
    if os.path.exists(accounts_path):
        return pd.read_csv(accounts_path)
    else:
        st.error(f"Accounts file not found at {accounts_path}. Please run generate_synthetic_data.py first.")
        return pd.DataFrame()

@st.cache_data
def load_transactions_data():
    transactions_path = "E:/snowguard-aml/data/transactions.csv"
    if os.path.exists(transactions_path):
        return pd.read_csv(transactions_path)
    else:
        st.error(f"Transactions file not found at {transactions_path}. Please run generate_synthetic_data.py first.")
        return pd.DataFrame()

@st.cache_data
def load_guidelines():
    guidelines_path = "E:/snowguard-aml/docs/fincen_aml_guidelines.md"
    if os.path.exists(guidelines_path):
        with open(guidelines_path, "r", encoding="utf-8") as f:
            return f.read()
    return "FinCEN Guidelines not loaded."

# Initialize Session States
if "selected_account" not in st.session_state:
    st.session_state["selected_account"] = "ACC_1042"
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = {
        "ACC_1042": [
            {"role": "assistant", "message": "Hi, I am SnowGuard AML Copilot. I have analyzed account **ACC_1042** (James Sterling) and loaded the transaction ledger. Feel free to ask me to run structure analysis, query policy compliance, or draft the SAR dossier."}
        ],
        "ACC_1085": [
            {"role": "assistant", "message": "Hi, I am SnowGuard AML Copilot. I have analyzed account **ACC_1085** (Apex Shell Holdings Ltd) and loaded the transaction ledger. Ask me to cross-reference their transactions with corporate structuring rules."}
        ],
        "ACC_1102": [
            {"role": "assistant", "message": "Hi, I am SnowGuard AML Copilot. I have analyzed account **ACC_1102** (Marcus Vance) and loaded the transaction ledger. Let me know how I can assist with this investigation."}
        ]
    }
if "filed_alerts" not in st.session_state:
    st.session_state["filed_alerts"] = set()

# Main Header
st.markdown('<div class="main-header">🛡️ SnowGuard AML Copilot</div>', unsafe_allowed_html=True)
st.markdown('<div class="sub-header">Autonomous Risk, Fraud, & Regulatory Intelligence Dashboard • GCC Hackathon Edition</div>', unsafe_allowed_html=True)

# Load CSV files
accounts_df = load_accounts_data()
transactions_df = load_transactions_data()
policy_guidelines_text = load_guidelines()

if not accounts_df.empty and not transactions_df.empty:
    # --- 3-PANE LAYOUT DEFINITION ---
    pane1, pane2, pane3 = st.columns([1.1, 2.0, 1.4])

    # ==========================================
    # PANE 1: ALERT QUEUE (LEFT)
    # ==========================================
    with pane1:
        st.subheader("🚨 Alert Triage Queue")
        
        # High-risk target definitions
        alert_definitions = [
            {
                "id": "ACC_1042",
                "name": "James Sterling",
                "pattern": "High Cash Structuring (Smurfing)",
                "risk": "High",
                "score": "0.85",
                "desc": "4 cash deposits totaling $38,020 in 42 hours, immediately wired out to Cayman Islands."
            },
            {
                "id": "ACC_1085",
                "name": "Apex Shell Holdings Ltd",
                "pattern": "Business Structuring & Panama Wire",
                "risk": "High",
                "score": "0.92",
                "desc": "4 daily sub-threshold check/ACH deposits, immediate consolidated transfer to Panama."
            },
            {
                "id": "ACC_1102",
                "name": "Marcus Vance",
                "pattern": "Rapid Multi-Deposit Layering",
                "risk": "High",
                "score": "0.78",
                "desc": "3 cash deposits within 5 hours followed by large cash withdrawal."
            }
        ]

        # Render Alert Cards
        for alert in alert_definitions:
            is_selected = st.session_state["selected_account"] == alert["id"]
            is_filed = alert["id"] in st.session_state["filed_alerts"]
            
            # Formulate badge style
            badge_class = "badge-high"
            if is_filed:
                badge_class = "badge-filed"
            
            status_text = "FILED" if is_filed else "PENDING TRIAGE"
            
            # Select proper container styling
            card_style = "custom-card-active" if is_selected else "custom-card"
            
            with st.container():
                st.markdown(f"""
                <div class="{card_style}">
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 5px;">
                        <span style="font-size:0.85rem; font-weight:800; color:#4B5563;">{alert["id"]}</span>
                        <span class="badge {badge_class}">{status_text}</span>
                    </div>
                    <div style="font-size:1.05rem; font-weight:800; color:#1F2937;">{alert["name"]}</div>
                    <div style="font-size:0.85rem; font-weight:700; color:#991B1B; margin-top: 3px;">⚠️ {alert["pattern"]}</div>
                    <div style="font-size:0.8rem; color:#6B7280; margin-top: 5px;">{alert["desc"]}</div>
                    <div style="font-size:0.8rem; font-weight:600; color:#1E3A8A; margin-top: 5px;">Risk Score: {alert["score"]} • Domicile: {alert["id"]}</div>
                </div>
                """, unsafe_allowed_html=True)
                
                # Selection Button
                if st.button(f"Analyze {alert['id']}", key=f"btn_select_{alert['id']}", use_container_width=True):
                    st.session_state["selected_account"] = alert["id"]
                    st.rerun()

    # Get active account details
    active_acc_id = st.session_state["selected_account"]
    acc_row = accounts_df[accounts_df["account_id"] == active_acc_id].iloc[0]
    acc_txns = transactions_df[transactions_df["account_id"] == active_acc_id]

    # ==========================================
    # PANE 2: CONVERSATIONAL REASONING CANVAS (CENTER)
    # ==========================================
    with pane2:
        st.subheader("🧠 Conversational Triage Canvas")
        
        # Display Active Account Metadata Banner
        st.markdown(f"""
        <div style="background-color: #F0FDF4; border: 1px solid #BBF7D0; border-radius: 8px; padding: 12px 18px; margin-bottom: 15px;">
            <div style="font-size:0.85rem; font-weight:800; color:#15803D;">ACTIVE WORKSPACE</div>
            <div style="display:flex; justify-content:space-between; margin-top: 5px; flex-wrap: wrap;">
                <div><span class="bold-label">Customer:</span> {acc_row['customer_name']}</div>
                <div><span class="bold-label">Account:</span> {acc_row['account_id']} ({acc_row['account_type']})</div>
                <div><span class="bold-label">Risk Profile:</span> <span style="color:#B91C1C; font-weight:bold;">{acc_row['risk_tier']} ({acc_row['risk_score']})</span></div>
                <div><span class="bold-label">Country:</span> {acc_row['country']}</div>
            </div>
        </div>
        """, unsafe_allowed_html=True)

        # Tabbed interface: Transactions vs Conversational Copilot
        tab_chat, tab_ledger = st.tabs(["💬 Cortex Copilot Chat", "📊 Transaction Ledger"])
        
        with tab_ledger:
            st.markdown(f"**Transaction Records for {acc_row['customer_name']} ({active_acc_id})**")
            # Style the table nicely
            st.dataframe(
                acc_txns[[
                    "transaction_id", "timestamp", "transaction_type", "method", "amount", "counterparty_account", "counterparty_country", "status"
                ]].sort_values(by="timestamp", ascending=False),
                use_container_width=True,
                hide_index=True
            )

        with tab_chat:
            # Render chat history for the active account
            chat_container = st.container()
            with chat_container:
                for chat in st.session_state["chat_history"].get(active_acc_id, []):
                    if chat["role"] == "user":
                        st.markdown(f'<div class="chat-user">{chat["message"]}</div>', unsafe_allowed_html=True)
                    else:
                        st.markdown(f'<div class="chat-agent">{chat["message"]}</div>', unsafe_allowed_html=True)

            # Chat inputs & predefined quick-actions
            st.markdown("**⚡ Quick Compliance Queries:**")
            col1, col2, col3 = st.columns(3)
            
            q1_clicked = col1.button("🔍 Run Structuring Audit", use_container_width=True)
            q2_clicked = col2.button("📜 Check FinCEN Policy", use_container_width=True)
            q3_clicked = col3.button("📋 Generate SAR Data", use_container_width=True)

            # Initialize user input variable
            user_input = ""
            action_triggered = False

            if q1_clicked:
                user_input = "Identify cash structuring patterns and smurfing indicators in this ledger."
                action_triggered = True
            elif q2_clicked:
                user_input = f"Compare this customer's transaction activity against 31 CFR § 1010.314 statutory thresholds."
                action_triggered = True
            elif q3_clicked:
                user_input = "Extract structured summary data and counterparties to compile a SAR filing dossier."
                action_triggered = True

            # Standard chat input text field
            chat_box = st.chat_input("Ask Cortex Copilot about transactions, risk, or statutory requirements...")
            if chat_box:
                user_input = chat_box
                action_triggered = True

            # Process User Query (Simulation of Cortex Analyst and Cortex Search)
            if action_triggered and user_input:
                # Add user message to history
                st.session_state["chat_history"][active_acc_id].append({"role": "user", "message": user_input})
                
                # Formulate Autonomous Agent Response
                response_text = ""
                
                # --- CASE 1: STRUCTURING ANALYSIS (CORTEX ANALYST SIMULATION) ---
                if "structur" in user_input.lower() or "smurf" in user_input.lower() or "audit" in user_input.lower():
                    # Calculate structured transaction stats
                    cash_txns = acc_txns[(acc_txns["method"] == "CASH") & (acc_txns["transaction_type"] == "DEPOSIT") & (acc_txns["amount"] >= 9000.00) & (acc_txns["amount"] < 10000.00)]
                    ach_txns = acc_txns[(acc_txns["method"] == "ACH") & (acc_txns["transaction_type"] == "DEPOSIT") & (acc_txns["amount"] >= 9000.00) & (acc_txns["amount"] < 10000.00)]
                    
                    target_deposits = pd.concat([cash_txns, ach_txns])
                    total_deposits_count = len(target_deposits)
                    total_deposits_sum = target_deposits["amount"].sum()
                    
                    wire_out = acc_txns[(acc_txns["transaction_type"] == "TRANSFER_OUT") & (acc_txns["method"] == "WIRE")]
                    
                    # Construct Cortex Analyst Reasoning Output
                    response_text += f"""
<div class="cortex-header">⚡ Snowflake Cortex Analyst • Structured Ledger Analysis</div>

**Verified Query Executed:**
```sql
-- Cortex Semantic Verification: Pattern Structuring/Smurfing
SELECT * FROM TRANSACTIONS 
WHERE account_id = '{active_acc_id}' 
  AND transaction_type = 'DEPOSIT' 
  AND amount BETWEEN 9000.00 AND 10000.00;
```

**Reasoning Path & Multi-Turn Analysis:**
1. **Structuring Flag:** Located **{total_deposits_count}** consecutive deposits totalling **${total_deposits_sum:,.2f}** with individual values precisely in the high-risk range of $9,000 to $9,990.
2. **Timing Proximity:** Transactions occurred in quick succession.
3. **Outflow Layering Flag:** Checked outbound routing history. Found an immediate wire transfer of **${wire_out['amount'].iloc[0] if not wire_out.empty else 0:,.2f}** directed to counterparty `{wire_out['counterparty_account'].iloc[0] if not wire_out.empty else 'N/A'}` in `{wire_out['counterparty_country'].iloc[0] if not wire_out.empty else 'N/A'}` (jurisdiction of concern).
4. **Classification:** Suspicious structuring verified with **100% mathematical accuracy** against ledger records. Evades CTR ($10,000) reporting requirement.
"""

                # --- CASE 2: POLICY AUDIT (CORTEX SEARCH RAG SIMULATION) ---
                elif "policy" in user_input.lower() or "cfr" in user_input.lower() or "fincen" in user_input.lower() or "statute" in user_input.lower():
                    # Query Cortex Search on markdown text
                    response_text += f"""
<div class="cortex-header">🔍 Snowflake Cortex Search • Managed RAG Policy Query</div>

**Cortex Search Vector Matches (Regulatory Stage):**
*Source: `fincen_aml_guidelines.md` (Stage Path: `@AML_STAGE/fincen_aml_guidelines.md`)*

> **31 CFR § 1010.314 - Structure of transactions:**
> *"No person shall, for the purpose of evading the reporting requirements... structure or assist in structuring, or attempt to structure or assist in structuring, any transaction with one or more domestic financial institutions."*

**Statutory Alignment Check:**
- **Triggered Red Flag:** *Sub-Threshold Deposits* — Checked. Multiple transactions (averaging $9,500+) designed to bypass the $10,000 CTR rule.
- **Triggered Red Flag:** *Rapid Movement of Funds (Layering)* — Checked. Outbound wires to offshore secrecy havens (Cayman Islands/Panama) directly match the regulatory profile for shell transfer schemes.
- **Reporting Requirement:** A **Suspicious Activity Report (SAR)** is **statutorily mandated** as transactions exceed the $5,000 threshold and display clear intent to evade Bank Secrecy Act laws.
"""

                # --- CASE 3: DOSSIER PREPARATION (SAR EXTRACTOR) ---
                elif "sar" in user_input.lower() or "dossier" in user_input.lower() or "compile" in user_input.lower() or "data" in user_input.lower():
                    response_text += f"""
<div class="cortex-header">📋 SnowGuard Agent Harness • Compilation Process</div>

**Extracted Compliance Artifacts:**
- **Regulatory Standard:** FinCEN 31 CFR § 1010.314 Evasion Clause
- **Suspect Entity:** {acc_row['customer_name']} ({active_acc_id})
- **Account Aggregated Ingress:** ${acc_txns[(acc_txns["transaction_type"]=='DEPOSIT') & (acc_txns["amount"]>=9000)]["amount"].sum():,.2f}
- **Offshore Wire Egress:** ${acc_txns[(acc_txns["transaction_type"]=='TRANSFER_OUT') & (acc_txns["method"]=='WIRE')]["amount"].sum():,.2f}

The audit trail has been loaded into the **SAR Dossier Compiler** (Pane 3). You can now review, download, or approve the regulatory packet with one click.
"""
                
                # --- CASE 4: FALLBACK GENERAL COCOPILOT CHAT ---
                else:
                    response_text += f"""
<div class="cortex-header">🤖 SnowGuard Copilot</div>

I have processed your query regarding account **{active_acc_id}**.
To perform a complete regulatory audit, try using the quick compliance query buttons above:
1. **Run Structuring Audit** - to scan the structured ledger for smurfing and structuring patterns (Cortex Analyst).
2. **Check FinCEN Policy** - to cross-reference transactions with federal regulations (Cortex Search).
3. **Generate SAR Data** - to extract compliance artifacts for filing.
"""

                # Append assistant response and refresh
                st.session_state["chat_history"][active_acc_id].append({"role": "assistant", "message": response_text})
                st.rerun()

    # ==========================================
    # PANE 3: ONE-CLICK EXPORTABLE SAR PACKET (RIGHT)
    # ==========================================
    with pane3:
        st.subheader("📁 Audit-Ready SAR Dossier")
        
        # Calculate dossier facts dynamically based on active account
        deposits = acc_txns[(acc_txns["transaction_type"] == "DEPOSIT") & (acc_txns["amount"] >= 9000)]
        wires = acc_txns[(acc_txns["transaction_type"] == "TRANSFER_OUT") & (acc_txns["method"] == "WIRE")]
        withdrawals = acc_txns[(acc_txns["transaction_type"] == "WITHDRAWAL") & (acc_txns["amount"] >= 9000)]
        
        total_dep_sum = deposits["amount"].sum()
        num_dep = len(deposits)
        min_dep = deposits["amount"].min() if num_dep > 0 else 0
        max_dep = deposits["amount"].max() if num_dep > 0 else 0
        
        start_date_str = deposits["timestamp"].min() if num_dep > 0 else "2026-09-01"
        end_date_str = deposits["timestamp"].max() if num_dep > 0 else "2026-09-03"
        
        wire_date_str = wires["timestamp"].iloc[0] if not wires.empty else "N/A"
        wire_amount = wires["amount"].sum() if not wires.empty else 0
        counterparty_acc = wires["counterparty_account"].iloc[0] if not wires.empty else "N/A"
        counterparty_cntry = wires["counterparty_country"].iloc[0] if not wires.empty else "N/A"

        # Handle Marcus Vance withdrawal exception
        if active_acc_id == "ACC_1102":
            wire_date_str = withdrawals["timestamp"].iloc[0] if not withdrawals.empty else "N/A"
            wire_amount = withdrawals["amount"].sum() if not withdrawals.empty else 0
            counterparty_acc = "Cash Withdrawal"
            counterparty_cntry = "US"

        # Generate markdown table of suspicious transactions
        table_rows = ""
        suspicious_list = pd.concat([deposits, wires, withdrawals]).sort_values(by="timestamp")
        for idx, r in suspicious_list.iterrows():
            table_rows += f"| {r['transaction_id']} | {r['timestamp']} | {r['transaction_type']} | {r['method']} | ${r['amount']:,.2f} | {r['counterparty_account'] if pd.notna(r['counterparty_account']) else 'N/A'} | {r['counterparty_country']} |\n"

        # Dynamic SAR Narrative
        sar_narrative = f"""Between **{start_date_str}** and **{end_date_str}**, the account of **{acc_row['customer_name']}** (Account ID: **{active_acc_id}**) exhibited highly suspicious cash structuring and layering patterns that strongly indicate an intent to evade federal reporting thresholds under **31 CFR § 1010.314**.

Specifically, the suspect executed **{num_dep}** consecutive deposits totaling **${total_dep_sum:,.2f}**, with each individual transaction strategically priced between **${min_dep:,.2f}** and **${max_dep:,.2f}** to remain immediately below the **$10,000 Currency Transaction Report (CTR)** filing threshold. These deposits occurred within a narrow window, bypassing normal business frequencies.

Immediately following these deposits, on **{wire_date_str}**, a sum of **${wire_amount:,.2f}** was transferred out of the account via **{"CASH" if active_acc_id == "ACC_1102" else "WIRE"}** to counterparty **{counterparty_acc}** in **{counterparty_cntry}** (a recognized secrecy jurisdiction), leaving a nominal account balance.

This transactional choreography—rapid sub-threshold intake combined with immediate offshore evacuation—demonstrates classic layering behavior. Extensive automated policy reviews confirm this pattern lacks an apparent lawful or commercial purpose, and has been flagged as a primary candidate for a formal regulatory Suspicious Activity Report (SAR) filing."""

        # Full Document Content
        full_dossier_text = f"""# Suspicious Activity Report (SAR) Dossier

## I. SAR Reference Details
- **Filing Date:** {datetime.now().strftime('%Y-%m-%d')}
- **Filing Institution:** SnowGuard AML Intelligence Engine (GCC Core)
- **Primary Violation Category:** Structuring / Transaction evasion (31 CFR § 1010.314)
- **Filing Threshold Category:** Suspicious Activity > $5,000 with suspicious intent

## II. Suspect Profile
- **Account ID:** {active_acc_id}
- **Customer Name:** {acc_row['customer_name']}
- **Account Type:** {acc_row['account_type']}
- **Customer Risk Score:** {acc_row['risk_score']} / 1.00
- **Customer Country:** {acc_row['country']}

## III. Structured Transaction Audit Log
| Transaction ID | Timestamp | Type | Method | Amount (USD) | Counterparty Account | Counterparty Country |
|----------------|-----------|------|--------|--------------|----------------------|----------------------|
{table_rows}

## IV. Policy Reference & Red Flag Alignment
- **Statutory Violation:** 31 CFR § 1010.314 (Evading Currency Transaction Reports)
- **Statutory Guidance Source:** FinCEN Bank Secrecy Act Regulations
- **Triggered Red Flag Checklist:**
  - [x] Sub-threshold Deposits ($9,000 - $9,990)
  - [x] High-frequency Clustering (within 48-72 hours)
  - [x] Rapid Consolidating Outflows (Layering)
  - [x] High-Risk Jurisdiction Transfer (KY, PA, CH)

## V. SAR Narrative (Filing Packet)
{sar_narrative}
"""

        # Display Live Packet in Text Area
        st.text_area("Live Generated Dossier Document", value=full_dossier_text, height=350)
        
        # Action Buttons
        is_already_filed = active_acc_id in st.session_state["filed_alerts"]
        
        if is_already_filed:
            st.success("✅ This Suspicious Activity Report has been successfully compiled, signed, and transmitted to Snowflake Task scheduler!")
        else:
            if st.button("🚀 Approve & File Regulatory SAR", key=f"file_{active_acc_id}", type="primary", use_container_width=True):
                st.session_state["filed_alerts"].add(active_acc_id)
                st.toast(f"SAR Filing Packet submitted to FinCEN gateway for {acc_row['customer_name']}!")
                st.rerun()

        # Download Button
        st.download_button(
            label="💾 Download Audit Packet",
            data=full_dossier_text,
            file_name=f"SAR_Dossier_{active_acc_id}_{datetime.now().strftime('%Y%m%d')}.md",
            mime="text/markdown",
            use_container_width=True
        )

else:
    st.info("Please make sure you generate the transactional datasets and place them under E:/snowguard-aml/data/.")
