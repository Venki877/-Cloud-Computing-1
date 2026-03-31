#!/bin/bash

echo "======================================"
echo "  Student Performance Prediction"
echo "  Starting Application..."
echo "======================================"
echo ""

if [ ! -f "saved_model.pkl" ]; then
    echo "⚠️  Model not found! Training models first..."
    echo ""
    python3 model_training.py
    echo ""
fi

echo "🚀 Launching Streamlit application..."
echo "📱 The app will open in your browser at http://localhost:8501"
echo ""

python3 -m streamlit run app.py
