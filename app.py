import os
import json
import base64
import io
import re
from datetime import datetime, timedelta
import google.generativeai as genai
from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import tensorflow as tf
from PIL import Image
import numpy as np
from database import DatabaseManager

# Weather API imports
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    print("⚠️  Requests not available. Weather functionality will be disabled.")
    REQUESTS_AVAILABLE = False
    requests = None

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not available. Using environment variables directly.")
    pass

# --- 1. Initialization and Configuration ---
app = Flask(__name__)
CORS(app)

# Initialize database
db = DatabaseManager()

# --- 2. Routes for serving HTML pages ---
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/disease-detection')
def disease_detection():
    return render_template('index.html')

@app.route('/aichat')
def aichat():
    # Note: In a production app, you'd check for a valid session/token here
    # For now, we'll let the frontend handle authentication
    return render_template('aichat.html')

# --- Weather API Routes ---
@app.route('/api/weather')
def get_weather():
    """Get current weather data"""
    city = request.args.get('city', 'Bengaluru')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    
    # Convert lat/lon to float if provided
    if lat and lon:
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            lat = lon = None
    
    weather_data = get_weather_data(city, lat, lon)
    return jsonify(weather_data)

@app.route('/api/weather/forecast')
def get_forecast():
    """Get weather forecast data"""
    city = request.args.get('city', 'Bengaluru')
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    days = int(request.args.get('days', 5))
    
    # Convert lat/lon to float if provided
    if lat and lon:
        try:
            lat = float(lat)
            lon = float(lon)
        except ValueError:
            lat = lon = None
    
    forecast_data = get_weather_forecast(city, lat, lon, days)
    return jsonify(forecast_data)

# --- Static file serving ---
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/static/uploads/<filename>')
def uploaded_files(filename):
    return send_from_directory('static/uploads', filename)

# --- 3. GEMINI API Configuration ---
try:
    api_key = os.getenv('GEMINI_API_KEY', 'AIzaSyDfvYhsvYOSCBE8r9GL72KXSJ6n9GMX8XA')
    
    if not api_key or api_key == "YOUR_GEMINI_API_KEY":
        raise ValueError("Please set GEMINI_API_KEY in your .env file")
        
    genai.configure(api_key=api_key)
    
    # Model for general text generation (treatments) - Using working model
    gemini_text_model = genai.GenerativeModel('gemini-2.5-flash')
    # Model for market prices - Using same working model (search tools may not be available in newer models)
    gemini_search_model = genai.GenerativeModel('gemini-2.5-flash')
    print("✅ Gemini AI models configured successfully.")
    
    # Test the models
    try:
        # List available models
        models = genai.list_models()
        available_models = [m.name for m in models if 'generateContent' in m.supported_generation_methods]
        print(f"📋 Available Gemini models: {available_models[:3]}...")  # Show first 3
        
        # Test text model
        test_response = gemini_text_model.generate_content("Test")
        if test_response:
            print("✅ Gemini text model test successful")
        else:
            print("⚠️ Gemini text model test failed")
    except Exception as e:
        print(f"⚠️ Gemini model test failed: {e}")
        print("🔄 Will use fallback treatment data")
except Exception as e:
    print(f"❌ Error configuring Gemini AI: {e}")
    gemini_text_model = None
    gemini_search_model = None

# --- 4. Load the Local TensorFlow Model ---
MODEL_PATH = 'crop_disease_detection_model.h5'
CLASSES_PATH = 'class_names.json'
model = None
class_names = []

if os.path.exists(MODEL_PATH) and os.path.exists(CLASSES_PATH):
    try:
        model = tf.keras.models.load_model(MODEL_PATH)
        with open(CLASSES_PATH, 'r') as f:
            class_names = json.load(f)
        print("✅ Local disease detection model loaded.")
    except Exception as e:
        print(f"❌ Error loading local model: {e}")
else:
    print("❌ Error: Local model or class names file not found. Please run `crop_disease_model.py`.")

# --- 5. Yield Impact Database ---
yield_impact_db = {
    "Apple___Apple_scab": "Medium (20-50% loss)", "Apple___Black_rot": "Low to Medium (10-30% loss)", "Apple___Cedar_apple_rust": "Low (5-15% loss)", "Apple___healthy": "None",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": "Medium (15-40% loss)", "Corn_(maize)___Common_rust_": "Low to Medium (10-25% loss)", "Corn_(maize)___Northern_Leaf_Blight": "Medium to High (20-50% loss)", "Corn_(maize)___healthy": "None",
    "Grape___Black_rot": "High (can destroy entire crop)", "Grape___Esca_(Black_Measles)": "High (30-70% loss)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": "Medium (15-35% loss)", "Grape___healthy": "None",
    "Potato___Early_blight": "Medium (20-30% tuber loss)", "Potato___Late_blight": "Very High (can cause 100% loss)", "Potato___healthy": "None", 
    "Tomato___Bacterial_spot": "Medium (15-40% loss)", "Tomato___Early_blight": "Medium (20-35% loss)", "Tomato___Late_blight": "High (40-70% loss if untreated)", "Tomato___Leaf_Mold": "Low to Medium (10-25% loss)", "Tomato___Septoria_leaf_spot": "Medium (20-40% loss)", "Tomato___Spider_mites Two-spotted_spider_mite": "Low to Medium (10-30% loss)", "Tomato___Target_Spot": "Medium (15-35% loss)", "Tomato___Tomato_Yellow_Leaf_Curl_Virus": "High (50-80% loss)", "Tomato___Tomato_mosaic_virus": "Medium to High (25-60% loss)", "Tomato___healthy": "None",
    "default": "Not Determined"
}

