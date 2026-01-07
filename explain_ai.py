def explain_result(verdict, sugar, salt, sat_fat, calories):
    reasons = []
    suggestions = []

    if sugar > 10:
        reasons.append(f"This product contains high sugar ({sugar}g per 100g), which can increase diabetes risk.")
        suggestions.append("Choose products with less than 5g sugar per 100g.")

    if salt > 1.2:
        reasons.append(f"Salt level is high ({salt}g per 100g), which may affect blood pressure.")
        suggestions.append("Look for low-salt alternatives.")

    if sat_fat > 5:
        reasons.append(f"Saturated fat is high ({sat_fat}g per 100g), which is linked to heart disease.")
        suggestions.append("Prefer foods with unsaturated fats like olive oil.")

    if calories > 400:
        reasons.append(f"This is a high-calorie food ({calories} kcal per 100g).")
        suggestions.append("Eat occasionally or choose lighter snacks.")

    if verdict == "Unhealthy":
        tone = "⚠️ From a health perspective, this product should be consumed rarely."
    else:
        tone = "✅ This product is generally a good choice."

    return {
        "tone": tone,
        "reasons": reasons,
        "suggestions": suggestions
    }
