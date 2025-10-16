// AI Raitha Mitra - Disease Detection JavaScript

// DOM Elements
let video, canvas, mediaContainer, initialButtons, captureButtons, loader, resultsView;
let startCameraBtn, uploadInput, uploadLabel, capturePhotoBtn, resetBtn, finalResetBtn;

// Initialize Disease Detection
function initializeDiseaseDetection() {
    // Get DOM elements with updated IDs
    video = document.getElementById('video');
    canvas = document.getElementById('canvas');
    mediaContainer = document.getElementById('mediaContainer');
    initialButtons = document.getElementById('initialButtons');
    captureButtons = document.getElementById('captureButtons');
    loader = document.getElementById('loader');
    
    startCameraBtn = document.getElementById('startCamera');
    uploadInput = document.getElementById('uploadInput');
    capturePhotoBtn = document.getElementById('capturePhoto');
    resetBtn = document.getElementById('resetBtn');
    
    // Setup event listeners
    setupEventListeners();
    
    // Setup navigation buttons
    setupNavigation();
    
    // Setup language selection
    setupLanguageSelection();
}

function setupLanguageSelection() {
    const languageSelect = document.getElementById('languageSelect');
    if (languageSelect) {
        // Load saved language preference
        const savedLanguage = localStorage.getItem('selectedLanguage') || 'en';
        languageSelect.value = savedLanguage;
        
        // Update UI language immediately
        updateUILanguage(savedLanguage);
        
        // Listen for language changes
        languageSelect.addEventListener('change', function() {
            const selectedLanguage = this.value;
            localStorage.setItem('selectedLanguage', selectedLanguage);
            updateUILanguage(selectedLanguage);
        });
    }
}