# --- 6. Default Treatment Database ---
default_treatment_db = {
    "Apple - Black rot": {
        "symptoms": "• ಕಪ್ಪು ಕಲೆಗಳು ಎಲೆಗಳ ಮೇಲೆ ಕಾಣಿಸುತ್ತವೆ\n• ಹಣ್ಣುಗಳ ಮೇಲೆ ಕಂದು ಬಣ್ಣದ ಕಲೆಗಳು\n• ಎಲೆಗಳು ಹಳದಿಯಾಗಿ ಉದುರುತ್ತವೆ\n• ಹಣ್ಣುಗಳು ಕೊಳೆಯುತ್ತವೆ",
        "organic_treatment": "• ನೀಮ್ ಎಣ್ಣೆ ಸಿಂಪಡಿಸಿ (10ml/ಲೀಟರ್ ನೀರು)\n• ಬೇಕಿಂಗ್ ಸೋಡಾ ದ್ರಾವಣ (5g/ಲೀಟರ್)\n• ತಾಮ್ರದ ಸಲ್ಫೇಟ್ ಸಿಂಪಡಣೆ\n• ಸೋಂಪು ಮತ್ತು ಬೆಳ್ಳುಳ್ಳಿ ದ್ರಾವಣ",
        "chemical_treatment": "• ಕಾರ್ಬೆಂಡಾಜಿಮ್ 50% WP (1g/ಲೀಟರ್)\n• ಮ್ಯಾಂಕೋಜೆಬ್ 75% WP (2g/ಲೀಟರ್)\n• ಪ್ರೊಪಿಕೊನಾಜೋಲ್ 25% EC (1ml/ಲೀಟರ್)\n• ಕಾಪರ್ ಆಕ್ಸಿಕ್ಲೋರೈಡ್ 50% WP",
        "prevention_tips": "• ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ತೆಗೆದು ನಾಶಪಡಿಸಿ\n• ಗಾಳಿ ಸಂಚಾರಕ್ಕಾಗಿ ಸರಿಯಾದ ಅಂತರ ಇರಿಸಿ\n• ನೀರು ಎಲೆಗಳ ಮೇಲೆ ಬೀಳದಂತೆ ನೋಡಿಕೊಳ್ಳಿ\n• ನಿಯಮಿತ ಪರಿಶೀಲನೆ ಮಾಡಿ"
    },
    "Apple - Apple scab": {
        "symptoms": "• ಎಲೆಗಳ ಮೇಲೆ ಕಂದು ಕಲೆಗಳು\n• ಹಣ್ಣುಗಳ ಮೇಲೆ ಒರಟು ಕಲೆಗಳು\n• ಎಲೆಗಳು ಮುಂಚೆಯೇ ಉದುರುತ್ತವೆ\n• ಹಣ್ಣಿನ ಗುಣಮಟ್ಟ ಕಡಿಮೆಯಾಗುತ್ತದೆ",
        "organic_treatment": "• ಬೇಕಿಂಗ್ ಸೋಡಾ ಮತ್ತು ಸಾಬೂನು ದ್ರಾವಣ\n• ನೀಮ್ ಎಣ್ಣೆ ಸಿಂಪಡಣೆ\n• ಕಾಮೋಮೈಲ್ ಚಹಾ ದ್ರಾವಣ\n• ಸಲ್ಫರ್ ಪುಡಿ ಸಿಂಪಡಣೆ",
        "chemical_treatment": "• ಮೈಕ್ಲೋಬುಟಾನಿಲ್ 10% WP\n• ಡೈಫೆನೊಕೊನಾಜೋಲ್ 25% EC\n• ಕ್ಯಾಪ್ಟಾನ್ 50% WP\n• ಡೊಡೈನ್ 65% WP",
        "prevention_tips": "• ಸೋಂಕಿತ ಎಲೆಗಳನ್ನು ಸಂಗ್ರಹಿಸಿ ನಾಶಪಡಿಸಿ\n• ಮರಗಳ ನಡುವೆ ಸಾಕಷ್ಟು ಅಂತರ ಇರಿಸಿ\n• ಮಳೆಗಾಲದ ಮೊದಲು ತಡೆಗಟ್ಟುವ ಸಿಂಪಡಣೆ\n• ನಿರೋಧಕ ಪ್ರಭೇದಗಳನ್ನು ಬೆಳೆಯಿರಿ"
    },
    "Tomato - Late blight": {
        "symptoms": "• ಎಲೆಗಳ ಮೇಲೆ ಕಂದು ಕಲೆಗಳು\n• ಬಿಳಿ ಶಿಲೀಂಧ್ರದ ಬೆಳವಣಿಗೆ\n• ಕಾಂಡ ಮತ್ತು ಹಣ್ಣುಗಳ ಮೇಲೆ ಕಲೆಗಳು\n• ಸಸ್ಯ ಬೇಗನೆ ಒಣಗುತ್ತದೆ",
        "organic_treatment": "• ತಾಮ್ರದ ಸಲ್ಫೇಟ್ ಸಿಂಪಡಣೆ\n• ಬೇಕಿಂಗ್ ಸೋಡಾ ದ್ರಾವಣ\n• ನೀಮ್ ಎಣ್ಣೆ ಮತ್ತು ಸಾಬೂನು\n• ಹಾಲು ಮತ್ತು ನೀರಿನ ಮಿಶ್ರಣ",
        "chemical_treatment": "• ಮೆಟಾಲಾಕ್ಸಿಲ್ + ಮ್ಯಾಂಕೋಜೆಬ್\n• ಸೈಮೋಕ್ಸಾನಿಲ್ + ಮ್ಯಾಂಕೋಜೆಬ್\n• ಡೈಮೆಥೋಮಾರ್ಫ್ 50% WP\n• ಫೆನಾಮಿಡೋನ್ + ಮ್ಯಾಂಕೋಜೆಬ್",
        "prevention_tips": "• ಸೋಂಕಿತ ಸಸ್ಯಗಳನ್ನು ತೆಗೆದುಹಾಕಿ\n• ಗಾಳಿ ಸಂಚಾರಕ್ಕಾಗಿ ಸರಿಯಾದ ಅಂತರ\n• ಮಳೆಯ ನಂತರ ತಡೆಗಟ್ಟುವ ಸಿಂಪಡಣೆ\n• ನಿರೋಧಕ ಪ್ರಭೇದಗಳನ್ನು ಬಳಸಿ"
    },
    "Potato - Late blight": {
        "symptoms": "• ಎಲೆಗಳ ಮೇಲೆ ಕಪ್ಪು ಕಲೆಗಳು\n• ಬಿಳಿ ಶಿಲೀಂಧ್ರದ ಬೆಳವಣಿಗೆ\n• ಕಾಂಡದ ಮೇಲೆ ಕಂದು ಕಲೆಗಳು\n• ಆಲೂಗಡ್ಡೆಗಳ ಮೇಲೆ ಕಂದು ಕಲೆಗಳು",
        "organic_treatment": "• ತಾಮ್ರದ ಸಲ್ಫೇಟ್ ಸಿಂಪಡಣೆ\n• ಬೋರ್ಡೋ ಮಿಶ್ರಣ\n• ನೀಮ್ ಎಣ್ಣೆ ಸಿಂಪಡಣೆ\n• ಬೆಳ್ಳುಳ್ಳಿ ಮತ್ತು ಮೆಣಸಿನಕಾಯಿ ದ್ರಾವಣ",
        "chemical_treatment": "• ಮೆಟಾಲಾಕ್ಸಿಲ್ M + ಮ್ಯಾಂಕೋಜೆಬ್\n• ಸೈಮೋಕ್ಸಾನಿಲ್ + ಮ್ಯಾಂಕೋಜೆಬ್\n• ಪ್ರೊಪಮೊಕಾರ್ಬ್ HCl 70% WP\n• ಫ್ಲೂಅಜಿನಾಮ್ 40% SC",
        "prevention_tips": "• ಸೋಂಕಿತ ಸಸ್ಯಗಳನ್ನು ನಾಶಪಡಿಸಿ\n• ಬೀಜ ಆಲೂಗಡ್ಡೆಗಳನ್ನು ಚಿಕಿತ್ಸೆ ಮಾಡಿ\n• ಸರಿಯಾದ ಒಳಚರಂಡಿ ವ್ಯವಸ್ಥೆ\n• ಮಳೆಗಾಲದಲ್ಲಿ ನಿಯಮಿತ ಪರಿಶೀಲನೆ"
    },
    "healthy": {
        "symptoms": "• ಸಸ್ಯ ಆರೋಗ್ಯಕರವಾಗಿದೆ! 🌱\n• ಎಲೆಗಳು ಹಸಿರು ಮತ್ತು ಹೊಳಪಿನಿಂದ ಕೂಡಿವೆ\n• ಯಾವುದೇ ರೋಗದ ಲಕ್ಷಣಗಳು ಕಾಣಿಸುತ್ತಿಲ್ಲ\n• ಸಸ್ಯದ ಬೆಳವಣಿಗೆ ಸಾಮಾನ್ಯವಾಗಿದೆ",
        "organic_treatment": "• ಚಿಕಿತ್ಸೆಯ ಅಗತ್ಯವಿಲ್ಲ - ಸಸ್ಯ ಆರೋಗ್ಯಕರ! ✅\n• ನಿಯಮಿತ ನೀರುಹಾಕುವಿಕೆ ಮುಂದುವರಿಸಿ\n• ಸಾವಯವ ಗೊಬ್ಬರ ಅನ್ವಯಿಸಿ\n• ಮಣ್ಣಿನ ತೇವಾಂಶ ಕಾಪಾಡಿ",
        "chemical_treatment": "• ರಾಸಾಯನಿಕ ಚಿಕಿತ್ಸೆಯ ಅಗತ್ಯವಿಲ್ಲ ✅\n• ತಡೆಗಟ್ಟುವ ಸಿಂಪಡಣೆ ಮಾತ್ರ ಮಾಡಬಹುದು\n• ಮ್ಯಾಂಕೋಜೆಬ್ ತಿಂಗಳಿಗೊಮ್ಮೆ (ತಡೆಗಟ್ಟುವಿಕೆಗಾಗಿ)\n• ಮಳೆಗಾಲದಲ್ಲಿ ಕಾಪರ್ ಸಲ್ಫೇಟ್",
        "prevention_tips": "• ಈ ಆರೋಗ್ಯಕರ ಸ್ಥಿತಿಯನ್ನು ಕಾಪಾಡಿ! 🌟\n• ನಿಯಮಿತ ಪರಿಶೀಲನೆ ಮುಂದುವರಿಸಿ\n• ಸರಿಯಾದ ನೀರುಹಾಕುವಿಕೆ ಮತ್ತು ಗೊಬ್ಬರ\n• ಸ್ವಚ್ಛತೆ ಮತ್ತು ಉತ್ತಮ ಗಾಳಿ ಸಂಚಾರ"
    },
    "default": {
        "symptoms": "• ಎಲೆಗಳ ಮೇಲೆ ಅಸಾಮಾನ್ಯ ಕಲೆಗಳು\n• ಸಸ್ಯದ ಬೆಳವಣಿಗೆ ನಿಧಾನವಾಗುವುದು\n• ಎಲೆಗಳು ಹಳದಿಯಾಗುವುದು\n• ಹಣ್ಣುಗಳ ಗುಣಮಟ್ಟ ಕಡಿಮೆಯಾಗುವುದು",
        "organic_treatment": "• ನೀಮ್ ಎಣ್ಣೆ ಸಿಂಪಡಣೆ (10ml/ಲೀಟರ್)\n• ಬೇಕಿಂಗ್ ಸೋಡಾ ದ್ರಾವಣ (5g/ಲೀಟರ್)\n• ಬೆಳ್ಳುಳ್ಳಿ ಮತ್ತು ಮೆಣಸಿನಕಾಯಿ ದ್ರಾವಣ\n• ಕಾಮೋಮೈಲ್ ಚಹಾ ಸಿಂಪಡಣೆ",
        "chemical_treatment": "• ಮ್ಯಾಂಕೋಜೆಬ್ 75% WP (2g/ಲೀಟರ್)\n• ಕಾರ್ಬೆಂಡಾಜಿಮ್ 50% WP (1g/ಲೀಟರ್)\n• ಕಾಪರ್ ಆಕ್ಸಿಕ್ಲೋರೈಡ್ 50% WP\n• ಪ್ರೊಪಿಕೊನಾಜೋಲ್ 25% EC",
        "prevention_tips": "• ಸೋಂಕಿತ ಭಾಗಗಳನ್ನು ತೆಗೆದುಹಾಕಿ\n• ಸರಿಯಾದ ಅಂತರ ಮತ್ತು ಗಾಳಿ ಸಂಚಾರ\n• ನಿಯಮಿತ ಪರಿಶೀಲನೆ ಮಾಡಿ\n• ಸ್ವಚ್ಛ ಕೃಷಿ ಪದ್ಧತಿಗಳನ್ನು ಅನುಸರಿಸಿ"
    }
}

