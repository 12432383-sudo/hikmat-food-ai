"""
train_model.py
Generates synthetic training data and trains a RandomForestClassifier
for food health analysis based on nutrition values.
"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
import os

def generate_synthetic_data(n_samples=1000):
    """
    Generate synthetic nutrition data for training.
    
    Features:
    - sugar: 0-50g per 100g
    - salt: 0-5g per 100g
    - saturated_fat: 0-30g per 100g
    - total_score: sum of the above
    
    Labels:
    - 0: Unhealthy (high values)
    - 1: Moderate (medium values)
    - 2: Healthy (low values)
    """
    np.random.seed(42)
    
    # Generate features
    sugar = np.random.uniform(0, 50, n_samples)
    salt = np.random.uniform(0, 5, n_samples)
    saturated_fat = np.random.uniform(0, 30, n_samples)
    total_score = sugar + salt + saturated_fat
    
    # Create labels based on thresholds
    # Healthy: low total score (< 20)
    # Moderate: medium total score (20-40)
    # Unhealthy: high total score (> 40)
    labels = np.zeros(n_samples, dtype=int)
    labels[total_score < 20] = 2  # Healthy
    labels[(total_score >= 20) & (total_score <= 40)] = 1  # Moderate
    labels[total_score > 40] = 0  # Unhealthy
    
    # Add some noise to make it more realistic
    noise_factor = 0.1
    sugar += np.random.normal(0, sugar * noise_factor)
    salt += np.random.normal(0, salt * noise_factor)
    saturated_fat += np.random.normal(0, saturated_fat * noise_factor)
    
    # Ensure non-negative values
    sugar = np.maximum(0, sugar)
    salt = np.maximum(0, salt)
    saturated_fat = np.maximum(0, saturated_fat)
    total_score = sugar + salt + saturated_fat
    
    # Create DataFrame
    data = pd.DataFrame({
        'sugar': sugar,
        'salt': salt,
        'saturated_fat': saturated_fat,
        'total_score': total_score,
        'label': labels
    })
    
    return data

def train_model():
    """Train the RandomForestClassifier and save it as food_model.pkl"""
    
    print("Generating synthetic training data...")
    data = generate_synthetic_data(n_samples=1000)
    
    # Prepare features and labels
    X = data[['sugar', 'salt', 'saturated_fat', 'total_score']].values
    y = data['label'].values
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print("Training RandomForestClassifier...")
    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=1  # Set to 1 to avoid multiprocessing issues
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"Training accuracy: {train_score:.4f}")
    print(f"Test accuracy: {test_score:.4f}")
    
    # Save model
    model_path = 'food_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Model saved to {model_path}")
    print("Training complete!")
    
    return model

if __name__ == "__main__":
    train_model()
