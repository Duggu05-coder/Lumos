import re
import logging
from textblob import TextBlob
import base64
from io import BytesIO
from PIL import Image
import numpy as np

class EmotionAnalyzer:
    def __init__(self):
        # Emotion keywords for enhanced text analysis
        self.emotion_keywords = {
            'joy': ['happy', 'excited', 'joyful', 'cheerful', 'delighted', 'pleased', 'glad', 'content'],
            'sadness': ['sad', 'depressed', 'down', 'melancholy', 'gloomy', 'sorrowful', 'upset', 'blue'],
            'anger': ['angry', 'furious', 'mad', 'irritated', 'annoyed', 'frustrated', 'rage', 'livid'],
            'fear': ['afraid', 'scared', 'anxious', 'worried', 'nervous', 'terrified', 'panic', 'frightened'],
            'disgust': ['disgusted', 'revolted', 'repulsed', 'sickened', 'appalled'],
            'surprise': ['surprised', 'shocked', 'amazed', 'astonished', 'startled', 'stunned'],
            'trauma': ['trauma', 'traumatic', 'ptsd', 'flashback', 'nightmare', 'triggered', 'abuse', 'assault', 'violence', 'harassment', 'bullying', 'betrayal', 'abandonment', 'grief', 'loss', 'devastated', 'overwhelmed', 'helpless', 'vulnerable', 'violated'],
            'neutral': ['okay', 'fine', 'normal', 'average', 'regular', 'typical']
        }
        
    def analyze_text_emotion(self, text):
        """Analyze emotion from text using TextBlob and keyword matching"""
        try:
            if not text or not text.strip():
                return 'neutral', 0.5
            
            # Clean and normalize text
            text = text.lower().strip()
            
            # Use TextBlob for sentiment analysis
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Keyword-based emotion detection
            emotion_scores = {}
            for emotion, keywords in self.emotion_keywords.items():
                score = sum(1 for keyword in keywords if keyword in text)
                if score > 0:
                    emotion_scores[emotion] = score
            
            # Determine primary emotion
            if emotion_scores:
                primary_emotion = max(emotion_scores, key=emotion_scores.get)
                confidence = min(emotion_scores[primary_emotion] * 0.3 + abs(polarity) * 0.7, 1.0)
            else:
                # Fall back to polarity-based classification
                if polarity > 0.3:
                    primary_emotion = 'joy'
                    confidence = polarity
                elif polarity < -0.3:
                    primary_emotion = 'sadness'
                    confidence = abs(polarity)
                else:
                    primary_emotion = 'neutral'
                    confidence = 1.0 - abs(polarity)
            
            logging.debug(f"Text emotion analysis: {text[:50]}... -> {primary_emotion} (confidence: {confidence:.2f})")
            return primary_emotion, confidence
            
        except Exception as e:
            logging.error(f"Error in text emotion analysis: {str(e)}")
            return 'neutral', 0.5
    
    def analyze_facial_emotion(self, image_data):
        """Basic facial emotion analysis from image data"""
        try:
            if not image_data:
                return 'neutral', 0.5
            
            # Decode base64 image data
            if 'data:image' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Basic image analysis (this is a simplified approach)
            # In a production system, you would use a trained facial emotion recognition model
            img_array = np.array(image)
            
            # Simple brightness and contrast analysis as a proxy for basic emotion detection
            brightness = np.mean(img_array)
            contrast = np.std(img_array)
            
            # Heuristic-based emotion detection (simplified)
            if brightness > 150 and contrast > 50:
                emotion = 'joy'
                confidence = 0.6
            elif brightness < 100:
                emotion = 'sadness'
                confidence = 0.5
            elif contrast > 80:
                emotion = 'surprise'
                confidence = 0.5
            else:
                emotion = 'neutral'
                confidence = 0.7
            
            logging.debug(f"Facial emotion analysis: brightness={brightness:.1f}, contrast={contrast:.1f} -> {emotion}")
            return emotion, confidence
            
        except Exception as e:
            logging.error(f"Error in facial emotion analysis: {str(e)}")
            return 'neutral', 0.5
    
    def analyze_voice_emotion(self, voice_text, audio_features=None):
        """Analyze emotion from voice text and optional audio features"""
        try:
            # For now, analyze the transcribed text
            # In a production system, you would analyze audio features like pitch, tone, pace
            text_emotion, text_confidence = self.analyze_text_emotion(voice_text)
            
            # If audio features are provided, incorporate them
            if audio_features:
                # This is where you would analyze pitch, volume, speaking rate, etc.
                # For now, we'll use the text analysis
                pass
            
            logging.debug(f"Voice emotion analysis: {voice_text[:50]}... -> {text_emotion}")
            return text_emotion, text_confidence
            
        except Exception as e:
            logging.error(f"Error in voice emotion analysis: {str(e)}")
            return 'neutral', 0.5
    
    def get_emotion_insights(self, emotion_records):
        """Analyze patterns in emotion records for insights"""
        if not emotion_records:
            return {}
        
        # Count emotions
        emotion_counts = {}
        total_records = len(emotion_records)
        
        for record in emotion_records:
            emotion = record.detected_emotion
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
        
        # Calculate percentages
        emotion_percentages = {
            emotion: (count / total_records) * 100 
            for emotion, count in emotion_counts.items()
        }
        
        # Determine dominant emotion
        dominant_emotion = max(emotion_counts, key=emotion_counts.get) if emotion_counts else 'neutral'
        
        return {
            'emotion_counts': emotion_counts,
            'emotion_percentages': emotion_percentages,
            'dominant_emotion': dominant_emotion,
            'total_records': total_records
        }
