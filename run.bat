@echo off
echo ======================================
echo   Student Performance Prediction
echo   Starting Application...
echo ======================================
echo.

if not exist "saved_model.pkl" (
    echo Warning: Model not found! Training models first...
    echo.
    python model_training.py
    echo.
)

echo Launching Streamlit application...
echo The app will open in your browser at http://localhost:8501
echo.

python -m streamlit run app.py
