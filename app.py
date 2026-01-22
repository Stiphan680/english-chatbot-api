from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

def get_chatbot_response(question):
    """Function to get response from chatbot API with English language"""
    english_instruction = "Please respond in English."
    enhanced_question = f"{english_instruction} {question}"
    
    payload = {
        "messages": [
            {"role": "assistant", "content": "Hello! How can I help you today?"},
            {"role": "user", "content": enhanced_question}
        ]
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "Location": "https://seoschmiede.at/en/ai-tools/chatgpt-tool",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    
    url = "https://chatbot-ji1z.onrender.com/chatbot-ji1z"
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 200:
            api_response = response.json()
            return {
                "success": True,
                "response": api_response['choices'][0]['message']['content']
            }
        else:
            return {
                "success": False,
                "error": f"API returned status code {response.status_code}"
            }
    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "error": f"Request failed: {str(e)}"
        }
    except json.JSONDecodeError as e:
        return {
            "success": False,
            "error": f"JSON parsing failed: {str(e)}"
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"An error occurred: {str(e)}"
        }

@app.route('/', methods=['GET'])
def home():
    """Home endpoint with API information"""
    return jsonify({
        "message": "English Chatbot API",
        "version": "1.0",
        "status": "active",
        "endpoints": {
            "/": "GET - API information",
            "/chat": "POST - Send a question and get response",
            "/health": "GET - Health check"
        },
        "usage": {
            "endpoint": "/chat",
            "method": "POST",
            "body": {
                "question": "Your question here"
            },
            "example": {
                "request": {"question": "What is AI?"},
                "response": {"success": True, "response": "AI is..."}
            }
        }
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        
        if not data or 'question' not in data:
            return jsonify({
                "success": False,
                "error": "Missing 'question' field in request body"
            }), 400
        
        question = data['question'].strip()
        
        if not question:
            return jsonify({
                "success": False,
                "error": "Question cannot be empty"
            }), 400
        
        result = get_chatbot_response(question)
        
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 500
            
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "API is running"
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)