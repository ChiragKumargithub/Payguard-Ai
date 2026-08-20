def calculate_risk_score(transaction):

    score = 0
    reasons = []

    # Rule 1 - Very high transaction amount
    if transaction["amount"] >= 3000:
        score += 40
        reasons.append("Very high transaction amount")

    elif transaction["amount"] >= 1500:
        score += 20
        reasons.append("High transaction amount")

    # Rule 2 - International transaction
    if transaction["is_international"] == 1:
        score += 15
        reasons.append("International transaction")

    # Rule 3 - Unknown device
    if str(transaction["device_id"]).startswith("UNKNOWN"):
        score += 35
        reasons.append("Unknown device")

    # Rule 4 - Declined transaction
    if transaction["status"] == "declined":
        score += 20
        reasons.append("Declined transaction")

    # Keep score between 0 and 100
    score = min(score, 100)

    return score, reasons


def get_risk_level(score):

    if score >= 70:
        return "HIGH"

    elif score >= 40:
        return "MEDIUM"

    else:
        return "LOW"


if __name__ == "__main__":

    test_transaction = {
        "amount": 6500,
        "is_international": 1,
        "device_id": "UNKNOWN-92841",
        "status": "approved"
    }

    score, reasons = calculate_risk_score(
        test_transaction
    )

    level = get_risk_level(score)

    print("PayGuard AI Risk Engine")
    print("-----------------------")
    print(f"Risk Score: {score}")
    print(f"Risk Level: {level}")
    print(f"Reasons: {reasons}")