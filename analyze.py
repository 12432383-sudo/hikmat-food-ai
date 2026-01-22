"""
analyze.py
Loads the trained model and provides food analysis functionality.
"""

import pickle
import numpy as np
import os

# Global variable to cache the model
_model = None

def load_model():
    """Load the trained model from food_model.pkl"""
    global _model
    if _model is None:
        model_path = 'food_model.pkl'
        if not os.path.exists(model_path):
            raise FileNotFoundError(
                f"Model file {model_path} not found. Please run train_model.py first."
            )
        with open(model_path, 'rb') as f:
            _model = pickle.load(f)
    return _model

def analyze_food(barcode, sugar, salt, fat):
    """
    Analyze food based on nutrition values.
    
    Args:
        barcode: Barcode string (can be empty, not used in prediction)
        sugar: Sugar content in grams per 100g
        salt: Salt content in grams per 100g
        fat: Saturated fat content in grams per 100g
    
    Returns:
        tuple: (verdict, explanation, suggestions, plastic_warning)
            - verdict: str - "Healthy", "Moderate", or "Unhealthy"
            - explanation: str - Explanation of the verdict
            - suggestions: list - List of improvement suggestions
            - plastic_warning: str - Warning about plastic packaging (if applicable)
    """
    try:
        # Load model
        model = load_model()
        
        # Ensure inputs are numeric and non-negative
        sugar = float(sugar) if sugar else 0.0
        salt = float(salt) if salt else 0.0
        fat = float(fat) if fat else 0.0
        
        sugar = max(0.0, sugar)
        salt = max(0.0, salt)
        fat = max(0.0, fat)
        
        # Calculate total score
        total_score = sugar + salt + fat
        
        # Prepare features array (must match training data shape)
        features = np.array([[sugar, salt, fat, total_score]])
        
        # Predict
        prediction = model.predict(features)[0]
        
        # Map prediction to verdict
        verdict_map = {
            0: "Unhealthy",
            1: "Moderate",
            2: "Healthy"
        }
        verdict = verdict_map.get(prediction, "Unknown")
        
        # Generate explanation
        explanation = f"This food has {sugar:.1f}g sugar, {salt:.1f}g salt, "
        explanation += f"and {fat:.1f}g saturated fat per 100g (total score: {total_score:.1f}). "
        
        if verdict == "Healthy":
            explanation += "The nutrition values are within healthy ranges."
        elif verdict == "Moderate":
            explanation += "The nutrition values are moderate. Consider healthier alternatives."
        else:
            explanation += "The nutrition values are high and may pose health risks."
        
        # Generate suggestions
        suggestions = []
        
        if sugar > 15:
            suggestions.append(f"High sugar content ({sugar:.1f}g). Consider reducing sugar intake.")
        if salt > 1.5:
            suggestions.append(f"High salt content ({salt:.1f}g). Excessive salt can increase blood pressure.")
        if fat > 10:
            suggestions.append(f"High saturated fat ({fat:.1f}g). Choose foods with lower saturated fat.")
        
        if verdict == "Healthy" and len(suggestions) == 0:
            suggestions.append("Great choice! This food has balanced nutrition values.")
        elif len(suggestions) == 0:
            suggestions.append("Consider maintaining a balanced diet with variety.")
        
        # Plastic warning (simple heuristic - can be enhanced)
        plastic_warning = ""
        # For now, we'll keep it simple - no plastic warning unless needed
        # This can be enhanced later with barcode-based lookups
        
        return verdict, explanation, suggestions, plastic_warning
        
    except Exception as e:
        # Return safe defaults if anything goes wrong
        return (
            "Error",
            f"An error occurred during analysis: {str(e)}",
            ["Please check your input values and try again."],
            ""
        )
