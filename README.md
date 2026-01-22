# English Chatbot API

A Flask-based REST API for an English chatbot with automatic language enforcement.

## Features

- RESTful API endpoints
- Automatic English language responses
- Health check endpoint
- Easy deployment to Render
- Error handling and validation

## API Endpoints

### GET `/`
Returns API information and usage instructions.

### POST `/chat`
Send a question and receive a chatbot response.

**Request Body:**
```json
{
  "question": "What is artificial intelligence?"
}
```

**Response:**
```json
{
  "success": true,
  "response": "Artificial intelligence is..."
}
```

### GET `/health`
Health check endpoint for monitoring.

## Local Development

1. Clone the repository:
```bash
git clone https://github.com/Stiphan680/english-chatbot-api.git
cd english-chatbot-api
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## Deploy to Render

### Quick Deploy Steps:

1. **Go to [Render Dashboard](https://dashboard.render.com/)**

2. **Click "New +" → "Web Service"**

3. **Connect your GitHub repository:**
   - Select "english-chatbot-api"

4. **Configure the service:**
   - **Name:** `english-chatbot-api` (or your choice)
   - **Region:** Select closest to your users
   - **Branch:** `main`
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`

5. **Instance Type:**
   - Select "Free" for testing

6. **Click "Create Web Service"**

7. **Wait for deployment** (2-3 minutes)

8. **Your API will be live at:** `https://your-service-name.onrender.com`

## Usage Examples

### Using cURL:
```bash
curl -X POST https://your-api-url.onrender.com/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is machine learning?"}'
```

### Using Python:
```python
import requests

url = "https://your-api-url.onrender.com/chat"
data = {"question": "What is machine learning?"}

response = requests.post(url, json=data)
print(response.json())
```

### Using JavaScript (fetch):
```javascript
fetch('https://your-api-url.onrender.com/chat', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({question: 'What is machine learning?'})
})
.then(res => res.json())
.then(data => console.log(data));
```

## Environment Variables (Optional)

If you need to configure anything, you can add environment variables in Render:
- Go to your service → Environment tab
- Add variables as needed

## Troubleshooting

- **Cold starts:** Free tier on Render has cold starts (15 sec delay after inactivity)
- **Logs:** Check Render logs tab for debugging
- **Timeout errors:** Increase timeout in requests if needed

## Tech Stack

- **Framework:** Flask 3.0.0
- **HTTP Client:** Requests 2.31.0
- **WSGI Server:** Gunicorn 21.2.0
- **Deployment:** Render

## License

MIT License - feel free to use and modify!

---

**Developer:** Stiphan680  
**Repository:** [https://github.com/Stiphan680/english-chatbot-api](https://github.com/Stiphan680/english-chatbot-api)