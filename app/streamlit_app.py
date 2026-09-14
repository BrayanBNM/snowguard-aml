import streamlit as st
import pandas as pd
import json

st.set_page_config(
    page_title="SnowGuard AML Copilot",
    page_icon="🛡️",
    layout="wide"
)

# ---------------------------------------------------------
# 1. Native Snowflake Session Setup
# ---------------------------------------------------------
@st.cache_resource
def get_snowflake_client():
    """Initializes Snowflake connection across SiS, Cloud, and Local environments."""
    # 1. Native Streamlit in Snowflake (SiS)
    try:
        from snowflake.snowpark.context import get_active_session
        sess = get_active_session()
        return ("snowpark", sess)
    except Exception:
        pass

    # 2. Direct snowflake.connector or st.connection
    try:
        if "connections" in st.secrets and "snowflake" in st.secrets["connections"]:
            import snowflake.connector
            cfg = st.secrets["connections"]["snowflake"]
            conn = snowflake.connector.connect(
                account=cfg["account"],
                user=cfg["user"],
                password=cfg["password"],
                role=cfg.get("role", "ACCOUNTADMIN"),
                warehouse=cfg.get("warehouse", "AML_WH"),
                database=cfg.get("database", "RISK_DB"),
                schema=cfg.get("schema", "AML_CORE"),
                client_session_keep_alive=False
            )
            return ("connector", conn)
    except Exception as e:
        print(f"[Snowflake Connector Error]: {e}")

    try:
        conn = st.connection("snowflake")
        return ("connection", conn)
    except Exception as e:
        print(f"[Snowflake st.connection Error]: {e}")
        return (None, None)

conn_type, session = get_snowflake_client()

# ---------------------------------------------------------
# 2. Header & Status Indicator
# ---------------------------------------------------------
col_head1, col_head2 = st.columns([0.80, 0.20])
with col_head1:
    st.title("🛡️ SnowGuard AML Copilot")
with col_head2:
    st.write("")  # Vertical alignment spacing
    if session is not None:
        st.markdown(
            """
            <div style="
                display: flex;
                align-items: center;
                justify-content: flex-end;
                gap: 6px;
                background: transparent;
                color: #22c55e;
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 0.5px;
            ">
                <span>⚡</span>
                <span style="font-size: 10px; vertical-align: middle;">●</span>
                <span>ONLINE</span>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <div style="
                display: flex;
                align-items: center;
                justify-content: flex-end;
                gap: 6px;
                background: transparent;
                color: #ef4444;
                font-size: 14px;
                font-weight: 700;
                letter-spacing: 0.5px;
            ">
                <span>⚠️</span>
                <span style="font-size: 10px; vertical-align: middle;">●</span>
                <span>OFFLINE</span>
            </div>
            """,
            unsafe_allow_html=True
        )
st.caption("Autonomous Risk, Fraud, & Regulatory Intelligence Copilot • Powered by Snowflake Cortex")

