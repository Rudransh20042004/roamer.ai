# 🚀 Tour Guide App Deployment Guide

## Overview
This guide will help you deploy your AI-powered tour guide app using **Vercel** (frontend) and **Railway** (backend).

## Prerequisites
- GitHub account
- Vercel account (free)
- Railway account (free)
- Your API keys ready

## Step 1: Deploy Backend to Railway

### 1.1 Push to GitHub
```bash
cd /Users/rudranshagrawal/Desktop/HackH2024
git init
git add .
git commit -m "Initial commit for deployment"
git branch -M main
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

### 1.2 Deploy to Railway
1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect it's a Python project

### 1.3 Set Environment Variables in Railway
In your Railway dashboard, go to Variables tab and add:
```
GENAI_API_KEY=AIzaSyBZIQRj8ZPbIDapJ3VbG3rYUTq7uXkI2tk
ELEVEN_API_KEY=sk_f97508bc90abc6598e9eab4339e1d1ba212a05e71c030533
MAPS_API_KEY=AlzaSyD78F2NJJFgkamEK9gOevznVBAN0HcBо3Е
```

### 1.4 Get Backend URL
After deployment, Railway will give you a URL like: `https://your-app-name.railway.app`

## Step 2: Deploy Frontend to Vercel

### 2.1 Create Environment File
```bash
cd frontend
cp env.example .env.local
```

Edit `.env.local`:
```
VITE_API_URL=https://your-app-name.railway.app
```

### 2.2 Deploy to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign in with GitHub
3. Click "New Project" → Import your repository
4. Set Root Directory to `frontend`
5. Vercel will auto-detect it's a Vite project
6. Add environment variable:
   - Name: `VITE_API_URL`
   - Value: `https://your-app-name.railway.app`

### 2.3 Build Settings
Vercel should auto-configure:
- Build Command: `npm run build`
- Output Directory: `dist`
- Install Command: `npm install`

## Step 3: Test Your Deployment

### 3.1 Test Backend
Visit: `https://your-app-name.railway.app/health`
Should return: `{"status": "healthy", "message": "Tour Guide API is running"}`

### 3.2 Test Frontend
Visit your Vercel URL and test:
- Location detection
- Audio generation
- Map functionality

## Step 4: Update Environment Variables

If you change your backend URL, update the frontend:
1. In Vercel dashboard → Settings → Environment Variables
2. Update `VITE_API_URL` to your new backend URL
3. Redeploy the frontend

## Troubleshooting

### Backend Issues
- Check Railway logs for errors
- Verify all environment variables are set
- Ensure `requirements.txt` is in the backend folder

### Frontend Issues
- Check browser console for API errors
- Verify `VITE_API_URL` is correct
- Ensure CORS is enabled in backend (already configured)

### CORS Issues
If you get CORS errors, the backend already has `flask-cors` configured.

## Production Considerations

### Security
- Move API keys to environment variables
- Consider rate limiting for API endpoints
- Add input validation

### Performance
- Add caching for audio generation
- Implement location-based caching
- Consider CDN for static assets

## Cost Estimation
- **Vercel**: Free tier includes 100GB bandwidth
- **Railway**: Free tier includes $5 credit monthly
- **Total**: Should be free for moderate usage

## Support
If you encounter issues:
1. Check Railway and Vercel logs
2. Verify environment variables
3. Test API endpoints directly
4. Check browser console for frontend errors

Your tour guide app should now be live! 🎉
