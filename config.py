import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # API Keys
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY', '')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    
    # Database
    MONGODB_URI = os.getenv('MONGODB_URI', '')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')
    
    # API Settings
    DEFAULT_MODEL = os.getenv('DEFAULT_MODEL', 'claude-3-5-sonnet-20241022')
    MAX_TOKENS = int(os.getenv('MAX_TOKENS', '4096'))
    TEMPERATURE = float(os.getenv('TEMPERATURE', '0.7'))
    
    # Performance
    ENABLE_CACHE = os.getenv('ENABLE_CACHE', 'true').lower() == 'true'
    CACHE_TTL = int(os.getenv('CACHE_TTL', '3600'))
    MAX_WORKERS = int(os.getenv('MAX_WORKERS', '4'))
    
    # Rate Limiting
    RATE_LIMIT_FREE = 100  # per hour
    RATE_LIMIT_BASIC = 1000
    RATE_LIMIT_PRO = 10000
    
    # Available Models
    MODELS = {
        # Claude models (Anthropic)
        'claude-3-5-sonnet': 'claude-3-5-sonnet-20241022',
        'claude-3-opus': 'claude-3-opus-20240229',
        'claude-3-haiku': 'claude-3-haiku-20240307',
        
        # OpenAI models
        'gpt-4-turbo': 'gpt-4-turbo-preview',
        'gpt-4': 'gpt-4',
        'gpt-3.5-turbo': 'gpt-3.5-turbo',
        
        # Google Gemini
        'gemini-pro': 'gemini-1.5-pro',
        'gemini-flash': 'gemini-1.5-flash'
    }
    
    # Feature flags
    ENABLE_VISION = True
    ENABLE_STREAMING = True
    ENABLE_FUNCTION_CALLING = True
    ENABLE_EMBEDDINGS = True