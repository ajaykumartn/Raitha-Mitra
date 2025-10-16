// AI Raitha Mitra - Main JavaScript File

// Global Variables
let currentLanguage = 'en';

// Language Translations
const translations = {
    en: {
        mainTitle: "Krishi Mitra AI",
        subtitle: "Upload a photo of your crop leaf to get instant AI-powered disease analysis and treatment recommendations",
        placeholderText: "Use your camera or upload an image to begin",
        useCameraBtn: "Use Camera",
        uploadImageBtn: "Upload Image",
        capturePhotoBtn: "Capture Photo",
        startOverBtn: "Start Over",
        loaderText: "Analyzing leaf & fetching market rates with Gemini...",
        analysisReport: "Analysis Report",
        detectedDisease: "Detected Disease:",
        yieldImpact: "Predicted Yield Impact:",
        marketRatesTitle: "✨ Today's Market Rates",
        symptomsTitle: "Symptoms",
        organicTitle: "Organic Treatment",
        chemicalTitle: "Chemical Treatment",
        preventionTitle: "Prevention Tips",
        newAnalysisBtn: "New Analysis",
        noMarketPrices: "Market prices not available",
        noDetails: "Details not available"
    },
    kn: {
        mainTitle: "ಕೃಷಿ ಮಿತ್ರ AI",
        subtitle: "ತ್ವರಿತ AI-ಚಾಲಿತ ರೋಗ ವಿಶ್ಲೇಷಣೆ ಮತ್ತು ಚಿಕಿತ್ಸಾ ಶಿಫಾರಸುಗಳನ್ನು ಪಡೆಯಲು ನಿಮ್ಮ ಬೆಳೆಯ ಎಲೆಯ ಫೋಟೋವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        placeholderText: "ಪ್ರಾರಂಭಿಸಲು ನಿಮ್ಮ ಕ್ಯಾಮೆರಾವನ್ನು ಬಳಸಿ ಅಥವಾ ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        useCameraBtn: "ಕ್ಯಾಮೆರಾ ಬಳಸಿ",
        uploadImageBtn: "ಚಿತ್ರ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        capturePhotoBtn: "ಫೋಟೋ ತೆಗೆಯಿರಿ",
        startOverBtn: "ಮತ್ತೆ ಪ್ರಾರಂಭಿಸಿ",
        loaderText: "ಎಲೆಯನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತಿದೆ ಮತ್ತು ಮಾರುಕಟ್ಟೆ ದರಗಳನ್ನು ಪಡೆಯುತ್ತಿದೆ...",
        analysisReport: "ವಿಶ್ಲೇಷಣೆ ವರದಿ",
        detectedDisease: "ಪತ್ತೆಯಾದ ರೋಗ:",
        yieldImpact: "ಅಂದಾಜು ಇಳುವರಿ ಪ್ರಭಾವ:",
        marketRatesTitle: "✨ ಇಂದಿನ ಮಾರುಕಟ್ಟೆ ದರಗಳು",
        symptomsTitle: "ರೋಗಲಕ್ಷಣಗಳು",
        organicTitle: "ಸಾವಯವ ಚಿಕಿತ್ಸೆ",
        chemicalTitle: "ರಾಸಾಯನಿಕ ಚಿಕಿತ್ಸೆ",
        preventionTitle: "ತಡೆಗಟ್ಟುವಿಕೆ ಸಲಹೆಗಳು",
        newAnalysisBtn: "ಹೊಸ ವಿಶ್ಲೇಷಣೆ",
        noMarketPrices: "ಮಾರುಕಟ್ಟೆ ದರಗಳು ಲಭ್ಯವಿಲ್ಲ",
        noDetails: "ವಿವರಗಳು ಲಭ್ಯವಿಲ್ಲ"
    }
};

