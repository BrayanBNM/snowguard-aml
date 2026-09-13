# Skill: Structured AML Transaction Triage

## Objective
Enable autonomous, high-precision scanning of structured transaction ledgers in Snowflake using Cortex Analyst semantic views to identify potential cash structuring (smurfing) and layering behaviors.

## Input Parameters
- `target_account_id` (optional): The account to investigate.
- `triage_window_hours`: Default is `48` hours.
- `structuring_lower_bound`: Default is `9000.00`.
- `structuring_upper_bound`: Default is `9999.99`.

## Operational Workflow
1. **Identify Cash Structuring Activities:**
   - Execute a Cortex Analyst query using the verified query: "Which accounts have multiple cash deposits between $9,000 and $10,000 within a 48-hour window?".
   - Extract the account ID, customer name, transaction amounts, and precise timing differentials.

2. **Assess Layering & Outbound Flows:**
   - Check if the targeted account shows rapid outbound transfers to international jurisdictions within 48 hours of the cash deposits.
   - Run the Cortex Analyst query: "List accounts that received deposits followed by immediate offshore wire transfers to tax havens or secrecy jurisdictions."
   - Confirm if the recipient country belongs to the high-risk registry (e.g., KY, PA, CH, SG).

3. **Aggregate Transaction Volume:**
   - Summarize the aggregate volume of suspected transactions to verify if the threshold of $5,000 for mandatory SAR filings has been exceeded under BSA standards.
   - Run the query: "Show the aggregate volume of sub-threshold cash transactions and total wire transfers grouped by account risk tier."

4. **Flag Account for Policy Evaluation:**
   - Compile the transactional timeline (dates, amounts, reference IDs, and counterparties) and pass it to `skill_2_policy_check.md` for unstructured statutory comparison.
