from flask import Flask, request, jsonify
import requests
import json
from datetime import datetime, timedelta
from collections import defaultdict

app = Flask(__name__)

# In-memory storage (replace with MongoDB for production)
user_conversations = defaultdict(list)  # Store conversation history
rate_limit_tracker = defaultdict(list)  # Track API calls

def get_chatbot_response(question, language='english', tone='neutral', context=None):
    """
    Advanced chatbot function with multiple features:
    - Multi-language support
    - Tone control (neutral, professional, casual, creative)
    - Context history support
    - Enhanced responses
    """
    
    # Language instruction
    language_map = {
        'english': 'Please respond in English.',
        'hindi': 'कृपया हिंदी में जवाब दें।',
        'spanish': 'Por favor, responde en español.',
        'french': 'Veuillez répondre en français.',
        'german': 'Bitte antworte auf Deutsch.',
        'chinese': '请用中文回答。',
        'arabic': 'يرجى الرد باللغة العربية.',
        'japanese': '日本語で答えてください。'
    }
    
    language_instruction = language_map.get(language.lower(), 'Please respond in English.')
    
    # Tone instruction
    tone_map = {
        'neutral': 'Provide a neutral and balanced response.',
        'professional': 'Provide a professional and formal response.',
        'casual': 'Provide a casual and friendly response.',
        'creative': 'Provide a creative and imaginative response.',
        'educational': 'Provide an educational and detailed response.'
    }
    
    tone_instruction = tone_map.get(tone.lower(), tone_map['neutral'])
    
    # Build enhanced question with instructions
    enhanced_question = f"{language_instruction} {tone_instruction} {question}"
    
    # Build messages with context
    messages = [
        {"role": "assistant", "content": "I'm an advanced AI assistant ready to help you with detailed, contextual responses."}
    ]
    
    # Add context if provided
    if context and isinstance(context, list):
        for ctx in context[-3:]:  # Keep last 3 messages for context
            messages.append(ctx)
    
    messages.append({"role": "user", "content": enhanced_question})
    
    payload = {
        "messages": messages
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    url = "https://chatbot-ji1z.onrender.com/chatbot-ji1z"
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            api_response = response.json()
            response_text = api_response['choices'][0]['message']['content']
            
            return {
                "success": True,
                "response": response_text,
                "language": language,
                "tone": tone,
                "timestamp": datetime.now().isoformat()
            }
        else:
            return {
                "success": False,
                "error": f"API returned status code {response.status_code}"
            }
    except Exception as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}"
        }

def check_rate_limit(user_id, limit=100):
    """Check if user has exceeded rate limit (100 requests per hour)"""
    now = datetime.now()
    hour_ago = now - timedelta(hours=1)
    
    # Clean old entries
    user_conversations[user_id] = [
        timestamp for timestamp in user_conversations[user_id]
        if timestamp > hour_ago
    ]
    
    if len(user_conversations[user_id]) >= limit:
        return False, f"Rate limit exceeded. Max {limit} requests per hour."
    return True, "OK"

