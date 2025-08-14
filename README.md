# Local Advanced Prompting System

A comprehensive Flask API for advanced prompting techniques with local deployment capabilities. Convert your prompting workflows into REST API endpoints for easy integration and scalability.

## 🚀 Features

- **Flask REST API** for all advanced prompting techniques
- **Few-shot Learning** endpoints for rapid task adaptation
- **Chain-of-Thought** reasoning for complex problem solving
- **Tree-of-Thought** exploration for multiple solution paths
- **Self-Consistency** validation for reliable outputs
- **Meta-Prompting** optimization for prompt improvement
- **Local Deployment** - no cloud dependencies required
- **Fast Unit Testing** with automated server management

## 📦 Installation

```bash
# Clone the repository
git clone https://github.com/Amruth22/Local-Advanced-Prompting-System.git
cd Local-Advanced-Prompting-System

# Install dependencies
pip install -r requirements.txt
```

## 🔧 Setup

1. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

2. **Add your Gemini API key:**
   ```env
   GEMINI_API_KEY=your_gemini_api_key_here
   FLASK_ENV=development
   FLASK_PORT=5000
   ```

3. **Start the Flask server:**
   ```bash
   python app.py
   ```

4. **Access Swagger UI for interactive testing:**
   ```
   http://localhost:5000/docs/
   ```

5. **Test the API:**
   ```bash
   curl http://localhost:5000/api/health
   ```

## 🌐 API Endpoints

### Health Check
```http
GET /api/health
```

### Few-shot Learning
```http
POST /api/few-shot/sentiment
Content-Type: application/json

{
  "text": "This product is amazing!"
}
```

```http
POST /api/few-shot/math
Content-Type: application/json

{
  "problem": "If a pizza costs $12 and has 8 slices, what's the cost per slice?"
}
```

```http
POST /api/few-shot/ner
Content-Type: application/json

{
  "text": "Apple Inc. was founded by Steve Jobs in California."
}
```

### Chain-of-Thought
```http
POST /api/chain-of-thought/math
Content-Type: application/json

{
  "problem": "A car travels 60 mph for 2.5 hours. How far does it go?"
}
```

```http
POST /api/chain-of-thought/logic
Content-Type: application/json

{
  "problem": "All birds can fly. Penguins are birds. Can penguins fly?"
}
```

### Tree-of-Thought
```http
POST /api/tree-of-thought/explore
Content-Type: application/json

{
  "problem": "How can we reduce plastic waste in cities?",
  "max_approaches": 3
}
```

### Self-Consistency
```http
POST /api/self-consistency/validate
Content-Type: application/json

{
  "question": "What are the benefits of renewable energy?",
  "num_samples": 3
}
```

### Meta-Prompting
```http
POST /api/meta-prompting/optimize
Content-Type: application/json

{
  "task": "Classify customer feedback",
  "current_prompt": "Is this feedback positive or negative: {text}"
}
```

## 📊 Response Format

All endpoints return JSON responses with consistent structure:

