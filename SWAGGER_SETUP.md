# 📚 Swagger UI Setup Guide

## 🚀 Quick Start with Swagger UI

The repository now includes **Swagger UI integration** for easy API testing and documentation. Here are the available options:

---

## 🎯 **Option 1: Simple Flasgger Integration (Recommended)**

### Step 1: Use the Simple Swagger App
```bash
# Run the app with built-in Swagger UI
python app_simple_swagger.py
```

### Step 2: Access Swagger UI
- **📚 Swagger UI**: http://localhost:5000/docs/
- **🏠 Root API**: http://localhost:5000/
- **❤️ Health Check**: http://localhost:5000/api/health
- **📊 API Info**: http://localhost:5000/api/info

---

## 🎯 **Option 2: Advanced Flask-RESTX Integration**

### Step 1: Install Additional Dependencies
```bash
pip install flask-restx
```

### Step 2: Run Setup Script
```bash
python setup_swagger.py
```

### Step 3: Start the Server
```bash
python app.py  # Now includes Swagger UI
```

### Step 4: Access Advanced Swagger UI
- **📚 Swagger UI**: http://localhost:5000/api/v1/docs/

---

## 🧪 **Testing Your API Endpoints**

Once you have Swagger UI running, you can test all endpoints directly from the browser:

### **Few-Shot Learning Endpoints:**
- `POST /api/v1/few-shot/sentiment` - Sentiment analysis
- `POST /api/v1/few-shot/math` - Math problem solving
- `POST /api/v1/few-shot/ner` - Named entity recognition
- `POST /api/v1/few-shot/classification` - Text classification

### **Chain-of-Thought Endpoints:**
- `POST /api/v1/chain-of-thought/math` - Step-by-step math reasoning
- `POST /api/v1/chain-of-thought/logic` - Logical reasoning
- `POST /api/v1/chain-of-thought/analysis` - Complex analysis

### **Tree-of-Thought Endpoints:**
- `POST /api/v1/tree-of-thought/explore` - Multi-approach exploration

### **Self-Consistency Endpoints:**
- `POST /api/v1/self-consistency/validate` - Consistency validation

### **Meta-Prompting Endpoints:**
- `POST /api/v1/meta-prompting/optimize` - Prompt optimization
- `POST /api/v1/meta-prompting/analyze` - Task analysis

---

## 📝 **Example API Calls**

### Sentiment Analysis
```json
POST /api/v1/few-shot/sentiment
{
  "text": "This product is absolutely amazing!"
}
```

### Math Problem Solving
```json
POST /api/v1/few-shot/math
{
  "problem": "If a pizza costs $12 and has 8 slices, what does each slice cost?"
}
```

### Chain-of-Thought Reasoning
```json
POST /api/v1/chain-of-thought/math
{
  "problem": "A car travels 60 mph for 2.5 hours. How far does it travel?"
}
```

### Tree-of-Thought Exploration
```json
POST /api/v1/tree-of-thought/explore
{
  "problem": "How can we reduce plastic waste in cities?",
  "max_approaches": 3
}
```

---

## 🔧 **Configuration**

Make sure your `.env` file is properly configured:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional
FLASK_ENV=development
FLASK_PORT=5000
FLASK_HOST=127.0.0.1
FLASK_DEBUG=true
```

---

## 🎉 **Features of Swagger UI**

✅ **Interactive Testing** - Test all endpoints directly from the browser  
✅ **Request/Response Examples** - See example payloads and responses  
✅ **Parameter Documentation** - Detailed parameter descriptions  
✅ **Error Code Documentation** - Understand error responses  
✅ **Model Schemas** - View request/response data structures  
✅ **Try It Out** - Execute real API calls with your data  

---

## 🚨 **Troubleshooting**

### Issue: Swagger UI not loading
**Solution**: Make sure you're using the correct file:
```bash
python app_simple_swagger.py  # For simple integration
```

### Issue: Missing dependencies
**Solution**: Install required packages:
```bash
pip install flasgger flask-restx
```

### Issue: API endpoints not working
**Solution**: Check your Gemini API key in `.env` file

---

## 📞 **Support**

If you encounter any issues:
1. Check the console logs for error messages
2. Verify your `.env` configuration
3. Ensure all dependencies are installed
4. Visit the health check endpoint: `/api/health`

---

## 🎯 **Quick Links**

- **📚 Swagger UI**: http://localhost:5000/docs/
- **🏠 API Root**: http://localhost:5000/
- **❤️ Health Check**: http://localhost:5000/api/health
- **📊 API Info**: http://localhost:5000/api/info

Happy testing! 🚀