# --- 6. Database is now handled by DatabaseManager ---
# No need for in-memory storage

# --- 7. Weather API Configuration ---
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')

# Weather API imports
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    print("⚠️  Requests not available. Weather functionality will be disabled.")
    REQUESTS_AVAILABLE = False
    requests = None

WEATHER_API_AVAILABLE = REQUESTS_AVAILABLE and OPENWEATHER_API_KEY and OPENWEATHER_API_KEY != "your_openweather_api_key_here"

if WEATHER_API_AVAILABLE:
    print("✅ Weather API configured successfully.")
else:
    print("⚠️  Weather API not configured. Add OPENWEATHER_API_KEY to .env file.")

# --- 8. Database Configuration ---
# Database is handled by DatabaseManager class



# --- 9. Weather API Functions ---
def get_weather_data(city="Bengaluru", lat=None, lon=None):
    """Get current weather data from OpenWeatherMap API"""
    if not WEATHER_API_AVAILABLE:
        return get_default_weather_data(city)
    
    try:
        base_url = "http://api.openweathermap.org/data/2.5/weather"
        
        # Use coordinates if provided, otherwise use city name
        if lat and lon:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': OPENWEATHER_API_KEY,
                'units': 'metric'
            }
        else:
            params = {
                'q': city,
                'appid': OPENWEATHER_API_KEY,
                'units': 'metric'
            }
        
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            weather_info = {
                'city': data['name'],
                'country': data['sys']['country'],
                'temperature': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'humidity': data['main']['humidity'],
                'pressure': data['main']['pressure'],
                'description': data['weather'][0]['description'].title(),
                'icon': data['weather'][0]['icon'],
                'wind_speed': data['wind']['speed'],
                'wind_direction': data['wind'].get('deg', 0),
                'visibility': data.get('visibility', 0) / 1000,  # Convert to km
                'sunrise': datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M'),
                'sunset': datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M'),
                'status': 'success'
            }
            
            print(f"✅ Weather data retrieved for {weather_info['city']}")
            return weather_info
            
        else:
            print(f"❌ Weather API error: {response.status_code}")
            return get_default_weather_data(city)
            
    except Exception as e:
        print(f"❌ Weather API exception: {e}")
        return get_default_weather_data(city)