```json
{
  "success": true,
  "data": {
    "technique": "Few-shot Learning",
    "input": "user input",
    "output": "generated response",
    "metadata": {
      "processing_time": 1.23,
      "model": "gemini-2.5-flash"
    }
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

Error responses:
```json
{
  "success": false,
  "error": {
    "code": "INVALID_INPUT",
    "message": "Missing required field: text"
  },
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## 🧪 Testing

### Run Fast Unit Tests
```bash
# Fast tests with mocked API calls (~15 seconds)
python test_api.py

# Run with test runner
python run_tests.py --fast

# Test specific endpoints
python run_tests.py --test few-shot
python run_tests.py --test chain-of-thought
```

### Test Categories
- ✅ **API Health & Configuration** - Server startup, environment validation
- ✅ **Few-shot Learning Endpoints** - Sentiment, math, NER, classification
- ✅ **Chain-of-Thought Endpoints** - Math reasoning, logical analysis
- ✅ **Tree-of-Thought Endpoints** - Multi-path exploration
- ✅ **Self-Consistency Endpoints** - Multiple sampling validation
- ✅ **Meta-Prompting Endpoints** - Prompt optimization
- ✅ **Error Handling & Rate Limits** - Validation, error responses

## 🏗️ Project Structure

```
local-advanced-prompting-system/
├── app.py                      # Flask application entry point
├── api/                        # API route handlers
│   ├── __init__.py
│   ├── few_shot.py            # Few-shot learning endpoints
│   ├── chain_of_thought.py    # Chain-of-thought endpoints
│   ├── tree_of_thought.py     # Tree-of-thought endpoints
│   ├── self_consistency.py    # Self-consistency endpoints
│   └── meta_prompting.py      # Meta-prompting endpoints
├── core/                       # Core business logic
│   ├── __init__.py
│   ├── prompting_service.py   # Main prompting service
│   └── gemini_client.py       # Gemini API client
├── prompts/                    # Prompt templates
│   ├── __init__.py
│   ├── few_shot.py
│   ├── chain_of_thought.py
│   ├── tree_of_thought.py
│   ├── self_consistency.py
│   └── meta_prompting.py
├── tests/                      # Test suite
│   ├── __init__.py
│   ├── test_api.py            # API endpoint tests
│   ├── test_mocks.py          # Mock responses
│   └── conftest.py            # Test configuration
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── validators.py          # Input validation
│   └── response_formatter.py  # Response formatting
├── requirements.txt
├── .env.example
├── .gitignore
└── run_tests.py               # Test runner
```

## 🎯 Usage Examples

### Python Client
```python
import requests

# Sentiment analysis
response = requests.post('http://localhost:5000/api/few-shot/sentiment', 
                        json={'text': 'I love this product!'})
result = response.json()
print(result['data']['output'])  # 'positive'

# Math problem solving
response = requests.post('http://localhost:5000/api/chain-of-thought/math',
                        json={'problem': 'What is 15% of 200?'})
result = response.json()
print(result['data']['output'])  # Step-by-step solution
```

### cURL Examples
```bash
# Health check
curl http://localhost:5000/api/health

# Sentiment analysis
curl -X POST http://localhost:5000/api/few-shot/sentiment \
  -H "Content-Type: application/json" \
  -d '{"text": "This API is fantastic!"}'

# Chain-of-thought reasoning
curl -X POST http://localhost:5000/api/chain-of-thought/logic \
  -H "Content-Type: application/json" \
  -d '{"problem": "If all cats are animals, and some animals are pets, are some cats pets?"}'
```

## ⚠️ Rate Limits & Performance

**Gemini Free Tier Limits:**
- 10 requests per minute
- API automatically handles rate limiting
- Use caching for repeated requests
- Consider request queuing for high load

**Performance Tips:**
- Enable response caching for repeated queries
- Use async endpoints for better throughput
- Monitor API usage with built-in metrics
- Implement request batching for bulk operations

## 🔧 Configuration

### Environment Variables
```env
# Required
GEMINI_API_KEY=your_api_key_here

# Optional
FLASK_ENV=development          # development/production
FLASK_PORT=5000               # Server port
FLASK_HOST=127.0.0.1          # Server host
CACHE_ENABLED=true            # Enable response caching
CACHE_TTL=3600               # Cache time-to-live in seconds
LOG_LEVEL=INFO               # Logging level
```

### Advanced Configuration
```python
# config.py
class Config:
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-2.5-flash')
    CACHE_ENABLED = os.getenv('CACHE_ENABLED', 'true').lower() == 'true'
    RATE_LIMIT_ENABLED = True
    MAX_REQUESTS_PER_MINUTE = 10
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `python run_tests.py --fast`
5. Commit changes: `git commit -m 'Add amazing feature'`
6. Push to branch: `git push origin feature/amazing-feature`
7. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🔗 Related Projects

- [Advanced Prompting Techniques](https://github.com/Amruth22/Advanced-Prompting-Techniques) - Original command-line implementation
- [Gemini API Documentation](https://ai.google.dev/docs)

## 📞 Support

- Create an issue for bug reports or feature requests
- Check existing issues before creating new ones
- Provide detailed information for faster resolution