// Utility Functions
function updateLanguage(lang) {
    currentLanguage = lang;
    const t = translations[lang];

    // Update text content
    const elements = {
        'main-title': t.mainTitle,
        'subtitle': t.subtitle,
        'placeholder-text': t.placeholderText,
        'start-camera': t.useCameraBtn,
        'upload-label': t.uploadImageBtn,
        'capture-photo': t.capturePhotoBtn,
        'reset-btn': t.startOverBtn,
        'loader-text': t.loaderText,
        'analysis-report': t.analysisReport,
        'detected-disease': t.detectedDisease,
        'yield-impact': t.yieldImpact,
        'market-rates-title': t.marketRatesTitle,
        'symptoms-title': t.symptomsTitle,
        'organic-title': t.organicTitle,
        'chemical-title': t.chemicalTitle,
        'prevention-title': t.preventionTitle,
        'final-reset-btn': t.newAnalysisBtn
    };

    Object.entries(elements).forEach(([id, text]) => {
        const element = document.getElementById(id);
        if (element) element.textContent = text;
    });
}

// Authentication Functions
function checkAuthentication() {
    const authToken = localStorage.getItem('authToken');
    const userData = localStorage.getItem('userData');

    if (!authToken || !userData) {
        alert('Please login first to access disease detection');
        window.location.href = '/login?redirect=disease';
        return false;
    }

    try {
        // Validate user data
        const user = JSON.parse(userData);
        if (!user || !user.id) {
            throw new Error('Invalid user data');
        }

        // Update welcome message if element exists
        const userWelcome = document.getElementById('userWelcome');
        if (userWelcome) {
            const name = user.name || user.email.split('@')[0];
            userWelcome.textContent = `Welcome, ${name}`;
        }

        return true;
    } catch (error) {
        console.error('Error validating user data:', error);
        localStorage.removeItem('authToken');
        localStorage.removeItem('userData');
        localStorage.removeItem('currentUser');
        alert('Session expired. Please login again.');
        window.location.href = '/login?redirect=disease';
        return false;
    }
}

function logout() {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    localStorage.removeItem('currentUser');
    window.location.href = '/';
}

// Navigation Functions
function navigateToHome() {
    window.location.href = '/home';
}

function navigateToLogin() {
    window.location.href = '/login';
}

function navigateToRegister() {
    window.location.href = '/register';
}

function navigateToDiseaseDetection() {
    const authToken = localStorage.getItem('authToken');
    const userData = localStorage.getItem('userData');

    if (authToken && userData) {
        window.location.href = '/disease-detection';
    } else {
        alert('Please login first to access disease detection');
        window.location.href = '/login?redirect=disease';
    }
}

// Form Validation Functions
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

function validateMobile(mobile) {
    const mobileRegex = /^[6-9]\d{9}$/;
    return mobileRegex.test(mobile);
}

function validatePassword(password) {
    return password.length >= 6;
}

// API Functions
async function apiCall(endpoint, method = 'GET', data = null) {
    const config = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };

    if (data) {
        config.body = JSON.stringify(data);
    }

    try {
        const response = await fetch(`http://127.0.0.1:5000${endpoint}`, config);
        const result = await response.json();

        if (!response.ok) {
            throw new Error(result.error || `HTTP error! Status: ${response.status}`);
        }

        return result;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// OTP Functions
function setupOTPInputs() {
    const otpInputs = document.querySelectorAll('.otp-input');
    otpInputs.forEach((input, index) => {
        input.addEventListener('input', function () {
            if (this.value.length === 1 && index < otpInputs.length - 1) {
                otpInputs[index + 1].focus();
            }
        });

        input.addEventListener('keydown', function (e) {
            if (e.key === 'Backspace' && this.value === '' && index > 0) {
                otpInputs[index - 1].focus();
            }
        });
    });
}

function getOTPValue() {
    const otpInputs = document.querySelectorAll('.otp-input');
    return Array.from(otpInputs).map(input => input.value).join('');
}

function clearOTPInputs() {
    const otpInputs = document.querySelectorAll('.otp-input');
    otpInputs.forEach(input => input.value = '');
    if (otpInputs.length > 0) otpInputs[0].focus();
}

// Location Functions
function getCurrentLocation() {
    return new Promise((resolve, reject) => {
        if (!navigator.geolocation) {
            reject(new Error('Geolocation is not supported by this browser'));
            return;
        }

        navigator.geolocation.getCurrentPosition(
            position => {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                resolve(`${lat}, ${lon}`);
            },
            error => {
                reject(new Error('Unable to get location'));
            }
        );
    });
}

// Password Toggle Function
function setupPasswordToggle(passwordFieldId, toggleButtonId) {
    const passwordField = document.getElementById(passwordFieldId);
    const toggleButton = document.getElementById(toggleButtonId);

    if (passwordField && toggleButton) {
        toggleButton.addEventListener('click', function () {
            const icon = this.querySelector('i');

            if (passwordField.type === 'password') {
                passwordField.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                passwordField.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    }
}

// Smooth Scrolling
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const href = this.getAttribute('href');

            // Skip if href is just '#' or empty
            if (!href || href === '#' || href.length <= 1) {
                return;
            }

            try {
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            } catch (error) {
                console.warn('Invalid selector:', href, error);
            }
        });
    });
}

