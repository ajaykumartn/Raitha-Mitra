# 🌾 AI Raitha Mitra - Smart Farming Solutions

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-green.svg)](https://flask.palletsprojects.com/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20.0-orange.svg)](https://tensorflow.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**AI Raitha Mitra** is an intelligent agricultural platform that empowers farmers with AI-powered crop disease detection, real-time weather information, and comprehensive treatment recommendations in multiple Indian languages.

## 🌟 Features

### 🤖 AI-Powered Disease Detection
- **95% Accuracy**: Advanced TensorFlow model trained on 38+ crop diseases
- **Instant Results**: Upload crop images and get immediate disease identification
- **Confidence Scoring**: Detailed confidence percentages for each prediction
- **Yield Impact Assessment**: Understand potential crop loss from diseases

### 🌤️ Real-Time Weather Integration
- **Current Weather**: Live temperature, humidity, wind speed, and pressure
- **5-Day Forecast**: Detailed weather predictions for farming decisions
- **Location Services**: Auto-detect user location or manual city selection
- **Farming-Focused**: Weather data tailored for agricultural planning

### 🌍 Multi-Language Support
- **10 Indian Languages**: Hindi, Kannada, Telugu, Tamil, Malayalam, Marathi, Gujarati, Bengali, Punjabi
- **AI Translation**: Gemini AI provides treatment advice in local languages
- **Farmer-Friendly**: Simple, actionable language for rural communities

### 🤖 AI Chat Assistant
- **24/7 Agricultural Support**: Get instant answers to farming questions
- **Gemini AI Powered**: Advanced conversational AI for agriculture
- **User-Specific Conversations**: Persistent chat history for each user
- **Farming Expertise**: Specialized knowledge in crops, diseases, and best practices
- **Multi-topic Support**: Weather advice, crop planning, pest management, and more

### 💊 Comprehensive Treatment Recommendations
- **Organic Solutions**: Natural, eco-friendly treatment methods
- **Chemical Options**: Effective chemical treatments with proper dosages
- **Prevention Tips**: Proactive measures to prevent disease recurrence
- **Market Prices**: Real-time crop pricing from major Indian markets

### 👤 User Management
- **Simple Authentication**: Email/mobile + password (no OTP complexity)
- **Prediction History**: Track all disease detections with images
- **Profile Management**: User profiles with prediction analytics
- **Secure Storage**: SQLite database with encrypted passwords

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- 4GB+ RAM (for TensorFlow model)
- Internet connection (for AI services)

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/ai-raitha-mitra.git
   cd ai-raitha-mitra
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv myenv
   
   # Windows
   myenv\Scripts\activate
   
   # Linux/Mac
   source myenv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   ```bash
   # Copy and edit environment file
   cp .env.example .env
   
   # Add your API keys (see Configuration section)
   ```

5. **Run the Application**
   ```bash
   python app.py
   ```

6. **Access the Application**
   ```
   Open http://127.0.0.1:5000 in your browser
   ```

## ⚙️ Configuration

### Required API Keys

#### 1. Gemini AI API (Required)
```env
GEMINI_API_KEY="your_gemini_api_key_here"
```
- Get free API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
- Used for treatment recommendations and translations

#### 2. OpenWeatherMap API (Optional)
```env
OPENWEATHER_API_KEY="your_openweather_api_key_here"
```
- Get free API key from [OpenWeatherMap](https://openweathermap.org/api)
- Used for live weather data (falls back to demo data if not configured)

### Environment Variables
```env
# AI Configuration
GEMINI_API_KEY="your_gemini_api_key_here"

# Weather Configuration
OPENWEATHER_API_KEY="your_openweather_api_key_here"

# Flask Configuration
FLASK_SECRET_KEY="your_secret_key_here"
FLASK_DEBUG=True
```

## 📱 Usage

### For Farmers

1. **Register/Login**
   - Create account with email/mobile and password
   - No OTP verification required - instant access

2. **Disease Detection**
   - Upload clear crop images (leaves, fruits, stems)
   - Get instant AI-powered disease identification
   - View detailed treatment recommendations

3. **Weather Information**
   - Check current weather conditions
   - View 5-day forecast for farming decisions
   - Use location services for accurate local weather

4. **Treatment Guidance**
   - Organic and chemical treatment options
   - Step-by-step instructions in local language
   - Prevention tips to avoid future issues

5. **History Tracking**
   - View all past disease predictions
   - Click predictions for detailed treatment info
   - Track farming decisions over time

### Demo Credentials
```
Email: demo@raithamitra.com
Password: 123456
```

## 🏗️ Project Structure

```
AI Raitha Mitra/
├── 📁 static/
│   ├── 📁 css/
│   │   └── main.css              # Main stylesheet with modern design
│   ├── 📁 js/
│   │   ├── auth.js               # Authentication functionality
│   │   ├── disease-detection.js  # Disease detection logic
│   │   ├── main.js               # Core JavaScript functionality
│   │   └── weather.js            # Weather widget functionality
│   └── 📁 uploads/               # User-uploaded images storage
├── 📁 templates/
│   ├── home.html                 # Landing page with weather widget
│   ├── login.html                # User login interface
│   ├── register.html             # User registration interface
│   └── index.html                # Disease detection interface
├── app.py                        # Main Flask application
├── database.py                   # SQLite database management
├── crop_disease_model.py         # AI model training script
├── class_names.json              # Disease classification labels
├── crop_disease_detection_model.h5  # Trained TensorFlow model
├── raitha_mitra.db              # SQLite database file
├── reset_user_password.py       # Password reset utility
├── requirements.txt              # Python dependencies
├── .env                          # Environment configuration
├── WEATHER_SETUP.md             # Weather API setup guide
└── README.md                     # This file
```

## 🤖 AI Model Details

### Disease Detection Model
- **Architecture**: Convolutional Neural Network (CNN)
- **Framework**: TensorFlow 2.20.0
- **Input Size**: 128x128x3 RGB images
- **Classes**: 38+ crop diseases across multiple crops
- **Accuracy**: 95%+ on validation dataset

### Supported Crops & Diseases
- **Apple**: Apple Scab, Black Rot, Cedar Apple Rust
- **Corn**: Cercospora Leaf Spot, Common Rust, Northern Leaf Blight
- **Grape**: Black Rot, Esca, Leaf Blight
- **Orange**: Huanglongbing (Citrus Greening)
- **Potato**: Early Blight, Late Blight
- **Tomato**: Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus
- **Cherry**: Various diseases and healthy detection

## 🌐 API Endpoints

### Authentication
```http
POST /api/register          # User registration
POST /api/login             # User login
POST /api/change-password   # Change password
```

### Disease Detection
```http
POST /predict               # Disease prediction from image
GET /api/prediction-history # User's prediction history
```

### Weather
```http
GET /api/weather           # Current weather data
GET /api/weather/forecast  # Weather forecast
```

## 🛠️ Development

### Setting Up Development Environment

1. **Install Development Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Enable Debug Mode**
   ```env
   FLASK_DEBUG=True
   ```

3. **Database Management**
   ```bash
   # Reset user password
   python reset_user_password.py
   
   # Train new model (if needed)
   python crop_disease_model.py
   ```

### Code Structure

#### Backend (Python/Flask)
- **app.py**: Main application with routes and business logic
- **database.py**: SQLite database operations and management
- **crop_disease_model.py**: AI model training and evaluation

#### Frontend (HTML/CSS/JavaScript)
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Modern UI**: Gradient buttons, animations, and clean layouts
- **Progressive Enhancement**: Works without JavaScript for basic functionality

#### AI Integration
- **TensorFlow**: Local disease detection model
- **Gemini AI**: Treatment recommendations and translations
- **Image Processing**: PIL for image preprocessing and optimization

## 🔧 Troubleshooting

### Common Issues

#### 1. Model Loading Error
```
Error: Local model or class names file not found
```
**Solution**: Ensure `crop_disease_detection_model.h5` and `class_names.json` exist in project root

#### 2. Gemini AI Error
```
Error configuring Gemini AI: Invalid API key
```
**Solution**: Check `GEMINI_API_KEY` in `.env` file and ensure it's valid

#### 3. Weather Not Loading
```
Weather API not configured
```
**Solution**: Add `OPENWEATHER_API_KEY` to `.env` file (optional - falls back to demo data)

#### 4. Database Error
```
Database connection failed
```
**Solution**: Ensure SQLite is installed and `raitha_mitra.db` has proper permissions

### Performance Optimization

1. **Image Upload Size**: Limit images to 5MB for faster processing
2. **Model Caching**: TensorFlow model is loaded once at startup
3. **Database Indexing**: Optimized queries for user data and predictions
4. **Static File Caching**: CSS/JS files cached for better performance

## 🚀 Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   # Set production environment
   export FLASK_ENV=production
   export FLASK_DEBUG=False
   ```

2. **Security Configuration**
   ```env
   # Use strong secret key
   FLASK_SECRET_KEY="your-strong-secret-key-here"
   
   # Configure HTTPS for production
   ```

3. **Web Server**
   ```bash
   # Using Gunicorn (recommended)
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   
   # Or using uWSGI
   pip install uwsgi
   uwsgi --http :8000 --wsgi-file app.py --callable app
   ```

4. **Database Backup**
   ```bash
   # Regular backup of SQLite database
   cp raitha_mitra.db raitha_mitra_backup_$(date +%Y%m%d).db
   ```

### Docker Deployment (Optional)

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 5000

CMD ["python", "app.py"]
```

## 📊 Analytics & Monitoring

### Built-in Analytics
- **User Registration Tracking**: Monitor farmer adoption
- **Disease Detection Stats**: Track most common diseases
- **Geographic Distribution**: Understand regional disease patterns
- **Treatment Effectiveness**: Monitor farmer feedback

### Monitoring Endpoints
```http
GET /api/health            # Application health check
GET /api/stats             # Basic usage statistics
```

## 🤝 Contributing

We welcome contributions from the community! Here's how you can help:

### Areas for Contribution
1. **New Disease Models**: Train models for additional crops
2. **Language Support**: Add more regional languages
3. **UI/UX Improvements**: Enhance farmer experience
4. **Performance Optimization**: Improve speed and efficiency
5. **Documentation**: Improve guides and tutorials

### Development Guidelines
1. **Fork the Repository**: Create your own copy
2. **Create Feature Branch**: `git checkout -b feature/new-feature`
3. **Follow Code Style**: Use Python PEP 8 standards
4. **Add Tests**: Include tests for new functionality
5. **Submit Pull Request**: Describe changes clearly

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **TensorFlow Team**: For the machine learning framework
- **Google AI**: For Gemini AI API and translation services
- **OpenWeatherMap**: For weather data API
- **Flask Community**: For the web framework
- **Indian Farmers**: For inspiration and feedback

## 📞 Support

### Getting Help
- **Documentation**: Check this README and `WEATHER_SETUP.md`
- **Issues**: Report bugs on GitHub Issues
- **Discussions**: Join community discussions
- **Email**: Contact support team

### Community
- **GitHub**: [AI Raitha Mitra Repository](https://github.com/yourusername/ai-raitha-mitra)
- **Discussions**: Share experiences and get help
- **Feedback**: Help improve the platform for farmers

---

## 🌾 Made with ❤️ for Indian Farmers

**AI Raitha Mitra** is dedicated to empowering farmers with technology, helping them make informed decisions, and improving agricultural productivity across India.

*"Technology should serve humanity, and agriculture feeds humanity."*

---

### 📈 Project Status

- ✅ **Core Features**: Complete and tested
- ✅ **AI Model**: Trained and optimized
- ✅ **Multi-language**: 10 Indian languages supported
- ✅ **Weather Integration**: Live data and forecasts
- ✅ **User Management**: Simplified authentication
- ✅ **Production Ready**: Deployed and scalable

**Version**: 1.0.0  
**Last Updated**: October 2025  
**Status**: Active Development