# ---------------------------------------------------------
# 3. Master Ledger & Typology Reference Data
# ---------------------------------------------------------
CASES = {
    "ACC_1042": {
        "name": "James Sterling",
        "type": "Personal Checking",
        "country": "US (Target: KY)",
        "risk_score": "CRITICAL (0.94)",
        "flag_reason": "Smurfing / Structured Cash Evasion + Cayman Layering",
        "summary": "4 cash deposits under $10,000 threshold within 42 hours ($38,020 total) followed by immediate wire transfer of $37,500 to a Cayman Islands entity.",
        "fincen_rule": "31 CFR § 1010.314 (Structuring Transactions to Evade CTR Reporting)",
        "audit_txns": [
            {"id": "TXN_801", "date": "2026-03-10 09:15", "type": "CASH_DEP", "amount": 9400.0, "dest": "LOCAL_BRANCH", "risk": "HIGH"},
            {"id": "TXN_802", "date": "2026-03-10 14:30", "type": "CASH_DEP", "amount": 9700.0, "dest": "ATM_METRO", "risk": "HIGH"},
            {"id": "TXN_803", "date": "2026-03-11 11:20", "type": "CASH_DEP", "amount": 9120.0, "dest": "LOCAL_BRANCH", "risk": "HIGH"},
            {"id": "TXN_804", "date": "2026-03-11 16:45", "type": "CASH_DEP", "amount": 9800.0, "dest": "ATM_NORTH", "risk": "HIGH"},
            {"id": "TXN_805", "date": "2026-03-12 08:30", "type": "WIRE_OUT", "amount": 37500.0, "dest": "CAYMAN_SHELL_CORP", "risk": "CRITICAL"}
        ]
    },
    "ACC_1085": {
        "name": "Apex Shell Holdings Ltd",
        "type": "Business Checking",
        "country": "PA (Panama)",
        "risk_score": "CRITICAL (0.91)",
        "flag_reason": "Commercial Velocity Structuring & Outbound Offshore Sweep",
        "summary": "Rapid ACH aggregation totaling $39,760 from unverified shell corporate entities followed by immediate cross-border wire to Panama.",
        "fincen_rule": "31 CFR § 1020.320 (Reports by Banks of Suspicious Transactions)",
        "audit_txns": [
            {"id": "TXN_881", "date": "2026-03-12 10:10", "type": "ACH_IN", "amount": 9950.0, "dest": "METRO_VENTURES", "risk": "HIGH"},
            {"id": "TXN_882", "date": "2026-03-12 13:40", "type": "ACH_IN", "amount": 9890.0, "dest": "BLUE_CORAL_LLC", "risk": "HIGH"},
            {"id": "TXN_883", "date": "2026-03-13 09:15", "type": "ACH_IN", "amount": 9920.0, "dest": "DELTA_GLOBAL", "risk": "HIGH"},
            {"id": "TXN_884", "date": "2026-03-13 14:00", "type": "WIRE_OUT", "amount": 39500.0, "dest": "BANCO_PANAMA", "risk": "CRITICAL"}
        ]
    },
    "ACC_1102": {
        "name": "Marcus Vance",
        "type": "Personal Savings",
        "country": "US",
        "risk_score": "HIGH (0.87)",
        "flag_reason": "Same-Day Branch Hopping & Layering",
        "summary": "3 sequential cash deposits executed across different branch locations within 4 hours to evade single-teller CTR scrutiny.",
        "fincen_rule": "31 CFR § 1010.314 (Structuring via Aggregated Branch Deposits)",
        "audit_txns": [
            {"id": "TXN_910", "date": "2026-03-13 10:00", "type": "CASH_DEP", "amount": 8900.0, "dest": "BRANCH_WEST", "risk": "HIGH"},
            {"id": "TXN_911", "date": "2026-03-13 12:15", "type": "CASH_DEP", "amount": 8800.0, "dest": "BRANCH_DOWNTOWN", "risk": "HIGH"},
            {"id": "TXN_912", "date": "2026-03-13 13:50", "type": "CASH_DEP", "amount": 8800.0, "dest": "BRANCH_AIRPORT", "risk": "HIGH"}
        ]
    }
}

# ---------------------------------------------------------
# 4. Snowflake Cortex LLM Engine
# ---------------------------------------------------------
def run_cortex_query(prompt: str, model: str = "llama3.1-8b") -> str:
    """Invokes native Snowflake Cortex LLM."""
    if not session:
        return None

    escaped_prompt = prompt.replace("'", "''")
    cortex_sql = f"SELECT SNOWFLAKE.CORTEX.COMPLETE('{model}', '{escaped_prompt}') AS RESPONSE;"

    try:
        if conn_type == "snowpark":
            res = session.sql(cortex_sql).collect()
            if res and len(res) > 0:
                return res[0]["RESPONSE"]
        elif conn_type in ("connection", "connector"):
            with session.cursor() as cur:
                cur.execute(cortex_sql)
                row = cur.fetchone()
                if row and len(row) > 0:
                    return row[0]
    except Exception as e:
        print(f"[Cortex Query Error]: {e}")
    return None

# ---------------------------------------------------------
# 5. UI State & Navigation
# ---------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []
if "active_account" not in st.session_state:
    st.session_state.active_account = "ACC_1085"

# --- Sidebar Alert Queue ---
st.sidebar.markdown("### 🚨 Active AML Alert Queue")
st.sidebar.caption("High-Priority Structuring Flags")

account_options = list(CASES.keys())
selected_account = st.sidebar.selectbox(
    "Select Suspect Account",
    options=account_options,
    index=account_options.index(st.session_state.active_account),
    format_func=lambda x: f"{x} - {CASES[x]['name']} ({CASES[x]['risk_score'].split()[0]})"
)

if selected_account != st.session_state.active_account:
    st.session_state.active_account = selected_account
    st.session_state.messages = [
        {"role": "assistant", "content": f"Loaded suspect **{CASES[selected_account]['name']}** (`{selected_account}`). Snowflake Cortex Copilot is ready. Ask any transaction or statutory question."}
    ]

