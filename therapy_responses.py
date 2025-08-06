import json
import random
import logging

class TherapyResponseGenerator:
    def __init__(self):
        self.therapy_responses = {
            'joy': {
                'validations': [
                    "I'm so glad to hear you're feeling positive! It's wonderful to see you in good spirits.",
                    "Your joy is contagious! It's beautiful to witness your happiness.",
                    "I can sense your enthusiasm, and it's truly uplifting. Embrace these positive moments!"
                ],
                'encouragements': [
                    "This positive energy you have is a strength. Try to remember this feeling during challenging times.",
                    "Joy is a powerful emotion. Consider keeping a gratitude journal to capture more moments like this.",
                    "Your happiness can be a source of resilience. What specifically is bringing you joy today?"
                ],
                'remedies': [
                    {
                        'type': 'joke',
                        'title': 'Happiness Joke',
                        'description': 'Why did the happy person bring a ladder to the party? Because they wanted to take their joy to the next level! Keep spreading those good vibes!',
                        'duration': '1 minute'
                    },
                    {
                        'type': 'song',
                        'title': 'Joyful Song: "Happy" by Pharrell Williams',
                        'description': '"Because I\'m happy, clap along if you feel like a room without a roof" - Perfect soundtrack for your positive mood!',
                        'duration': '4 minutes'
                    },
                    {
                        'type': 'song',
                        'title': 'Feel-Good Song: "Good as Hell" by Lizzo',
                        'description': 'An empowering anthem to celebrate feeling good about yourself and life.',
                        'duration': '3 minutes'
                    },
                    {
                        'type': 'activity',
                        'title': 'Gratitude Practice',
                        'description': 'Write down three things you\'re grateful for today',
                        'duration': '5 minutes'
                    },
                    {
                        'type': 'mindfulness',
                        'title': 'Joy Meditation',
                        'description': 'Sit quietly and focus on the feeling of joy. Let it fill your entire being.',
                        'duration': '10 minutes'
                    }
                ]
            },
            'sadness': {
                'validations': [
                    "I hear that you're going through a difficult time. Your feelings are completely valid.",
                    "It's okay to feel sad. These emotions are part of the human experience, and I'm here with you.",
                    "Thank you for sharing this with me. It takes courage to acknowledge when we're struggling."
                ],
                'encouragements': [
                    "Remember that sadness is temporary. You have the strength to work through this.",
                    "This difficult period doesn't define you. You've overcome challenges before.",
                    "Be gentle with yourself right now. Healing takes time, and that's perfectly okay."
                ],
                'remedies': [
                    {
                        'type': 'joke',
                        'title': 'Gentle Humor',
                        'description': 'Why don\'t scientists trust atoms? Because they make up everything! Sometimes a little smile can be the first step toward feeling better.',
                        'duration': '1 minute'
                    },
                    {
                        'type': 'song',
                        'title': 'Comforting Song: "Here Comes the Sun" by The Beatles',
                        'description': '"Here comes the sun, and I say it\'s all right" - A gentle reminder that difficult times pass.',
                        'duration': '3 minutes'
                    },
                    {
                        'type': 'song',
                        'title': 'Healing Song: "Three Little Birds" by Bob Marley',
                        'description': '"Don\'t worry about a thing, \'cause every little thing gonna be all right" - A soothing message of hope.',
                        'duration': '3 minutes'
                    },
                    {
                        'type': 'breathing',
                        'title': '4-7-8 Breathing Technique',
                        'description': 'Breathe in for 4 counts, hold for 7, exhale for 8. Repeat 4 times.',
                        'duration': '5 minutes'
                    },
                    {
                        'type': 'activity',
                        'title': 'Gentle Movement',
                        'description': 'Take a slow walk outside or do some gentle stretching',
                        'duration': '15 minutes'
                    },
                    {
                        'type': 'connection',
                        'title': 'Reach Out',
                        'description': 'Consider calling a friend or family member who makes you feel supported',
                        'duration': '10 minutes'
                    }
                ]
            },
            'anger': {
                'validations': [
                    "I can sense your frustration, and it's understandable to feel this way.",
                    "Anger often signals that something important to you has been threatened. Your feelings are valid.",
                    "Thank you for expressing this. It's healthy to acknowledge angry feelings rather than suppress them."
                ],
                'encouragements': [
                    "You have the power to channel this energy constructively. Let's work on some techniques together.",
                    "Anger can be a catalyst for positive change when managed well. You're stronger than this feeling.",
                    "Take a moment to breathe. You can navigate through this intense emotion."
                ],
                'remedies': [
                    {
                        'type': 'joke',
                        'title': 'Anger Release Joke',
                        'description': 'Why did the angry person go to the gym? Because they wanted to work out their issues! Remember, laughter can be a great way to release tension.',
                        'duration': '1 minute'
                    },
                    {
                        'type': 'song',
                        'title': 'Calming Song: "Weightless" by Marconi Union',
                        'description': 'Scientifically designed to reduce anxiety by 65%. Perfect for cooling down anger.',
                        'duration': '8 minutes'
                    },
                    {
                        'type': 'song',
                        'title': 'Release Song: "Let It Go" from Frozen',
                        'description': 'Sometimes we need to let go of anger that no longer serves us.',
                        'duration': '4 minutes'
                    },
                    {
                        'type': 'breathing',
                        'title': 'Box Breathing',
                        'description': 'Breathe in for 4, hold for 4, breathe out for 4, hold for 4. Repeat.',
                        'duration': '5 minutes'
                    },
                    {
                        'type': 'activity',
                        'title': 'Physical Release',
                        'description': 'Do some jumping jacks, push-ups, or vigorous exercise to release tension',
                        'duration': '10 minutes'
                    },
                    {
                        'type': 'mindfulness',
                        'title': 'Progressive Muscle Relaxation',
                        'description': 'Tense and release each muscle group from toes to head',
                        'duration': '15 minutes'
                    }
                ]
            },
            'fear': {
                'validations': [
                    "I understand you're feeling anxious or afraid. These feelings are your mind's way of trying to protect you.",
                    "Fear can be overwhelming, but you're not alone in this. I'm here to support you.",
                    "It's completely natural to feel scared sometimes. Acknowledging fear is the first step in addressing it."
                ],
                'encouragements': [
                    "You are braver than you believe. You can face this fear step by step.",
                    "Fear often feels bigger than it actually is. Let's break this down into manageable pieces.",
                    "Remember past times when you've overcome fears. You have that same strength now."
                ],
                'remedies': [
                    {
                        'type': 'joke',
                        'title': 'Courage Boost',
                        'description': 'What do you call a brave person facing their fears? A fear-less warrior! Remember, courage isn\'t the absence of fear - it\'s feeling the fear and doing it anyway.',
                        'duration': '1 minute'
                    },
                    {
                        'type': 'song',
                        'title': 'Brave Song: "Brave" by Sara Bareilles',
                        'description': '"Say what you wanna say, and let the words fall out" - Sometimes being brave means speaking up.',
                        'duration': '4 minutes'
                    },
                    {
                        'type': 'song',
                        'title': 'Calming Song: "Breathe" by Telepopmusik',
                        'description': 'A soothing electronic track that helps calm anxiety and fear.',
                        'duration': '4 minutes'
                    },
                    {
                        'type': 'breathing',
                        'title': 'Calm Breathing',
                        'description': 'Take slow, deep breaths. Focus on making your exhale longer than your inhale.',
                        'duration': '5 minutes'
                    },
                    {
                        'type': 'grounding',
                        'title': '5-4-3-2-1 Technique',
                        'description': 'Name 5 things you see, 4 you can touch, 3 you hear, 2 you smell, 1 you taste',
                        'duration': '5 minutes'
                    },
                    {
                        'type': 'mindfulness',
                        'title': 'Safe Place Visualization',
                        'description': 'Imagine yourself in a place where you feel completely safe and calm',
                        'duration': '10 minutes'
                    }
                ]
            },
            'trauma': {
                'validations': [
                    "I recognize that you're dealing with something very difficult. Your courage in sharing this shows incredible strength.",
                    "What you've experienced is significant, and your feelings are completely valid. I'm here to support you through this.",
                    "Thank you for trusting me with this. Trauma can feel overwhelming, but you don't have to face it alone."
                ],
                'encouragements': [
                    "Healing from trauma takes time, and it's okay to take it one step at a time. You are more resilient than you know.",
                    "Recovery isn't linear, and that's perfectly normal. Every small step forward is a victory worth celebrating.",
                    "You survived what happened to you, which shows your incredible inner strength. That same strength will help you heal."
                ],
                'remedies': [
                    {
                        'type': 'joke',
                        'title': 'Healing Through Humor',
                        'description': 'Why did the trauma survivor go to therapy? Because they wanted to turn their pain into their superpower! Remember: healing doesn\'t mean forgetting - it means growing stronger.',
                        'duration': '1 minute'
                    },
                    {
                        'type': 'joke',
                        'title': 'Gentle Smile',
                        'description': 'What do you call a person working through trauma? A warrior in training! Every therapy session, every moment of self-care, every breath you take is part of your training.',
                        'duration': '1 minute'
                    },
                    {
                        'type': 'song',
                        'title': 'Healing Song: "Stronger" by Kelly Clarkson',
                        'description': '"What doesn\'t kill you makes you stronger, stand a little taller" - Sometimes music can remind us of our resilience.',
                        'duration': '4 minutes'
                    },
                    {
                        'type': 'song',
                        'title': 'Peaceful Song: "Breathe Me" by Sia',
                        'description': 'A gentle song about vulnerability and healing. Sometimes it\'s okay to feel small while you\'re rebuilding.',
                        'duration': '4 minutes'
                    },
                    {
                        'type': 'song',
                        'title': 'Empowering Song: "Rise Up" by Andra Day',
                        'description': '"I\'ll rise up, I\'ll rise like the day" - A powerful anthem for survivors finding their strength.',
                        'duration': '4 minutes'
                    },
                    {
                        'type': 'breathing',
                        'title': 'Trauma-Informed Breathing',
                        'description': 'Breathe in safety for 4 counts, hold peace for 4 counts, breathe out tension for 6 counts. You are safe in this moment.',
                        'duration': '5 minutes'
                    },
                    {
                        'type': 'grounding',
                        'title': '5-4-3-2-1 Grounding Technique',
                        'description': 'Name 5 things you can see, 4 you can touch, 3 you can hear, 2 you can smell, 1 you can taste. This brings you back to the present moment.',
                        'duration': '5 minutes'
                    },
                    {
                        'type': 'self-care',
                        'title': 'Gentle Self-Care',
                        'description': 'Wrap yourself in a soft blanket, make a warm drink, or take a gentle shower. Physical comfort can help soothe emotional pain.',
                        'duration': '15 minutes'
                    }
                ]
            },
            'disgust': {
                'validations': [
                    "I can sense that you're feeling disgusted or repulsed by something. These feelings are completely valid.",
                    "Disgust is a natural protective emotion. It often tells us when something doesn't align with our values or comfort zone.",
                    "Thank you for sharing this difficult feeling. Disgust can be overwhelming, but we can work through it together."
                ],
                'encouragements': [
                    "This feeling will pass. Disgust is temporary, even when it feels intense in the moment.",
                    "You have the right to feel disgusted when something violates your boundaries or values.",
                    "Let's focus on what you can control and how to process these uncomfortable feelings healthily."
                ],
                'remedies': [
                    {
                        'type': 'joke',
                        'title': 'Cleansing Humor',
                        'description': 'Why did the person feeling disgusted become a comedian? Because laughter is the best disinfectant for bad feelings! Sometimes humor helps wash away the icky stuff.',
                        'duration': '1 minute'
                    },
                    {
                        'type': 'song',
                        'title': 'Cleansing Song: "Shake It Off" by Taylor Swift',
                        'description': '"I shake it off, I shake it off" - Sometimes you just need to shake off those gross feelings.',
                        'duration': '4 minutes'
                    },
                    {
                        'type': 'song',
                        'title': 'Fresh Start Song: "New Rules" by Dua Lipa',
                        'description': 'About setting boundaries and moving away from things that don\'t serve you.',
                        'duration': '3 minutes'
                    },
                    {
                        'type': 'breathing',
                        'title': 'Cleansing Breath',
                        'description': 'Breathe in fresh, clean air for 4 counts, hold for 2, breathe out anything unpleasant for 6 counts.',
                        'duration': '5 minutes'
                    },
                    {
                        'type': 'activity',
                        'title': 'Physical Cleansing',
                        'description': 'Take a shower, wash your hands, or clean your space to feel physically refreshed',
                        'duration': '10 minutes'
                    }
                ]
            },
            'surprise': {
                'validations': [
                    "I can sense that something unexpected has happened. Surprise can bring many different emotions with it.",
                    "Whether this surprise is positive or negative, it's natural to feel a bit unsettled by the unexpected.",
                    "Thank you for sharing this moment of surprise. These sudden changes can be quite overwhelming."
                ],
                'encouragements': [
                    "Surprises, whether good or challenging, often lead to growth and new perspectives.",
                    "You have the resilience to adapt to unexpected situations. Take your time to process this.",
                    "Remember that surprises are part of life's journey, and you can handle whatever comes your way."
                ],
                'remedies': [
                    {
                        'type': 'joke',
                        'title': 'Surprise Joke',
                        'description': 'Why don\'t surprises ever get lost? Because they always know how to make an unexpected entrance! Life\'s surprises keep things interesting.',
                        'duration': '1 minute'
                    },
                    {
                        'type': 'song',
                        'title': 'Uplifting Song: "What a Wonderful World" by Louis Armstrong',
                        'description': 'A reminder that even in surprising moments, there\'s beauty to be found in the world.',
                        'duration': '2 minutes'
                    },
                    {
                        'type': 'song',
                        'title': 'Adaptability Song: "Changes" by David Bowie',
                        'description': '"Ch-ch-ch-changes" - A song about embracing life\'s unexpected turns.',
                        'duration': '3 minutes'
                    },
                    {
                        'type': 'breathing',
                        'title': 'Grounding Breath',
                        'description': 'Breathe deeply to center yourself after an unexpected event. In for 4, hold for 4, out for 4.',
                        'duration': '5 minutes'
                    },
                    {
                        'type': 'mindfulness',
                        'title': 'Present Moment Awareness',
                        'description': 'Focus on what you can observe right now to ground yourself in the present moment',
                        'duration': '10 minutes'
                    }
                ]
            },
            'neutral': {
                'validations': [
                    "Thank you for sharing. How are you feeling in this moment?",
                    "I'm here to listen and support you. What's on your mind today?",
                    "It's perfectly okay to feel neutral or uncertain about your emotions."
                ],
                'encouragements': [
                    "Sometimes taking a moment to check in with ourselves is exactly what we need.",
                    "Neutral feelings can be a sign of balance. How can we build on this foundation?",
                    "This is a good time to practice some self-care or mindfulness."
                ],
                'remedies': [
                    {
                        'type': 'joke',
                        'title': 'Neutral Humor',
                        'description': 'Why did the neutral person become a referee? Because they\'re great at staying balanced! Sometimes a little laugh is all we need to shift our energy.',
                        'duration': '1 minute'
                    },
                    {
                        'type': 'song',
                        'title': 'Peaceful Song: "Weightless" by Marconi Union',
                        'description': 'A scientifically designed ambient track to promote relaxation and calm focus.',
                        'duration': '8 minutes'
                    },
                    {
                        'type': 'song',
                        'title': 'Motivating Song: "Can\'t Stop the Feeling!" by Justin Timberlake',
                        'description': 'An upbeat song to help shift from neutral into a more positive energy.',
                        'duration': '4 minutes'
                    },
                    {
                        'type': 'mindfulness',
                        'title': 'Body Scan',
                        'description': 'Slowly focus attention on each part of your body from head to toe',
                        'duration': '10 minutes'
                    },
                    {
                        'type': 'activity',
                        'title': 'Intention Setting',
                        'description': 'Think about what you\'d like to accomplish or focus on today',
                        'duration': '5 minutes'
                    }
                ]
            }
        }
    
    def generate_response(self, emotion, confidence=0.5, session_context=None):
        """Generate therapeutic response based on detected emotion"""
        try:
            emotion = emotion.lower()
            if emotion not in self.therapy_responses:
                emotion = 'neutral'
            
            responses = self.therapy_responses[emotion]
            
            # Select validation message
            validation = random.choice(responses['validations'])
            
            # Select encouragement if available
            encouragement = ""
            if 'encouragements' in responses:
                encouragement = random.choice(responses['encouragements'])
            
            # Select remedies
            selected_remedies = responses.get('remedies', [])
            if len(selected_remedies) > 2:
                selected_remedies = random.sample(selected_remedies, 2)
            
            # Construct full response
            full_response = validation
            if encouragement:
                full_response += f"\n\n{encouragement}"
            
            response_data = {
                'validation': validation,
                'encouragement': encouragement,
                'remedies': selected_remedies,
                'full_response': full_response,
                'emotion': emotion,
                'confidence': confidence
            }
            
            logging.debug(f"Generated therapy response for {emotion}: {len(full_response)} characters")
            return response_data
            
        except Exception as e:
            logging.error(f"Error generating therapy response: {str(e)}")
            return {
                'validation': "I'm here to listen and support you.",
                'encouragement': "Take a moment to breathe deeply.",
                'remedies': [],
                'full_response': "I'm here to listen and support you. Take a moment to breathe deeply.",
                'emotion': 'neutral',
                'confidence': 0.5
            }
    
    def get_breathing_exercise(self, exercise_type='basic'):
        """Get specific breathing exercise instructions"""
        exercises = {
            'basic': {
                'name': 'Deep Breathing',
                'instructions': 'Breathe in slowly through your nose for 4 counts, hold for 2 counts, then breathe out through your mouth for 6 counts. Repeat 5 times.',
                'duration': '3 minutes'
            },
            '478': {
                'name': '4-7-8 Breathing',
                'instructions': 'Breathe in through your nose for 4 counts, hold your breath for 7 counts, then exhale through your mouth for 8 counts. Repeat 4 times.',
                'duration': '5 minutes'
            },
            'box': {
                'name': 'Box Breathing',
                'instructions': 'Breathe in for 4 counts, hold for 4 counts, breathe out for 4 counts, hold empty for 4 counts. Repeat for several cycles.',
                'duration': '5 minutes'
            }
        }
        
        return exercises.get(exercise_type, exercises['basic'])
    
    def get_coping_strategies(self, emotion):
        """Get specific coping strategies for an emotion"""
        strategies = {
            'anger': [
                'Count to 10 before responding',
                'Take a cold shower or splash cold water on your face',
                'Write down your feelings in a journal',
                'Do some physical exercise'
            ],
            'sadness': [
                'Reach out to a supportive friend or family member',
                'Engage in a creative activity',
                'Listen to uplifting music',
                'Practice self-compassion'
            ],
            'fear': [
                'Break down the fear into smaller, manageable parts',
                'Challenge negative thoughts with realistic ones',
                'Use grounding techniques',
                'Seek support from others'
            ],
            'joy': [
                'Share your happiness with others',
                'Practice gratitude',
                'Engage in activities that bring you joy',
                'Create positive memories'
            ],
            'trauma': [
                'Practice grounding techniques like 5-4-3-2-1',
                'Use gentle breathing exercises',
                'Engage in soothing self-care activities',
                'Connect with trusted support people',
                'Listen to calming or empowering music',
                'Use humor as appropriate for healing'
            ],
            'disgust': [
                'Take deep cleansing breaths',
                'Engage in physical cleansing activities',
                'Create physical distance from the trigger',
                'Practice boundary-setting exercises',
                'Use humor to lighten the mood',
                'Listen to uplifting music'
            ],
            'surprise': [
                'Take grounding breaths to center yourself',
                'Focus on the present moment',
                'Give yourself time to process the unexpected',
                'Practice acceptance of change',
                'Use humor to cope with the unexpected',
                'Listen to calming or adaptive music'
            ]
        }
        
        return strategies.get(emotion.lower(), ['Take deep breaths', 'Practice mindfulness', 'Be kind to yourself'])