def get_weather_forecast(city="Bengaluru", lat=None, lon=None, days=5):
    """Get weather forecast from OpenWeatherMap API"""
    if not WEATHER_API_AVAILABLE:
        return get_default_forecast_data(city, days)
    
    try:
        base_url = "http://api.openweathermap.org/data/2.5/forecast"
        
        # Use coordinates if provided, otherwise use city name
        if lat and lon:
            params = {
                'lat': lat,
                'lon': lon,
                'appid': OPENWEATHER_API_KEY,
                'units': 'metric'
            }
        else:
            params = {
                'q': city,
                'appid': OPENWEATHER_API_KEY,
                'units': 'metric'
            }
        
        response = requests.get(base_url, params=params, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Process forecast data (5-day forecast with 3-hour intervals)
            forecast_list = []
            current_date = None
            daily_data = {}
            
            for item in data['list'][:40]:  # 5 days * 8 intervals per day
                forecast_date = datetime.fromtimestamp(item['dt']).date()
                
                if forecast_date != current_date:
                    if current_date and daily_data:
                        forecast_list.append(daily_data)
                    
                    current_date = forecast_date
                    daily_data = {
                        'date': forecast_date.strftime('%Y-%m-%d'),
                        'day': forecast_date.strftime('%A'),
                        'temp_min': item['main']['temp'],
                        'temp_max': item['main']['temp'],
                        'description': item['weather'][0]['description'].title(),
                        'icon': item['weather'][0]['icon'],
                        'humidity': item['main']['humidity'],
                        'wind_speed': item['wind']['speed']
                    }
                else:
                    # Update min/max temperatures for the day
                    daily_data['temp_min'] = min(daily_data['temp_min'], item['main']['temp'])
                    daily_data['temp_max'] = max(daily_data['temp_max'], item['main']['temp'])
            
            # Add the last day
            if daily_data:
                forecast_list.append(daily_data)
            
            # Round temperatures
            for day in forecast_list:
                day['temp_min'] = round(day['temp_min'])
                day['temp_max'] = round(day['temp_max'])
            
            print(f"✅ Weather forecast retrieved for {data['city']['name']}")
            return {
                'city': data['city']['name'],
                'forecast': forecast_list[:days],
                'status': 'success'
            }
            
        else:
            print(f"❌ Weather forecast API error: {response.status_code}")
            return get_default_forecast_data(city, days)
            
    except Exception as e:
        print(f"❌ Weather forecast API exception: {e}")
        return get_default_forecast_data(city, days)

def get_default_weather_data(city="Bengaluru"):
    """Default weather data when API is not available"""
    return {
        'city': city,
        'country': 'IN',
        'temperature': 26,
        'feels_like': 28,
        'humidity': 65,
        'pressure': 1013,
        'description': 'Partly Cloudy',
        'icon': '02d',
        'wind_speed': 3.5,
        'wind_direction': 180,
        'visibility': 10,
        'sunrise': '06:30',
        'sunset': '18:45',
        'status': 'demo'
    }

def get_default_forecast_data(city="Bengaluru", days=5):
    """Default forecast data when API is not available"""
    forecast_list = []
    base_date = datetime.now().date()
    
    for i in range(days):
        forecast_date = base_date + timedelta(days=i)
        forecast_list.append({
            'date': forecast_date.strftime('%Y-%m-%d'),
            'day': forecast_date.strftime('%A'),
            'temp_min': 22 + (i % 3),
            'temp_max': 28 + (i % 4),
            'description': ['Sunny', 'Partly Cloudy', 'Cloudy', 'Light Rain', 'Clear'][i % 5],
            'icon': ['01d', '02d', '03d', '10d', '01d'][i % 5],
            'humidity': 60 + (i * 5),
            'wind_speed': 2.5 + (i * 0.5)
        })
    
    return {
        'city': city,
        'forecast': forecast_list,
        'status': 'demo'
    }

# --- 10. Gemini Interaction Functions ---
def get_gemini_treatment_details(disease_name, target_language='en'):
    """Get treatment details from Gemini AI with fallback to default data"""
    
    # Language mapping for prompts
    language_names = {
        'en': 'English',
        'hi': 'Hindi',
        'kn': 'Kannada', 
        'te': 'Telugu',
        'ta': 'Tamil',
        'ml': 'Malayalam',
        'mr': 'Marathi',
        'gu': 'Gujarati',
        'bn': 'Bengali',
        'pa': 'Punjabi'
    }
    
    target_lang_name = language_names.get(target_language, 'English')
    
    # First try Gemini AI
    if gemini_text_model:
        prompt = f"""You are an expert agricultural advisor for farmers in India. A farmer has identified '{disease_name}'. 

        Provide a detailed action plan in {target_lang_name}. Organize your response into four sections with these exact English headings followed by {target_lang_name} content:

        1. Symptoms: 
        [Write a clear bulleted list of key symptoms in simple {target_lang_name}. Use simple bullet points (•) and avoid asterisks or markdown formatting.]

        2. Organic Treatment: 
        [Write a clear bulleted list of organic remedies in simple {target_lang_name}. Include specific instructions and quantities. Use simple bullet points (•) and avoid asterisks or markdown formatting.]

        3. Chemical Treatment: 
        [Write a clear bulleted list of recommended chemical treatments, including common brand names available in India, in simple {target_lang_name}. Use simple bullet points (•) and avoid asterisks or markdown formatting.]

        4. Prevention Tips: 
        [Write a clear bulleted list of preventive measures in simple {target_lang_name}. Use simple bullet points (•) and avoid asterisks or markdown formatting.]

        IMPORTANT FORMATTING RULES: 
        - Use simple, farmer-friendly language that is easy to understand and implement
        - Do NOT use asterisks (*), markdown formatting, hashtags (#), or complex symbols
        - Use simple bullet points (•) for lists only
        - Write in clear, plain text format without any special formatting
        - Keep sentences short and actionable
        - Use proper spacing between sections
        - Include specific quantities, timings, and brand names where applicable
        - Write as if explaining to a farmer in person"""
        
        try:
            print(f"🤖 Calling Gemini AI for: {disease_name}")
            response = gemini_text_model.generate_content(prompt)
            if response and response.text:
                print(f"✅ Gemini AI response received")
                return parse_gemini_response(response.text)
            else:
                print(f"⚠️ Gemini AI returned empty response")
        except Exception as e:
            print(f"❌ Gemini (Text) API Error: {e}")
    
    # Fallback to default treatment data
    print(f"🔄 Using fallback treatment data for: {disease_name}")
    return get_default_treatment_details(disease_name, target_language)

def get_market_prices(crop_name, target_language='en'):
    """Get market prices from Gemini AI with fallback to default data"""
    
    # Language mapping for prompts
    language_names = {
        'en': 'English',
        'hi': 'Hindi',
        'kn': 'Kannada', 
        'te': 'Telugu',
        'ta': 'Tamil',
        'ml': 'Malayalam',
        'mr': 'Marathi',
        'gu': 'Gujarati',
        'bn': 'Bengali',
        'pa': 'Punjabi'
    }
    
    target_lang_name = language_names.get(target_language, 'English')
    
    # Try Gemini AI first
    if gemini_search_model:
        prompt = f"""Find today's wholesale market price (APMC mandi rates) for '{crop_name}' in major markets of India, like Bengaluru, Delhi, Mumbai, Chennai. 

        Provide the information in {target_lang_name} using this format:
        • Market Name: Price range per kg/quintal
        • Quality Grade: Price details

        IMPORTANT:
        - Use simple bullet points (•) only
        - Do NOT use asterisks (*), markdown formatting, or complex symbols  
        - Write in clear, plain text format
        - Use farmer-friendly language
        - Include currency symbols (₹) for prices
        - Keep it simple and easy to read"""
        try:
            print(f"💰 Getting market prices from Gemini AI for: {crop_name}")
            response = gemini_search_model.generate_content(prompt)
            if response and response.text:
                print(f"✅ Market prices received from Gemini AI")
                # Clean the market prices text
                cleaned_prices = clean_gemini_text(response.text)
                return cleaned_prices
        except Exception as e:
            print(f"❌ Gemini (Search) API Error: {e}")
    
    # Fallback to default market data
    print(f"🔄 Using fallback market data for: {crop_name}")
    return get_default_market_prices(crop_name, target_language)

def get_default_market_prices(crop_name, target_language='en'):
    """Default market prices when Gemini AI is not available"""
    default_prices = {
        "Apple": "• ಬೆಂಗಳೂರು: ₹80-120/ಕೆಜಿ\n• ಮೈಸೂರು: ₹75-110/ಕೆಜಿ\n• ಹುಬ್ಬಳ್ಳಿ: ₹70-105/ಕೆಜಿ\n• ಗುಣಮಟ್ಟ: A ಗ್ರೇಡ್ - ಹೆಚ್ಚಿನ ದರ, B ಗ್ರೇಡ್ - ಮಧ್ಯಮ ದರ",
        "Tomato": "• ಬೆಂಗಳೂರು: ₹25-45/ಕೆಜಿ\n• ಮೈಸೂರು: ₹20-40/ಕೆಜಿ\n• ಹುಬ್ಬಳ್ಳಿ: ₹18-38/ಕೆಜಿ\n• ಗುಣಮಟ್ಟ: ದೊಡ್ಡ ಗಾತ್ರ - ಹೆಚ್ಚಿನ ದರ",
        "Potato": "• ಬೆಂಗಳೂರು: ₹15-25/ಕೆಜಿ\n• ಮೈಸೂರು: ₹12-22/ಕೆಜಿ\n• ಹುಬ್ಬಳ್ಳಿ: ₹10-20/ಕೆಜಿ\n• ಗುಣಮಟ್ಟ: ದೊಡ್ಡ ಗಾತ್ರ - ಉತ್ತಮ ದರ",
        "Corn": "• ಬೆಂಗಳೂರು: ₹18-28/ಕೆಜಿ\n• ಮೈಸೂರು: ₹16-26/ಕೆಜಿ\n• ಹುಬ್ಬಳ್ಳಿ: ₹15-25/ಕೆಜಿ\n• ಗುಣಮಟ್ಟ: ಒಣ ಮೆಕ್ಕೆಜೋಳ - ಉತ್ತಮ ದರ",
        "Grape": "• ಬೆಂಗಳೂರು: ₹60-100/ಕೆಜಿ\n• ಮೈಸೂರು: ₹55-95/ಕೆಜಿ\n• ಹುಬ್ಬಳ್ಳಿ: ₹50-90/ಕೆಜಿ\n• ಗುಣಮಟ್ಟ: ರಫ್ತು ಗುಣಮಟ್ಟ - ಹೆಚ್ಚಿನ ದರ",
        "Cherry": "• ಬೆಂಗಳೂರು: ₹200-350/ಕೆಜಿ\n• ಮೈಸೂರು: ₹180-320/ಕೆಜಿ\n• ಹುಬ್ಬಳ್ಳಿ: ₹170-300/ಕೆಜಿ\n• ಗುಣಮಟ್ಟ: ತಾಜಾ ಮತ್ತು ದೊಡ್ಡ ಗಾತ್ರ - ಪ್ರೀಮಿಯಂ ದರ"
    }
    
    # Find matching crop
    base_price = None
    for crop in default_prices.keys():
        if crop.lower() in crop_name.lower():
            base_price = default_prices[crop]
            break
    
    if not base_price:
        # Default message
        base_price = f"• {crop_name} ಗಾಗಿ ಮಾರುಕಟ್ಟೆ ದರಗಳು:\n• ಸ್ಥಳೀಯ ಮಾರುಕಟ್ಟೆಯಲ್ಲಿ ವಿಚಾರಿಸಿ\n• APMC ಮಂಡಿಯಲ್ಲಿ ಪರಿಶೀಲಿಸಿ\n• ಗುಣಮಟ್ಟದ ಆಧಾರದ ಮೇಲೆ ದರ ಬದಲಾಗುತ್ತದೆ"
    
    # Translate if not English or Kannada
    if target_language not in ['en', 'kn']:
        return get_fallback_translation(base_price, target_language)
    
    return base_price

def clean_gemini_text(text):
    """Clean up Gemini AI response text by removing markdown formatting"""
    if not text:
        return text
    
    # Remove excessive asterisks and markdown formatting
    text = re.sub(r'\*{2,}', '', text)  # Remove multiple asterisks
    text = re.sub(r'\*([^*]+)\*', r'\1', text)  # Remove single asterisks around text
    text = re.sub(r'#{1,6}\s*', '', text)  # Remove markdown headers
    text = re.sub(r'`([^`]+)`', r'\1', text)  # Remove code formatting
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)  # Remove markdown links
    
    # Clean up bullet points and formatting
    text = re.sub(r'^\s*[-•*]\s*', '• ', text, flags=re.MULTILINE)  # Standardize bullet points
    text = re.sub(r'\n\s*\n\s*\n', '\n\n', text)  # Remove excessive line breaks
    text = re.sub(r'^\s+|\s+$', '', text)  # Remove leading/trailing whitespace
    
    # Fix common formatting issues
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with single space
    text = re.sub(r'\n\s*', '\n', text)  # Clean up line breaks
    
    return text.strip()

