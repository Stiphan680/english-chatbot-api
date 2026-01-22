# Advanced English Chatbot API v2.0

High-performance REST API with advanced AI features including multi-language support, tone control, conversation history, and more.

## ✨ New Premium Features

### 1. 🌍 Multi-Language Support (8+ Languages)
- English
- Hindi
- Spanish
- French
- German
- Chinese (Simplified)
- Arabic
- Japanese

### 2. 🎭 Tone Control
- **Neutral** - Balanced and objective responses
- **Professional** - Formal and business-appropriate
- **Casual** - Friendly and conversational
- **Creative** - Imaginative and unique responses
- **Educational** - Detailed and informative

### 3. 📚 Conversation History & Context
- Track conversation history per user
- Include context from previous messages
- Personalized responses based on history
- Clear history when needed

### 4. 📊 Advanced Analysis
- **Sentiment Analysis** - Analyze emotions in text
- **Keyword Extraction** - Find important points
- **Text Summarization** - Create bullet-points or detailed summaries
- **Content Analysis** - Deep understanding of content

### 5. ⚡ Streaming Responses
- Real-time response generation
- Lower latency
- Better user experience

### 6. 🛡️ Rate Limiting
- 100 requests per hour per user (Free)
- Unlimited for Premium plans
- Prevent abuse

## API Endpoints

### Basic Chat
**POST** `/chat`
```json
{
  "question": "What is machine learning?",
  "language": "english",
  "tone": "professional",
  "user_id": "user123",
  "include_context": true,
  "format": "markdown"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Machine learning is...",
  "language": "english",
  "tone": "professional",
  "timestamp": "2026-01-22T09:15:00",
  "metadata": {
    "conversation_length": 5,
    "format": "markdown",
    "context_used": true
  }
}
```

### Streaming Responses
**POST** `/chat/stream`
```json
{
  "question": "Explain quantum computing",
  "language": "english",
  "tone": "educational",
  "user_id": "user123"
}
```

### Get Conversation History
**GET** `/chat/history?user_id=user123&limit=10`

**Response:**
```json
{
  "success": true,
  "user_id": "user123",
  "conversation_length": 15,
  "history": [
    {"role": "user", "content": "Hello"},
    {"role": "assistant", "content": "Hi there!"}
  ]
}
```

### Clear History
**POST** `/chat/clear`
```json
{
  "user_id": "user123"
}
```

### Analyze Text
**POST** `/analyze`
```json
{
  "text": "Your text here",
  "type": "sentiment"
}
```

### Summarize Content
**POST** `/summarize`
```json
{
  "content": "Long content to summarize",
  "type": "bullet-points"
}
```

## Usage Examples

### Python
```python
import requests

url = "https://english-chatbot-api.onrender.com/chat"
headers = {
    "X-API-Key": "your-api-key",
    "Content-Type": "application/json"
}

# Multi-language request
data = {
    "question": "What is artificial intelligence?",
    "language": "english",
    "tone": "professional",
    "user_id": "user123",
    "include_context": True
}

response = requests.post(url, json=data, headers=headers)
print(response.json())
```

### JavaScript (Fetch)
```javascript
const url = "https://english-chatbot-api.onrender.com/chat";
const headers = {
  "X-API-Key": "your-api-key",
  "Content-Type": "application/json"
};

const data = {
  question: "What is artificial intelligence?",
  language: "english",
  tone: "professional",
  user_id: "user123",
  include_context: true
};

fetch(url, {
  method: "POST",
  headers: headers,
  body: JSON.stringify(data)
})
.then(res => res.json())
.then(data => console.log(data));
```

### cURL
```bash
curl -X POST https://english-chatbot-api.onrender.com/chat \
  -H "X-API-Key: your-api-key" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Explain blockchain",
    "language": "english",
    "tone": "professional",
    "user_id": "user123",
    "include_context": true
  }'
```

## Advanced Features Guide

### Multi-Language Support

Set `language` parameter to one of:
- `english` - Default
- `hindi` - Hindi
- `spanish` - Spanish
- `french` - French
- `german` - German
- `chinese` - Chinese
- `arabic` - Arabic
- `japanese` - Japanese

### Tone Control

Set `tone` parameter to:
- `neutral` - Balanced response
- `professional` - Business tone
- `casual` - Friendly tone
- `creative` - Imaginative response
- `educational` - Detailed explanation

### Conversation Context

Enable with `include_context: true` to:
- Maintain conversation history
- Reference previous messages
- Provide personalized responses
- Track user preferences

### Response Formatting

Set `format` parameter to:
- `plain` - Plain text (default)
- `markdown` - With markdown formatting
- `detailed` - With metadata

## Deployment

### Deploy to Render

1. Push to GitHub
2. Connect repository to Render
3. Configure:
   ```
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```
4. Set environment variables if needed
5. Deploy!

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Access at http://localhost:5000
```

## Requirements

```
Flask==3.0.0
requests==2.31.0
gunicorn==21.2.0
```

## Rate Limiting

- **Free Plan**: 100 requests/hour
- **Basic Plan**: Unlimited requests
- **Pro Plan**: Unlimited + priority support

## Error Handling

All endpoints return structured error responses:

```json
{
  "success": false,
  "error": "Error message here",
  "status_code": 400
}
```

Common status codes:
- `200` - Success
- `400` - Bad request
- `401` - Unauthorized
- `429` - Rate limit exceeded
- `500` - Server error

## Security

- API key validation
- Rate limiting per user
- Input validation
- Error message sanitization
- Secure headers

## Support & Documentation

- **GitHub Issues**: Report bugs
- **Documentation**: Check `/` endpoint
- **API Status**: `/health` endpoint

## License

MIT License - Free to use and modify!

---

**Made with ❤️ by Stiphan680**

**Repository**: https://github.com/Stiphan680/english-chatbot-api