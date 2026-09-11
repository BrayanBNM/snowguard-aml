# Skill: Unstructured AML Policy & Regulatory Check

## Objective
Evaluate the transactional patterns identified in the structured triage phase against federal statutes, Bank Secrecy Act guidelines, and internal circulars stored in Snowflake stages using Cortex Search.

## Input Parameters
- `triage_results`: Structured transactional facts and timelines compiled during transaction triage.
- `target_statute`: Default is `31 CFR § 1010.314` (Structuring).

## Operational Workflow
1. **Query Cortex Search Policy Index:**
   - Call Snowflake Cortex Search over the regulatory stage containing `fincen_aml_guidelines.md` using semantic prompts like:
     - "What is the statutory definition of cash structuring under 31 CFR § 1010.314?"
     - "What are the suspicious activity indicators and red flags associated with smurfing?"
     - "What are the currency transaction reporting (CTR) thresholds and Suspicious Activity Report (SAR) requirements?"

2. **Map Behavior to Indicators:**
   - Compare the triaged transactional behaviors to the extracted red flag list:
     - Check for sub-threshold cash deposits (deposits between $9,000 and $10,000).
     - Check if transactions were executed within the 24-to-72 hour high-risk window.
     - Assess if there is rapid consolidation and immediate wire transfer to a high-risk offshore shell account (e.g., Cayman Islands, Panama).

3. **Validate Lack of Lawful Purpose:**
   - Review whether the customer's business profile (e.g., individual Checking, corporate entity) justifies large cash volumes or offshore flows.
   - Assert if the transaction sequence has an obvious commercial purpose or if it aligns with patterns designed specifically to evade the $10,000 CTR reporting threshold.

4. **Prepare Regulatory Audit Trail:**
   - Extract the specific statutory clauses and exact legal citations from the policy guidelines.
   - Pass these citations along with the behavioral match analysis to `skill_sar_dossier.md` for compilation of the audit-ready dossier.
