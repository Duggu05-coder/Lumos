// Emotion Detection Main Controller
class EmotionDetectionController {
    constructor() {
        this.currentMode = 'text';
        this.isProcessing = false;
        this.init();
    }

    init() {
        this.setupModeButtons();
        this.setupTextInput();
        this.showTextMode();
        
        // Load existing chat history from session storage
        this.loadChatHistoryFromSession();
        
        // Initialize voice and camera handlers
        if (typeof VoiceHandler !== 'undefined') {
            this.voiceHandler = new VoiceHandler();
        }
        if (typeof CameraHandler !== 'undefined') {
            this.cameraHandler = new CameraHandler();
        }
    }

    setupModeButtons() {
        document.getElementById('textModeBtn').addEventListener('click', () => this.switchMode('text'));
        document.getElementById('voiceModeBtn').addEventListener('click', () => this.switchMode('voice'));
        document.getElementById('cameraModeBtn').addEventListener('click', () => this.switchMode('camera'));
    }

    setupTextInput() {
        const textInput = document.getElementById('textInput');
        const sendBtn = document.getElementById('sendTextBtn');

        sendBtn.addEventListener('click', () => this.sendTextMessage());
        textInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendTextMessage();
            }
        });
    }

    switchMode(mode) {
        this.currentMode = mode;
        
        // Update button states
        document.querySelectorAll('.btn-group .btn').forEach(btn => {
            btn.classList.remove('active');
        });
        document.getElementById(mode + 'ModeBtn').classList.add('active');

        // Show/hide input areas
        document.getElementById('textInputArea').classList.toggle('d-none', mode !== 'text');
        document.getElementById('voiceInputArea').classList.toggle('d-none', mode !== 'voice');
        document.getElementById('cameraInputArea').classList.toggle('d-none', mode !== 'camera');

        // Initialize mode-specific handlers
        if (mode === 'voice' && this.voiceHandler) {
            this.voiceHandler.initialize();
        } else if (mode === 'camera' && this.cameraHandler) {
            this.cameraHandler.initialize();
        }
    }

    showTextMode() {
        this.switchMode('text');
    }

    async sendTextMessage() {
        const textInput = document.getElementById('textInput');
        const text = textInput.value.trim();

        if (!text || this.isProcessing) return;

        this.isProcessing = true;
        this.showProcessingState();

        try {
            // Add user message to chat
            this.addChatMessage(text, 'user');
            textInput.value = '';

            // Send to server for analysis
            const response = await fetch('/analyze_text', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: text })
            });

            if (!response.ok) {
                throw new Error('Failed to analyze text');
            }

            const result = await response.json();
            this.handleEmotionResult(result);

        } catch (error) {
            console.error('Error analyzing text:', error);
            this.showError('Sorry, I had trouble analyzing your message. Please try again.');
        } finally {
            this.isProcessing = false;
            this.hideProcessingState();
        }
    }

    addChatMessage(content, sender, timestamp = null, inputType = 'text') {
        const chatArea = document.getElementById('chatArea');
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender}-message`;

        const time = timestamp ? new Date(timestamp) : new Date();
        const timeString = time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        // Add input type indicator for user messages
        let inputTypeIndicator = '';
        if (sender === 'user' && inputType !== 'text') {
            const iconMap = {
                'voice': 'fas fa-microphone text-success',
                'facial': 'fas fa-camera text-warning'
            };
            inputTypeIndicator = `<span class="input-type-badge"><i class="${iconMap[inputType] || 'fas fa-keyboard'}"></i></span>`;
        }

        messageDiv.innerHTML = `
            <div class="message-bubble">
                ${inputTypeIndicator}
                ${this.formatMessage(content)}
            </div>
            <div class="message-timestamp">${timeString}</div>
        `;

        chatArea.appendChild(messageDiv);
        chatArea.scrollTop = chatArea.scrollHeight;

        // Store message in session storage for persistence
        this.storeMessageInSession(content, sender, time.toISOString(), inputType);

        // Remove welcome message if it exists
        const welcomeMsg = chatArea.querySelector('.text-center.text-muted.py-5');
        if (welcomeMsg) {
            welcomeMsg.remove();
        }
    }

    formatMessage(content) {
        // Convert line breaks to <br> tags and handle basic formatting
        return content.replace(/\n/g, '<br>');
    }

    handleEmotionResult(result) {
        // Add therapist response to chat
        this.addChatMessage(result.therapy_response.full_response, 'therapist', result.timestamp);

        // Update emotion display
        this.updateEmotionDisplay(result.emotion, result.confidence);

        // Update remedies
        this.updateQuickRemedies(result.therapy_response.remedies);

        // Speak the response if speech synthesis is available
        this.speakResponse(result.therapy_response.full_response);
    }

    updateEmotionDisplay(emotion, confidence) {
        const emotionDisplay = document.getElementById('currentEmotionDisplay');
        
        const emotionIcons = {
            'joy': 'fas fa-smile text-warning',
            'sadness': 'fas fa-frown text-info',
            'anger': 'fas fa-angry text-danger',
            'fear': 'fas fa-grimace text-primary',
            'surprise': 'fas fa-surprise text-success',
            'disgust': 'fas fa-meh text-secondary',
            'neutral': 'fas fa-meh-blank text-muted'
        };

        const icon = emotionIcons[emotion] || emotionIcons['neutral'];
        const confidencePercent = Math.round(confidence * 100);

        emotionDisplay.innerHTML = `
            <div class="emotion-badge emotion-${emotion}">
                <i class="${icon}"></i>
                <span>${emotion.charAt(0).toUpperCase() + emotion.slice(1)}</span>
            </div>
            <div class="confidence-meter mt-3">
                <div class="confidence-fill" style="width: ${confidencePercent}%"></div>
            </div>
            <div class="small text-muted mt-2">Confidence: ${confidencePercent}%</div>
        `;
    }

    updateQuickRemedies(remedies) {
        const remediesContainer = document.getElementById('quickRemedies');
        
        if (!remedies || remedies.length === 0) {
            remediesContainer.innerHTML = `
                <div class="text-center text-muted">
                    <i class="fas fa-spa fa-2x mb-3"></i>
                    <div>No specific remedies right now</div>
                </div>
            `;
            return;
        }

        const remedyIcons = {
            'breathing': 'fas fa-wind',
            'activity': 'fas fa-running',
            'mindfulness': 'fas fa-om',
            'connection': 'fas fa-users',
            'grounding': 'fas fa-tree',
            'joke': 'fas fa-laugh',
            'song': 'fas fa-music',
            'self-care': 'fas fa-spa'
        };

        const remedyHtml = remedies.map(remedy => `
            <div class="remedy-card" data-remedy-type="${remedy.type}">
                <div class="d-flex align-items-start">
                    <div class="remedy-icon remedy-${remedy.type}">
                        <i class="${remedyIcons[remedy.type] || 'fas fa-leaf'}"></i>
                    </div>
                    <div class="flex-grow-1">
                        <h6 class="mb-1">${remedy.title}</h6>
                        <p class="mb-2 small">${remedy.description}</p>
                        <div class="small text-muted">
                            <i class="fas fa-clock me-1"></i>
                            ${remedy.duration}
                        </div>
                    </div>
                </div>
            </div>
        `).join('');

        remediesContainer.innerHTML = remedyHtml;
    }

    speakResponse(text) {
        if ('speechSynthesis' in window) {
            // Cancel any existing speech
            speechSynthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.rate = 0.8;
            utterance.pitch = 1;
            utterance.volume = 0.7;
            
            // Try to use a calm, soothing voice
            const voices = speechSynthesis.getVoices();
            const preferredVoice = voices.find(voice => 
                voice.name.includes('Female') || 
                voice.name.includes('Samantha') ||
                voice.name.includes('Alex')
            );
            
            if (preferredVoice) {
                utterance.voice = preferredVoice;
            }
            
            speechSynthesis.speak(utterance);
        }
    }

    showProcessingState() {
        const sendBtn = document.getElementById('sendTextBtn');
        sendBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        sendBtn.disabled = true;
    }

    hideProcessingState() {
        const sendBtn = document.getElementById('sendTextBtn');
        sendBtn.innerHTML = '<i class="fas fa-paper-plane"></i>';
        sendBtn.disabled = false;
    }

    showError(message) {
        this.addChatMessage(message, 'therapist');
    }

    storeMessageInSession(content, sender, timestamp, inputType = 'text') {
        const sessionMessages = JSON.parse(sessionStorage.getItem('chatHistory') || '[]');
        sessionMessages.push({
            content,
            sender,
            timestamp,
            inputType
        });
        
        // Keep only last 50 messages to prevent storage overflow
        if (sessionMessages.length > 50) {
            sessionMessages.splice(0, sessionMessages.length - 50);
        }
        
        sessionStorage.setItem('chatHistory', JSON.stringify(sessionMessages));
    }

    loadChatHistoryFromSession() {
        const sessionMessages = JSON.parse(sessionStorage.getItem('chatHistory') || '[]');
        const chatArea = document.getElementById('chatArea');
        
        if (sessionMessages.length > 0) {
            // Remove welcome message
            const welcomeMsg = chatArea.querySelector('.text-center.text-muted.py-5');
            if (welcomeMsg) {
                welcomeMsg.remove();
            }
            
            // Load previous messages
            sessionMessages.forEach(msg => {
                this.addChatMessageDirect(msg.content, msg.sender, msg.timestamp, msg.inputType);
            });
        }
    }

    addChatMessageDirect(content, sender, timestamp, inputType = 'text') {
        // Add message without storing in session (to avoid duplication during load)
        const chatArea = document.getElementById('chatArea');
        const messageDiv = document.createElement('div');
        messageDiv.className = `chat-message ${sender}-message`;

        const time = new Date(timestamp);
        const timeString = time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        let inputTypeIndicator = '';
        if (sender === 'user' && inputType !== 'text') {
            const iconMap = {
                'voice': 'fas fa-microphone text-success',
                'facial': 'fas fa-camera text-warning'
            };
            inputTypeIndicator = `<span class="input-type-badge"><i class="${iconMap[inputType] || 'fas fa-keyboard'}"></i></span>`;
        }

        messageDiv.innerHTML = `
            <div class="message-bubble">
                ${inputTypeIndicator}
                ${this.formatMessage(content)}
            </div>
            <div class="message-timestamp">${timeString}</div>
        `;

        chatArea.appendChild(messageDiv);
        chatArea.scrollTop = chatArea.scrollHeight;
    }

    clearChatHistory() {
        sessionStorage.removeItem('chatHistory');
        const chatArea = document.getElementById('chatArea');
        chatArea.innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="fas fa-heart fa-3x text-primary mb-3"></i>
                <h5>Welcome to Your Therapy Session</h5>
                <p>I'm here to listen and support you. Choose how you'd like to communicate:</p>
                <div class="d-flex justify-content-center gap-3 mt-4">
                    <div class="text-center">
                        <i class="fas fa-keyboard fa-2x text-info mb-2"></i>
                        <div class="small">Type your thoughts</div>
                    </div>
                    <div class="text-center">
                        <i class="fas fa-microphone fa-2x text-success mb-2"></i>
                        <div class="small">Speak your feelings</div>
                    </div>
                    <div class="text-center">
                        <i class="fas fa-camera fa-2x text-warning mb-2"></i>
                        <div class="small">Express with your face</div>
                    </div>
                </div>
            </div>
        `;
    }
}