// Dynamic Background Functions
function setupVideoBackground() {
    const video = document.getElementById('heroVideo');
    const videoToggle = document.getElementById('videoToggle');
    const videoIcon = document.getElementById('videoIcon');
    const videoText = document.getElementById('videoText');
    const watchDemoBtn = document.getElementById('watchDemoBtn');
    const heroBackground = document.getElementById('heroBackground');

    // Start background slideshow
    if (heroBackground) {
        heroBackground.classList.add('hero-slideshow');
    }

    // Try to load and play video
    if (video) {
        // Attempt to load video
        video.addEventListener('loadeddata', function () {
            console.log('Video loaded successfully');
            video.style.display = 'block';
            video.style.opacity = '1';

            video.play().then(function () {
                console.log('Video playing');
                // Hide slideshow background when video plays
                if (heroBackground) {
                    heroBackground.style.opacity = '0';
                }
            }).catch(function (error) {
                console.log('Autoplay prevented:', error);
                handleVideoError();
            });
        });

        video.addEventListener('error', function () {
            console.log('Video failed to load, using slideshow background');
            handleVideoError();
        });

        // Video toggle functionality
        if (videoToggle) {
            videoToggle.addEventListener('click', function () {
                if (video.style.display === 'none') {
                    // Try to show video
                    video.style.display = 'block';
                    video.play().then(function () {
                        video.style.opacity = '1';
                        heroBackground.style.opacity = '0';
                        videoIcon.className = 'fas fa-pause mr-2';
                        videoText.textContent = 'Pause Video';
                    }).catch(function () {
                        handleVideoError();
                    });
                } else if (video.paused) {
                    video.play();
                    video.style.opacity = '1';
                    heroBackground.style.opacity = '0';
                    videoIcon.className = 'fas fa-pause mr-2';
                    videoText.textContent = 'Pause Video';
                } else {
                    video.pause();
                    video.style.opacity = '0';
                    heroBackground.style.opacity = '1';
                    videoIcon.className = 'fas fa-play mr-2';
                    videoText.textContent = 'Play Video';
                }
            });
        }
    }

    function handleVideoError() {
        if (video) {
            video.style.display = 'none';
        }
        if (heroBackground) {
            heroBackground.style.opacity = '1';
        }
        if (videoToggle) {
            videoToggle.style.display = 'none';
        }
    }

    // Watch Demo button functionality
    if (watchDemoBtn) {
        watchDemoBtn.addEventListener('click', function () {
            // Create demo modal
            showDemoModal();
        });
    }
}

function showDemoModal() {
    // Use the new video modal instead
    const videoModal = document.getElementById('videoDemoModal');
    if (videoModal) {
        videoModal.classList.remove('hidden');
        document.body.style.overflow = 'hidden';
    }
}

// Initialize Common Functions
document.addEventListener('DOMContentLoaded', function () {
    // Setup smooth scrolling
    setupSmoothScrolling();

    // Setup video background if on home page
    if (window.location.pathname === '/' || window.location.pathname === '/home' || window.location.pathname.includes('home')) {
        setupVideoBackground();
    }

    // Setup language selector if present
    const languageSelect = document.getElementById('language-select');
    if (languageSelect) {
        languageSelect.addEventListener('change', function () {
            updateLanguage(this.value);
        });
    }

    // Setup OTP inputs if present
    setupOTPInputs();

    // Setup password toggles if present
    setupPasswordToggle('password', 'togglePassword');

    // Update initial language
    updateLanguage(currentLanguage);
});

