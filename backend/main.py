import os

import psycopg2
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()


app = FastAPI(
    title="PayGuard AI API",
    description="Backend API for payment fraud intelligence",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


@app.get("/")
def root():
    return {
        "message": "PayGuard AI API is running"
    }


@app.get("/health")
def health_check():

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "SELECT current_database();"
        )

        database_name = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return {
            "status": "healthy",
            "database": database_name
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.get("/transactions")
def get_transactions(limit: int = 20):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            transaction_id,
            customer_id,
            merchant_id,
            amount,
            currency,
            country,
            status,
            is_fraud
        FROM transactions
        ORDER BY transaction_timestamp DESC
        LIMIT %s;
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    transactions = []

    for row in rows:

        transactions.append({
            "transaction_id": row[0],
            "customer_id": row[1],
            "merchant_id": row[2],
            "amount": float(row[3]),
            "currency": row[4],
            "country": row[5],
            "status": row[6],
            "is_fraud": row[7]
        })

    return {
        "count": len(transactions),
        "transactions": transactions
    }


@app.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: str):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            transaction_id,
            customer_id,
            merchant_id,
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
            fraud_reason
        FROM transactions
        WHERE transaction_id = %s;
        """,
        (transaction_id,)
    )

    row = cursor.fetchone()

    cursor.close()
    connection.close()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return {
        "transaction_id": row[0],
        "customer_id": row[1],
        "merchant_id": row[2],
        "amount": float(row[3]),
        "currency": row[4],
        "city": row[5],
        "country": row[6],
        "payment_method": row[7],
        "device_id": row[8],
        "transaction_timestamp": row[9],
        "status": row[10],
        "is_fraud": row[11],
        "fraud_type": row[12],
        "fraud_reason": row[13]
    }


@app.get("/alerts")
def get_alerts(limit: int = 20):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            fa.alert_id,
            fa.transaction_id,
            fa.risk_score,
            fa.risk_level,
            fa.alert_status,
            t.amount,
            t.country,
            t.status
        FROM fraud_alerts fa

        JOIN transactions t
            ON fa.transaction_id =
               t.transaction_id

        ORDER BY fa.risk_score DESC

        LIMIT %s;
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    alerts = []

    for row in rows:

        alerts.append({
            "alert_id": row[0],
            "transaction_id": row[1],
            "risk_score": float(row[2]),
            "risk_level": row[3],
            "alert_status": row[4],
            "amount": float(row[5]),
            "country": row[6],
            "transaction_status": row[7]
        })

    return {
        "count": len(alerts),
        "alerts": alerts
    }


@app.get("/alerts/high-risk")
def get_high_risk_alerts():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            fa.alert_id,
            fa.transaction_id,
            fa.risk_score,
            t.amount,
            t.country
        FROM fraud_alerts fa

        JOIN transactions t
            ON fa.transaction_id =
               t.transaction_id

        WHERE fa.risk_level = 'HIGH'

        ORDER BY fa.risk_score DESC;
        """
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    alerts = []

    for row in rows:

        alerts.append({
            "alert_id": row[0],
            "transaction_id": row[1],
            "risk_score": float(row[2]),
            "amount": float(row[3]),
            "country": row[4]
        })

    return alerts


@app.get("/analytics/summary")
def analytics_summary():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT
            COUNT(*),
            COALESCE(SUM(amount), 0),
            COALESCE(AVG(amount), 0),
            COALESCE(SUM(is_fraud), 0)
        FROM transactions;
        """
    )

    transaction_data = cursor.fetchone()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM fraud_alerts;
        """
    )

    alert_count = cursor.fetchone()[0]

    cursor.close()
    connection.close()

    total_transactions = transaction_data[0]
    total_value = float(transaction_data[1])
    average_amount = float(transaction_data[2])
    fraud_transactions = int(
        transaction_data[3]
    )

    fraud_rate = 0

    if total_transactions > 0:
        fraud_rate = (
            fraud_transactions
            / total_transactions
        ) * 100

    return {
        "total_transactions":
            total_transactions,

        "total_transaction_value":
            round(total_value, 2),

        "average_transaction_amount":
            round(average_amount, 2),

        "fraud_transactions":
            fraud_transactions,

        "fraud_rate_percent":
            round(fraud_rate, 2),

        "fraud_alerts":
            alert_count
    }