// Global functions for breathing exercises and modals
function startBreathingExercise(type) {
    fetch(`/get_breathing_exercise/${type}`)
        .then(response => response.json())
        .then(exercise => {
            document.getElementById('breathingContent').innerHTML = `
                <h5>${exercise.name}</h5>
                <div class="breathing-circle breathing-inhale">
                    <span>Breathe In</span>
                </div>
                <p class="mb-3">${exercise.instructions}</p>
                <div class="small text-muted">Duration: ${exercise.duration}</div>
                <button class="btn btn-primary mt-3" onclick="stopBreathingExercise()">
                    Stop Exercise
                </button>
            `;
            
            const modal = new bootstrap.Modal(document.getElementById('breathingModal'));
            modal.show();
            
            // Start breathing animation cycle
            startBreathingAnimation();
        })
        .catch(error => {
            console.error('Error loading breathing exercise:', error);
        });
}

function startBreathingAnimation() {
    const circle = document.querySelector('.breathing-circle');
    if (!circle) return;
    
    let phase = 'inhale';
    
    const breathingCycle = setInterval(() => {
        if (phase === 'inhale') {
            circle.className = 'breathing-circle breathing-inhale';
            circle.innerHTML = '<span>Breathe In</span>';
            phase = 'exhale';
        } else {
            circle.className = 'breathing-circle breathing-exhale';
            circle.innerHTML = '<span>Breathe Out</span>';
            phase = 'inhale';
        }
    }, 4000);
    
    // Store interval ID for cleanup
    window.currentBreathingInterval = breathingCycle;
}

