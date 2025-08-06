# Emotion Recognition Therapy Chatbot

## Overview

This is a Flask-based web application that provides therapeutic support through multimodal emotion recognition. The system analyzes user emotions through text, voice, and facial inputs, then provides personalized therapeutic responses including validations, encouragements, and coping strategies. The app works without user authentication - sessions are tracked locally for the current browser session.

## User Preferences

Preferred communication style: Simple, everyday language.

## Recent Changes

- **Removed Authentication System** (July 31, 2025): Removed sign-in/sign-up functionality to make the app work without user accounts
- **Simplified Session Management**: Chat history now works per browser session only
- **Prepared for Download**: App is now ready for local deployment without external authentication dependencies

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with SQLAlchemy ORM
- **Database**: SQLite for development (configurable to PostgreSQL via DATABASE_URL environment variable)
- **Session Management**: Flask sessions with UUID-based session tracking
- **Logging**: Python's built-in logging module configured for DEBUG level

### Frontend Architecture
- **UI Framework**: Bootstrap 5 with dark theme optimized for Replit
- **JavaScript Architecture**: Modular ES6 classes for different input handlers
- **Responsive Design**: Mobile-first approach with Bootstrap grid system
- **Real-time Interaction**: AJAX-based communication with backend APIs

### Database Schema
The application uses three main models:
- **EmotionSession**: Tracks user sessions with unique session IDs
- **EmotionRecord**: Stores emotion detection results from various input types
- **TherapyResponse**: Contains therapeutic responses linked to emotion records

## Key Components

### Emotion Analysis Engine
- **Text Analysis**: Uses TextBlob for sentiment analysis combined with keyword-based emotion detection
- **Multimodal Support**: Architecture prepared for voice and facial emotion recognition
- **Confidence Scoring**: Implements confidence levels for emotion predictions

### Therapy Response System
- **Response Categories**: Validations, encouragements, and remedies
- **Emotion-Specific Content**: Tailored responses for joy, sadness, anger, fear, disgust, surprise, and neutral states
- **Structured Remedies**: Includes breathing exercises, mindfulness activities, and coping strategies

### Input Handlers
- **Text Handler**: Real-time text processing with 500-character limit
- **Voice Handler**: Web Speech API integration for speech-to-text conversion
- **Camera Handler**: Prepared for facial expression analysis using MediaDevices API

### User Interface
- **Chat Interface**: Conversational UI with message bubbles and animations
- **Mode Switching**: Toggle between text, voice, and camera input modes
- **Session Management**: Persistent session tracking with history and insights

## Data Flow

1. **Session Initialization**: User visits the application, receives unique session ID stored in Flask session
2. **Input Processing**: User provides input via text, voice, or camera
3. **Emotion Analysis**: Input is processed through the EmotionAnalyzer to detect emotions and confidence levels
4. **Database Storage**: Emotion records are persisted with session tracking
5. **Response Generation**: TherapyResponseGenerator creates personalized therapeutic responses
6. **User Feedback**: Responses are displayed in the chat interface with appropriate styling and animations

## External Dependencies

### Python Packages
- **Flask**: Web framework and session management
- **SQLAlchemy**: Database ORM and migrations
- **TextBlob**: Natural language processing for sentiment analysis
- **Pillow**: Image processing for future facial recognition features
- **NumPy**: Numerical computing support

### Frontend Libraries
- **Bootstrap 5**: UI framework with Replit dark theme
- **Font Awesome**: Icon library for UI elements
- **Web APIs**: MediaDevices API for camera access, Web Speech API for voice recognition

### Environment Configuration
- **SESSION_SECRET**: Flask session encryption key
- **DATABASE_URL**: Database connection string (defaults to SQLite)

## Deployment Strategy

### Development Setup
- **Debug Mode**: Enabled for development with hot reload
- **Database Initialization**: Auto-creates tables on first run
- **Static Assets**: Served directly by Flask in development

### Production Considerations
- **Proxy Configuration**: ProxyFix middleware configured for reverse proxy deployment
- **Database Pooling**: Connection pool with 300-second recycle and pre-ping enabled
- **Environment Variables**: Sensitive configuration externalized to environment variables

### Scalability Architecture
- **Session-based Design**: Horizontal scaling possible with external session storage
- **Database Agnostic**: Can migrate from SQLite to PostgreSQL for production
- **Stateless Design**: Each request is self-contained for load balancing

The application follows a modular architecture that separates concerns between emotion detection, therapy response generation, and user interface management, making it extensible for additional emotion recognition modalities and therapeutic interventions.