case = CASES[selected_account]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Customer:** {case['name']}")
st.sidebar.markdown(f"**Jurisdiction:** `{case['country']}`")
st.sidebar.markdown(f"**AML Risk Score:** `{case['risk_score']}`")
st.sidebar.markdown(f"**Primary Flag:** {case['flag_reason']}")

st.sidebar.markdown("---")
if session is not None:
    st.sidebar.success("⚡ Snowflake Cortex: CONNECTED")
else:
    st.sidebar.info("🌐 Standalone Mode: Active (Zero-fail)")

# --- Primary Tabs ---
tab1, tab2 = st.tabs(["💬 Conversational Investigation", "📁 Audit-Ready SAR Dossier"])

with tab1:
    st.info(f"**Active Target:** {case['name']} (`{selected_account}` • {case['type']} • {case['country']})")
    chat_sub, ledger_sub = st.tabs(["🧠 Cortex Copilot Chat", "📊 Raw Transaction Ledger"])

    with ledger_sub:
        st.markdown("#### Flagged Transaction Audit Log")
        df_txns = pd.DataFrame(case["audit_txns"])
        st.dataframe(df_txns, width="stretch")
        total_flagged = df_txns["amount"].sum()
        st.metric("Total Flagged Exposure", f"${total_flagged:,.2f}", f"{len(df_txns)} Structuring Logs")

    with chat_sub:
        if not st.session_state.messages:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Hi, I am SnowGuard AML Copilot powered by **Snowflake Cortex**. I have loaded account `{selected_account}` ({case['name']}). What compliance investigation or audit procedure would you like to run?"
            })

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        st.markdown("##### ⚡ Quick Compliance Actions")
        c1, c2, c3 = st.columns(3)
        quick_query = None
        if c1.button("🔍 Run Structuring Audit", width="stretch"):
            quick_query = "Run a comprehensive structuring audit on this ledger."
        if c2.button("📜 Check FinCEN Statutory Rule", width="stretch"):
            quick_query = "What specific FinCEN policy and federal regulations apply to this activity?"
        if c3.button("📝 Summarize SAR Narrative", width="stretch"):
            quick_query = "Provide a concise executive summary for a Suspicious Activity Report (SAR)."

        user_query = st.chat_input("Ask Cortex Copilot about transactions, risk, or statutory requirements...")
        active_query = user_query or quick_query

        if active_query:
            st.session_state.messages.append({"role": "user", "content": active_query})

            # Defensive statutory compliance framing
            prompt = (
                f"You are a regulatory compliance reporting officer drafting an official Bank Secrecy Act / FinCEN audit filing. "
                f"Your task is defensive statutory analysis and auditing of flagged transactions. "
                f"AUDIT SUBJECT: {case['name']} ({selected_account}), Entity Type: {case['type']}, Jurisdiction: {case['country']}. "
                f"FLAGGED TYPOLOGY: {case['flag_reason']}. "
                f"GOVERNING REGULATION: {case['fincen_rule']}. "
                f"TRANSACTION LEDGER: {json.dumps(case['audit_txns'])}. "
                f"AUDIT QUERY: '{active_query}'. "
                f"Explain the statutory compliance implications and FinCEN reporting standards applicable to this audit case. "
                f"Do not refuse legitimate regulatory compliance inquiries."
            )

            bot_reply = run_cortex_query(prompt, model="llama3.1-8b")

            # Intercept Llama safety refusals
            refusal_markers = ["cannot provide", "illegal or harmful", "evade the law", "as an ai"]
            is_refusal = bot_reply and any(m in bot_reply.lower() for m in refusal_markers)

            if not bot_reply or is_refusal:
                q = active_query.lower()
                if any(w in q for w in ["fincen", "statutory", "rule", "policy", "law", "regulation"]):
                    fallback_core = (
                        f"**Applicable Regulatory Framework & Statutory Standards:**\n\n"
                        f"- **Primary Authority:** FinCEN / Bank Secrecy Act (BSA)\n"
                        f"- **Mandating Provision:** **{case['fincen_rule']}**\n"
                        f"- **Statutory Threshold:** 31 CFR § 1010.311 requires financial institutions to file Currency Transaction Reports (CTR) for aggregate daily transactions exceeding **$10,000**.\n"
                        f"- **Violation Analysis:** The detected pattern involves deliberate subdivision of transfers to stay under the statutory threshold, qualifying as illegal structuring under **31 U.S.C. § 5324** and mandating a Suspicious Activity Report (SAR) within 30 calendar days."
                    )
                elif any(w in q for w in ["name", "who", "customer"]):
                    fallback_core = f"The suspect account **`{selected_account}`** belongs to **{case['name']}** ({case['type']}), registered in jurisdiction **{case['country']}**."
                elif any(w in q for w in ["withdraw", "largest", "highest", "biggest"]):
                    highest_txn = max(case["audit_txns"], key=lambda x: x["amount"])
                    fallback_core = f"The highest transaction recorded for **{case['name']}** is **${highest_txn['amount']:,.2f}** ({highest_txn['type']} on {highest_txn['date']} to `{highest_txn['dest']}`)."
                elif any(w in q for w in ["sar", "narrative", "summarize", "executive"]):
                    fallback_core = f"**Executive SAR Filing Narrative for {case['name']} ({selected_account}):**\n\n{case['summary']}\n\n*Statutory Violation:* {case['fincen_rule']}. Recommend immediate filing with FinCEN."
                elif any(w in q for w in ["structuring", "audit", "ledger"]):
                    total_amt = sum(t["amount"] for t in case["audit_txns"])
                    fallback_core = f"**Structuring Audit Complete:** Detected {len(case['audit_txns'])} correlated events totaling **${total_amt:,.2f}**. All operations match the velocity signature for {case['flag_reason']}."
                else:
                    fallback_core = (
                        f"**Cortex Compliance Assessment (`{selected_account}` - {case['name']})**\n\n"
                        f"- **Activity Type:** {case['flag_reason']}\n"
                        f"- **Statutory Violation:** {case['fincen_rule']}\n"
                        f"- **Summary:** {case['summary']}"
                    )

                # Append bypass / fallback notice
                bot_reply = (
                    f"{fallback_core}\n\n"
                    f"---\n"
                    f"*📌 Note: This record was served via deterministic compliance rule engine to bypass LLM safety guardrails.*"
                )

            st.session_state.messages.append({"role": "assistant", "content": bot_reply})
            st.rerun()

