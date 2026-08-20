import os

import pandas as pd
import psycopg2
from dotenv import load_dotenv


load_dotenv()


CSV_PATH = "data/processed/transactions_clean.csv"


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

def load_customers(df, cursor):

    print("[LOAD] Loading customers...")

    customer_ids = (
        df["customer_id"]
        .dropna()
        .unique()
    )

    for customer_id in customer_ids:

        cursor.execute(
            """
            INSERT INTO customers (
                customer_id
            )
            VALUES (%s)
            ON CONFLICT (customer_id)
            DO NOTHING;
            """,
            (customer_id,)
        )

def load_merchants(df, cursor):

    print("[LOAD] Loading merchants...")

    merchants = (
        df[
            [
                "merchant_id",
                "merchant_category",
                "country"
            ]
        ]
        .drop_duplicates(
            subset=["merchant_id"]
        )
    )

    for _, row in merchants.iterrows():

        cursor.execute(
            """
            INSERT INTO merchants (
                merchant_id,
                merchant_category,
                country
            )
            VALUES (%s, %s, %s)
            ON CONFLICT (merchant_id)
            DO NOTHING;
            """,
            (
                row["merchant_id"],
                row["merchant_category"],
                row["country"]
            )
        )

def load_transactions():
    print("\n[LOAD] Reading processed transaction data...")

    df = pd.read_csv(CSV_PATH)

    print(f"[LOAD] Rows found: {len(df)}")

    connection = get_connection()
    cursor = connection.cursor()
    load_customers(df, cursor)
    load_merchants(df, cursor)

    inserted_count = 0

    for _, row in df.iterrows():

        query = """
        INSERT INTO transactions (
            transaction_id,
            customer_id,
            card_id,
            merchant_id,
            merchant_category,
            amount,
            currency,
            city,
            country,
            payment_method,
            device_id,
            transaction_timestamp,
            status,
            is_fraud,
            fraud_type,
            fraud_reason,
            transaction_date,
            transaction_hour,
            is_international,
            amount_category
        )
        VALUES (
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s
        )
        ON CONFLICT (transaction_id)
        DO NOTHING;
        """

        values = (
            row["transaction_id"],
            row["customer_id"],
            row["card_id"],
            row["merchant_id"],
            row["merchant_category"],
            row["amount"],
            row["currency"],
            row["city"],
            row["country"],
            row["payment_method"],
            row["device_id"],
            row["transaction_timestamp"],
            row["status"],
            int(row["is_fraud"]),
            row["fraud_type"],
            row["fraud_reason"],
            row["transaction_date"],
            int(row["transaction_hour"]),
            int(row["is_international"]),
            row["amount_category"]
        )

        cursor.execute(query, values)

        if cursor.rowcount == 1:
            inserted_count += 1

    connection.commit()

    cursor.close()
    connection.close()

    print(
        f"[LOAD] Successfully inserted "
        f"{inserted_count} new transactions."
    )


if __name__ == "__main__":
    load_transactions()