function stopBreathingExercise() {
    if (window.currentBreathingInterval) {
        clearInterval(window.currentBreathingInterval);
        window.currentBreathingInterval = null;
    }
    
    const modal = bootstrap.Modal.getInstance(document.getElementById('breathingModal'));
    if (modal) {
        modal.hide();
    }
}

function showSessionInsights() {
    const modal = new bootstrap.Modal(document.getElementById('insightsModal'));
    modal.show();
    
    fetch('/get_session_insights')
        .then(response => response.json())
        .then(data => {
            const insights = data.insights;
            let content = '<div class="row">';
            
            if (insights.total_records > 0) {
                // Emotion distribution chart
                content += `
                    <div class="col-md-6">
                        <h6>Emotion Distribution</h6>
                        <div class="emotion-chart">
                `;
                
                Object.entries(insights.emotion_percentages).forEach(([emotion, percentage]) => {
                    content += `
                        <div class="d-flex justify-content-between align-items-center mb-2">
                            <span class="text-capitalize">${emotion}</span>
                            <div class="flex-grow-1 mx-3">
                                <div class="progress" style="height: 20px;">
                                    <div class="progress-bar bg-${emotion === 'joy' ? 'warning' : emotion === 'sadness' ? 'info' : emotion === 'anger' ? 'danger' : 'secondary'}" 
                                         style="width: ${percentage}%"></div>
                                </div>
                            </div>
                            <span class="small">${percentage.toFixed(1)}%</span>
                        </div>
                    `;
                });
                
                content += `
                        </div>
                    </div>
                    <div class="col-md-6">
                        <h6>Session Summary</h6>
                        <div class="card bg-secondary">
                            <div class="card-body">
                                <p><strong>Total Interactions:</strong> ${insights.total_records}</p>
                                <p><strong>Dominant Emotion:</strong> 
                                   <span class="text-capitalize badge bg-primary">${insights.dominant_emotion}</span>
                                </p>
                                <p><strong>Session Duration:</strong> Active</p>
                            </div>
                        </div>
                    </div>
                `;
            } else {
                content += `
                    <div class="col-12 text-center">
                        <i class="fas fa-chart-pie fa-3x text-muted mb-3"></i>
                        <h5>No Data Yet</h5>
                        <p class="text-muted">Start interacting to see your emotion insights!</p>
                    </div>
                `;
            }
            
            content += '</div>';
            document.getElementById('insightsContent').innerHTML = content;
        })
        .catch(error => {
            console.error('Error loading insights:', error);
            document.getElementById('insightsContent').innerHTML = `
                <div class="text-center text-danger">
                    <i class="fas fa-exclamation-triangle fa-2x mb-3"></i>
                    <p>Error loading insights. Please try again.</p>
                </div>
            `;
        });
}

