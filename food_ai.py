import openfoodfacts

def analyze_bad_things(product):
    """Analyze sugar, salt, fat, and additives in the product."""
    issues = []
    nutriments = product.get("nutriments", {})
    sugar = nutriments.get("sugars_100g", 0)
    salt = nutriments.get("salt_100g", 0)
    fat = nutriments.get("saturated-fat_100g", 0)

    if sugar > 10:
        issues.append("High sugar – increases risk of diabetes")
    if salt > 1.5:
        issues.append("High salt – may raise blood pressure")
    if fat > 5:
        issues.append("High saturated fat – bad for heart health")

    additives = product.get("additives_tags", [])
    if additives:
        readable_additives = [a.replace("en:", "").replace("-", " ") for a in additives]
        issues.append(f"Contains additives: {', '.join(readable_additives)}")

    return issues

def get_product_by_barcode(barcode):
    """Fetch product data by barcode."""
    api = openfoodfacts.API(user_agent="HikmatFoodAI/1.0")
    product = api.product.get(barcode)
    return product

def print_product_info(product):
    """Print product details and health warnings."""
    p = product["product"]
    print("\nProduct name:", p.get("product_name"))
    print("Ingredients:", p.get("ingredients_text"))
    print("Sugar (per 100g):", p.get("nutriments", {}).get("sugars_100g"))
    print("Salt (per 100g):", p.get("nutriments", {}).get("salt_100g"))
    print("Saturated fat (per 100g):", p.get("nutriments", {}).get("saturated-fat_100g"))

    issues = analyze_bad_things(p)
    print("\n⚠️ Health warnings:")
    if issues:
        for i in issues:
            print("-", i)
    else:
        print("No major issues detected. Seems healthy!")

# ------------------------
# Main program
# ------------------------
print("Welcome to Hikmat Food AI! 🥗")
barcode = input("Enter the product barcode (numbers only): ")

product = get_product_by_barcode(barcode)

# ✅ Only analyze if product exists
if product and "product" in product:
    print_product_info(product)
else:
    print("Product not found. Please check the barcode and try again.")
