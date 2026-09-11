# Suspicious Activity Reporting & Structuring Guidelines

## 1. Statutory Context: Structuring (31 CFR § 1010.314)
Under the Bank Secrecy Act (BSA) and Financial Crimes Enforcement Network (FinCEN) regulations, structuring is the practice of conducting one or more financial transactions at or below the statutory threshold ($10,000) for the purpose of evading the Currency Transaction Report (CTR) filing requirement.

### 31 CFR § 1010.314 - Structure of transactions:
> "No person shall, for the purpose of evading the reporting requirements of 31 U.S.C. 5313(a) or 5325 or any regulation issued thereunder... structure or assist in structuring, or attempt to structure or assist in structuring, any transaction with one or more domestic financial institutions."

### Key Thresholds & Rules:
- **Currency Transaction Report (CTR):** Must be filed for any transaction in currency (deposit, withdrawal, exchange, or other payment/transfer) of more than $10,000 by, through, or to the financial institution in a single business day.
- **Aggregated Transactions:** Multiple cash transactions conducted by or on behalf of the same person on the same business day must be aggregated and treated as a single transaction if they total more than $10,000.
- **Suspicious Activity Report (SAR):** A financial institution is required to file a SAR for any transaction (or aggregation of transactions) conducted or attempted by, at, or through the institution, involving or aggregating $5,000 or more, where the institution knows, suspects, or has reason to suspect that the transaction:
  1. Involves funds derived from illegal activity or is intended to hide or disguise funds or assets derived from illegal activity.
  2. Is designed to evade any regulations promulgated under the Bank Secrecy Act (specifically structuring).
  3. Has no business or apparent lawful purpose, or is not the sort of transaction in which the particular customer would normally be expected to engage, and the institution knows of no reasonable explanation for the transaction after examining the available facts.

## 2. Suspicious Activity Indicators for Structuring (Smurfing)
Smurfing is a specific method of structuring where multiple individuals ("smurfs") or a single individual make multiple small transactions across different branches or accounts, each below the $10,000 threshold, which collectively aggregate to a substantial sum.

### Red Flag Indicators:
- **Sub-Threshold Deposits:** A series of cash deposits or withdrawals just under the CTR threshold (e.g., multiple transactions between $9,000 and $9,990) over a short time frame (typically within 24 to 72 hours).
- **Rapid Movement of Funds (Layering):** Funds deposited in small cash increments are immediately transferred out of the account via wire transfer, official check, or ACH to offshore entities or high-risk jurisdictions.
- **Multiple Branches or ATMs:** A customer makes consecutive deposits or withdrawals at multiple physical branches or ATMs of the financial institution within the same day or consecutive days.
- **Unusual Business Activity:** A business customer whose business model does not inherently generate high volumes of cash (e.g., consulting, software development) begins making frequent, round-sum cash deposits under $10,000.
- **Inexplicable Offshore Outflows:** Rapid aggregation of funds followed by wire transfers to secrecy jurisdictions or tax havens (e.g., Cayman Islands, Panama, Switzerland, Bahamas) without a clear commercial or lawful purpose.

## 3. Investigatory Protocol (Autonomous Triage Workflow)
When an alert for potential structuring is triggered:
1. **Analyze Structured Pattern:** Calculate the cumulative total of cash/ACH deposits made within a rolling 48-to-72-hour window. Identify whether the single transaction amounts fall consistently in the high-risk range of $9,000 to $9,990.
2. **Examine Counterparty Risk:** Audit outbound transactions. Check if funds were immediately consolidated and sent to a high-risk offshore jurisdiction or an unrelated third party.
3. **Cross-Reference with Regulatory Guidelines:** Query this statutory reference text to ensure the identified patterns meet the definition of "structuring" under 31 CFR § 1010.314.
4. **Draft SAR Narrative:** Summarize the chronologically ordered transactions, explain the specific red flags triggered, cite the relevant federal statutes, and document why the activity lacks an apparent lawful or business purpose.
