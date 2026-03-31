"""
Student Performance Prediction System
A complete ML-based web application to predict student academic performance
and provide personalized improvement suggestions.
"""

import streamlit as st
import pandas as pd
import numpy as np
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.metrics import r2_score
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: 600;
        border: none;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .prediction-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #2196F3;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #e8f5e9;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3e0;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #ff9800;
        margin: 1rem 0;
    }
    h1 {
        color: #1e3a8a;
        font-weight: 700;
    }
    h2 {
        color: #1e40af;
        font-weight: 600;
    }
    h3 {
        color: #3b82f6;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

# Load the trained model
@st.cache_resource
def load_model():
    """Load the trained model and associated data"""
    try:
        with open('saved_model.pkl', 'rb') as f:
            model_data = pickle.load(f)
        return model_data
    except FileNotFoundError:
        st.error("❌ Model not found! Please train the model first by running 'python model_training.py'")
        st.stop()

# Load dataset for visualizations
@st.cache_data
def load_dataset():
    """Load the student performance dataset"""
    try:
        df = pd.read_csv('dataset/student_performance.csv')
        return df
    except FileNotFoundError:
        st.error("❌ Dataset not found!")
        st.stop()

def get_grade_category(score):
    """Convert numerical score to grade category"""
    if score >= 90:
        return "Excellent", "🌟", "#4CAF50"
    elif score >= 75:
        return "Good", "👍", "#2196F3"
    elif score >= 60:
        return "Average", "📚", "#FF9800"
    else:
        return "Poor", "⚠️", "#F44336"

def generate_recommendations(input_data, predicted_score):
    """Generate personalized improvement suggestions based on student data"""
    recommendations = []

    # Study hours recommendations
    if input_data['study_hours'] < 4:
        recommendations.append("📖 **Increase Study Hours**: Try to study at least 5-6 hours daily for better results.")
    elif input_data['study_hours'] >= 7:
        recommendations.append("⭐ **Great Study Routine**: Your study hours are excellent! Keep it up!")

    # Attendance recommendations
    if input_data['attendance'] < 75:
        recommendations.append("🎯 **Improve Attendance**: Aim for at least 85% attendance. Every class matters!")
    elif input_data['attendance'] >= 90:
        recommendations.append("✅ **Excellent Attendance**: Your attendance is outstanding!")

    # Sleep recommendations
    if input_data['sleep_hours'] < 6:
        recommendations.append("😴 **Get More Sleep**: Aim for 7-8 hours of sleep for better concentration and memory.")
    elif input_data['sleep_hours'] > 9:
        recommendations.append("⏰ **Optimize Sleep**: While sleep is important, 7-8 hours is ideal. Use extra time for studies.")

    # Assignment completion
    if input_data['assignment_completion'] < 80:
        recommendations.append("📝 **Complete Assignments**: Try to complete at least 90% of assignments on time.")
    elif input_data['assignment_completion'] >= 90:
        recommendations.append("💯 **Perfect Assignment Record**: Keep maintaining this excellent habit!")

    # Class participation
    if input_data['class_participation'] < 6:
        recommendations.append("🗣️ **Participate More**: Active participation helps in better understanding. Try to engage more in class.")
    elif input_data['class_participation'] >= 8:
        recommendations.append("🎤 **Great Participation**: Your active involvement is commendable!")

    # Internet access
    if input_data['internet_access'] == 0:
        recommendations.append("🌐 **Access Learning Resources**: Try to get internet access for online learning materials and resources.")

    # Extra classes
    if input_data['extra_classes_attended'] < 2 and predicted_score < 75:
        recommendations.append("📚 **Attend Extra Classes**: Consider attending extra classes or tutorials for difficult subjects.")
    elif input_data['extra_classes_attended'] >= 4:
        recommendations.append("🎓 **Dedicated Learner**: Your commitment to extra learning is impressive!")

    # Overall performance based recommendations
    if predicted_score >= 90:
        recommendations.append("🏆 **Outstanding Performance**: You're on track for excellent results! Consider mentoring peers.")
    elif predicted_score >= 75:
        recommendations.append("📈 **Good Progress**: You're doing well! A little more effort can push you to excellence.")
    elif predicted_score >= 60:
        recommendations.append("💪 **Room for Improvement**: Focus on consistent study habits and regular practice.")
    else:
        recommendations.append("🎯 **Action Required**: Consider meeting with professors and forming study groups for better support.")

    return recommendations

def get_sample_students():
    """Return sample student profiles for testing"""
    return {
        "Excellent Student": {
            'study_hours': 8.0,
            'attendance': 95,
            'internal_marks': 90,
            'sleep_hours': 8,
            'assignment_completion': 95,
            'previous_semester_marks': 88,
            'class_participation': 10,
            'internet_access': 1,
            'extra_classes_attended': 5
        },
        "Good Student": {
            'study_hours': 6.0,
            'attendance': 85,
            'internal_marks': 78,
            'sleep_hours': 7,
            'assignment_completion': 85,
            'previous_semester_marks': 75,
            'class_participation': 8,
            'internet_access': 1,
            'extra_classes_attended': 3
        },
        "Average Student": {
            'study_hours': 4.0,
            'attendance': 70,
            'internal_marks': 65,
            'sleep_hours': 6,
            'assignment_completion': 70,
            'previous_semester_marks': 65,
            'class_participation': 5,
            'internet_access': 1,
            'extra_classes_attended': 1
        },
        "Struggling Student": {
            'study_hours': 2.0,
            'attendance': 60,
            'internal_marks': 50,
            'sleep_hours': 5,
            'assignment_completion': 55,
            'previous_semester_marks': 55,
            'class_participation': 3,
            'internet_access': 0,
            'extra_classes_attended': 0
        }
    }

# Sidebar
with st.sidebar:
    st.image("https://images.pexels.com/photos/256490/pexels-photo-256490.jpeg?auto=compress&cs=tinysrgb&w=400", use_container_width=True)
    st.title("🎓 Navigation")

    page = st.radio(
        "Select Page:",
        ["🏠 Home", "📊 Predict Performance", "📈 Data Insights", "🤖 Model Comparison", "ℹ️ About Project"],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### 📚 Quick Info")
    st.info("This system uses Machine Learning to predict student performance and provide personalized recommendations.")

    st.markdown("---")
    st.markdown("### 👨‍💻 Developer")
    st.markdown("**Mini Project**  \nComputer Science Engineering")

# Load model and data
model_data = load_model()
df = load_dataset()

# Main content based on selected page
if page == "🏠 Home":
    st.title("🎓 Student Performance Prediction System")
    st.markdown("### Welcome to the AI-Powered Academic Performance Analyzer")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="metric-card">
            <h2>📊 100+</h2>
            <p>Students Analyzed</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="metric-card">
            <h2>🤖 3</h2>
            <p>ML Models Trained</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        best_r2 = max([v['test_r2'] for v in model_data['results'].values()])
        st.markdown(f"""
        <div class="metric-card">
            <h2>⭐ {best_r2:.2%}</h2>
            <p>Model Accuracy</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## 🎯 Project Objective")
        st.markdown("""
        <div class="info-box">
        This project aims to help students and educators predict academic performance
        based on various factors like study habits, attendance, and previous performance.
        The system provides:

        - **Accurate Predictions** using Machine Learning
        - **Personalized Recommendations** for improvement
        - **Data-Driven Insights** for better decision making
        - **Easy-to-Use Interface** for everyone
        </div>
        """, unsafe_allow_html=True)

        st.markdown("## 📋 Key Features")
        st.markdown("""
        - ✅ Multiple ML models (Linear Regression, Random Forest, Gradient Boosting)
        - ✅ Real-time performance prediction
        - ✅ Personalized improvement suggestions
        - ✅ Comprehensive data visualizations
        - ✅ Model performance comparison
        - ✅ Feature importance analysis
        - ✅ Sample student profiles for testing
        """)

    with col2:
        st.markdown("## 📊 Input Parameters")
        st.markdown("""
        The system analyzes the following factors:

        1. **Study Hours** - Daily study time
        2. **Attendance** - Class attendance percentage
        3. **Internal Marks** - Mid-term exam scores
        4. **Sleep Hours** - Average sleep duration
        5. **Assignment Completion** - Percentage of completed assignments
        6. **Previous Semester Marks** - Last semester's performance
        7. **Class Participation** - Engagement level (1-10)
        8. **Internet Access** - Availability of online resources
        9. **Extra Classes** - Additional learning sessions attended
        """)

        st.markdown("## 🚀 Get Started")
        st.markdown("""
        <div class="success-box">
        Click on <b>📊 Predict Performance</b> in the sidebar to start analyzing
        student performance and get personalized recommendations!
        </div>
        """, unsafe_allow_html=True)

elif page == "📊 Predict Performance":
    st.title("📊 Student Performance Prediction")
    st.markdown("### Enter student details to predict academic performance")

    # Sample student selector
    st.markdown("---")
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("#### 💡 Quick Test with Sample Profiles")
    with col2:
        sample_students = get_sample_students()
        selected_sample = st.selectbox(
            "Select Sample",
            ["Custom Input"] + list(sample_students.keys()),
            label_visibility="collapsed"
        )

    st.markdown("---")

    # Input form
    st.markdown("### 📝 Student Information Form")

    # Initialize input values
    if selected_sample == "Custom Input":
        default_values = {
            'study_hours': 5.0,
            'attendance': 80,
            'internal_marks': 70,
            'sleep_hours': 7,
            'assignment_completion': 80,
            'previous_semester_marks': 75,
            'class_participation': 7,
            'internet_access': 1,
            'extra_classes_attended': 2
        }
    else:
        default_values = sample_students[selected_sample]

    col1, col2, col3 = st.columns(3)

    with col1:
        study_hours = st.slider(
            "📖 Daily Study Hours",
            min_value=0.0,
            max_value=12.0,
            value=float(default_values['study_hours']),
            step=0.5,
            help="Average number of hours spent studying per day"
        )

        attendance = st.slider(
            "🎯 Attendance (%)",
            min_value=0,
            max_value=100,
            value=int(default_values['attendance']),
            help="Percentage of classes attended"
        )

        internal_marks = st.slider(
            "📄 Internal Marks",
            min_value=0,
            max_value=100,
            value=int(default_values['internal_marks']),
            help="Marks obtained in internal assessments"
        )

    with col2:
        sleep_hours = st.slider(
            "😴 Sleep Hours",
            min_value=3,
            max_value=12,
            value=int(default_values['sleep_hours']),
            help="Average hours of sleep per night"
        )

        assignment_completion = st.slider(
            "📝 Assignment Completion (%)",
            min_value=0,
            max_value=100,
            value=int(default_values['assignment_completion']),
            help="Percentage of assignments completed on time"
        )

        previous_marks = st.slider(
            "📚 Previous Semester Marks",
            min_value=0,
            max_value=100,
            value=int(default_values['previous_semester_marks']),
            help="Marks from previous semester"
        )

    with col3:
        class_participation = st.slider(
            "🗣️ Class Participation (1-10)",
            min_value=1,
            max_value=10,
            value=int(default_values['class_participation']),
            help="Level of participation in class discussions"
        )

        internet_access = st.selectbox(
            "🌐 Internet Access",
            options=[1, 0],
            format_func=lambda x: "Yes" if x == 1 else "No",
            index=0 if default_values['internet_access'] == 1 else 1,
            help="Access to internet for learning"
        )

        extra_classes = st.slider(
            "📚 Extra Classes Attended",
            min_value=0,
            max_value=10,
            value=int(default_values['extra_classes_attended']),
            help="Number of extra classes or tutorials attended"
        )

    st.markdown("---")

    # Prediction buttons
    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        predict_button = st.button("🎯 Predict Performance", type="primary", use_container_width=True)
    with col2:
        reset_button = st.button("🔄 Reset Form", use_container_width=True)

    if reset_button:
        st.rerun()

    if predict_button:
        # Prepare input data
        input_data = {
            'study_hours': study_hours,
            'attendance': attendance,
            'internal_marks': internal_marks,
            'sleep_hours': sleep_hours,
            'assignment_completion': assignment_completion,
            'previous_semester_marks': previous_marks,
            'class_participation': class_participation,
            'internet_access': internet_access,
            'extra_classes_attended': extra_classes
        }

        input_df = pd.DataFrame([input_data])

        # Scale and predict
        input_scaled = model_data['scaler'].transform(input_df)
        prediction = model_data['model'].predict(input_scaled)[0]

        # Ensure prediction is within valid range
        prediction = np.clip(prediction, 0, 100)

        grade, emoji, color = get_grade_category(prediction)

        # Display prediction
        st.markdown("---")
        st.markdown("## 🎯 Prediction Results")

        col1, col2 = st.columns([2, 3])

        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%);
                        padding: 2rem; border-radius: 15px; color: white; text-align: center;
                        box-shadow: 0 8px 16px rgba(0,0,0,0.2);">
                <h1 style="color: white; margin: 0; font-size: 4rem;">{emoji}</h1>
                <h2 style="color: white; margin: 0.5rem 0;">Predicted Score</h2>
                <h1 style="color: white; margin: 0; font-size: 3.5rem; font-weight: 700;">
                    {prediction:.1f}/100
                </h1>
                <h3 style="color: white; margin: 0.5rem 0;">Grade: {grade}</h3>
            </div>
            """, unsafe_allow_html=True)

            # Display input summary
            st.markdown("### 📋 Input Summary")
            summary_df = pd.DataFrame({
                'Parameter': ['Study Hours', 'Attendance', 'Internal Marks', 'Sleep Hours',
                             'Assignments', 'Prev. Marks', 'Participation', 'Internet', 'Extra Classes'],
                'Value': [f"{study_hours} hrs", f"{attendance}%", f"{internal_marks}",
                         f"{sleep_hours} hrs", f"{assignment_completion}%", f"{previous_marks}",
                         f"{class_participation}/10", "Yes" if internet_access else "No",
                         f"{extra_classes}"]
            })
            st.dataframe(summary_df, hide_index=True, use_container_width=True)

        with col2:
            st.markdown("### 💡 Personalized Recommendations")
            recommendations = generate_recommendations(input_data, prediction)

            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"""
                <div style="background-color: #f0f9ff; padding: 1rem; border-radius: 8px;
                            margin: 0.5rem 0; border-left: 4px solid #3b82f6;">
                    {rec}
                </div>
                """, unsafe_allow_html=True)

            # Performance interpretation
            st.markdown("### 📊 Performance Interpretation")
            if prediction >= 90:
                st.success("🌟 **Outstanding Performance!** This student is performing exceptionally well and is on track for excellent academic success.")
            elif prediction >= 75:
                st.info("👍 **Good Performance!** This student is doing well and with slight improvements can achieve excellence.")
            elif prediction >= 60:
                st.warning("📚 **Average Performance.** There's significant room for improvement. Focus on study habits and attendance.")
            else:
                st.error("⚠️ **Needs Attention!** This student requires immediate support and intervention to improve academic performance.")

elif page == "📈 Data Insights":
    st.title("📈 Data Insights & Visualizations")
    st.markdown("### Explore patterns and correlations in student performance data")

    # Dataset overview
    st.markdown("## 📊 Dataset Overview")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Students", len(df))
    with col2:
        st.metric("Average Score", f"{df['final_score'].mean():.1f}")
    with col3:
        st.metric("Highest Score", f"{df['final_score'].max():.1f}")
    with col4:
        st.metric("Lowest Score", f"{df['final_score'].min():.1f}")

    st.markdown("---")

    # Correlation heatmap
    st.markdown("## 🔥 Feature Correlation Heatmap")
    st.markdown("Shows how different factors are related to each other and the final score")

    fig, ax = plt.subplots(figsize=(12, 8))
    correlation = df.drop('student_id', axis=1).corr()
    sns.heatmap(correlation, annot=True, fmt='.2f', cmap='coolwarm', center=0,
                square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax)
    plt.title('Correlation Matrix of Student Performance Factors', fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    st.pyplot(fig)

    st.markdown("---")

    # Study hours vs Final score
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## 📖 Study Hours vs Final Score")
        fig = px.scatter(df, x='study_hours', y='final_score',
                        color='final_score', size='attendance',
                        color_continuous_scale='viridis',
                        title='Impact of Study Hours on Performance',
                        labels={'study_hours': 'Daily Study Hours',
                               'final_score': 'Final Score',
                               'attendance': 'Attendance %'},
                        hover_data=['attendance', 'internal_marks'])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("## 🎯 Attendance vs Final Score")
        fig = px.scatter(df, x='attendance', y='final_score',
                        color='final_score', size='study_hours',
                        color_continuous_scale='plasma',
                        title='Impact of Attendance on Performance',
                        labels={'attendance': 'Attendance %',
                               'final_score': 'Final Score',
                               'study_hours': 'Study Hours'},
                        hover_data=['study_hours', 'internal_marks'])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Distribution plots
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## 📊 Final Score Distribution")
        fig = px.histogram(df, x='final_score', nbins=20,
                          title='Distribution of Final Scores',
                          labels={'final_score': 'Final Score', 'count': 'Number of Students'},
                          color_discrete_sequence=['#4CAF50'])
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("## 😴 Sleep Hours vs Performance")
        avg_by_sleep = df.groupby('sleep_hours')['final_score'].mean().reset_index()
        fig = px.bar(avg_by_sleep, x='sleep_hours', y='final_score',
                    title='Average Score by Sleep Hours',
                    labels={'sleep_hours': 'Sleep Hours', 'final_score': 'Average Score'},
                    color='final_score', color_continuous_scale='blues')
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Box plots
    st.markdown("## 📦 Performance by Internet Access")
    fig = px.box(df, x='internet_access', y='final_score',
                color='internet_access',
                title='Final Score Distribution by Internet Access',
                labels={'internet_access': 'Internet Access', 'final_score': 'Final Score'},
                category_orders={'internet_access': [0, 1]})
    fig.update_xaxes(ticktext=['No', 'Yes'], tickvals=[0, 1])
    fig.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

elif page == "🤖 Model Comparison":
    st.title("🤖 Model Comparison & Performance")
    st.markdown("### Compare different machine learning models used in this project")

    results = model_data['results']

    # Model metrics comparison
    st.markdown("## 📊 Model Performance Metrics")

    metrics_data = []
    for model_name, metrics in results.items():
        metrics_data.append({
            'Model': model_name,
            'Train R²': f"{metrics['train_r2']:.4f}",
            'Test R²': f"{metrics['test_r2']:.4f}",
            'RMSE': f"{metrics['rmse']:.4f}",
            'MAE': f"{metrics['mae']:.4f}",
            'CV Score': f"{metrics['cv_score']:.4f}"
        })

    metrics_df = pd.DataFrame(metrics_data)
    st.dataframe(metrics_df, hide_index=True, use_container_width=True)

    # Highlight best model
    best_model = max(results, key=lambda x: results[x]['test_r2'])
    st.markdown(f"""
    <div class="success-box">
        <h3>🏆 Best Performing Model: {best_model}</h3>
        <p>Selected based on highest Test R² Score: {results[best_model]['test_r2']:.4f}</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Visual comparison
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## 📈 R² Score Comparison")
        comparison_data = []
        for model_name, metrics in results.items():
            comparison_data.append({'Model': model_name, 'Score Type': 'Train R²', 'Score': metrics['train_r2']})
            comparison_data.append({'Model': model_name, 'Score Type': 'Test R²', 'Score': metrics['test_r2']})

        comparison_df = pd.DataFrame(comparison_data)
        fig = px.bar(comparison_df, x='Model', y='Score', color='Score Type',
                    barmode='group', title='Train vs Test R² Scores',
                    color_discrete_sequence=['#3b82f6', '#10b981'])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("## 📉 Error Metrics Comparison")
        error_data = []
        for model_name, metrics in results.items():
            error_data.append({'Model': model_name, 'Metric': 'RMSE', 'Value': metrics['rmse']})
            error_data.append({'Model': model_name, 'Metric': 'MAE', 'Value': metrics['mae']})

        error_df = pd.DataFrame(error_data)
        fig = px.bar(error_df, x='Model', y='Value', color='Metric',
                    barmode='group', title='RMSE and MAE Comparison',
                    color_discrete_sequence=['#ef4444', '#f59e0b'])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # Feature importance (for tree-based models)
    st.markdown("## 🎯 Feature Importance Analysis")
    st.markdown("Shows which factors have the most impact on predicting student performance")

    model = model_data['model']
    feature_names = model_data['feature_names']

    if hasattr(model, 'feature_importances_'):
        importances = model.feature_importances_
        feature_imp_df = pd.DataFrame({
            'Feature': feature_names,
            'Importance': importances
        }).sort_values('Importance', ascending=True)

        fig = px.bar(feature_imp_df, x='Importance', y='Feature',
                    orientation='h',
                    title=f'Feature Importance - {best_model}',
                    color='Importance',
                    color_continuous_scale='viridis')
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        <div class="info-box">
            <strong>💡 Interpretation:</strong> Features with higher importance values have more
            influence on the final prediction. Focus on improving these factors for better academic performance.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Feature importance is only available for tree-based models (Random Forest, Gradient Boosting)")

    st.markdown("---")

    # Model explanations
    st.markdown("## 📚 Model Descriptions")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        <div class="info-box">
            <h4>📊 Linear Regression</h4>
            <p><strong>Type:</strong> Simple linear model</p>
            <p><strong>Pros:</strong> Fast, interpretable, works well for linear relationships</p>
            <p><strong>Cons:</strong> May underfit complex patterns</p>
            <p><strong>Use Case:</strong> Baseline model for comparison</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("""
        <div class="info-box">
            <h4>🌳 Random Forest</h4>
            <p><strong>Type:</strong> Ensemble of decision trees</p>
            <p><strong>Pros:</strong> Handles non-linear relationships, robust to outliers</p>
            <p><strong>Cons:</strong> Less interpretable, can overfit</p>
            <p><strong>Use Case:</strong> Good for complex patterns</p>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown("""
        <div class="info-box">
            <h4>⚡ Gradient Boosting</h4>
            <p><strong>Type:</strong> Sequential tree ensemble</p>
            <p><strong>Pros:</strong> High accuracy, handles complex relationships</p>
            <p><strong>Cons:</strong> Slower training, requires tuning</p>
            <p><strong>Use Case:</strong> Best for maximum accuracy</p>
        </div>
        """, unsafe_allow_html=True)

elif page == "ℹ️ About Project":
    st.title("ℹ️ About This Project")
    st.markdown("### Student Performance Prediction System - Complete Documentation")

    # Project overview
    st.markdown("""
    <div class="info-box">
        <h3>🎯 Project Overview</h3>
        <p>
        This is a complete Machine Learning mini-project designed for Computer Science Engineering students.
        It demonstrates the end-to-end process of building an AI/ML application from data collection to deployment.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Technologies used
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## 🛠️ Technologies Used")
        st.markdown("""
        - **Python** - Programming language
        - **Streamlit** - Web application framework
        - **Pandas** - Data manipulation
        - **NumPy** - Numerical computing
        - **Scikit-learn** - Machine learning
        - **Matplotlib/Seaborn** - Data visualization
        - **Plotly** - Interactive charts
        """)

        st.markdown("## 📊 Machine Learning Models")
        st.markdown("""
        1. **Linear Regression** - Baseline model
        2. **Random Forest** - Ensemble learning
        3. **Gradient Boosting** - Advanced ensemble
        """)

    with col2:
        st.markdown("## ✨ Key Features")
        st.markdown("""
        - ✅ Multi-model training and comparison
        - ✅ Real-time performance prediction
        - ✅ Personalized recommendations
        - ✅ Interactive visualizations
        - ✅ Feature importance analysis
        - ✅ Sample student profiles
        - ✅ Professional UI/UX design
        - ✅ Model persistence
        """)

        st.markdown("## 🎓 Learning Outcomes")
        st.markdown("""
        - Data preprocessing techniques
        - Model training and evaluation
        - Feature engineering
        - Model comparison and selection
        - Web application development
        - Data visualization best practices
        """)

    st.markdown("---")

    # How it works
    st.markdown("## 🔄 How It Works")

    workflow = """
    ```
    1. DATA COLLECTION
       ↓
    2. DATA PREPROCESSING
       ↓
    3. FEATURE SCALING
       ↓
    4. MODEL TRAINING
       ├── Linear Regression
       ├── Random Forest
       └── Gradient Boosting
       ↓
    5. MODEL EVALUATION
       ↓
    6. BEST MODEL SELECTION
       ↓
    7. MODEL DEPLOYMENT
       ↓
    8. PREDICTION & RECOMMENDATIONS
    ```
    """
    st.code(workflow)

    st.markdown("---")

    # Project structure
    st.markdown("## 📁 Project Structure")
    st.code("""
    student-performance-prediction/
    ├── app.py                          # Main Streamlit application
    ├── model_training.py               # Model training script
    ├── requirements.txt                # Python dependencies
    ├── README.md                       # Project documentation
    ├── saved_model.pkl                 # Trained model (generated)
    └── dataset/
        └── student_performance.csv     # Student data
    """, language="text")

    st.markdown("---")

    # Future enhancements
    st.markdown("## 🚀 Possible Future Enhancements")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### Technical Improvements
        - Deep Learning models (Neural Networks)
        - Hyperparameter tuning with GridSearchCV
        - Cross-validation improvements
        - Real-time data integration
        - Database integration (PostgreSQL/MongoDB)
        - REST API development
        """)

    with col2:
        st.markdown("""
        ### Feature Additions
        - Student progress tracking over time
        - Comparison with peer performance
        - Subject-wise performance analysis
        - Alert system for at-risk students
        - PDF report generation
        - Email notifications
        """)

    st.markdown("---")

    # Viva questions
    st.markdown("## 🎤 Common Viva Questions & Answers")

    with st.expander("1. What is the objective of your project?"):
        st.markdown("""
        The objective is to develop an intelligent system that predicts student academic performance
        using machine learning algorithms. The system analyzes various factors like study hours,
        attendance, and previous marks to forecast final scores and provide personalized improvement
        recommendations.
        """)

    with st.expander("2. Why did you choose these specific ML algorithms?"):
        st.markdown("""
        - **Linear Regression**: Provides a baseline and is easy to interpret
        - **Random Forest**: Handles non-linear relationships and is robust to outliers
        - **Gradient Boosting**: Often provides the best accuracy for tabular data

        By using multiple models, we can compare performance and select the best one.
        """)

    with st.expander("3. How do you evaluate model performance?"):
        st.markdown("""
        We use multiple metrics:
        - **R² Score**: Measures how well the model explains variance (0-1, higher is better)
        - **RMSE**: Root Mean Squared Error (lower is better)
        - **MAE**: Mean Absolute Error (lower is better)
        - **Cross-validation**: 5-fold CV to ensure model generalization
        """)

    with st.expander("4. What is the accuracy of your model?"):
        best_model_name = max(results, key=lambda x: results[x]['test_r2'])
        best_r2 = results[best_model_name]['test_r2']
        st.markdown(f"""
        The best performing model is **{best_model_name}** with an R² score of **{best_r2:.4f}**
        ({best_r2*100:.2f}% accuracy). This means the model can explain {best_r2*100:.2f}% of the
        variance in student performance.
        """)

    with st.expander("5. How do you handle overfitting?"):
        st.markdown("""
        - Train-test split (80-20) to evaluate on unseen data
        - Cross-validation to ensure consistency
        - Regularization in models (max_depth, n_estimators limits)
        - Compare train vs test scores to detect overfitting
        """)

    with st.expander("6. What are the real-world applications?"):
        st.markdown("""
        - **Early intervention**: Identify struggling students early
        - **Resource allocation**: Focus support where needed
        - **Personalized learning**: Tailor recommendations to each student
        - **Academic counseling**: Data-driven guidance
        - **Policy making**: Understand factors affecting performance
        """)

    with st.expander("7. How can this project be improved?"):
        st.markdown("""
        - Include more features (socio-economic factors, health data)
        - Use deep learning for complex patterns
        - Real-time integration with student management systems
        - Mobile application development
        - Multi-year trend analysis
        - Subject-specific predictions
        """)

    st.markdown("---")

    # Credits
    st.markdown("""
    <div class="success-box">
        <h3>✅ Project Completion Status</h3>
        <p>
        This project is complete and ready for demonstration. All modules are functional,
        well-documented, and tested. The code follows best practices and is suitable for
        academic submission and viva presentation.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background-color: #f8fafc; border-radius: 10px;">
        <h4>Made with ❤️ for Computer Science Engineering Students</h4>
        <p>Good luck with your presentation! 🎓</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #64748b; padding: 1rem;">
    <p>Student Performance Prediction System | AI/ML Mini Project | 2024</p>
</div>
""", unsafe_allow_html=True)