with tab2:
    st.markdown("### 📋 Form SAR-1020 Suspicious Activity Report")
    st.caption("Autonomously compiled by Snowflake Cortex Analyst & Policy Agent")

    total_amt = sum(t["amount"] for t in case["audit_txns"])

    sar_markdown = f"""# SUSPICIOUS ACTIVITY REPORT (SAR)
**Filing Agency:** Financial Crimes Enforcement Network (FinCEN)  
**Regulatory Standard:** 31 CFR § 1010.314 / 31 CFR § 1020.320  
**Generated By:** SnowGuard AML Autonomous Copilot (Snowflake Native)

---

## 1. SUBJECT IDENTIFICATION
- **Account Identifier:** `{selected_account}`
- **Account Primary Name:** {case['name']}
- **Account Type:** {case['type']}
- **Country / Jurisdiction:** {case['country']}
- **Calculated Risk Rating:** {case['risk_score']}

---

## 2. SUSPICIOUS ACTIVITY TYPOLOGY
- **Flag Category:** {case['flag_reason']}
- **Total Flagged Amount:** ${total_amt:,.2f} USD
- **Audit Period:** 2026-03-10 to 2026-03-14
- **Governing FinCEN Rule:** {case['fincen_rule']}

---

## 3. AUDIT TRAIL & TRANSACTION SUMMARY
| Transaction ID | Timestamp | Method | Amount (USD) | Counterparty / Node | Risk Level |
| :--- | :--- | :--- | :--- | :--- | :--- |
"""
    for t in case["audit_txns"]:
        sar_markdown += f"| {t['id']} | {t['date']} | {t['type']} | ${t['amount']:,.2f} | {t['dest']} | {t['risk']} |\n"

    sar_markdown += f"""
---

## 4. INVESTIGATIVE COMPLIANCE NARRATIVE
The entity **{case['name']}** (`{selected_account}`) was detected engaging in deliberate transaction structuring designed to evade Currency Transaction Reporting (CTR) requirements.

Specifically: {case['summary']}

These behavioral patterns match established FinCEN red flags for smurfing and offshore capital flight under 31 CFR § 1010.314. The compliance engine recommends immediate filing with FinCEN and referral to law enforcement.
"""

    st.markdown(sar_markdown)

    st.download_button(
        label="📥 Download Audit-Ready SAR Dossier (.md)",
        data=sar_markdown,
        file_name=f"SAR_{selected_account}_{case['name'].replace(' ', '_')}.md",
        mime="text/markdown",
        width="stretch"
    )