function updateUILanguage(language) {
    const translations = {
        'en': {
            'detection-title': 'AI Crop Disease Detection',
            'detection-subtitle': 'Upload or capture an image of your crop leaf for instant AI analysis',
            'placeholder-text': 'Click to capture or upload an image',
            'use-camera': 'Use Camera',
            'upload-image': 'Upload Image',
            'capture-photo': 'Capture Photo',
            'analyzing': 'Analyzing leaf & getting treatment recommendations...',
            'analysis-report': 'Analysis Report',
            'confidence': 'Confidence',
            'yield-impact': 'Yield Impact',
            'symptoms': 'Symptoms',
            'organic-treatment': 'Organic Treatment',
            'chemical-treatment': 'Chemical Treatment',
            'prevention': 'Prevention Tips',
            'market-prices': 'Market Prices',
            'new-analysis': 'New Analysis'
        },
        'hi': {
            'detection-title': 'AI फसल रोग पहचान',
            'detection-subtitle': 'तुरंत AI विश्लेषण के लिए अपनी फसल की पत्ती की तस्वीर अपलोड या कैप्चर करें',
            'placeholder-text': 'तस्वीर लेने या अपलोड करने के लिए क्लिक करें',
            'use-camera': 'कैमरा उपयोग करें',
            'upload-image': 'तस्वीर अपलोड करें',
            'capture-photo': 'फोटो लें',
            'analyzing': 'पत्ती का विश्लेषण और उपचार सुझाव प्राप्त कर रहे हैं...',
            'analysis-report': 'विश्लेषण रिपोर्ट',
            'confidence': 'विश्वसनीयता',
            'yield-impact': 'उत्पादन प्रभाव',
            'symptoms': 'लक्षण',
            'organic-treatment': 'जैविक उपचार',
            'chemical-treatment': 'रासायनिक उपचार',
            'prevention': 'रोकथाम के सुझाव',
            'market-prices': 'बाजार दर',
            'new-analysis': 'नया विश्लेषण'
        },
        'kn': {
            'detection-title': 'AI ಬೆಳೆ ರೋಗ ಪತ್ತೆ',
            'detection-subtitle': 'ತ್ವರಿತ AI ವಿಶ್ಲೇಷಣೆಗಾಗಿ ನಿಮ್ಮ ಬೆಳೆಯ ಎಲೆಯ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಅಥವಾ ಕ್ಯಾಪ್ಚರ್ ಮಾಡಿ',
            'placeholder-text': 'ಚಿತ್ರ ತೆಗೆಯಲು ಅಥವಾ ಅಪ್‌ಲೋಡ್ ಮಾಡಲು ಕ್ಲಿಕ್ ಮಾಡಿ',
            'use-camera': 'ಕ್ಯಾಮೆರಾ ಬಳಸಿ',
            'upload-image': 'ಚಿತ್ರ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
            'capture-photo': 'ಫೋಟೋ ತೆಗೆಯಿರಿ',
            'analyzing': 'ಎಲೆಯನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತಿದೆ ಮತ್ತು ಚಿಕಿತ್ಸಾ ಶಿಫಾರಸುಗಳನ್ನು ಪಡೆಯುತ್ತಿದೆ...',
            'analysis-report': 'ವಿಶ್ಲೇಷಣೆ ವರದಿ',
            'confidence': 'ವಿಶ್ವಾಸಾರ್ಹತೆ',
            'yield-impact': 'ಇಳುವರಿ ಪ್ರಭಾವ',
            'symptoms': 'ರೋಗಲಕ್ಷಣಗಳು',
            'organic-treatment': 'ಸಾವಯವ ಚಿಕಿತ್ಸೆ',
            'chemical-treatment': 'ರಾಸಾಯನಿಕ ಚಿಕಿತ್ಸೆ',
            'prevention': 'ತಡೆಗಟ್ಟುವ ಸಲಹೆಗಳು',
            'market-prices': 'ಮಾರುಕಟ್ಟೆ ದರಗಳು',
            'new-analysis': 'ಹೊಸ ವಿಶ್ಲೇಷಣೆ'
        },
        'te': {
            'detection-title': 'AI పంట వ్యాధి గుర్తింపు',
            'detection-subtitle': 'తక్షణ AI విశ్లేషణ కోసం మీ పంట ఆకు చిత్రాన్ని అప్‌లోడ్ చేయండి లేదా క్యాప్చర్ చేయండి',
            'placeholder-text': 'చిత్రం తీయడానికి లేదా అప్‌లోడ్ చేయడానికి క్లిక్ చేయండి',
            'use-camera': 'కెమెరా ఉపయోగించండి',
            'upload-image': 'చిత్రం అప్‌లోడ్ చేయండి',
            'capture-photo': 'ఫోటో తీయండి',
            'analyzing': 'ఆకును విశ్లేషిస్తున్నాము మరియు చికిత్స సిఫార్సులను పొందుతున్నాము...',
            'analysis-report': 'విశ్లేషణ నివేదిక',
            'confidence': 'విశ్వసనీయత',
            'yield-impact': 'దిగుబడి ప్రభావం',
            'symptoms': 'లక్షణాలు',
            'organic-treatment': 'సేంద్రీయ చికిత్స',
            'chemical-treatment': 'రసాయనిక చికిత్స',
            'prevention': 'నివారణ చిట్కాలు',
            'market-prices': 'మార్కెట్ ధరలు',
            'new-analysis': 'కొత్త విశ్లేషణ'
        },
        'ta': {
            'detection-title': 'AI பயிர் நோய் கண்டறிதல்',
            'detection-subtitle': 'உடனடி AI பகுப்பாய்வுக்காக உங்கள் பயிர் இலையின் படத்தை பதிவேற்றவும் அல்லது எடுக்கவும்',
            'placeholder-text': 'படம் எடுக்க அல்லது பதிவேற்ற கிளிக் செய்யவும்',
            'use-camera': 'கேமராவைப் பயன்படுத்தவும்',
            'upload-image': 'படத்தை பதிவேற்றவும்',
            'capture-photo': 'புகைப்படம் எடுக்கவும்',
            'analyzing': 'இலையை பகுப்பாய்வு செய்து சிகிச்சை பரிந்துரைகளைப் பெறுகிறோம்...',
            'analysis-report': 'பகுப்பாய்வு அறிக்கை',
            'confidence': 'நம்பகத்தன்மை',
            'yield-impact': 'விளைச்சல் தாக்கம்',
            'symptoms': 'அறிகுறிகள்',
            'organic-treatment': 'இயற்கை சிகிச்சை',
            'chemical-treatment': 'இரசாயன சிகிச்சை',
            'prevention': 'தடுப்பு குறிப்புகள்',
            'market-prices': 'சந்தை விலைகள்',
            'new-analysis': 'புதிய பகுப்பாய்வு'
        }
    };
    
    const langTranslations = translations[language] || translations['en'];
    
    // Update all elements with data-translate attributes
    document.querySelectorAll('[data-translate]').forEach(element => {
        const key = element.getAttribute('data-translate');
        if (langTranslations[key]) {
            element.textContent = langTranslations[key];
        }
    });
}

