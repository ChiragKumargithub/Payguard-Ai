


-- 1. CUSTOMERS TABLE

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(255),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 2. MERCHANTS TABLE

CREATE TABLE IF NOT EXISTS merchants (
    merchant_id VARCHAR(20) PRIMARY KEY,
    merchant_name VARCHAR(255),
    merchant_category VARCHAR(100),
    country VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 3. TRANSACTIONS TABLE

CREATE TABLE IF NOT EXISTS transactions (
    transaction_id VARCHAR(30) PRIMARY KEY,

    customer_id VARCHAR(20),
    card_id VARCHAR(20),
    merchant_id VARCHAR(20),

    merchant_category VARCHAR(100),

    amount DECIMAL(12, 2) NOT NULL,

    currency VARCHAR(10),

    city VARCHAR(100),
    country VARCHAR(100),

    payment_method VARCHAR(50),
    device_id VARCHAR(50),

    transaction_timestamp TIMESTAMP NOT NULL,

    status VARCHAR(30),

    is_fraud INTEGER DEFAULT 0,

    fraud_type VARCHAR(100),
    fraud_reason TEXT,

    transaction_date DATE,
    transaction_hour INTEGER,

    is_international INTEGER,

    amount_category VARCHAR(30),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- 4. FRAUD ALERTS TABLE

CREATE TABLE IF NOT EXISTS fraud_alerts (
    alert_id SERIAL PRIMARY KEY,

    transaction_id VARCHAR(30) NOT NULL,

    risk_score DECIMAL(5, 2),

    risk_level VARCHAR(20),

    alert_status VARCHAR(30) DEFAULT 'open',

    assigned_to VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    resolved_at TIMESTAMP
);




ALTER TABLE transactions
ADD CONSTRAINT fk_transaction_customer
FOREIGN KEY (customer_id)
REFERENCES customers(customer_id);


ALTER TABLE transactions
ADD CONSTRAINT fk_transaction_merchant
FOREIGN KEY (merchant_id)
REFERENCES merchants(merchant_id);


ALTER TABLE fraud_alerts
ADD CONSTRAINT fk_alert_transaction
FOREIGN KEY (transaction_id)
REFERENCES transactions(transaction_id);