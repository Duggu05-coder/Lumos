from app import db
from datetime import datetime
from sqlalchemy import Text

# Emotion tracking models  
class EmotionSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class EmotionRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    input_type = db.Column(db.String(20), nullable=False)  # 'text', 'voice', 'facial'
    input_content = db.Column(Text)
    detected_emotion = db.Column(db.String(50))
    confidence_score = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class TherapyResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, index=True)
    emotion_record_id = db.Column(db.Integer, db.ForeignKey('emotion_record.id'))
    response_text = db.Column(Text)
    response_type = db.Column(db.String(50))  # 'validation', 'coping_strategy', 'breathing_exercise'
    remedy_suggestions = db.Column(Text)  # JSON string of suggested remedies
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    emotion_record = db.relationship('EmotionRecord', backref='therapy_responses')
