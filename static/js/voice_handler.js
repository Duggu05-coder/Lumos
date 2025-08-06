// Voice Input Handler for Emotion Detection
class VoiceHandler {
    constructor() {
        this.recognition = null;
        this.isRecording = false;
        this.isSupported = false;
        this.initialize();
    }

    initialize() {
        // Check for Web Speech API support
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.warn('Speech recognition not supported');
            this.showUnsupportedMessage();
            return;
        }

        this.isSupported = true;
        this.setupSpeechRecognition();
        this.setupVoiceControls();
    }

    setupSpeechRecognition() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();

        // Configure recognition settings
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';
        this.recognition.maxAlternatives = 1;

        // Event handlers
        this.recognition.onstart = () => {
            console.log('Voice recognition started');
            this.onRecordingStart();
        };

        this.recognition.onresult = (event) => {
            let finalTranscript = '';
            let interimTranscript = '';

            for (let i = event.resultIndex; i < event.results.length; i++) {
                const transcript = event.results[i][0].transcript;
                if (event.results[i].isFinal) {
                    finalTranscript += transcript;
                } else {
                    interimTranscript += transcript;
                }
            }

            this.updateVoiceStatus(interimTranscript || finalTranscript);

            if (finalTranscript) {
                this.onRecordingComplete(finalTranscript);
            }
        };

        this.recognition.onerror = (event) => {
            console.error('Voice recognition error:', event.error);
            this.onRecordingError(event.error);
        };

        this.recognition.onend = () => {
            console.log('Voice recognition ended');
            this.onRecordingEnd();
        };
    }

    setupVoiceControls() {
        const startBtn = document.getElementById('startVoiceBtn');
        const stopBtn = document.getElementById('stopVoiceBtn');

        if (startBtn) {
            startBtn.addEventListener('click', () => this.startRecording());
        }

        if (stopBtn) {
            stopBtn.addEventListener('click', () => this.stopRecording());
        }

        // Show/hide controls based on support
        if (!this.isSupported) {
            if (startBtn) startBtn.style.display = 'none';
            if (stopBtn) stopBtn.style.display = 'none';
        }
    }

    startRecording() {
        if (!this.isSupported || this.isRecording) return;

        try {
            this.recognition.start();
            this.isRecording = true;
        } catch (error) {
            console.error('Error starting voice recognition:', error);
            this.showError('Could not start voice recording. Please try again.');
        }
    }

    stopRecording() {
        if (!this.isRecording) return;

        try {
            this.recognition.stop();
            this.isRecording = false;
        } catch (error) {
            console.error('Error stopping voice recognition:', error);
        }
    }

    onRecordingStart() {
        this.isRecording = true;
        this.updateVoiceControls();
        this.updateVoiceStatus('Listening... speak now');
        this.showVoiceWaveAnimation();
    }

    onRecordingComplete(transcript) {
        console.log('Voice transcript:', transcript);
        this.processVoiceInput(transcript);
    }

    onRecordingEnd() {
        this.isRecording = false;
        this.updateVoiceControls();
        this.hideVoiceWaveAnimation();
    }

    onRecordingError(error) {
        this.isRecording = false;
        this.updateVoiceControls();
        this.hideVoiceWaveAnimation();

        let errorMessage = 'Voice recognition error occurred.';
        
        switch(error) {
            case 'network':
                errorMessage = 'Network error. Please check your connection.';
                break;
            case 'not-allowed':
                errorMessage = 'Microphone access denied. Please allow microphone access.';
                break;
            case 'no-speech':
                errorMessage = 'No speech detected. Please try again.';
                break;
            case 'audio-capture':
                errorMessage = 'No microphone found. Please check your audio settings.';
                break;
        }

        this.updateVoiceStatus(errorMessage);
        setTimeout(() => {
            this.updateVoiceStatus('Click to start voice recording');
        }, 3000);
    }

    async processVoiceInput(transcript) {
        if (!transcript.trim()) {
            this.updateVoiceStatus('No speech detected. Please try again.');
            return;
        }

        try {
            this.updateVoiceStatus('Analyzing your voice...');

            // Add user message to chat
            if (window.emotionController) {
                window.emotionController.addChatMessage(transcript, 'user', null, 'voice');
            }

            // Send to server for analysis
            const response = await fetch('/analyze_voice', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ 
                    text: transcript,
                    audio_features: this.getAudioFeatures()
                })
            });

            if (!response.ok) {
                throw new Error('Failed to analyze voice');
            }

            const result = await response.json();
            
            // Handle the emotion result
            if (window.emotionController) {
                window.emotionController.handleEmotionResult(result);
            }

            this.updateVoiceStatus('Click to start voice recording');

        } catch (error) {
            console.error('Error processing voice input:', error);
            this.updateVoiceStatus('Error analyzing voice. Please try again.');
            
            if (window.emotionController) {
                window.emotionController.showError('Sorry, I had trouble analyzing your voice. Please try again.');
            }
        }
    }

    getAudioFeatures() {
        // In a full implementation, you would analyze audio features
        // like pitch, tone, speaking rate, volume, etc.
        // For now, return empty object
        return {};
    }

    updateVoiceControls() {
        const startBtn = document.getElementById('startVoiceBtn');
        const stopBtn = document.getElementById('stopVoiceBtn');

        if (startBtn && stopBtn) {
            if (this.isRecording) {
                startBtn.classList.add('d-none');
                stopBtn.classList.remove('d-none');
                stopBtn.classList.add('voice-recording');
            } else {
                startBtn.classList.remove('d-none');
                stopBtn.classList.add('d-none');
                stopBtn.classList.remove('voice-recording');
            }
        }
    }

    updateVoiceStatus(message) {
        const statusElement = document.getElementById('voiceStatus');
        if (statusElement) {
            statusElement.textContent = message;
        }
    }

    showVoiceWaveAnimation() {
        const statusElement = document.getElementById('voiceStatus');
        if (statusElement) {
            statusElement.innerHTML = `
                <div class="voice-waves">
                    <span class="voice-wave"></span>
                    <span class="voice-wave"></span>
                    <span class="voice-wave"></span>
                    <span class="voice-wave"></span>
                    <span class="voice-wave"></span>
                </div>
                <div class="mt-2">Listening...</div>
            `;
        }
    }

    hideVoiceWaveAnimation() {
        // Status will be updated by other methods
    }

    showUnsupportedMessage() {
        const voiceArea = document.getElementById('voiceInputArea');
        if (voiceArea) {
            voiceArea.innerHTML = `
                <div class="text-center text-muted">
                    <i class="fas fa-microphone-slash fa-2x mb-3"></i>
                    <p>Voice recognition is not supported in this browser.</p>
                    <p class="small">Please use Chrome, Safari, or Edge for voice features.</p>
                </div>
            `;
        }
    }

    showError(message) {
        this.updateVoiceStatus(message);
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = VoiceHandler;
}