def parse_gemini_response(text):
    """Parse Gemini AI response into structured format"""
    details = {key: "Information not available." for key in ["symptoms", "organic_treatment", "chemical_treatment", "prevention_tips"]}
    
    # Clean the input text first
    text = clean_gemini_text(text)
    
    patterns = {
        "symptoms": r"Symptoms:(.*?)(Organic Treatment:|Chemical Treatment:|Prevention Tips:|$)",
        "organic_treatment": r"Organic Treatment:(.*?)(Chemical Treatment:|Prevention Tips:|$)",
        "chemical_treatment": r"Chemical Treatment:(.*?)(Prevention Tips:|$)",
        "prevention_tips": r"Prevention Tips:(.*)"
    }
    
    for key, pattern in patterns.items():
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match: 
            extracted_text = match.group(1).strip()
            # Clean the extracted text
            cleaned_text = clean_gemini_text(extracted_text)
            details[key] = cleaned_text if cleaned_text else "Information not available."
    
    return details

def get_default_treatment_details(disease_name, target_language='en'):
    """Get default treatment details when Gemini AI is not available"""
    
    # Check if plant is healthy
    if "healthy" in disease_name.lower():
        base_details = default_treatment_db["healthy"]
    else:
        # Try to find exact match first
        if disease_name in default_treatment_db:
            base_details = default_treatment_db[disease_name]
        else:
            # Try to find partial match
            found = False
            for key in default_treatment_db.keys():
                if key != "healthy" and key != "default":  # Skip special keys
                    if key.lower() in disease_name.lower() or disease_name.lower() in key.lower():
                        base_details = default_treatment_db[key]
                        found = True
                        break
            
            if not found:
                # Return default treatment
                base_details = default_treatment_db["default"]
    
    # Translate the details if not English
    if target_language != 'en':
        translated_details = {}
        for key, value in base_details.items():
            if isinstance(value, str):
                translated_details[key] = get_fallback_translation(value, target_language)
            else:
                translated_details[key] = value
        return translated_details
    
    return base_details

# --- 8. Image Preprocessing ---
def preprocess_image(image_data, target_size=(128, 128)):
    image_bytes = base64.b64decode(image_data.split(',')[1])
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    img = img.resize(target_size)
    img_array = np.array(img) / 255.0
    return np.expand_dims(img_array, axis=0)

