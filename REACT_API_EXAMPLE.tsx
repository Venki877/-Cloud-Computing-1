// Example React component for making predictions via API
// Place this in your src/ folder

import { useState } from 'react';

export default function PredictionForm() {
  const [formData, setFormData] = useState({
    study_hours: 0,
    attendance: 0,
    internal_marks: 0,
    sleep_hours: 0,
    assignment_completion: 0,
    previous_marks: 0,
    class_participation: 0,
    internet_access: false,
    extra_classes: 0,
  });

  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : parseFloat(value) || 0
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Use relative URL which will work on Vercel
      const apiUrl = process.env.VITE_API_URL || '';
      const response = await fetch(`${apiUrl}/api/predict`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
      }

      const data = await response.json();
      setPrediction(data);
    } catch (err) {
      setError(err.message);
      console.error('Prediction error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="prediction-form">
      <h2>Student Performance Predictor</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Study Hours (0-12)</label>
          <input
            type="number"
            name="study_hours"
            min="0"
            max="12"
            step="0.5"
            value={formData.study_hours}
            onChange={handleInputChange}
          />
        </div>

        <div className="form-group">
          <label>Attendance (%)</label>
          <input
            type="number"
            name="attendance"
            min="0"
            max="100"
            value={formData.attendance}
            onChange={handleInputChange}
          />
        </div>

        <div className="form-group">
          <label>Internal Marks (0-100)</label>
          <input
            type="number"
            name="internal_marks"
            min="0"
            max="100"
            value={formData.internal_marks}
            onChange={handleInputChange}
          />
        </div>

        <div className="form-group">
          <label>Sleep Hours (3-12)</label>
          <input
            type="number"
            name="sleep_hours"
            min="3"
            max="12"
            step="0.5"
            value={formData.sleep_hours}
            onChange={handleInputChange}
          />
        </div>

        <div className="form-group">
          <label>Assignment Completion (%)</label>
          <input
            type="number"
            name="assignment_completion"
            min="0"
            max="100"
            value={formData.assignment_completion}
            onChange={handleInputChange}
          />
        </div>

        <div className="form-group">
          <label>Previous Semester Marks (0-100)</label>
          <input
            type="number"
            name="previous_marks"
            min="0"
            max="100"
            value={formData.previous_marks}
            onChange={handleInputChange}
          />
        </div>

        <div className="form-group">
          <label>Class Participation (1-10)</label>
          <input
            type="number"
            name="class_participation"
            min="1"
            max="10"
            value={formData.class_participation}
            onChange={handleInputChange}
          />
        </div>

        <div className="form-group">
          <label>
            <input
              type="checkbox"
              name="internet_access"
              checked={formData.internet_access}
              onChange={handleInputChange}
            />
            Internet Access
          </label>
        </div>

        <div className="form-group">
          <label>Extra Classes Attended (0-10)</label>
          <input
            type="number"
            name="extra_classes"
            min="0"
            max="10"
            value={formData.extra_classes}
            onChange={handleInputChange}
          />
        </div>

        <button type="submit" disabled={loading}>
          {loading ? 'Predicting...' : 'Predict Performance'}
        </button>
      </form>

      {error && (
        <div className="error-message">
          Error: {error}
        </div>
      )}

      {prediction && (
        <div className="prediction-result">
          <h3>Prediction Result</h3>
          <p>Predicted Score: <strong>{prediction.prediction.toFixed(2)}</strong></p>
          <p>Grade: <strong>{prediction.grade}</strong></p>
        </div>
      )}
    </div>
  );
}