function setupEventListeners() {
    if (startCameraBtn) {
        startCameraBtn.addEventListener('click', startCamera);
    }
    
    if (uploadInput) {
        uploadInput.addEventListener('change', handleImageUpload);
    }
    
    if (capturePhotoBtn) {
        capturePhotoBtn.addEventListener('click', capturePhoto);
    }
    
    if (resetBtn) {
        resetBtn.addEventListener('click', resetState);
    }
}

function setupNavigation() {
    // Home buttons
    const homeBtn = document.getElementById('homeBtn');
    const homeFromResults = document.getElementById('homeFromResults');
    
    [homeBtn, homeFromResults].forEach(btn => {
        if (btn) {
            btn.addEventListener('click', function() {
                window.location.href = '/';
            });
        }
    });
    
    // Logout button
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function() {
            localStorage.removeItem('authToken');
            localStorage.removeItem('userData');
            localStorage.removeItem('currentUser');
            window.location.href = '/';
        });
    }
    
    // New analysis buttons
    const newAnalysisBtn = document.getElementById('newAnalysisBtn');
    const analyzeAgainBtn = document.getElementById('analyzeAgainBtn');
    
    [newAnalysisBtn, analyzeAgainBtn].forEach(btn => {
        if (btn) {
            btn.addEventListener('click', function() {
                // Reset to detection interface
                document.getElementById('resultsSection').classList.add('hidden');
                document.getElementById('detectionInterface').classList.remove('hidden');
                resetState();
                window.scrollTo(0, 0);
            });
        }
    });
    
    // Download report button
    const downloadReportBtn = document.getElementById('downloadReportBtn');
    if (downloadReportBtn) {
        downloadReportBtn.addEventListener('click', downloadReport);
    }
    
    // Share results button
    const shareResultsBtn = document.getElementById('shareResultsBtn');
    if (shareResultsBtn) {
        shareResultsBtn.addEventListener('click', shareResults);
    }
    
    // Show user welcome message
    const userWelcome = document.getElementById('userWelcome');
    if (userWelcome) {
        const userData = JSON.parse(localStorage.getItem('userData') || '{}');
        if (userData.name) {
            userWelcome.textContent = `Welcome, ${userData.name}`;
        }
    }
}

// Remove the addHomeButton function as navigation is now handled in setupNavigation

async function startCamera() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ 
            video: { facingMode: 'environment' } 
        });
        
        video.srcObject = stream;
        video.classList.remove('hidden');
        canvas.classList.add('hidden');
        
        initialButtons.classList.add('hidden');
        captureButtons.classList.remove('hidden');
        
        document.getElementById('placeholderContent').classList.add('hidden');
    } catch (error) {
        console.error('Camera access error:', error);
        alert('Unable to access camera. Please check permissions or use image upload instead.');
    }
}

function handleImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        const img = new Image();
        img.onload = function() {
            // Draw image to canvas
            canvas.width = img.width;
            canvas.height = img.height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            
            // Show canvas and hide video
            canvas.classList.remove('hidden');
            video.classList.add('hidden');
            document.getElementById('placeholderContent').classList.add('hidden');
            
            // Update buttons
            initialButtons.classList.add('hidden');
            captureButtons.classList.remove('hidden');
            
            // Auto-analyze the uploaded image
            analyzeImage();
        };
        img.src = e.target.result;
    };
    reader.readAsDataURL(file);
}

function capturePhoto() {
    if (!video.srcObject) return;
    
    // Set canvas dimensions to match video
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    
    // Draw video frame to canvas
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0);
    
    // Stop video stream
    const stream = video.srcObject;
    const tracks = stream.getTracks();
    tracks.forEach(track => track.stop());
    video.srcObject = null;
    
    // Show canvas and hide video
    canvas.classList.remove('hidden');
    video.classList.add('hidden');
    
    // Analyze the captured image
    analyzeImage();
}

