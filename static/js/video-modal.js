// Simple Video Modal for AI Raitha Mitra Demo

class VideoModal {
    constructor() {
        this.modal = null;
        this.video = null;
        this.init();
    }

    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupEventListeners());
        } else {
            this.setupEventListeners();
        }
    }

    setupEventListeners() {
        // Watch Demo button
        const watchDemoBtn = document.getElementById('watchDemoBtn');
        if (watchDemoBtn) {
            watchDemoBtn.addEventListener('click', () => this.openModal());
        }

        // Modal elements
        this.modal = document.getElementById('videoDemoModal');
        this.video = document.getElementById('demoVideo');

        if (this.modal) {
            // Close modal button
            const closeBtn = document.getElementById('closeVideoModal');
            if (closeBtn) {
                closeBtn.addEventListener('click', () => this.closeModal());
            }

            // Close on backdrop click
            this.modal.addEventListener('click', (e) => {
                if (e.target === this.modal) {
                    this.closeModal();
                }
            });

            // Escape key to close
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && !this.modal.classList.contains('hidden')) {
                    this.closeModal();
                }
            });
        }

        // Setup video controls
        this.setupVideoControls();
        
        // Setup action buttons
        this.setupActionButtons();
    }

    setupVideoControls() {
        const fullscreenBtn = document.getElementById('fullscreenBtn');

        // Fullscreen functionality
        if (fullscreenBtn) {
            fullscreenBtn.addEventListener('click', () => {
                this.toggleFullscreen();
            });
        }

        // Video event listeners
        if (this.video) {
            this.video.addEventListener('loadeddata', () => {
                console.log('Video loaded successfully');
            });

            this.video.addEventListener('error', (e) => {
                console.log('Video error:', e);
            });
        }
    }

    setupActionButtons() {
        // Try Now button
        const tryNowBtn = document.getElementById('tryNowBtn');
        if (tryNowBtn) {
            tryNowBtn.addEventListener('click', () => {
                this.closeModal();
                // Navigate to disease detection
                if (window.RaithaMitra && window.RaithaMitra.navigateToDiseaseDetection) {
                    window.RaithaMitra.navigateToDiseaseDetection();
                } else {
                    window.location.href = '/disease-detection';
                }
            });
        }

        // Learn More button
        const learnMoreBtn = document.getElementById('learnMoreBtn');
        if (learnMoreBtn) {
            learnMoreBtn.addEventListener('click', () => {
                this.closeModal();
                // Scroll to features section
                const featuresSection = document.getElementById('features');
                if (featuresSection) {
                    featuresSection.scrollIntoView({ behavior: 'smooth' });
                }
            });
        }
    }

    openModal() {
        if (this.modal) {
            this.modal.classList.remove('hidden');
            document.body.style.overflow = 'hidden';
            
            // Reset video to beginning
            if (this.video) {
                this.video.currentTime = 0;
            }
        }
    }

    closeModal() {
        if (this.modal) {
            this.modal.classList.add('hidden');
            document.body.style.overflow = '';
            
            // Pause video when closing
            if (this.video && !this.video.paused) {
                this.video.pause();
            }
        }
    }

    toggleFullscreen() {
        if (this.video) {
            if (this.video.requestFullscreen) {
                this.video.requestFullscreen();
            } else if (this.video.webkitRequestFullscreen) {
                this.video.webkitRequestFullscreen();
            } else if (this.video.msRequestFullscreen) {
                this.video.msRequestFullscreen();
            }
        }
    }
}

// Initialize video modal when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    new VideoModal();
});

// Also initialize if script loads after DOM is ready
if (document.readyState !== 'loading') {
    new VideoModal();
}