# --- 9. Authentication Endpoints ---
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        required_fields = ['name', 'email', 'mobile', 'password', 'location']
        
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'{field} is required'}), 400
        
        # Validate email format
        if not re.match(r'^[^\s@]+@[^\s@]+\.[^\s@]+$', data['email']):
            return jsonify({'error': 'Invalid email format'}), 400
        
        # Validate mobile format
        if not re.match(r'^[6-9]\d{9}$', data['mobile']):
            return jsonify({'error': 'Invalid mobile number format'}), 400
        
        # Validate password length
        if len(data['password']) < 6:
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        # Check if user already exists
        existing_user = db.get_user_by_email_or_mobile(data['email'])
        if existing_user:
            return jsonify({'error': 'User with this email already exists'}), 409
            
        existing_user = db.get_user_by_email_or_mobile(data['mobile'])
        if existing_user:
            return jsonify({'error': 'User with this mobile number already exists'}), 409
        
        # Create user in database (no OTP verification needed)
        user_id = db.create_user(
            name=data['name'],
            email=data['email'],
            mobile=data['mobile'],
            password=data['password'],
            location=data['location']
        )
        
        print(f"✅ User registered: {data['name']} ({data['email']}, {data['mobile']}) - ID: {user_id}")
        
        # Generate a simple token for auto-login
        import secrets
        token = secrets.token_urlsafe(32)
        
        return jsonify({
            'message': 'Registration successful! You are now logged in.', 
            'user_id': user_id,
            'user': {
                'id': user_id,
                'name': data['name'],
                'email': data['email'],
                'mobile': data['mobile'],
                'location': data['location'],
                'created_at': datetime.now().isoformat()
            },
            'token': token
        }), 201
        
    except Exception as e:
        print(f"❌ Registration Error: {e}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email_or_mobile = data.get('emailOrMobile')
        password = data.get('password')
        
        print(f"🔐 Login attempt: {email_or_mobile}")
        
        if not email_or_mobile or not password:
            return jsonify({'error': 'Email/mobile and password are required'}), 400
        
        # Get user from database
        user_data = db.get_user_by_email_or_mobile(email_or_mobile)
        
        if not user_data:
            print(f"❌ User not found: {email_or_mobile}")
            return jsonify({'error': 'User not found. Please register first.'}), 401
        
        print(f"👤 Found user: {user_data.get('name', 'Unknown')}")
        
        # Verify password
        password_valid = db.verify_password(user_data, password)
        print(f"🔒 Password verification: {password_valid}")
        print(f"🔍 Password hash starts with: {user_data['password_hash'][:20]}...")
        print(f"🔍 Provided password length: {len(password)}")
        
        if password_valid:
            # Generate a simple token (in production, use JWT or similar)
            import secrets
            token = secrets.token_urlsafe(32)
            
            # Return user data without password
            response_user = {
                'id': user_data['id'],
                'name': user_data['name'],
                'email': user_data['email'],
                'mobile': user_data['mobile'],
                'location': user_data['location'],
                'created_at': user_data['created_at']
            }
            print(f"✅ Login successful for: {response_user.get('name')}")
            return jsonify({
                'message': 'Login successful', 
                'user': response_user,
                'token': token
            }), 200
        else:
            print(f"❌ Invalid password for: {email_or_mobile}")
            return jsonify({'error': 'Invalid password'}), 401
            
    except Exception as e:
        print(f"❌ Login Error: {e}")
        return jsonify({'error': 'Login failed'}), 500

# OTP endpoints disabled - registration now works without OTP verification
# @app.route('/api/send-otp', methods=['POST'])
# def send_otp():
#     try:
#         data = request.get_json()
#         mobile = data.get('mobile')
#         
#         if not mobile:
#             return jsonify({'error': 'Mobile number is required'}), 400
#         
#         # Validate mobile number format
#         if not re.match(r'^[6-9]\d{9}$', mobile):
#             return jsonify({'error': 'Invalid mobile number format'}), 400
#         
#         # Generate OTP
#         otp = generate_otp()
#         
#         # Store OTP
#         store_otp(mobile, otp)
#         
#         # Send SMS
#         success, message = send_sms_otp(mobile, otp)
#         
#         if success:
#             return jsonify({
#                 'message': message,
#                 'demo_otp': otp if not firebase_app and not twilio_client else None  # Only show OTP in demo mode
#             }), 200
#         else:
#             return jsonify({'error': message}), 500
#         
#     except Exception as e:
#         print(f"❌ OTP Error: {e}")
#         return jsonify({'error': 'Failed to send OTP'}), 500

@app.route('/api/user/<int:user_id>/predictions', methods=['GET'])
def get_user_predictions(user_id):
    """Get user's prediction history"""
    try:
        limit = request.args.get('limit', 10, type=int)
        predictions = db.get_user_predictions(user_id, limit)
        
        return jsonify({
            'predictions': predictions,
            'total': len(predictions)
        }), 200
        
    except Exception as e:
        print(f"❌ Error getting user predictions: {e}")
        return jsonify({'error': 'Failed to get predictions'}), 500

@app.route('/api/predictions/all', methods=['GET'])
def get_all_predictions():
    """Get all predictions for analytics (admin only)"""
    try:
        limit = request.args.get('limit', 50, type=int)
        predictions = db.get_all_predictions(limit)
        
        return jsonify({
            'predictions': predictions,
            'total': len(predictions)
        }), 200
        
    except Exception as e:
        print(f"❌ Error getting all predictions: {e}")
        return jsonify({'error': 'Failed to get predictions'}), 500

@app.route('/api/reset-password', methods=['POST'])
def reset_password():
    """Reset user password (for demo/testing purposes)"""
    try:
        data = request.get_json()
        email_or_mobile = data.get('emailOrMobile')
        new_password = data.get('newPassword', '123456')  # Default to demo password
        
        if not email_or_mobile:
            return jsonify({'error': 'Email or mobile is required'}), 400
        
        # Get user from database
        user_data = db.get_user_by_email_or_mobile(email_or_mobile)
        
        if not user_data:
            return jsonify({'error': 'User not found'}), 404
        
        # Update password in database
        conn = db.get_connection()
        cursor = conn.cursor()
        
        # Hash the new password
        from werkzeug.security import generate_password_hash
        new_password_hash = generate_password_hash(new_password)
        
        cursor.execute('''
            UPDATE users 
            SET password_hash = ? 
            WHERE email = ? OR mobile = ?
        ''', (new_password_hash, email_or_mobile, email_or_mobile))
        
        conn.commit()
        conn.close()
        
        print(f"🔄 Password reset for user: {user_data['name']} ({email_or_mobile})")
        
        return jsonify({
            'message': 'Password reset successful',
            'new_password': new_password,
            'user': user_data['name']
        }), 200
        
    except Exception as e:
        print(f"❌ Password reset error: {e}")
        return jsonify({'error': 'Password reset failed'}), 500

# OTP verification endpoint disabled - no longer needed
# @app.route('/api/verify-otp', methods=['POST'])
# def verify_otp_endpoint():
#     try:
#         data = request.get_json()
#         mobile = data.get('mobile')
#         provided_otp = data.get('otp')
#         
#         if not mobile or not provided_otp:
#             return jsonify({'error': 'Mobile number and OTP are required'}), 400
#         
#         # Verify OTP
#         is_valid, message = verify_otp(mobile, provided_otp)
#         
#         if is_valid:
#             return jsonify({'message': message, 'verified': True}), 200
#         else:
#             return jsonify({'error': message, 'verified': False}), 400
#         
#     except Exception as e:
#         print(f"❌ OTP Verification Error: {e}")
#         return jsonify({'error': 'Failed to verify OTP'}), 500

@app.route('/api/change-password', methods=['POST'])
def change_password():
    """Change user password"""
    try:
        # Get user from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        data = request.get_json()
        current_password = data.get('current_password')  # Updated field name to match JavaScript
        new_password = data.get('new_password')  # Updated field name to match JavaScript
        
        if not current_password or not new_password:
            return jsonify({'error': 'Current password and new password are required'}), 400
        
        # Validate new password
        if len(new_password) < 6:
            return jsonify({'error': 'New password must be at least 6 characters long'}), 400
        
        # For demo purposes, use the demo user
        # In production, you'd decode the token to get the user info
        user = db.get_user_by_email_or_mobile('demo@raithamitra.com')
        if not user:
            print(f"❌ Demo user not found")
            return jsonify({'error': 'User not found'}), 404
        
        email = user['email']
        print(f"🔍 Found user: {email}, verifying password...")
        
        # Verify current password
        if not db.verify_password(user, current_password):
            print(f"❌ Current password verification failed for user: {email}")
            return jsonify({'error': 'Current password is incorrect'}), 400
        
        print(f"✅ Current password verified for user: {email}")
        
        # Hash new password
        new_password_hash = generate_password_hash(new_password)
        
        # Update password in database
        success = db.update_user_password(email, new_password_hash)
        
        if success:
            print(f"✅ Password changed successfully for user: {email}")
            return jsonify({'message': 'Password changed successfully'}), 200
        else:
            return jsonify({'error': 'Failed to update password'}), 500
        
    except Exception as e:
        print(f"❌ Change password error: {e}")
        return jsonify({'error': 'Failed to change password'}), 500

@app.route('/api/prediction-history', methods=['GET'])
def get_prediction_history():
    """Get user's prediction history"""
    try:
        # Get user from Authorization header (simplified token validation)
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization token required'}), 401
        
        # For demo purposes, we'll use a simple approach
        # In production, you'd validate the JWT token and extract user info
        # For now, we'll get the user from localStorage data or use demo user
        
        # Get limit parameter
        limit = request.args.get('limit', 10, type=int)
        
        # For demo purposes, let's show all recent predictions
        # This way any user can see predictions made during testing
        predictions = db.get_all_predictions(limit)
        print(f"📊 Found {len(predictions)} total predictions in database")
        
        # Format predictions for frontend
        formatted_predictions = []
        for pred in predictions:
            formatted_pred = {
                'id': pred['id'],
                'predicted_disease': pred['disease_name'],  # JavaScript expects this field name
                'confidence': pred['confidence'],
                'yield_impact': pred['yield_impact'],
                'symptoms': pred['symptoms'],
                'organic_treatment': pred['organic_treatment'],
                'chemical_treatment': pred['chemical_treatment'],
                'prevention_tips': pred['prevention_tips'],
                'market_prices': pred['market_prices'],
                'created_at': pred['created_at'],
                'image_path': pred['image_path']
            }
            formatted_predictions.append(formatted_pred)
        
        return jsonify({
            'predictions': formatted_predictions,
            'total': len(formatted_predictions)
        }), 200
        
    except Exception as e:
        print(f"❌ Get prediction history error: {e}")
        return jsonify({'error': 'Failed to get prediction history'}), 500

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """Translate text to specified language"""
    try:
        data = request.get_json()
        text = data.get('text')
        target_language = data.get('target_language', 'en')
        
        if not text:
            return jsonify({'error': 'Text is required'}), 400
        
        # Use Google Translate API if available, otherwise use local translations
        translated_text = translate_with_gemini(text, target_language)
        
        return jsonify({
            'original_text': text,
            'translated_text': translated_text,
            'target_language': target_language
        }), 200
        
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return jsonify({'error': 'Translation failed'}), 500

def translate_with_gemini(text, target_language):
    """Translate text using Gemini AI"""
    try:
        # Language mapping
        language_names = {
            'en': 'English',
            'hi': 'Hindi',
            'kn': 'Kannada', 
            'te': 'Telugu',
            'ta': 'Tamil',
            'ml': 'Malayalam',
            'mr': 'Marathi',
            'gu': 'Gujarati',
            'bn': 'Bengali',
            'pa': 'Punjabi'
        }
        
        target_lang_name = language_names.get(target_language, 'English')
        
        if target_language == 'en':
            return text  # No translation needed
        
        # Use Gemini for translation
        if genai and gemini_text_model:
            prompt = f"""
            Translate the following text to {target_lang_name}. 
            Provide only the translation, no explanations or additional text.
            Keep technical terms related to agriculture and plant diseases accurate.
            
            Text to translate: {text}
            """
            
            response = gemini_text_model.generate_content(prompt)
            translated = response.text.strip()
            
            print(f"🌐 Translated '{text[:50]}...' to {target_lang_name}")
            return translated
        else:
            # Fallback to basic translations for common terms
            return get_fallback_translation(text, target_language)
            
    except Exception as e:
        print(f"❌ Gemini translation error: {e}")
        return get_fallback_translation(text, target_language)

def get_fallback_translation(text, target_language):
    """Fallback translations for common agricultural terms"""
    translations = {
        'hi': {  # Hindi
            'Healthy': 'स्वस्थ',
            'Disease': 'रोग',
            'Treatment': 'उपचार',
            'Symptoms': 'लक्षण',
            'Prevention': 'रोकथाम',
            'Organic': 'जैविक',
            'Chemical': 'रासायनिक',
            'Leaf': 'पत्ता',
            'Plant': 'पौधा',
            'Crop': 'फसल',
            'Apply': 'लगाएं',
            'Spray': 'छिड़काव',
            'Remove': 'हटाएं',
            'Water': 'पानी',
            'Soil': 'मिट्टी',
            'Fertilizer': 'उर्वरक',
            'Neem': 'नीम',
            'Oil': 'तेल',
            'Weekly': 'साप्ताहिक',
            'Daily': 'दैनिक'
        },
        'kn': {  # Kannada
            'Healthy': 'ಆರೋಗ್ಯಕರ',
            'Disease': 'ರೋಗ',
            'Treatment': 'ಚಿಕಿತ್ಸೆ',
            'Symptoms': 'ಲಕ್ಷಣಗಳು',
            'Prevention': 'ತಡೆಗಟ್ಟುವಿಕೆ',
            'Organic': 'ಸಾವಯವ',
            'Chemical': 'ರಾಸಾಯನಿಕ',
            'Leaf': 'ಎಲೆ',
            'Plant': 'ಸಸ್ಯ',
            'Crop': 'ಬೆಳೆ',
            'Apply': 'ಅನ್ವಯಿಸಿ',
            'Spray': 'ಸಿಂಪಡಿಸಿ',
            'Remove': 'ತೆಗೆದುಹಾಕಿ',
            'Water': 'ನೀರು',
            'Soil': 'ಮಣ್ಣು',
            'Fertilizer': 'ಗೊಬ್ಬರ',
            'Neem': 'ಬೇವು',
            'Oil': 'ಎಣ್ಣೆ',
            'Weekly': 'ವಾರಕ್ಕೊಮ್ಮೆ',
            'Daily': 'ದೈನಂದಿನ'
        },
        'te': {  # Telugu
            'Healthy': 'ఆరోగ్యకరమైన',
            'Disease': 'వ్యాధి',
            'Treatment': 'చికిత్స',
            'Symptoms': 'లక్షణాలు',
            'Prevention': 'నివారణ',
            'Organic': 'సేంద్రీయ',
            'Chemical': 'రసాయనిక',
            'Leaf': 'ఆకు',
            'Plant': 'మొక్క',
            'Crop': 'పంట',
            'Apply': 'వర్తింపజేయండి',
            'Spray': 'స్ప్రే చేయండి',
            'Remove': 'తొలగించండి',
            'Water': 'నీరు',
            'Soil': 'మట్టి',
            'Fertilizer': 'ఎరువులు',
            'Neem': 'వేప',
            'Oil': 'నూనె',
            'Weekly': 'వారానికి',
            'Daily': 'రోజువారీ'
        },
        'ta': {  # Tamil
            'Healthy': 'ஆரோக்கியமான',
            'Disease': 'நோய்',
            'Treatment': 'சிகிச்சை',
            'Symptoms': 'அறிகுறிகள்',
            'Prevention': 'தடுப்பு',
            'Organic': 'இயற்கை',
            'Chemical': 'இரசாயன',
            'Leaf': 'இலை',
            'Plant': 'செடி',
            'Crop': 'பயிர்',
            'Apply': 'பயன்படுத்தவும்',
            'Spray': 'தெளிக்கவும்',
            'Remove': 'அகற்றவும்',
            'Water': 'நீர்',
            'Soil': 'மண்',
            'Fertilizer': 'உரம்',
            'Neem': 'வேம்பு',
            'Oil': 'எண்ணெய்',
            'Weekly': 'வாராந்திர',
            'Daily': 'தினசரி'
        }
    }
    
    lang_dict = translations.get(target_language, {})
    
    # Simple word replacement for fallback
    translated = text
    for english_word, local_word in lang_dict.items():
        # Case-insensitive replacement
        translated = translated.replace(english_word, local_word)
        translated = translated.replace(english_word.lower(), local_word)
    
    return translated if translated != text else text

# --- 10. AI Chat API Endpoints ---
@app.route('/api/chat/conversations', methods=['GET'])
def get_chat_conversations():
    """Get user's chat conversations"""
    try:
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        conversations = db.get_user_conversations(int(user_id))
        return jsonify(conversations), 200
        
    except Exception as e:
        print(f"❌ Error getting conversations: {e}")
        return jsonify({'error': 'Failed to get conversations'}), 500

@app.route('/api/chat/conversations', methods=['POST'])
def create_chat_conversation():
    """Create a new chat conversation"""
    try:
        user_id = request.headers.get('X-User-ID')
        print(f"💬 Creating new conversation for user ID: {user_id}")
        
        if not user_id:
            print("❌ No user ID provided")
            return jsonify({'error': 'User ID required'}), 400
        
        data = request.get_json()
        title = data.get('title', 'New Chat')
        print(f"📝 Conversation title: {title}")
        
        conversation_id = db.create_chat_conversation(int(user_id), title)
        print(f"✅ Created conversation with ID: {conversation_id}")
        
        return jsonify({
            'id': conversation_id,
            'title': title,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat(),
            'message_count': 0,
            'last_message': None
        }), 201
        
    except Exception as e:
        print(f"❌ Error creating conversation: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to create conversation'}), 500

@app.route('/api/chat/conversations/<int:conversation_id>/messages', methods=['GET'])
def get_conversation_messages(conversation_id):
    """Get messages from a conversation"""
    try:
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        messages = db.get_conversation_messages(conversation_id)
        return jsonify(messages), 200
        
    except Exception as e:
        print(f"❌ Error getting messages: {e}")
        return jsonify({'error': 'Failed to get messages'}), 500

@app.route('/api/chat/message', methods=['POST'])
def send_chat_message():
    """Send a message and get AI response"""
    try:
        user_id = request.headers.get('X-User-ID')
        print(f"🤖 Chat message request - User ID: {user_id}")
        
        if not user_id:
            print("❌ No user ID provided")
            return jsonify({'error': 'User ID required'}), 400
        
        data = request.get_json()
        conversation_id = data.get('conversation_id')
        message = data.get('message')
        
        print(f"📝 Message: {message}")
        print(f"💬 Conversation ID: {conversation_id}")
        
        if not conversation_id or not message:
            print("❌ Missing conversation ID or message")
            return jsonify({'error': 'Conversation ID and message are required'}), 400
        
        # Get AI response using Gemini
        print("🤖 Getting AI response...")
        ai_response = get_ai_chat_response(message)
        print(f"✅ AI response: {ai_response[:100]}...")
        
        # Save message and response to database
        print("💾 Saving to database...")
        db.save_chat_message(conversation_id, int(user_id), message, ai_response)
        
        # Update conversation title if it's the first message
        title_updated = False
        messages = db.get_conversation_messages(conversation_id)
        if len(messages) == 1:  # First message
            # Generate a title from the first message
            title = generate_conversation_title(message)
            db.update_conversation_title(conversation_id, title)
            title_updated = True
            print(f"📝 Updated conversation title: {title}")
        
        print("✅ Chat message processed successfully")
        return jsonify({
            'response': ai_response,
            'title_updated': title_updated
        }), 200
        
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': 'Failed to send message'}), 500

@app.route('/api/chat/conversations/<int:conversation_id>', methods=['DELETE'])
def delete_chat_conversation(conversation_id):
    """Delete a chat conversation"""
    try:
        user_id = request.headers.get('X-User-ID')
        if not user_id:
            return jsonify({'error': 'User ID required'}), 400
        
        success = db.delete_conversation(conversation_id, int(user_id))
        
        if success:
            return jsonify({'message': 'Conversation deleted successfully'}), 200
        else:
            return jsonify({'error': 'Conversation not found or access denied'}), 404
        
    except Exception as e:
        print(f"❌ Error deleting conversation: {e}")
        return jsonify({'error': 'Failed to delete conversation'}), 500

def get_ai_chat_response(message):
    """Get AI response using Gemini"""
    try:
        print(f"🤖 Getting AI response for message: {message[:50]}...")
        
        if not gemini_text_model:
            print("❌ Gemini model not available")
            return "I'm sorry, but the AI service is currently unavailable. Please try again later."
        
        print("✅ Gemini model is available")
        
        # Create a farming-focused prompt
        prompt = f"""You are an expert agricultural AI assistant for Indian farmers. You help with:
- Crop diseases and pest management
- Farming techniques and best practices
- Weather and seasonal advice
- Market information and crop planning
- Organic and sustainable farming methods
- Government schemes and subsidies
- Equipment and technology recommendations

Please provide helpful, practical advice in a friendly and conversational tone. Keep responses concise but informative.

User question: {message}

Please respond in a helpful and encouraging manner, focusing on practical solutions that Indian farmers can implement."""

        print("🔄 Calling Gemini API...")
        response = gemini_text_model.generate_content(prompt)
        print("✅ Gemini API call completed")
        
        if response and response.text:
            ai_response = response.text.strip()
            print(f"✅ Got AI response: {ai_response[:100]}...")
            return ai_response
        else:
            print("❌ Empty response from Gemini")
            return "I'm sorry, I couldn't generate a response. Please try rephrasing your question."
            
    except Exception as e:
        print(f"❌ Gemini chat error: {e}")
        import traceback
        traceback.print_exc()
        return "I'm experiencing some technical difficulties. Please try again in a moment."

def generate_conversation_title(first_message):
    """Generate a conversation title from the first message"""
    try:
        if not gemini_text_model:
            # Fallback: use first few words
            words = first_message.split()[:4]
            return ' '.join(words) + ('...' if len(first_message.split()) > 4 else '')
        
        prompt = f"""Generate a short, descriptive title (maximum 4-5 words) for a conversation that starts with this message: "{first_message}"

The title should be relevant to farming/agriculture and capture the main topic. Respond with only the title, no quotes or additional text."""

        response = gemini_text_model.generate_content(prompt)
        
        if response and response.text:
            title = response.text.strip().replace('"', '').replace("'", '')
            return title[:50]  # Limit length
        else:
            # Fallback
            words = first_message.split()[:4]
            return ' '.join(words) + ('...' if len(first_message.split()) > 4 else '')
            
    except Exception as e:
        print(f"❌ Title generation error: {e}")
        # Fallback
        words = first_message.split()[:4]
        return ' '.join(words) + ('...' if len(first_message.split()) > 4 else '')

# --- 11. Prediction API Endpoint ---
@app.route('/predict', methods=['POST'])
def predict():
    if model is None: 
        return jsonify({'error': 'Local model not loaded.'}), 500
    
    try:
        data = request.get_json()
        if 'image' not in data: 
            return jsonify({'error': 'No image data found.'}), 400
        
        # Get user ID and language from request
        user_id = data.get('user_id')  # This should come from session/token
        target_language = data.get('language', 'en')  # Default to English
        
        print(f"🔬 Starting prediction for user: {user_id}")
        
        # Process image
        processed_image = preprocess_image(data['image'])
        print(f"📸 Image processed, shape: {processed_image.shape}")
        
        # Make prediction
        prediction = model.predict(processed_image)
        predicted_class_index = np.argmax(prediction[0])
        confidence = float(prediction[0][predicted_class_index])
        predicted_class_name = class_names[predicted_class_index]
        formatted_disease_name = predicted_class_name.replace("___", " - ").replace("_", " ")
        
        print(f"🎯 Prediction: {formatted_disease_name} (confidence: {confidence:.2f})")

        yield_impact = yield_impact_db.get(predicted_class_name, yield_impact_db['default'])
        
        # Extract crop name for market search
        crop_name = predicted_class_name.split('___')[0].replace("_", " ")
        
        # Get treatment details and market prices in the selected language
        print(f"🤖 Getting treatment details from Gemini AI in {target_language}...")
        treatment_details = get_gemini_treatment_details(formatted_disease_name, target_language)
        
        print(f"💰 Getting market prices for {crop_name} in {target_language}...")
        if "healthy" not in predicted_class_name:
            market_prices = get_market_prices(crop_name, target_language)
        else:
            # Healthy plant message in different languages
            healthy_messages = {
                'en': "Plant is healthy, no market rates needed.",
                'hi': "पौधा स्वस्थ है, बाजार दर की आवश्यकता नहीं।",
                'kn': "ಸಸ್ಯ ಆರೋಗ್ಯಕರವಾಗಿರುವುದರಿಂದ ಮಾರುಕಟ್ಟೆ ದರ ಅಗತ್ಯವಿಲ್ಲ।",
                'te': "మొక్క ఆరోగ్యంగా ఉంది, మార్కెట్ రేట్లు అవసరం లేదు।",
                'ta': "செடி ஆரோக்கியமாக உள்ளது, சந்தை விலைகள் தேவையில்லை।",
                'ml': "ചെടി ആരോഗ്യകരമാണ്, മാർക്കറ്റ് നിരക്കുകൾ ആവശ്യമില്ല।",
                'mr': "रोप निरोगी आहे, बाजार दर आवश्यक नाही।",
                'gu': "છોડ સ્વસ્થ છે, બજાર દરોની જરૂર નથી।",
                'bn': "গাছ সুস্থ, বাজার দরের প্রয়োজন নেই।",
                'pa': "ਪੌਧਾ ਸਿਹਤਮੰਦ ਹੈ, ਮਾਰਕੀਟ ਰੇਟ ਦੀ ਲੋੜ ਨਹੀਂ।"
            }
            market_prices = healthy_messages.get(target_language, healthy_messages['en'])

        if treatment_details is None: 
            print(f"❌ Failed to get treatment details from Gemini AI")
            return jsonify({'error': 'Failed to get details from Gemini AI.'}), 503

        # Save the uploaded image
        image_path = None
        if user_id:
            try:
                # Create uploads directory if it doesn't exist
                import os
                uploads_dir = 'static/uploads'
                if not os.path.exists(uploads_dir):
                    os.makedirs(uploads_dir)
                
                # Save the image with a unique filename
                from datetime import datetime
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                image_filename = f"prediction_{user_id}_{timestamp}.jpg"
                image_path = f"{uploads_dir}/{image_filename}"
                
                # Decode and save the base64 image
                import base64
                import io
                from PIL import Image
                
                # Remove data URL prefix if present
                if data['image'].startswith('data:image'):
                    image_data = data['image'].split(',')[1]
                else:
                    image_data = data['image']
                
                # Decode base64 image
                image_bytes = base64.b64decode(image_data)
                image = Image.open(io.BytesIO(image_bytes))
                
                # Convert to RGB if necessary and save
                if image.mode != 'RGB':
                    image = image.convert('RGB')
                image.save(image_path, 'JPEG', quality=85)
                
                # Use relative path for database storage
                image_path = f"/static/uploads/{image_filename}"
                print(f"📸 Image saved to: {image_path}")
                
            except Exception as e:
                print(f"❌ Error saving image: {e}")
                image_path = None

        # Save prediction to database if user_id is provided
        if user_id:
            try:
                prediction_id = db.save_prediction(
                    user_id=user_id,
                    disease_name=formatted_disease_name,
                    confidence=confidence,
                    yield_impact=yield_impact,
                    symptoms=treatment_details.get('symptoms', ''),
                    organic_treatment=treatment_details.get('organic_treatment', ''),
                    chemical_treatment=treatment_details.get('chemical_treatment', ''),
                    prevention_tips=treatment_details.get('prevention_tips', ''),
                    market_prices=market_prices,
                    image_path=image_path
                )
                print(f"💾 Prediction saved to database with ID: {prediction_id}")
            except Exception as e:
                print(f"⚠️ Failed to save prediction to database: {e}")

        # Translate disease name and yield impact if not English
        if target_language != 'en':
            print(f"🌐 Translating disease name and yield impact to {target_language}...")
            try:
                translated_disease_name = translate_with_gemini(formatted_disease_name, target_language)
                translated_yield_impact = translate_with_gemini(yield_impact, target_language)
            except Exception as e:
                print(f"⚠️ Translation failed for disease name/yield impact: {e}")
                translated_disease_name = formatted_disease_name
                translated_yield_impact = yield_impact
        else:
            translated_disease_name = formatted_disease_name
            translated_yield_impact = yield_impact
        
        response = {
            'disease': translated_disease_name,
            'original_disease': formatted_disease_name,
            'confidence': confidence,
            'yield_impact': translated_yield_impact,
            'details': treatment_details,  # Already in target language from Gemini
            'market_prices': market_prices,  # Already in target language from Gemini
            'language': target_language
        }
        
        print(f"✅ Prediction completed successfully")
        return jsonify(response)
        
    except Exception as e:
        print(f"❌ Prediction Endpoint Error: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': f'An internal error occurred: {str(e)}'}), 500

# --- 11. Run the Flask App ---
if __name__ == '__main__':
    print("🌱 AI Raitha Mitra - Smart Farming Solutions")
    print("=" * 50)
    print("� Stmarting Flask server...")
    
    print("🔐 Authentication: Simple email/password (no OTP required)")
    
    print("💾 Storage: SQLite database (persistent storage)")
    
    print("🔑 Demo login credentials:")
    print("   Email: demo@raithamitra.com")
    print("   Mobile: 9876543210")
    print("   Password: 123456")
    print("=" * 50)
    
    # Production configuration
    port = int(os.environ.get('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    if os.getenv('RENDER') or os.getenv('PORT'):
        # Running on Render or other cloud platform
        print("🚀 Starting on cloud platform...")
        app.run(debug=False, host='0.0.0.0', port=port)
    else:
        # Running locally
        print("🏠 Open http://127.0.0.1:5000 in your browser")
        app.run(debug=debug, host='127.0.0.1', port=port)