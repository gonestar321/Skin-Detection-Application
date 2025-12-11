# 🚀 Deployment Guide

This guide covers deploying the Skin Disease Classification app with:
- **Frontend**: Vercel (React + Vite)
- **Backend**: Render (Flask + TensorFlow)

---

## Part 1: Deploy Backend to Render

### Step 1: Create a Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub for easy repository access

### Step 2: Create a New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `Skin-Disease-Classification`
3. Configure the service:

| Setting | Value |
|---------|-------|
| **Name** | `skin-disease-api` (or your preferred name) |
| **Region** | Choose closest to your users |
| **Root Directory** | `backend` |
| **Runtime** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT` |

### Step 3: Configure Instance Type
- **Free tier**: Good for testing (may spin down after inactivity)
- **Starter ($7/month)**: Recommended for production (always on)

> ⚠️ **Important**: Free tier instances spin down after 15 minutes of inactivity. First request after spin-down takes ~30 seconds.

### Step 4: Add Environment Variables (Optional)
If you need any environment variables:
1. Go to **Environment** tab
2. Add key-value pairs as needed

### Step 5: Deploy!
1. Click **"Create Web Service"**
2. Wait for the build to complete (5-10 minutes first time due to TensorFlow)
3. Your backend URL will be: `https://skin-disease-api.onrender.com`

### Step 6: Verify Backend
Test your API:
```bash
curl https://your-app-name.onrender.com/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "detectable_diseases": 8
}
```

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Create a Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub

### Step 2: Import Your Project
1. Click **"Add New..."** → **"Project"**
2. Import your GitHub repository: `Skin-Disease-Classification`

### Step 3: Configure Project Settings

| Setting | Value |
|---------|-------|
| **Framework Preset** | Vite |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` |
| **Output Directory** | `dist` |
| **Install Command** | `npm install` |

### Step 4: Add Environment Variables ⚠️ CRITICAL
1. Expand **"Environment Variables"**
2. Add the following:

| Key | Value |
|-----|-------|
| `VITE_API_URL` | `https://your-render-app.onrender.com` |

> 📝 Replace `your-render-app` with your actual Render app name from Part 1.

### Step 5: Deploy!
1. Click **"Deploy"**
2. Wait for build to complete (usually 1-2 minutes)
3. Your frontend URL: `https://your-app.vercel.app`

---

## 🔄 Quick Deploy Checklist

### Before Deploying:
- [ ] Push all code to GitHub
- [ ] Ensure `efficientnet_model.h5` or `skin_disease_model.h5` is in `backend/models/`
- [ ] Verify `requirements.txt` includes `gunicorn`
- [ ] Verify `Procfile` exists in `backend/`

### Deploy Order:
1. [ ] Deploy backend to Render first
2. [ ] Get your Render URL (e.g., `https://skin-disease-api.onrender.com`)
3. [ ] Deploy frontend to Vercel with `VITE_API_URL` environment variable

### After Deploying:
- [ ] Test backend health: `curl https://your-backend.onrender.com/api/health`
- [ ] Test frontend: Visit your Vercel URL
- [ ] Test full flow: Upload an image and verify prediction works

---

## 🔧 Troubleshooting

### Backend Issues

**Build fails with memory error:**
- TensorFlow is large. Use Render's paid tier for more resources.

**Model not found error:**
- Ensure the model file is committed to Git (check `.gitignore`)
- Verify path in `app.py` matches your model filename

**CORS errors:**
- The backend already has `flask-cors` configured
- Verify `CORS(app)` is in `app.py`

### Frontend Issues

**API calls failing:**
- Verify `VITE_API_URL` is set correctly in Vercel
- Check browser console for errors
- Ensure backend is running (not spun down on free tier)

**Environment variable not working:**
- Vite requires `VITE_` prefix for env vars
- Redeploy after adding/changing env vars

---

## 📁 Files Created for Deployment

```
Skin-Disease-Classification/
├── backend/
│   ├── Procfile              # Tells Render how to run the app
│   └── requirements.txt      # Added gunicorn
└── frontend/
    ├── vercel.json           # Vercel configuration
    ├── .env.example          # Example environment file
    └── src/
        └── App.jsx           # Updated with API_BASE_URL
```

---

## 🌐 Final URLs

After deployment, you'll have:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-backend.onrender.com`

---

## 💡 Tips for Production

1. **Use paid tiers** for always-on backends
2. **Set up custom domains** for professional URLs
3. **Monitor errors** using Render and Vercel dashboards
4. **Consider model optimization** - TensorFlow Lite for faster cold starts
