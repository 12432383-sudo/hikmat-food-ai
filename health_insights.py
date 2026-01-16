def explain_prediction(label, sugar, salt, sat_fat, palm_oil):
    reasons = []

    if sugar > 10:
        reasons.append("• High sugar content can increase diabetes risk.")
    if salt > 1:
        reasons.append("• High salt level may increase blood pressure.")
    if sat_fat > 5:
        reasons.append("• Saturated fats contribute to heart disease.")
    if palm_oil == 1:
        reasons.append("• Contains palm oil, which is inflammatory and less healthy.")

    if not reasons:
        reasons.append("• This product has good nutritional balance.")

    alternatives = [
        "Try choosing items with no added sugar.",
        "Look for foods labeled 'low salt'.",
        "Pick products with healthier oils like olive or sunflower oil.",
        "Choose snacks with less saturated fat."
    ]

    advice = "\n".join(alternatives[:2])

    return "\n".join(reasons), advice
