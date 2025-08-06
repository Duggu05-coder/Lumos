from flask import render_template, request, jsonify, session
from app import app, db
from models import EmotionSession, EmotionRecord, TherapyResponse
from emotion_analyzer import EmotionAnalyzer
from therapy_responses import TherapyResponseGenerator
import uuid
import logging
from datetime import datetime
import json

# Initialize analyzers
emotion_analyzer = EmotionAnalyzer()
therapy_generator = TherapyResponseGenerator()

# Make session permanent
@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/')
def index():
    """Main therapy chatbot interface"""
    # Create or get session ID
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
        
        # Create database session record
        emotion_session = EmotionSession()
        emotion_session.session_id = session['session_id']
        db.session.add(emotion_session)
        db.session.commit()
    
    return render_template('index.html')

@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    """Analyze emotion from text input"""
    try:
        data = request.get_json()
        text_input = data.get('text', '').strip()
        
        if not text_input:
            return jsonify({'error': 'No text provided'}), 400
        
        # Analyze emotion
        emotion, confidence = emotion_analyzer.analyze_text_emotion(text_input)
        
        # Save emotion record
        emotion_record = EmotionRecord()
        emotion_record.session_id = session['session_id']
        emotion_record.input_type = 'text'
        emotion_record.input_content = text_input
        emotion_record.detected_emotion = emotion
        emotion_record.confidence_score = confidence
        db.session.add(emotion_record)
        db.session.commit()
        
        # Generate therapy response
        therapy_response = therapy_generator.generate_response(emotion, confidence)
        
        # Save therapy response
        therapy_record = TherapyResponse(
            session_id=session['session_id'],
            emotion_record_id=emotion_record.id,
            response_text=therapy_response['full_response'],
            response_type='comprehensive',
            remedy_suggestions=json.dumps(therapy_response['remedies'])
        )
        db.session.add(therapy_record)
        db.session.commit()
        
        return jsonify({
            'emotion': emotion,
            'confidence': confidence,
            'therapy_response': therapy_response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Error in text analysis: {str(e)}")
        return jsonify({'error': 'Analysis failed'}), 500

@app.route('/analyze_voice', methods=['POST'])
def analyze_voice():
    """Analyze emotion from voice input"""
    try:
        data = request.get_json()
        voice_text = data.get('text', '').strip()
        audio_features = data.get('audio_features', {})
        
        if not voice_text:
            return jsonify({'error': 'No voice text provided'}), 400
        
        # Analyze emotion
        emotion, confidence = emotion_analyzer.analyze_voice_emotion(voice_text, audio_features)
        
        # Save emotion record
        emotion_record = EmotionRecord()
        emotion_record.session_id = session['session_id']
        emotion_record.input_type = 'voice'
        emotion_record.input_content = voice_text
        emotion_record.detected_emotion = emotion
        emotion_record.confidence_score = confidence
        db.session.add(emotion_record)
        db.session.commit()
        
        # Generate therapy response
        therapy_response = therapy_generator.generate_response(emotion, confidence)
        
        # Save therapy response
        therapy_record = TherapyResponse()
        therapy_record.session_id = session['session_id']
        therapy_record.emotion_record_id = emotion_record.id
        therapy_record.response_text = therapy_response['full_response']
        therapy_record.response_type = 'comprehensive'
        therapy_record.remedy_suggestions = json.dumps(therapy_response['remedies'])
        db.session.add(therapy_record)
        db.session.commit()
        
        return jsonify({
            'emotion': emotion,
            'confidence': confidence,
            'therapy_response': therapy_response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Error in voice analysis: {str(e)}")
        return jsonify({'error': 'Voice analysis failed'}), 500

@app.route('/analyze_facial', methods=['POST'])
def analyze_facial():
    """Analyze emotion from facial expression"""
    try:
        data = request.get_json()
        image_data = data.get('image_data')
        
        if not image_data:
            return jsonify({'error': 'No image data provided'}), 400
        
        # Analyze emotion
        emotion, confidence = emotion_analyzer.analyze_facial_emotion(image_data)
        
        # Save emotion record (don't store the full image for privacy)
        emotion_record = EmotionRecord()
        emotion_record.session_id = session['session_id']
        emotion_record.input_type = 'facial'
        emotion_record.input_content = 'facial_expression_analyzed'
        emotion_record.detected_emotion = emotion
        emotion_record.confidence_score = confidence
        db.session.add(emotion_record)
        db.session.commit()
        
        # Generate therapy response
        therapy_response = therapy_generator.generate_response(emotion, confidence)
        
        # Save therapy response
        therapy_record = TherapyResponse()
        therapy_record.session_id = session['session_id']
        therapy_record.emotion_record_id = emotion_record.id
        therapy_record.response_text = therapy_response['full_response']
        therapy_record.response_type = 'comprehensive'
        therapy_record.remedy_suggestions = json.dumps(therapy_response['remedies'])
        db.session.add(therapy_record)
        db.session.commit()
        
        return jsonify({
            'emotion': emotion,
            'confidence': confidence,
            'therapy_response': therapy_response,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Error in facial analysis: {str(e)}")
        return jsonify({'error': 'Facial analysis failed'}), 500

@app.route('/get_breathing_exercise/<exercise_type>')
def get_breathing_exercise(exercise_type):
    """Get specific breathing exercise"""
    try:
        exercise = therapy_generator.get_breathing_exercise(exercise_type)
        return jsonify(exercise)
    except Exception as e:
        logging.error(f"Error getting breathing exercise: {str(e)}")
        return jsonify({'error': 'Could not retrieve exercise'}), 500

@app.route('/get_session_insights')
def get_session_insights():
    """Get insights about the current session"""
    try:
        session_id = session.get('session_id')
        if not session_id:
            return jsonify({'error': 'No active session'}), 400
        
        # Get emotion records for this session
        emotion_records = EmotionRecord.query.filter_by(session_id=session_id).all()
        
        # Generate insights
        insights = emotion_analyzer.get_emotion_insights(emotion_records)
        
        return jsonify({
            'insights': insights,
            'session_duration': len(emotion_records),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logging.error(f"Error getting session insights: {str(e)}")
        return jsonify({'error': 'Could not retrieve insights'}), 500

@app.route('/get_conversation_history')
def get_conversation_history():
    """Get conversation history for the current session"""
    try:
        session_id = session.get('session_id')
        if not session_id:
            return jsonify({'error': 'No active session'}), 400
        
        # Get emotion records and their responses
        emotion_records = db.session.query(EmotionRecord, TherapyResponse).join(
            TherapyResponse, EmotionRecord.id == TherapyResponse.emotion_record_id
        ).filter(EmotionRecord.session_id == session_id).order_by(EmotionRecord.timestamp).all()
        
        conversation = []
        for emotion_record, therapy_response in emotion_records:
            conversation.append({
                'timestamp': emotion_record.timestamp.isoformat(),
                'input_type': emotion_record.input_type,
                'input_content': emotion_record.input_content if emotion_record.input_type != 'facial' else 'Facial expression',
                'detected_emotion': emotion_record.detected_emotion,
                'confidence': emotion_record.confidence_score,
                'therapy_response': therapy_response.response_text,
                'remedies': json.loads(therapy_response.remedy_suggestions) if therapy_response.remedy_suggestions else []
            })
        
        return jsonify({
            'conversation': conversation,
            'total_interactions': len(conversation)
        })
        
    except Exception as e:
        logging.error(f"Error getting conversation history: {str(e)}")
        return jsonify({'error': 'Could not retrieve conversation history'}), 500

@app.route('/clear_session_history', methods=['POST'])
def clear_session_history():
    """Clear conversation history for the current session"""
    try:
        session_id = session.get('session_id')
        if not session_id:
            return jsonify({'error': 'No active session'}), 400
        
        # Delete therapy responses first (due to foreign key constraint)
        therapy_responses = TherapyResponse.query.filter_by(session_id=session_id).all()
        for response in therapy_responses:
            db.session.delete(response)
        
        # Delete emotion records
        emotion_records = EmotionRecord.query.filter_by(session_id=session_id).all()
        for record in emotion_records:
            db.session.delete(record)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Session history cleared successfully'
        })
        
    except Exception as e:
        logging.error(f"Error clearing session history: {str(e)}")
        db.session.rollback()
        return jsonify({'error': 'Could not clear session history'}), 500
