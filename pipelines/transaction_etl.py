from pathlib import Path

import pandas as pd


RAW_DATA_PATH = Path("data/raw/transactions.csv")

PROCESSED_DATA_PATH = Path(
    "data/processed/transactions_clean.csv"
)


def extract_data():
    print("\n[EXTRACT] Reading raw transaction data...")

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Raw data file not found: {RAW_DATA_PATH}"
        )

    df = pd.read_csv(RAW_DATA_PATH)

    print(
        f"[EXTRACT] Successfully extracted {len(df)} transactions."
    )

    return df

def validate_data(df):

    print("\n[VALIDATE] Running data quality checks...")

    required_columns = [
        "transaction_id",
        "customer_id",
        "card_id",
        "merchant_id",
        "merchant_category",
        "amount",
        "currency",
        "city",
        "country",
        "payment_method",
        "device_id",
        "transaction_timestamp",
        "status",
        "is_fraud",
        "fraud_type",
        "fraud_reason"
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    print("[VALIDATE] Required columns: PASS")

    duplicate_ids = df["transaction_id"].duplicated().sum()

    print(
        f"[VALIDATE] Duplicate transaction IDs: {duplicate_ids}"
    )

    missing_ids = df["transaction_id"].isna().sum()

    print(
        f"[VALIDATE] Missing transaction IDs: {missing_ids}"
    )

    invalid_amounts = (df["amount"] <= 0).sum()

    print(
        f"[VALIDATE] Invalid transaction amounts: {invalid_amounts}"
    )

    return df

def transform_data(df):

    print("\n[TRANSFORM] Transforming transaction data...")

    df = df.copy()

    # Remove duplicate transactions
    df = df.drop_duplicates(
        subset=["transaction_id"]
    )

    # Remove rows without essential identifiers
    df = df.dropna(
        subset=[
            "transaction_id",
            "customer_id"
        ]
    )

    # Remove impossible transaction amounts
    df = df[
        df["amount"] > 0
    ]

    # Convert timestamp
    df["transaction_timestamp"] = pd.to_datetime(
        df["transaction_timestamp"],
        errors="coerce"
    )

    # Remove invalid timestamps
    df = df.dropna(
        subset=["transaction_timestamp"]
    )

    # Standardize currency
    df["currency"] = (
        df["currency"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    # Standardize transaction status
    df["status"] = (
        df["status"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # Standardize payment method
    df["payment_method"] = (
        df["payment_method"]
        .astype(str)
        .str.lower()
        .str.strip()
    )

    # Create transaction date
    df["transaction_date"] = (
        df["transaction_timestamp"].dt.date
    )

    # Create transaction hour
    df["transaction_hour"] = (
        df["transaction_timestamp"].dt.hour
    )

    # Identify international transactions
    df["is_international"] = (
        df["country"] != "Canada"
    ).astype(int)

    # Categorize transaction amounts
    df["amount_category"] = pd.cut(
        df["amount"],
        bins=[
            0,
            100,
            500,
            1500,
            float("inf")
        ],
        labels=[
            "low",
            "medium",
            "high",
            "very_high"
        ]
    )

    print(
        f"[TRANSFORM] Transactions remaining: {len(df)}"
    )

    return df



def load_data(df):

    print("\n[LOAD] Saving processed transaction data...")

    PROCESSED_DATA_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        PROCESSED_DATA_PATH,
        index=False
    )

    print(
        f"[LOAD] Saved {len(df)} transactions to "
        f"{PROCESSED_DATA_PATH}"
    )




def print_quality_report(df):

    print("\n" + "=" * 50)
    print("PAYGUARD AI - DATA QUALITY REPORT")
    print("=" * 50)

    print(f"Total processed rows: {len(df)}")

    print(
        f"Duplicate IDs: "
        f"{df['transaction_id'].duplicated().sum()}"
    )

    print(
        f"Missing transaction IDs: "
        f"{df['transaction_id'].isna().sum()}"
    )

    print(
        f"Missing customer IDs: "
        f"{df['customer_id'].isna().sum()}"
    )

    print(
        f"Invalid amounts: "
        f"{(df['amount'] <= 0).sum()}"
    )

    print(
        f"Fraud transactions: "
        f"{df['is_fraud'].sum()}"
    )

    print("=" * 50)



def run_pipeline():

    print("\nStarting PayGuard AI ETL Pipeline")

    raw_df = extract_data()

    validated_df = validate_data(raw_df)

    processed_df = transform_data(validated_df)

    load_data(processed_df)

    print_quality_report(processed_df)

    print("\nETL Pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()