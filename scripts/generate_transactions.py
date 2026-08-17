import random
import uuid
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker




fake = Faker()

RANDOM_SEED = 42

random.seed(RANDOM_SEED)
Faker.seed(RANDOM_SEED)

NUM_TRANSACTIONS = 1000
FRAUD_RATE = 0.05




CURRENCIES = [
    "CAD",
    "USD"
]

PAYMENT_METHODS = [
    "credit_card",
    "debit_card",
    "digital_wallet"
]

MERCHANT_CATEGORIES = [
    "groceries",
    "electronics",
    "restaurants",
    "travel",
    "clothing",
    "entertainment",
    "fuel",
    "health"
]

CITIES = [
    ("Toronto", "Canada"),
    ("Ottawa", "Canada"),
    ("Vancouver", "Canada"),
    ("Montreal", "Canada"),
    ("New York", "USA"),
    ("Chicago", "USA")
]




def generate_transaction(transaction_number):

    city, country = random.choice(CITIES)

    transaction_time = datetime.now() - timedelta(
        days=random.randint(0, 30),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59)
    )

    transaction = {
        "transaction_id": f"TXN-{transaction_number:06d}",
        "customer_id": f"CUST-{random.randint(1, 500):05d}",
        "card_id": f"CARD-{random.randint(1, 600):05d}",
        "merchant_id": f"MER-{random.randint(1, 100):04d}",
        "merchant_category": random.choice(MERCHANT_CATEGORIES),

        "amount": round(
            random.uniform(5.00, 1500.00),
            2
        ),

        "currency": random.choice(CURRENCIES),

        "city": city,
        "country": country,

        "payment_method": random.choice(
            PAYMENT_METHODS
        ),

        "device_id": (
            f"DEV-{random.randint(1, 800):05d}"
        ),

        "transaction_timestamp": transaction_time,

        "status": random.choices(
            ["approved", "declined"],
            weights=[95, 5]
        )[0],

        
        "is_fraud": 0,
        "fraud_type": "none",
        "fraud_reason": "none"
    }

    return transaction




def inject_fraud(transaction):

    
    if random.random() >= FRAUD_RATE:
        return transaction
    
    transaction["is_fraud"] = 1
    fraud_type = random.choice([
        "high_amount",
        "unusual_location",
        "suspicious_device",
        "declined_fraud"
    ])

    

    if fraud_type == "high_amount":

        transaction["amount"] = round(
            random.uniform(3000, 10000),
            2
        )

        transaction["fraud_type"] = (
            "high_amount"
        )

        transaction["fraud_reason"] = (
            "Transaction amount is unusually high."
        )

    

    elif fraud_type == "unusual_location":

        transaction["city"] = random.choice([
            "London",
            "Dubai",
            "Singapore",
            "Tokyo"
        ])

        transaction["country"] = (
            "International"
        )

        transaction["fraud_type"] = (
            "unusual_location"
        )

        transaction["fraud_reason"] = (
            "Transaction occurred from an unusual location."
        )

    

    elif fraud_type == "suspicious_device":

        transaction["device_id"] = (
            f"UNKNOWN-{random.randint(10000, 99999)}"
        )

        transaction["fraud_type"] = (
            "suspicious_device"
        )

        transaction["fraud_reason"] = (
            "Transaction originated from an unknown device."
        )

    

    elif fraud_type == "declined_fraud":

        transaction["status"] = (
            "declined"
        )

        transaction["fraud_type"] = (
            "declined_fraud"
        )

        transaction["fraud_reason"] = (
            "Suspicious transaction was declined."
        )

    return transaction




transactions = []

for i in range(1, NUM_TRANSACTIONS + 1):
    transaction = generate_transaction(i)
    transaction = inject_fraud(transaction)
    transactions.append(transaction)






df = pd.DataFrame(transactions)



print("\nPayGuard AI - Synthetic Payment Generator")
print("-----------------------------------------")

print(
    f"Transactions generated: {len(df)}"
)

print("\nSample transactions:")

print(
    df.head()
)




OUTPUT_PATH = "data/raw/transactions.csv"

df.to_csv(
    OUTPUT_PATH,
    index=False
)

print(
    f"\nTransactions saved to: {OUTPUT_PATH}"
)




print("\nTransaction Summary")
print("-------------------")

print(
    f"Total transactions: {len(df)}"
)

print(
    f"Total value: ${df['amount'].sum():,.2f}"
)

print(
    f"Average transaction: ${df['amount'].mean():,.2f}"
)


print("\nTransaction Status:")

print(
    df["status"].value_counts()
)


print("\nTransactions by Country:")

print(
    df["country"].value_counts()
)

fraud_count = df["is_fraud"].sum()
fraud_rate = df["is_fraud"].mean() * 100

print("\nFraud Summary")
print("-------------------")
print(f"Fraud transactions: {fraud_count}")
print(f"Fraud rate: {fraud_rate:.2f}%")

print("\nFraud Types:")
print(
    df[df["is_fraud"] == 1]["fraud_type"]
    .value_counts()
)

fraud_transactions = df[df["is_fraud"] == 1]

print("\nSample Fraud Transactions:")
print(
    fraud_transactions[
        [
            "transaction_id",
            "customer_id",
            "amount",
            "country",
            "fraud_type"
        ]
    ].head(10)
)


print("\nData Validation")
print("-------------------")

print("Missing transaction IDs:",
      df["transaction_id"].isnull().sum())

print("Duplicate transaction IDs:",
      df["transaction_id"].duplicated().sum())

print("Negative amounts:",
      (df["amount"] < 0).sum())

print("Missing customer IDs:",
      df["customer_id"].isnull().sum())