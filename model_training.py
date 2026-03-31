"""
Student Performance Prediction System - Model Training Module
This script handles:
1. Loading and preprocessing the dataset
2. Training multiple ML models
3. Evaluating and comparing model performance
4. Saving the best performing model
"""

import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import warnings
warnings.filterwarnings('ignore')

def load_and_preprocess_data():
    """
    Load the student performance dataset and prepare it for training
    Returns: Features (X), Target (y), and feature names
    """
    print("📊 Loading dataset...")
    df = pd.read_csv('dataset/student_performance.csv')

    print(f"✓ Dataset loaded successfully: {len(df)} students")
    print(f"✓ Features: {df.shape[1] - 1}")

    # Drop student_id as it's not useful for prediction
    df = df.drop('student_id', axis=1)

    # Separate features and target
    X = df.drop('final_score', axis=1)
    y = df['final_score']

    feature_names = X.columns.tolist()

    return X, y, feature_names

def train_models(X_train, X_test, y_train, y_test):
    """
    Train multiple ML models and compare their performance
    Returns: Dictionary of trained models and their metrics
    """
    models = {
        'Linear Regression': LinearRegression(),
        'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10),
        'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42, max_depth=5)
    }

    results = {}

    print("\n🤖 Training models...")
    print("-" * 70)

    for name, model in models.items():
        print(f"\nTraining {name}...")

        # Train the model
        model.fit(X_train, y_train)

        # Make predictions
        train_pred = model.predict(X_train)
        test_pred = model.predict(X_test)

        # Calculate metrics
        train_r2 = r2_score(y_train, train_pred)
        test_r2 = r2_score(y_test, test_pred)
        test_rmse = np.sqrt(mean_squared_error(y_test, test_pred))
        test_mae = mean_absolute_error(y_test, test_pred)

        # Cross-validation score
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
        cv_mean = cv_scores.mean()

        results[name] = {
            'model': model,
            'train_r2': train_r2,
            'test_r2': test_r2,
            'rmse': test_rmse,
            'mae': test_mae,
            'cv_score': cv_mean
        }

        print(f"  ✓ Training R² Score: {train_r2:.4f}")
        print(f"  ✓ Testing R² Score: {test_r2:.4f}")
        print(f"  ✓ RMSE: {test_rmse:.4f}")
        print(f"  ✓ MAE: {test_mae:.4f}")
        print(f"  ✓ Cross-validation R² Score: {cv_mean:.4f}")

    print("\n" + "-" * 70)
    return results

def select_best_model(results):
    """
    Select the best performing model based on test R² score
    Returns: Best model name and the model object
    """
    best_model_name = max(results, key=lambda x: results[x]['test_r2'])
    best_model = results[best_model_name]['model']

    print(f"\n🏆 Best Model: {best_model_name}")
    print(f"   Test R² Score: {results[best_model_name]['test_r2']:.4f}")

    return best_model_name, best_model

def save_model_and_scaler(model, scaler, feature_names, model_results):
    """
    Save the trained model, scaler, feature names, and results to disk
    """
    model_data = {
        'model': model,
        'scaler': scaler,
        'feature_names': feature_names,
        'results': model_results
    }

    with open('saved_model.pkl', 'wb') as f:
        pickle.dump(model_data, f)

    print("\n💾 Model saved successfully as 'saved_model.pkl'")

def main():
    """
    Main function to orchestrate the training pipeline
    """
    print("=" * 70)
    print("  STUDENT PERFORMANCE PREDICTION - MODEL TRAINING")
    print("=" * 70)

    # Load and preprocess data
    X, y, feature_names = load_and_preprocess_data()

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    print(f"\n📈 Data split:")
    print(f"   Training set: {len(X_train)} samples")
    print(f"   Testing set: {len(X_test)} samples")

    # Scale the features
    print("\n⚙️  Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    print("   ✓ Features scaled successfully")

    # Train multiple models
    model_results = train_models(X_train_scaled, X_test_scaled, y_train, y_test)

    # Select the best model
    best_model_name, best_model = select_best_model(model_results)

    # Save model and scaler
    save_model_and_scaler(best_model, scaler, feature_names, model_results)

    print("\n✅ Training completed successfully!")
    print("=" * 70)

if __name__ == "__main__":
    main()
