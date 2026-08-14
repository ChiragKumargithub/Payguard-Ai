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

CURRENCIES = ["CAD", "USD"]

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
        "amount": round(random.uniform(2.00, 2500.00), 2),
        "currency": random.choice(CURRENCIES),
        "city": city,
        "country": country,
        "payment_method": random.choice(PAYMENT_METHODS),
        "device_id": f"DEV-{random.randint(1, 800):05d}",
        "transaction_timestamp": transaction_time,
        "status": random.choices(
            ["approved", "declined"],
            weights=[95, 5]
        )[0]
    }

    return transaction


transactions = []

for i in range(1, NUM_TRANSACTIONS + 1):
    transaction = generate_transaction(i)
    transactions.append(transaction)

df = pd.DataFrame(transactions)

print("\nPayGuard AI - Synthetic Payment Generator")
print("-----------------------------------------")

print(f"Transactions generated: {len(df)}")

print("\nSample transactions:")
print(df.head())

OUTPUT_PATH = "data/raw/transactions.csv"

df.to_csv(OUTPUT_PATH, index=False)

print(f"\nTransactions saved to: {OUTPUT_PATH}")


print("\nTransaction Summary")
print("-------------------")

print(f"Total transactions: {len(df)}")
print(f"Total value: ${df['amount'].sum():,.2f}")
print(f"Average transaction: ${df['amount'].mean():,.2f}")

print("\nTransaction Status:")
print(df["status"].value_counts())

print("\nTransactions by Country:")
print(df["country"].value_counts())