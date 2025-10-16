# Deployment Guide for AI Raitha Mitra

## Deploy to Render

### Prerequisites
1. GitHub account with your code pushed
2. Render account (free tier available)
3. Gemini API key from Google AI Studio

### Step-by-Step Deployment

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for Render deployment"
   git push origin main
   ```

2. **Create Render Service**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Choose your repository

3. **Configure Render Settings**
   - **Name**: `ai-raitha-mitra` (or your preferred name)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`
   - **Python Version**: `3.11.0`

4. **Set Environment Variables**
   In Render dashboard, add these environment variables:
   - `GEMINI_API_KEY`: Your Google Gemini API key
   - `OPENWEATHER_API_KEY`: Your OpenWeather API key (optional)
   - `FLASK_DEBUG`: `False`

5. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment to complete (5-10 minutes)
   - Your app will be available at: `https://your-app-name.onrender.com`

### Getting API Keys

#### Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Copy and add to Render environment variables

#### OpenWeather API Key (Optional)
1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for free account
3. Get API key from dashboard
4. Add to Render environment variables

### Important Notes

- **Large Model File**: Your 155MB model file is handled by Git LFS
- **Free Tier Limits**: Render free tier has some limitations
- **Cold Starts**: Free tier apps may sleep after inactivity
- **Database**: Uses SQLite (file-based) - data persists between deployments

### Troubleshooting

1. **Build Fails**: Check requirements.txt and Python version
2. **App Won't Start**: Check logs in Render dashboard
3. **Model Loading Issues**: Ensure Git LFS is properly configured
4. **API Errors**: Verify environment variables are set correctly

### Demo Credentials
- Email: `demo@raithamitra.com`
- Mobile: `9876543210`
- Password: `123456`