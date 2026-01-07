def explain_like_human(verdict, sugar, salt, sat_fat, calories):
    reasons = []
    advice = []

    if sugar > 10:
        reasons.append(
            f"High sugar content ({sugar}g per 100g) can increase the risk of diabetes and weight gain."
        )
        advice.append("Choose products with less than 5g sugar per 100g.")

    if salt > 1.2:
        reasons.append(
            f"Salt level is high ({salt}g per 100g), which may raise blood pressure."
        )
        advice.append("Prefer low-salt or no-added-salt options.")

    if sat_fat > 5:
        reasons.append(
            f"Saturated fat is high ({sat_fat}g per 100g), which is linked to heart disease."
        )
        advice.append("Look for foods with healthier fats like olive oil or nuts.")

    if calories > 400:
        reasons.append(
            f"This is a high-calorie product ({calories} kcal per 100g)."
        )
        advice.append("Consume occasionally and balance with fresh foods.")

    if verdict == "Unhealthy":
        tone = "⚠️ From a health perspective, this product should be consumed sparingly."
    else:
        tone = "✅ This product is generally a reasonable choice when eaten in moderation."

    return tone, reasons, advice