function resetState() {
    // Stop video stream if active
    if (video.srcObject) {
        const stream = video.srcObject;
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
        video.srcObject = null;
    }
    
    // Reset UI elements
    video.classList.add('hidden');
    canvas.classList.add('hidden');
    document.getElementById('placeholderContent').classList.remove('hidden');
    
    initialButtons.classList.remove('hidden');
    captureButtons.classList.add('hidden');
    resultsView.classList.add('hidden');
    loader.classList.add('hidden');
    
    // Clear upload input
    if (uploadInput) {
        uploadInput.value = '';
    }
}

async function analyzeImage() {
    if (!canvas) return;
    
    loader.classList.remove('hidden');
    
    const imageDataURL = canvas.toDataURL('image/jpeg');
    
    // Get user data for the prediction
    const userData = JSON.parse(localStorage.getItem('userData') || '{}');
    const userId = userData.id;
    
    try {
        console.log('🔬 Starting image analysis...');
        
        // Get selected language
        const languageSelect = document.getElementById('languageSelect');
        const selectedLanguage = languageSelect ? languageSelect.value : 'en';
        
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                image: imageDataURL,
                user_id: userId,
                language: selectedLanguage
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
        }
        
        const data = await response.json();
        console.log('✅ Analysis completed:', data);
        displayResults(data);

    } catch (error) {
        console.error("❌ Analysis Error:", error);
        loader.classList.add('hidden');
        alert(`Failed to get analysis from the server: ${error.message}\n\nPlease ensure the Python backend is running and try again.`);
        resetState();
    }
}