function showConversationHistory() {
    const modal = new bootstrap.Modal(document.getElementById('historyModal'));
    modal.show();
    
    fetch('/get_conversation_history')
        .then(response => response.json())
        .then(data => {
            const conversations = data.conversation;
            let content = '';
            
            if (conversations.length > 0) {
                conversations.forEach((conv, index) => {
                    const time = new Date(conv.timestamp).toLocaleTimeString();
                    const inputContent = conv.input_type === 'facial' ? 'Facial expression analyzed' : conv.input_content;
                    
                    content += `
                        <div class="card bg-dark border-secondary mb-3">
                            <div class="card-header d-flex justify-content-between align-items-center">
                                <div>
                                    <span class="badge bg-${conv.input_type === 'text' ? 'primary' : conv.input_type === 'voice' ? 'success' : 'warning'}">
                                        ${conv.input_type.toUpperCase()}
                                    </span>
                                    <span class="badge bg-secondary ms-2">${conv.detected_emotion}</span>
                                </div>
                                <small class="text-muted">${time}</small>
                            </div>
                            <div class="card-body">
                                <div class="mb-3">
                                    <strong>Your input:</strong>
                                    <p class="mb-0">${inputContent}</p>
                                </div>
                                <div>
                                    <strong>Therapy response:</strong>
                                    <p class="mb-0">${conv.therapy_response}</p>
                                </div>
                            </div>
                        </div>
                    `;
                });
            } else {
                content = `
                    <div class="text-center text-muted">
                        <i class="fas fa-comments fa-3x mb-3"></i>
                        <h5>No Conversation History</h5>
                        <p>Your conversation history will appear here as you interact.</p>
                    </div>
                `;
            }
            
            document.getElementById('historyContent').innerHTML = content;
        })
        .catch(error => {
            console.error('Error loading conversation history:', error);
            document.getElementById('historyContent').innerHTML = `
                <div class="text-center text-danger">
                    <i class="fas fa-exclamation-triangle fa-2x mb-3"></i>
                    <p>Error loading conversation history. Please try again.</p>
                </div>
            `;
        });
}

// Global function to clear current chat history
function clearCurrentChatHistory() {
    if (window.emotionController) {
        const confirmed = confirm('Are you sure you want to clear the current chat history? This action cannot be undone.');
        if (confirmed) {
            window.emotionController.clearChatHistory();
        }
    }
}

// Global function to clear database history
function clearDatabaseHistory() {
    const confirmed = confirm('Are you sure you want to clear all conversation history from the database? This action cannot be undone.');
    if (confirmed) {
        fetch('/clear_session_history', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Database history cleared successfully!');
                // Close the modal and refresh insights
                const modal = bootstrap.Modal.getInstance(document.getElementById('historyModal'));
                if (modal) modal.hide();
            } else {
                alert('Error clearing database history: ' + (data.error || 'Unknown error'));
            }
        })
        .catch(error => {
            console.error('Error clearing database history:', error);
            alert('Error clearing database history. Please try again.');
        });
    }
}

// Initialize the emotion detection controller when the page loads
document.addEventListener('DOMContentLoaded', function() {
    window.emotionController = new EmotionDetectionController();
});
