import os

import psycopg2
from dotenv import load_dotenv

from risk_engine import (
    calculate_risk_score,
    get_risk_level
)


load_dotenv()


def get_connection():

    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
def get_transactions(cursor):

    query = """
        SELECT
            transaction_id,
            amount,
            is_international,
            device_id,
            status
        FROM transactions;
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    transactions = []

    for row in rows:

        transaction = {
            "transaction_id": row[0],
            "amount": float(row[1]),
            "is_international": row[2],
            "device_id": row[3],
            "status": row[4]
        }

        transactions.append(transaction)

    return transactions

def create_alert(
    cursor,
    transaction_id,
    risk_score,
    risk_level
):

    query = """
        INSERT INTO fraud_alerts (
            transaction_id,
            risk_score,
            risk_level,
            alert_status
        )
        VALUES (%s, %s, %s, %s)

        ON CONFLICT (transaction_id)
        DO UPDATE SET
            risk_score = EXCLUDED.risk_score,
            risk_level = EXCLUDED.risk_level;
    """

    cursor.execute(
        query,
        (
            transaction_id,
            risk_score,
            risk_level,
            "open"
        )
    )

    
def run_fraud_detection():

    print("\nPayGuard AI Fraud Detection")
    print("---------------------------")

    connection = get_connection()

    cursor = connection.cursor()

    transactions = get_transactions(cursor)

    print(
        f"Transactions analyzed: {len(transactions)}"
    )

    alerts_created = 0

    for transaction in transactions:

        score, reasons = calculate_risk_score(
            transaction
        )

        level = get_risk_level(score)

        # Only MEDIUM and HIGH create alerts
        if level in ["MEDIUM", "HIGH"]:

            create_alert(
                cursor,
                transaction["transaction_id"],
                score,
                level
            )

            alerts_created += 1

    connection.commit()

    cursor.close()
    connection.close()

    print(
        f"Fraud alerts created: {alerts_created}"
    )


if __name__ == "__main__":
    run_fraud_detection()