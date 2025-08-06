// Camera Handler for Facial Emotion Detection
class CameraHandler {
    constructor() {
        this.stream = null;
        this.video = null;
        this.canvas = null;
        this.context = null;
        this.isActive = false;
        this.isSupported = false;
        this.captureInterval = null;
        this.initialize();
    }

    initialize() {
        // Check for camera support
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            console.warn('Camera access not supported');
            this.showUnsupportedMessage();
            return;
        }

        this.isSupported = true;
        this.setupCameraElements();
        this.setupCameraControls();
    }

    setupCameraElements() {
        this.video = document.getElementById('cameraVideo');
        this.canvas = document.getElementById('cameraCanvas');
        
        if (this.canvas) {
            this.context = this.canvas.getContext('2d');
            this.canvas.width = 200;
            this.canvas.height = 150;
        }
    }

    setupCameraControls() {
        const startBtn = document.getElementById('startCameraBtn');
        const captureBtn = document.getElementById('captureBtn');
        const stopBtn = document.getElementById('stopCameraBtn');

        if (startBtn) {
            startBtn.addEventListener('click', () => this.startCamera());
        }

        if (captureBtn) {
            captureBtn.addEventListener('click', () => this.captureExpression());
        }

        if (stopBtn) {
            stopBtn.addEventListener('click', () => this.stopCamera());
        }

        // Show/hide controls based on support
        if (!this.isSupported) {
            if (startBtn) startBtn.style.display = 'none';
            if (captureBtn) captureBtn.style.display = 'none';
            if (stopBtn) stopBtn.style.display = 'none';
        }
    }

    async startCamera() {
        if (!this.isSupported || this.isActive) return;

        try {
            this.updateCameraStatus('Requesting camera access...');

            // Request camera access
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: { 
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'user'
                },
                audio: false
            });

            if (this.video) {
                this.video.srcObject = this.stream;
                this.video.classList.remove('d-none');
                
                await new Promise((resolve) => {
                    this.video.onloadedmetadata = resolve;
                });
                
                await this.video.play();
            }

            this.isActive = true;
            this.updateCameraControls();
            this.updateCameraStatus('Camera active - position your face in the frame');
            
            // Add camera active class for styling
            document.getElementById('cameraInputArea').classList.add('camera-active');

            // Auto-capture every 5 seconds for continuous monitoring
            this.startAutoCaptureMode();

        } catch (error) {
            console.error('Error starting camera:', error);
            this.handleCameraError(error);
        }
    }

    stopCamera() {
        if (!this.isActive) return;

        try {
            // Stop auto-capture
            this.stopAutoCaptureMode();

            // Stop camera stream
            if (this.stream) {
                this.stream.getTracks().forEach(track => track.stop());
                this.stream = null;
            }

            // Hide video
            if (this.video) {
                this.video.srcObject = null;
                this.video.classList.add('d-none');
            }

            this.isActive = false;
            this.updateCameraControls();
            this.updateCameraStatus('Click to start camera for facial emotion detection');
            
            // Remove camera active class
            document.getElementById('cameraInputArea').classList.remove('camera-active');

        } catch (error) {
            console.error('Error stopping camera:', error);
        }
    }

    startAutoCaptureMode() {
        // Auto-capture every 10 seconds
        this.captureInterval = setInterval(() => {
            this.captureExpression(true); // true for auto-capture
        }, 10000);
    }

    stopAutoCaptureMode() {
        if (this.captureInterval) {
            clearInterval(this.captureInterval);
            this.captureInterval = null;
        }
    }

    async captureExpression(isAutoCapture = false) {
        if (!this.isActive || !this.video || !this.canvas) return;

        try {
            // Draw current video frame to canvas
            this.context.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
            
            // Get image data
            const imageDataUrl = this.canvas.toDataURL('image/jpeg', 0.8);
            
            if (!isAutoCapture) {
                this.updateCameraStatus('Analyzing facial expression...');
            }

            // Send to server for analysis
            const response = await fetch('/analyze_facial', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    image_data: imageDataUrl
                })
            });

            if (!response.ok) {
                throw new Error('Failed to analyze facial expression');
            }

            const result = await response.json();
            
            // Add message to chat (only for manual captures)
            if (!isAutoCapture && window.emotionController) {
                window.emotionController.addChatMessage('Facial expression captured and analyzed', 'user', null, 'facial');
            }

            // Handle the emotion result
            if (window.emotionController) {
                window.emotionController.handleEmotionResult(result);
            }

            if (!isAutoCapture) {
                this.updateCameraStatus('Expression analyzed! Camera continues monitoring...');
            }

            // Visual feedback for capture
            this.showCaptureFlash();

        } catch (error) {
            console.error('Error capturing expression:', error);
            this.updateCameraStatus('Error analyzing expression. Please try again.');
            
            if (window.emotionController) {
                window.emotionController.showError('Sorry, I had trouble analyzing your facial expression. Please try again.');
            }
        }
    }

    showCaptureFlash() {
        // Create a brief visual flash effect
        const flash = document.createElement('div');
        flash.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(255, 255, 255, 0.7);
            z-index: 9999;
            pointer-events: none;
        `;
        
        document.body.appendChild(flash);
        
        setTimeout(() => {
            flash.style.opacity = '0';
            flash.style.transition = 'opacity 0.3s';
            setTimeout(() => {
                document.body.removeChild(flash);
            }, 300);
        }, 100);
    }

    updateCameraControls() {
        const startBtn = document.getElementById('startCameraBtn');
        const captureBtn = document.getElementById('captureBtn');
        const stopBtn = document.getElementById('stopCameraBtn');

        if (startBtn && captureBtn && stopBtn) {
            if (this.isActive) {
                startBtn.classList.add('d-none');
                captureBtn.classList.remove('d-none');
                stopBtn.classList.remove('d-none');
            } else {
                startBtn.classList.remove('d-none');
                captureBtn.classList.add('d-none');
                stopBtn.classList.add('d-none');
            }
        }
    }

    updateCameraStatus(message) {
        const statusElement = document.getElementById('cameraStatus');
        if (statusElement) {
            statusElement.textContent = message;
        }
    }

    handleCameraError(error) {
        let errorMessage = 'Camera error occurred.';
        
        if (error.name === 'NotAllowedError') {
            errorMessage = 'Camera access denied. Please allow camera access and try again.';
        } else if (error.name === 'NotFoundError') {
            errorMessage = 'No camera found. Please check your camera and try again.';
        } else if (error.name === 'NotReadableError') {
            errorMessage = 'Camera is being used by another application.';
        } else if (error.name === 'OverconstrainedError') {
            errorMessage = 'Camera constraints could not be satisfied.';
        } else if (error.name === 'SecurityError') {
            errorMessage = 'Camera access blocked for security reasons.';
        }

        this.updateCameraStatus(errorMessage);
        console.error('Camera error details:', error);
    }

    showUnsupportedMessage() {
        const cameraArea = document.getElementById('cameraInputArea');
        if (cameraArea) {
            cameraArea.innerHTML = `
                <div class="text-center text-muted">
                    <i class="fas fa-camera-slash fa-2x mb-3"></i>
                    <p>Camera access is not supported in this browser.</p>
                    <p class="small">Please use a modern browser with camera support.</p>
                </div>
            `;
        }
    }

    // Cleanup method
    destroy() {
        this.stopCamera();
        this.stopAutoCaptureMode();
    }
}

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
    if (window.cameraHandler) {
        window.cameraHandler.destroy();
    }
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = CameraHandler;
}
