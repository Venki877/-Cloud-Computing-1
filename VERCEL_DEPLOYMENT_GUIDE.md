# Deploy to Vercel - Complete Step-by-Step Guide

## 🚀 Quick Start (5 minutes)

### 1. Train Your Model Locally

```bash
cd project
python model_training.py
```

This creates `saved_model.pkl` which will be deployed with your app.

### 2. Initialize Git

```bash
git init
git add .
git commit -m "Initial commit"
```

### 3. Push to GitHub

```bash
# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/student-performance-prediction.git
git branch -M main
git push -u origin main
```

### 4. Deploy on Vercel

**Option A: Using Vercel Dashboard (Easiest)**

1. Go to https://vercel.com/new
2. Click "Import Git Repository"
3. Select your GitHub repository
4. Select "Other" as framework
5. Leave Build Command empty (default works fine)
6. Click "Deploy"

**Option B: Using Vercel CLI**

```bash
# Install Vercel CLI
npm install -g vercel

# Login
vercel login

# Deploy
vercel
```

## ⚙️ Configuration Details

### What Gets Deployed

- **Frontend**: React/Vite app (built and optimized)
- **Backend**: Python Flask API with ML predictions (serverless functions)
- **Model**: `saved_model.pkl` (pre-trained ML model)

### Build Process

Vercel automatically:
1. Installs Node.js dependencies from `package.json`
2. Builds the Vite React app to `dist/`
3. Serves static files
4. Routes `/api/*` requests to Python serverless functions
5. Python dependencies installed automatically for API

### Important: Pre-trained Model

**Your ML model must be pre-trained locally and committed to Git:**

```bash
# Do this BEFORE deploying
python model_training.py
git add saved_model.pkl
git commit -m "Add pre-trained model"
git push
```

Vercel will NOT train the model during deployment (to avoid timeout). The training happens locally, and `saved_model.pkl` is deployed with your code.

### Environment Variables

No additional environment variables needed for basic setup.

Optional environment variables (set in Vercel Dashboard):
```
FLASK_ENV=production
DEBUG=false
```

## 📝 Project Structure for Vercel

```
project/
├── api/
│   └── index.py           # Python API endpoint
├── src/
│   ├── App.tsx            # Main React component
│   ├── index.css
│   └── main.tsx
├── dataset/
│   └── student_performance.csv
├── public/
├── vercel.json            # Vercel configuration
├── package.json           # Frontend dependencies
├── requirements.txt       # Python dependencies
├── model_training.py      # ML training script
├── saved_model.pkl        # Trained model (crucial!)
├── tsconfig.json
├── vite.config.ts
└── .gitignore
```

## 🔧 How the API Works

### Endpoint: `/api/predict`

**Request:**
```json
{
  "study_hours": 8,
  "attendance": 85,
  "internal_marks": 78,
  "sleep_hours": 7,
  "assignment_completion": 90,
  "previous_marks": 82,
  "class_participation": 8,
  "internet_access": true,
  "extra_classes": 2
}
```

**Response:**
```json
{
  "prediction": 85.3,
  "grade": "Good",
  "success": true
}
```

### Testing Locally

```bash
# Test API health
curl http://localhost:5000/api/health

# Test prediction
curl -X POST http://localhost:5000/api/predict \
  -H "Content-Type: application/json" \
  -d '{"study_hours": 8, "attendance": 85, ...}'
```

## 🐛 Troubleshooting

### Issue: "saved_model.pkl not found"

**Solution:**
```bash
# Train the model locally
python model_training.py

# Ensure it's in git
git add saved_model.pkl
git commit -m "Add trained model"
git push
```

### Issue: "ModuleNotFoundError: No module named 'flask'"

**Solution:**
Flask should be installed automatically. If not:
```bash
pip install -r requirements.txt
vercel redeploy
```

### Issue: Build timeout

**Solution:**
- Ensure `saved_model.pkl` is already created (pre-trained)
- Reduce dataset size if training during build
- Increase timeout in `vercel.json` if needed

### Issue: API returns 500 error

**Check logs:**
```bash
vercel logs --tail
```

**Common causes:**
- Model file not found
- Incorrect feature input format
- Missing dependencies

## 🎯 Next Steps After Deployment

### 1. Update React Components

Replace API calls to use your Vercel URL:

```javascript
const response = await fetch('/api/predict', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify(formData)
});
```

### 2. Test Your Live App

Once deployed, visit: `https://your-project.vercel.app`

### 3. Monitor Performance

On Vercel dashboard:
- View logs: `vercel logs --tail`
- Check analytics
- Monitor function duration

## 📊 Performance Tips

1. **Model Size**: Keep `saved_model.pkl` under 50MB
2. **API Response Time**: Typically <200ms for predictions
3. **Cold Start**: First request may take 1-2 seconds

## 🔐 Security

Before deploying:
- [ ] Remove any credentials from code
- [ ] Add `.env.local` containing sensitive data
- [ ] Don't commit API keys or passwords

## 🚀 Advanced: Custom Domain

1. Go to Vercel Project Settings → Domains
2. Add your custom domain
3. Follow DNS configuration instructions

## 📱 Using from Mobile

Your Vercel deployment is automatically mobile-friendly!

Test by opening `https://your-project.vercel.app` on mobile.

## 💡 Additional Resources

- [Vercel Docs](https://vercel.com/docs)
- [Python on Vercel](https://vercel.com/docs/concepts/serverless-functions/supported-languages#python)
- [Flask Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)

## ❓ Need Help?

1. Check build logs: `vercel logs`
2. Review error messages in Vercel dashboard
3. Test API locally first: `python api/index.py`
4. Check if model file exists: `ls -la saved_model.pkl`

---

**Happy deploying! 🎉**
