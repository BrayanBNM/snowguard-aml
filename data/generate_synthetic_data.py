import csv
import random
from datetime import datetime, timedelta

def generate_data():
    # Set seed for reproducibility
    random.seed(42)

    # 1. Generate Accounts
    accounts = []
    countries = ["US", "US", "US", "US", "CA", "GB", "DE", "KY", "PA", "CH", "SG"]
    account_types = ["Checking", "Savings", "Business Checking"]
    risk_tiers = ["Low", "Medium", "High"]

    # Main suspect ACC_1042
    accounts.append({
        "account_id": "ACC_1042",
        "customer_name": "James Sterling",
        "account_type": "Checking",
        "risk_score": 0.85,
        "risk_tier": "High",
        "country": "US",
        "created_at": "2024-01-15 09:00:00"
    })

    # Suspect ACC_1085
    accounts.append({
        "account_id": "ACC_1085",
        "customer_name": "Apex Shell Holdings Ltd",
        "account_type": "Business Checking",
        "risk_score": 0.92,
        "risk_tier": "High",
        "country": "PA",
        "created_at": "2024-03-10 10:30:00"
    })

    # Suspect ACC_1102
    accounts.append({
        "account_id": "ACC_1102",
        "customer_name": "Marcus Vance",
        "account_type": "Savings",
        "risk_score": 0.78,
        "risk_tier": "High",
        "country": "US",
        "created_at": "2024-06-01 14:15:00"
    })

    # Generate 47 more normal accounts to make 50 total accounts
    names = [
        "Alice Smith", "Bob Jones", "Charlie Brown", "Diana Prince", "Evan Wright",
        "Fiona Gallagher", "George Costanza", "Hannah Abbott", "Ian Malcolm", "Julia Roberts",
        "Kevin Bacon", "Laura Croft", "Michael Scott", "Nancy Drew", "Oscar Martinez",
        "Pam Beesly", "Quentin Tarantino", "Rachel Green", "Steve Rogers", "Tony Stark",
        "Bruce Wayne", "Clark Kent", "Diana Ross", "Barry Allen", "Hal Jordan",
        "Arthur Curry", "Victor Stone", "Oliver Queen", "Selina Kyle", "Lois Lane",
        "Lex Luthor", "Wally West", "Dick Grayson", "Barbara Gordon", "Tim Drake",
        "Jason Todd", "Damian Wayne", "Alfred Pennyworth", "Jim Gordon", "Harvey Dent",
        "Peter Parker", "Mary Jane", "Harry Osborn", "Gwen Stacy", "Miles Morales",
        "Otto Octavius", "Norman Osborn"
    ]

    for i in range(1001, 1051):
        id_str = f"ACC_{i}"
        if id_str in ["ACC_1042"]:
            continue
        
        # Determine country and risk profile
        country = random.choice(countries)
        risk_score = round(random.uniform(0.05, 0.65), 2)
        if country in ["KY", "PA", "CH"]:
            risk_tier = "High"
            risk_score = round(random.uniform(0.65, 0.95), 2)
        elif risk_score > 0.4:
            risk_tier = "Medium"
        else:
            risk_tier = "Low"

        accounts.append({
            "account_id": id_str,
            "customer_name": names[(i-1001) % len(names)],
            "account_type": random.choice(account_types),
            "risk_score": risk_score,
            "risk_tier": risk_tier,
            "country": country,
            "created_at": (datetime(2023, 1, 1) + timedelta(days=random.randint(0, 500))).strftime("%Y-%m-%d %H:%M:%S")
        })

    # Write accounts to CSV
    with open("E:/snowguard-aml/data/accounts.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["account_id", "customer_name", "account_type", "risk_score", "risk_tier", "country", "created_at"])
        writer.writeheader()
        for acc in accounts:
            writer.writerow(acc)

    # 2. Generate Transactions
    transactions = []
    txn_id_counter = 50000

    # Start date for general transaction history
    start_date = datetime(2026, 8, 1)

    # Helper to add transaction
    def add_txn(acc_id, amount, t_type, method, dt, counterparty="", cp_country="US", status="COMPLETED"):
        nonlocal txn_id_counter
        transactions.append({
            "transaction_id": f"TXN_{txn_id_counter}",
            "account_id": acc_id,
            "amount": float(amount),
            "transaction_type": t_type,
            "method": method,
            "timestamp": dt.strftime("%Y-%m-%d %H:%M:%S"),
            "counterparty_account": counterparty,
            "counterparty_country": cp_country,
            "status": status
        })
        txn_id_counter += 1

    # --- INJECT SUSPICIOUS PATTERNS ---

    # Pattern A: James Sterling (ACC_1042)
    # Receiving multiple cash deposits between $9,000 and $9,950 within 48 hours,
    # followed by an immediate wire out to an offshore shell.
    acc_1042_base_time = datetime(2026, 9, 1, 10, 0, 0)
    # Cash deposits (Smurfing/Structuring to avoid $10,000 CTR trigger)
    add_txn("ACC_1042", 9450.00, "DEPOSIT", "CASH", acc_1042_base_time)
    add_txn("ACC_1042", 9800.00, "DEPOSIT", "CASH", acc_1042_base_time + timedelta(hours=14, minutes=15))
    add_txn("ACC_1042", 9120.00, "DEPOSIT", "CASH", acc_1042_base_time + timedelta(hours=28, minutes=40))
    add_txn("ACC_1042", 9650.00, "DEPOSIT", "CASH", acc_1042_base_time + timedelta(hours=42, minutes=5))
    # Immediate wire out to Cayman Islands offshore entity
    add_txn("ACC_1042", 37500.00, "TRANSFER_OUT", "WIRE", acc_1042_base_time + timedelta(hours=44, minutes=30), 
            counterparty="SHELL_CORP_KY_8829", cp_country="KY")

    # Pattern B: Apex Shell Holdings Ltd (ACC_1085)
    # Regular daily business structuring: series of check or wire deposits right under $10,000,
    # rapidly transferred to Panama.
    acc_1085_base_time = datetime(2026, 9, 3, 9, 0, 0)
    add_txn("ACC_1085", 9950.00, "DEPOSIT", "ACH", acc_1085_base_time)
    add_txn("ACC_1085", 9920.00, "DEPOSIT", "ACH", acc_1085_base_time + timedelta(days=1))
    add_txn("ACC_1085", 9980.00, "DEPOSIT", "ACH", acc_1085_base_time + timedelta(days=2))
    add_txn("ACC_1085", 9910.00, "DEPOSIT", "ACH", acc_1085_base_time + timedelta(days=3))
    # Immediate consolidation and outbound transfer
    add_txn("ACC_1085", 39500.00, "TRANSFER_OUT", "WIRE", acc_1085_base_time + timedelta(days=3, hours=4), 
            counterparty="PANAMA_GLOBAL_CORP", cp_country="PA")

    # Pattern C: Marcus Vance (ACC_1102)
    # Rapid layering structure: multiple deposits within hours, total sum highly suspicious,
    # followed by immediate withdrawal.
    acc_1102_base_time = datetime(2026, 9, 5, 12, 0, 0)
    add_txn("ACC_1102", 9850.00, "DEPOSIT", "CASH", acc_1102_base_time)
    add_txn("ACC_1102", 9900.00, "DEPOSIT", "CASH", acc_1102_base_time + timedelta(hours=2))
    add_txn("ACC_1102", 9750.00, "DEPOSIT", "CASH", acc_1102_base_time + timedelta(hours=5))
    add_txn("ACC_1102", 29000.00, "WITHDRAWAL", "CASH", acc_1102_base_time + timedelta(hours=6))

    # --- GENERATE RANDOM NORMAL TRANSACTIONS ---
    # Add regular transactions for other accounts to make the ledger realistic
    normal_methods = ["ACH", "WIRE", "CHECK", "CASH"]
    for acc in accounts:
        acc_id = acc["account_id"]
        # Skip suspicious accounts or add normal history to them in different periods
        if acc_id in ["ACC_1042", "ACC_1085", "ACC_1102"]:
            # Add some minor normal transactions weeks prior
            prior_time = datetime(2026, 8, 5)
            add_txn(acc_id, 1200.00, "DEPOSIT", "ACH", prior_time)
            add_txn(acc_id, 150.00, "WITHDRAWAL", "CASH", prior_time + timedelta(days=2))
            continue

        # For normal accounts, generate 10-25 transactions
        num_txns = random.randint(10, 25)
        curr_time = start_date + timedelta(hours=random.randint(1, 24))
        
        for _ in range(num_txns):
            amount = round(random.uniform(20, 4500), 2)
            # Occasional larger transaction but not structured
            if random.random() < 0.05:
                amount = round(random.uniform(12000, 25000), 2)

            t_type = random.choice(["DEPOSIT", "WITHDRAWAL", "TRANSFER_IN", "TRANSFER_OUT"])
            method = random.choice(normal_methods)
            
            # Match method logic
            if method == "CASH" and t_type in ["TRANSFER_IN", "TRANSFER_OUT"]:
                method = "WIRE"
            
            cp = ""
            cp_c = "US"
            if t_type in ["TRANSFER_IN", "TRANSFER_OUT"]:
                cp = f"ACC_{random.randint(1001, 1050)}"
                cp_c = random.choice(countries)

            add_txn(acc_id, amount, t_type, method, curr_time, cp, cp_c)
            curr_time += timedelta(days=random.randint(1, 3), hours=random.randint(1, 12))

    # Sort transactions by timestamp
    transactions.sort(key=lambda x: x["timestamp"])

    # Write transactions to CSV
    with open("E:/snowguard-aml/data/transactions.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "transaction_id", "account_id", "amount", "transaction_type", "method", 
            "timestamp", "counterparty_account", "counterparty_country", "status"
        ])
        writer.writeheader()
        for txn in transactions:
            writer.writerow(txn)

    print(f"Data Generation Completed successfully.")
    print(f"Generated {len(accounts)} accounts in accounts.csv")
    print(f"Generated {len(transactions)} transactions in transactions.csv")

if __name__ == "__main__":
    generate_data()
