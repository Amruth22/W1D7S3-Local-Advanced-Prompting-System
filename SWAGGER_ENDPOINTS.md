# 📚 Complete Swagger UI Endpoints

## 🚀 **Access Your Swagger UI**

After running `python app.py`, visit: **http://localhost:5000/docs/**

---

## 📋 **All Available Endpoints in Swagger UI**

### **🔧 System Endpoints**
- `GET /api/health` - Health Check
- `GET /api/info` - API Information  
- `GET /` - Welcome Message

### **🧠 Few-Shot Learning**
- `POST /api/v1/few-shot/sentiment` - Sentiment Analysis
- `POST /api/v1/few-shot/math` - Math Problem Solver
- `POST /api/v1/few-shot/ner` - Named Entity Recognition
- `POST /api/v1/few-shot/classification` - Text Classification

### **🔗 Chain-of-Thought**
- `POST /api/v1/chain-of-thought/math` - Math Reasoning
- `POST /api/v1/chain-of-thought/logic` - Logical Reasoning
- `POST /api/v1/chain-of-thought/analysis` - Complex Analysis

### **🌳 Tree-of-Thought**
- `POST /api/v1/tree-of-thought/explore` - Multi-Approach Problem Exploration

### **🔄 Self-Consistency**
- `POST /api/v1/self-consistency/validate` - Consistency Validation

### **🎯 Meta-Prompting**
- `POST /api/v1/meta-prompting/optimize` - Prompt Optimization
- `POST /api/v1/meta-prompting/analyze` - Task Analysis

---

## 🧪 **Quick Test Examples**

### **Sentiment Analysis**
```json
POST /api/v1/few-shot/sentiment
{
  "text": "This Swagger UI integration is fantastic!"
}
```

### **Math Reasoning**
```json
POST /api/v1/chain-of-thought/math
{
  "problem": "If I buy 3 books for $15 each and get a 20% discount, how much do I pay?"
}
```

### **Tree-of-Thought Exploration**
```json
POST /api/v1/tree-of-thought/explore
{
  "problem": "How can we improve team productivity?",
  "max_approaches": 3
}
```

### **Self-Consistency Validation**
```json
POST /api/v1/self-consistency/validate
{
  "question": "What are the benefits of exercise?",
  "num_samples": 3
}
```

### **Prompt Optimization**
```json
POST /api/v1/meta-prompting/optimize
{
  "task": "Summarize articles",
  "current_prompt": "Summarize this: {text}"
}
```

---

## ✨ **Swagger UI Features**

- **📝 Interactive Forms** - Fill out request bodies easily
- **🔄 Try It Out** - Execute real API calls
- **📊 Response Examples** - See what responses look like
- **🔍 Parameter Details** - Understand each parameter
- **📋 Schema Validation** - Built-in request validation
- **🏷️ Organized by Tags** - Grouped by technique type

---

## 🎯 **What You Can Do Now**

1. **🚀 Start the server**: `python app.py`
2. **📚 Open Swagger UI**: http://localhost:5000/docs/
3. **🧪 Test any endpoint** by clicking "Try it out"
4. **📝 See request/response examples** for each endpoint
5. **🔧 Understand parameters** with detailed descriptions
6. **⚡ Execute real API calls** directly from the browser

---

## 🎉 **All Endpoints Now Documented!**

Your `app.py` now includes:
- ✅ **Complete Swagger UI integration**
- ✅ **All 13 API endpoints documented**
- ✅ **Interactive testing interface**
- ✅ **Request/response schemas**
- ✅ **Parameter validation**
- ✅ **Error response documentation**

**Ready to test your advanced prompting techniques! 🚀**