// Function to clean text formatting
function cleanDisplayText(text) {
    if (!text) return text;
    
    // Remove excessive asterisks and markdown formatting
    text = text.replace(/\*{2,}/g, '');  // Remove multiple asterisks
    text = text.replace(/\*([^*]+)\*/g, '$1');  // Remove single asterisks around text
    text = text.replace(/#{1,6}\s*/g, '');  // Remove markdown headers
    text = text.replace(/`([^`]+)`/g, '$1');  // Remove code formatting
    text = text.replace(/\[([^\]]+)\]\([^)]+\)/g, '$1');  // Remove markdown links
    
    // Clean up bullet points and formatting
    text = text.replace(/^\s*[-•*]\s*/gm, '• ');  // Standardize bullet points
    text = text.replace(/\n\s*\n\s*\n/g, '\n\n');  // Remove excessive line breaks
    text = text.replace(/^\s+|\s+$/g, '');  // Remove leading/trailing whitespace
    
    // Fix common formatting issues
    text = text.replace(/\s+/g, ' ');  // Replace multiple spaces with single space
    text = text.replace(/\n\s*/g, '\n');  // Clean up line breaks
    
    // Improve number formatting and spacing
    text = text.replace(/(\d+)\.\s*/g, '$1. ');  // Fix numbered lists
    text = text.replace(/:\s*\n/g, ':\n');  // Clean up colons before line breaks
    text = text.replace(/\.\s*\n/g, '.\n');  // Clean up periods before line breaks
    
    return text.trim();
}

function displayResults(data) {
    // Update result elements with cleaned content
    const elements = {
        'diseaseName': cleanDisplayText(data.disease) || "N/A",
        'yieldImpact': cleanDisplayText(data.yield_impact) || "N/A", 
        'marketPrices': cleanDisplayText(data.market_prices) || "Market prices not available",
        'symptoms': cleanDisplayText(data.details.symptoms) || "Details not available",
        'organicTreatment': cleanDisplayText(data.details.organic_treatment) || "Details not available",
        'chemicalTreatment': cleanDisplayText(data.details.chemical_treatment) || "Details not available",
        'preventionTips': cleanDisplayText(data.details.prevention_tips) || "Details not available"
    };
    
    Object.entries(elements).forEach(([id, content]) => {
        const element = document.getElementById(id);
        if (element) {
            // Enhanced formatting for better readability
            let formattedContent = content
                .replace(/\n/g, '<br>')  // Convert line breaks to HTML
                .replace(/• /g, '<br>• ')  // Add line breaks before bullet points
                .replace(/(\d+\.\s)/g, '<br>$1')  // Add line breaks before numbered items
                .replace(/^<br>/, '')  // Remove leading line break
                .replace(/<br>\s*<br>/g, '<br>');  // Remove double line breaks
            
            // Add proper spacing for different content types
            if (id === 'marketPrices') {
                // Special formatting for market prices
                formattedContent = formattedContent
                    .replace(/₹/g, '<strong>₹</strong>')  // Bold currency symbols
                    .replace(/(\d+\s*-\s*₹?\d+)/g, '<strong>$1</strong>');  // Bold price ranges
            }
            
            element.innerHTML = formattedContent;
        }
    });
    
    // Update confidence score with animation
    if (data.confidence) {
        const confidencePercent = Math.round(data.confidence * 100);
        const confidenceBar = document.getElementById('confidenceBar');
        const confidenceText = document.getElementById('confidenceText');
        
        if (confidenceBar && confidenceText) {
            // Animate the progress bar
            setTimeout(() => {
                confidenceBar.style.width = confidencePercent + '%';
                confidenceText.textContent = confidencePercent + '%';
                
                // Change color based on confidence level
                if (confidencePercent >= 80) {
                    confidenceBar.className = 'bg-green-500 h-4 rounded-full transition-all duration-1000';
                } else if (confidencePercent >= 60) {
                    confidenceBar.className = 'bg-yellow-500 h-4 rounded-full transition-all duration-1000';
                } else {
                    confidenceBar.className = 'bg-red-500 h-4 rounded-full transition-all duration-1000';
                }
            }, 500);
        }
    }
    
    // Update language indicator
    const languageSelect = document.getElementById('languageSelect');
    const currentLanguageSpan = document.getElementById('currentLanguage');
    if (languageSelect && currentLanguageSpan) {
        const selectedOption = languageSelect.options[languageSelect.selectedIndex];
        currentLanguageSpan.textContent = selectedOption.text;
    }
    
    // Hide detection interface and show results section
    document.getElementById('detectionInterface').classList.add('hidden');
    document.getElementById('resultsSection').classList.remove('hidden');
    
    // Scroll to top
    window.scrollTo(0, 0);
}

// Download report functionality
function downloadReport() {
    const reportData = {
        disease: document.getElementById('diseaseName').textContent,
        yieldImpact: document.getElementById('yieldImpact').textContent,
        marketPrices: document.getElementById('marketPrices').textContent,
        symptoms: document.getElementById('symptoms').textContent,
        organicTreatment: document.getElementById('organicTreatment').textContent,
        chemicalTreatment: document.getElementById('chemicalTreatment').textContent,
        preventionTips: document.getElementById('preventionTips').textContent,
        date: new Date().toLocaleDateString(),
        time: new Date().toLocaleTimeString()
    };
    
    const reportContent = `
AI RAITHA MITRA - DISEASE ANALYSIS REPORT
=========================================
Date: ${reportData.date}
Time: ${reportData.time}

DETECTED DISEASE: ${reportData.disease}
YIELD IMPACT: ${reportData.yieldImpact}

MARKET PRICES:
${reportData.marketPrices}

SYMPTOMS:
${reportData.symptoms}

ORGANIC TREATMENT:
${reportData.organicTreatment}

CHEMICAL TREATMENT:
${reportData.chemicalTreatment}

PREVENTION TIPS:
${reportData.preventionTips}

Generated by AI Raitha Mitra
Smart Farming Solutions
    `;
    
    const blob = new Blob([reportContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `crop-analysis-report-${new Date().toISOString().split('T')[0]}.txt`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);
}

// Share results functionality
function shareResults() {
    const disease = document.getElementById('diseaseName').textContent;
    const yieldImpact = document.getElementById('yieldImpact').textContent;
    
    const shareText = `🌱 AI Raitha Mitra Analysis Results\n\n` +
                     `🦠 Disease: ${disease}\n` +
                     `📊 Yield Impact: ${yieldImpact}\n\n` +
                     `Get instant crop disease detection at AI Raitha Mitra!`;
    
    if (navigator.share) {
        // Use native sharing if available
        navigator.share({
            title: 'Crop Disease Analysis Results',
            text: shareText,
            url: window.location.href
        }).catch(console.error);
    } else {
        // Fallback to copying to clipboard
        navigator.clipboard.writeText(shareText).then(() => {
            alert('Results copied to clipboard! You can now paste and share.');
        }).catch(() => {
            // Final fallback - show text in alert
            alert('Share this result:\n\n' + shareText);
        });
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Check authentication first
    if (!RaithaMitra.checkAuthentication()) {
        return;
    }
    
    // Initialize disease detection
    initializeDiseaseDetection();
});