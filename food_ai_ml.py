import requests
import joblib

# -----------------------------------
# Load trained ML model
# -----------------------------------
model = joblib.load("food_ai_model.pkl")

LABELS = {
    0: "Healthy ✅",
    1: "Moderate ⚠️",
    2: "Unhealthy ❌"
}

# -----------------------------------
# Fetch product from OpenFoodFacts
# -----------------------------------
def get_product(barcode):
    url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        if data.get("status") != 1:
            return None
        return data["product"]
    except Exception as e:
        print("❌ API error:", e)
        return None

# -----------------------------------
# Extract ML features
# -----------------------------------
def extract_features(product):
    nutriments = product.get("nutriments", {})

    sugar = nutriments.get("sugars_100g", 0)
    salt = nutriments.get("salt_100g", 0)
    sat_fat = nutriments.get("saturated-fat_100g", 0)

    ingredients = (
        product.get("ingredients_text", "")
        + product.get("ingredients_text_en", "")
    ).lower()

    palm_oil = 1 if "palm oil" in ingredients else 0

    return [[sugar, salt, sat_fat, palm_oil]]

# -----------------------------------
# Main App
# -----------------------------------
def main():
    print("🥗 Welcome to Hikmat Food AI (ML Edition)")
    barcode = input("Enter the product barcode: ").strip()

    product = get_product(barcode)
    if not product:
        print("❌ Product not found")
        return

    name = product.get("product_name", "Unknown product")

    features = extract_features(product)
    prediction = model.predict(features)[0]

    print("\n📦 Product:", name)
    print("🤖 AI Verdict:", LABELS[prediction])

# -----------------------------------
if __name__ == "__main__":
    main()