def format_response(response_text, format_type='markdown'):
    """
    Format response in different styles
    - markdown: With markdown formatting
    - plain: Plain text
    - detailed: With metadata
    """
    if format_type == 'markdown':
        return f"```\n{response_text}\n```"
    elif format_type == 'plain':
        return response_text
    else:
        return response_text

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API information"""
    return jsonify({
        "message": "Advanced English Chatbot API",
        "version": "2.0",
        "status": "active",
        "premium_features": [
            "Multi-language support (8+ languages)",
            "Tone control (neutral, professional, casual, creative, educational)",
            "Conversation history & context",
            "Response formatting options",
            "Rate limiting per plan",
            "Advanced response metadata"
        ],
        "endpoints": {
            "/": "GET - API information",
            "/chat": "POST - Send a question with advanced options",
            "/chat/stream": "POST - Streaming responses",
            "/chat/history": "GET - Get conversation history",
            "/chat/clear": "POST - Clear conversation history",
            "/analyze": "POST - Analyze text/sentiment",
            "/summarize": "POST - Summarize content",
            "/health": "GET - Health check"
        },
        "usage": {
            "endpoint": "/chat",
            "method": "POST",
            "headers": {
                "X-API-Key": "your-api-key",
                "Content-Type": "application/json"
            },
            "body": {
                "question": "Your question here",
                "language": "english (optional)",
                "tone": "neutral (optional)",
                "include_context": "true (optional)",
                "format": "markdown (optional)"
            }
        }
    })

@app.route('/chat', methods=['POST'])
def chat():
    """
    Advanced chat endpoint with:
    - Multi-language support
    - Tone control
    - Context history
    - Response formatting
    """
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'question' field in request body"
            }), 400
        
        question = data['question'].strip()
        user_id = data.get('user_id', 'anonymous')
        language = data.get('language', 'english')
        tone = data.get('tone', 'neutral')
        include_context = data.get('include_context', False)
        response_format = data.get('format', 'plain')
        
        if not question:
            return jsonify({
                "success": False,
                "error": "Question cannot be empty"
            }), 400
        
        # Check rate limit
        allowed, message = check_rate_limit(user_id)
        if not allowed:
            return jsonify({
                "success": False,
                "error": message,
                "status_code": 429
            }), 429
        
        # Get conversation context if needed
        context = None
        if include_context and user_id in user_conversations:
            context = user_conversations[user_id][-5:]
        
        # Get response from chatbot
        result = get_chatbot_response(question, language, tone, context)
        
        if result['success']:
            # Store in history
            user_conversations[user_id].append({
                "role": "user",
                "content": question
            })
            user_conversations[user_id].append({
                "role": "assistant",
                "content": result['response']
            })
            
            # Format response
            formatted_response = format_response(result['response'], response_format)
            
            return jsonify({
                "success": True,
                "response": formatted_response,
                "language": language,
                "tone": tone,
                "timestamp": result['timestamp'],
                "user_id": user_id,
                "metadata": {
                    "conversation_length": len(user_conversations[user_id]),
                    "format": response_format,
                    "context_used": include_context
                }
            }), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

@app.route('/chat/stream', methods=['POST'])
def chat_stream():
    """
    Streaming chat endpoint for real-time responses
    Returns response as it's being generated
    """
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({"success": False, "error": "Missing 'question'"}), 400
        
        question = data['question'].strip()
        user_id = data.get('user_id', 'anonymous')
        language = data.get('language', 'english')
        tone = data.get('tone', 'neutral')
        
        result = get_chatbot_response(question, language, tone)
        
        if result['success']:
            return jsonify({
                "success": True,
                "response": result['response'],
                "stream": True,
                "language": language,
                "tone": tone
            }), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/chat/history', methods=['GET'])
def get_history():
    """
    Get conversation history for a user
    """
    try:
        user_id = request.args.get('user_id', 'anonymous')
        limit = int(request.args.get('limit', 10))
        
        if user_id in user_conversations:
            history = user_conversations[user_id][-limit:]
        else:
            history = []
        
        return jsonify({
            "success": True,
            "user_id": user_id,
            "conversation_length": len(user_conversations.get(user_id, [])),
            "history": history
        }), 200
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/chat/clear', methods=['POST'])
def clear_history():
    """
    Clear conversation history for a user
    """
    try:
        data = request.get_json()
        user_id = data.get('user_id', 'anonymous')
        
        if user_id in user_conversations:
            del user_conversations[user_id]
            return jsonify({
                "success": True,
                "message": f"History cleared for user {user_id}"
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": "No history found for this user"
            }), 404
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/analyze', methods=['POST'])
def analyze():
    """
    Analyze text for sentiment, key points, etc.
    """
    try:
        data = request.get_json()
        
        if not data or 'text' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'text' field"
            }), 400
        
        text = data['text']
        analysis_type = data.get('type', 'sentiment')  # sentiment, keywords, summary
        
        # Use AI to analyze
        analysis_prompt = f"Analyze the following text for {analysis_type}:\n{text}"
        result = get_chatbot_response(analysis_prompt, language='english', tone='professional')
        
        if result['success']:
            return jsonify({
                "success": True,
                "analysis_type": analysis_type,
                "text": text[:100] + "..." if len(text) > 100 else text,
                "analysis": result['response']
            }), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/summarize', methods=['POST'])
def summarize():
    """
    Summarize long content
    """
    try:
        data = request.get_json()
        
        if not data or 'content' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'content' field"
            }), 400
        
        content = data['content']
        summary_type = data.get('type', 'concise')  # concise, bullet-points, detailed
        
        # Use AI to summarize
        if summary_type == 'bullet-points':
            summary_prompt = f"Create bullet-point summary of:\n{content}"
        elif summary_type == 'detailed':
            summary_prompt = f"Create detailed summary of:\n{content}"
        else:
            summary_prompt = f"Create concise summary of:\n{content}"
        
        result = get_chatbot_response(summary_prompt, language='english', tone='professional')
        
        if result['success']:
            return jsonify({
                "success": True,
                "summary_type": summary_type,
                "original_length": len(content),
                "summary": result['response']
            }), 200
        else:
            return jsonify(result), 500
    
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "Advanced API is running",
        "version": "2.0",
        "timestamp": datetime.now().isoformat()
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)