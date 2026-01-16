def explain_like_human(verdict, sugar, salt, sat_fat, calories):
    reasons = []
    advice = []

    if sugar > 10:
        reasons.append(f"High sugar ({sugar}g). Can increase diabetes and weight gain risk.")
        advice.append("Choose foods with under 5g sugar per 100g.")

    if salt > 1.2:
        reasons.append(f"High salt ({salt}g). This may raise blood pressure.")
        advice.append("Prefer low-salt or no-added-salt foods.")

    if sat_fat > 5:
        reasons.append(f"High saturated fat ({sat_fat}g). Linked to heart disease.")
        advice.append("Look for unsaturated fats like olive oil.")

    if calories > 400:
        reasons.append(f"High calorie density ({calories} kcal).")
        advice.append("Eat smaller portions or choose lighter alternatives.")

    if verdict == "Unhealthy":
        tone = "⚠️ This product may not support good long-term health."
    else:
        tone = "✅ This product is a reasonable choice when consumed in moderation."

    return tone, reasons, advice