// Export functions for use in other files
window.RaithaMitra = {
    checkAuthentication,
    logout,
    navigateToHome,
    navigateToLogin,
    navigateToRegister,
    navigateToDiseaseDetection,
    validateEmail,
    validateMobile,
    validatePassword,
    apiCall,
    getCurrentLocation,
    getOTPValue,
    clearOTPInputs,
    updateLanguage,
    setupPasswordToggle: setupPasswordToggle
};

// Mobile Menu Functionality
document.addEventListener('DOMContentLoaded', function () {
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const mobileMenu = document.getElementById('mobileMenu');
    const mobileMenuOverlay = document.getElementById('mobileMenuOverlay');
    const closeMobileMenu = document.getElementById('closeMobileMenu');

    function openMobileMenu() {
        mobileMenu.classList.remove('-translate-x-full');
        mobileMenu.classList.add('translate-x-0');
        mobileMenuOverlay.classList.remove('hidden');
        document.body.style.overflow = 'hidden';

        // Change hamburger to X
        const icon = mobileMenuBtn.querySelector('i');
        if (icon) {
            icon.className = 'fas fa-times text-xl';
        }
    }

    function closeMobileMenuFunc() {
        mobileMenu.classList.remove('translate-x-0');
        mobileMenu.classList.add('-translate-x-full');
        mobileMenuOverlay.classList.add('hidden');
        document.body.style.overflow = '';

        // Change X back to hamburger
        const icon = mobileMenuBtn.querySelector('i');
        if (icon) {
            icon.className = 'fas fa-bars text-xl';
        }
    }

    if (mobileMenuBtn && mobileMenu) {
        // Toggle mobile menu
        mobileMenuBtn.addEventListener('click', function () {
            if (mobileMenu.classList.contains('-translate-x-full')) {
                openMobileMenu();
            } else {
                closeMobileMenuFunc();
            }
        });

        // Close button
        if (closeMobileMenu) {
            closeMobileMenu.addEventListener('click', closeMobileMenuFunc);
        }

        // Close when clicking overlay
        if (mobileMenuOverlay) {
            mobileMenuOverlay.addEventListener('click', closeMobileMenuFunc);
        }

        // Close mobile menu when clicking on links
        const mobileLinks = mobileMenu.querySelectorAll('.mobile-menu-link');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function () {
                closeMobileMenuFunc();
            });
        });

        // Handle escape key
        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' && !mobileMenu.classList.contains('-translate-x-full')) {
                closeMobileMenuFunc();
            }
        });
    }

    // Update mobile menu auth state
    function updateMobileAuthState() {
        const authToken = localStorage.getItem('authToken');
        const userData = localStorage.getItem('userData');
        const mobileAuthButtons = document.getElementById('mobileAuthButtons');
        const mobileUserMenu = document.getElementById('mobileUserMenu');
        const mobileUserGreeting = document.getElementById('mobileUserGreeting');
        const aiChatMobileLink = document.getElementById('aiChatMobileLink');

        if (authToken && userData) {
            try {
                const user = JSON.parse(userData);
                // Show user menu, hide auth buttons
                if (mobileAuthButtons) mobileAuthButtons.classList.add('hidden');
                if (mobileUserMenu) mobileUserMenu.classList.remove('hidden');
                if (aiChatMobileLink) aiChatMobileLink.classList.remove('hidden');

                // Update greeting
                if (mobileUserGreeting) {
                    const name = user.name || user.email.split('@')[0];
                    mobileUserGreeting.textContent = name;
                }
            } catch (error) {
                console.error('Error parsing user data:', error);
            }
        } else {
            // Show auth buttons, hide user menu
            if (mobileAuthButtons) mobileAuthButtons.classList.remove('hidden');
            if (mobileUserMenu) mobileUserMenu.classList.add('hidden');
            if (aiChatMobileLink) aiChatMobileLink.classList.add('hidden');
        }
    }

    // Mobile logout
    const mobileLogoutBtn = document.getElementById('mobileLogoutBtn');
    if (mobileLogoutBtn) {
        mobileLogoutBtn.addEventListener('click', function () {
            localStorage.removeItem('authToken');
            localStorage.removeItem('userData');
            localStorage.removeItem('currentUser');
            updateMobileAuthState();
            closeMobileMenuFunc();
            window.location.href = '/';
        });
    }

    // Initialize mobile auth state
    updateMobileAuthState();

    // Listen for auth state changes
    window.addEventListener('storage', updateMobileAuthState);
});