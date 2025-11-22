# 🚀 Quick Start Guide - Voice to ML Estimate Integration

## What's New?

The Voice Recorder now uses **real ML models** to analyze plumbing job descriptions and generate accurate cost & time estimates!

## 📋 Prerequisites

1. **Python 3.8+** installed
2. **Node.js** installed
3. **OpenAI API Key** (for feature extraction)

## 🔧 Setup & Run

### Step 1: Set Up the Backend (Models API)

```powershell
# Navigate to models directory
cd models

# Install Python dependencies (if not already installed)
pip install -r requirements.txt

# Create .env file with your OpenAI API key
# Create a file named .env in the models folder with:
# OPENAI_API_KEY=your_api_key_here

# Start the API server
python -m uvicorn api:app --reload
```

The API will start at `http://localhost:8000`

**Verify it's running:**
- Open browser to: http://localhost:8000/docs
- You should see the Swagger UI with API documentation

### Step 2: Start the Frontend

```powershell
# Open a NEW terminal window
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already installed)
npm install

# Start the development server
npm run dev
```

The frontend will start at `http://localhost:5173` (or similar)

## 🎯 How to Use

### Option 1: Voice Input

1. **Click the microphone button** 🎤
2. **Speak your job description**, for example:
   - "I need to fix a leaking pipe under the kitchen sink"
   - "Install a luxury bathroom with wall-hung toilet and shower"
   - "Replace the old sink with a new pedestal sink"
3. **Wait for the AI response** - it will:
   - Show the conversation
   - Extract job details
   - Generate cost estimate (GBP & DZD)
   - Show estimated time in days
   - Read the response aloud

### Option 2: Text Input

1. **Type your job description** in the text box
2. **Click the send button** (➤)
3. **See the same AI-powered analysis and estimate**

## 💬 Example Conversations

### Example 1: Leak Repair
```
You: "Fix a leaking pipe under my sink"

AI: "I understand you need help with: Fix a leaking pipe under my sink

Based on my analysis, here's what I estimate:
💰 Cost: £1,890.00 (DZD 337,500.00)
⏱️ Time: 2.5 days

This estimate is based on the specific details you provided..."
```

### Example 2: Bathroom Installation
```
You: "Install a luxury bathroom with wall-hung toilet and premium shower"

AI: "I understand you need help with: Install a luxury bathroom...

Based on my analysis, here's what I estimate:
💰 Cost: £2,520.00 (DZD 450,000.00)
⏱️ Time: 12.5 days

Detected Features:
- toilet: 1, toiletType: Wall-Hung
- shower: 1, showerType: Luxury_Enclosure"
```

## 🧪 Testing the API

Test the chat endpoint directly:

```powershell
cd models
python test_chat.py
```

This will run several test cases to verify the API is working correctly.

## 🎨 Features

✅ **Voice Recognition** - Speak naturally, AI understands  
✅ **Text Input** - Type if you prefer  
✅ **Real ML Models** - XGBoost & Ridge regression  
✅ **Feature Extraction** - ChatGPT analyzes job details  
✅ **Cost Estimates** - In GBP and DZD  
✅ **Time Estimates** - Days required for job  
✅ **Conversational** - Natural back-and-forth dialogue  
✅ **Text-to-Speech** - AI reads responses aloud  
✅ **Beautiful UI** - Modern, responsive design  

## 🛠 Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **XGBoost** - ML model for cost prediction
- **Ridge Regression** - ML model for time prediction
- **OpenAI GPT-3.5** - Feature extraction from natural language
- **Pydantic** - Data validation

### Frontend
- **React** - UI framework
- **Web Speech API** - Voice recognition
- **Speech Synthesis API** - Text-to-speech

## 📊 What Gets Analyzed?

The AI extracts features like:
- **Fixtures**: toilet, sink, shower, bath, bidet
- **Types**: Wall-Hung, Floor-Mounted, Luxury, Standard, Budget
- **Quantities**: How many of each
- **Additional**: mirrors, cabinets, tiles, plumbing complexity

## 🔧 Troubleshooting

### Backend won't start
- **Check Python version**: `python --version` (should be 3.8+)
- **Reinstall dependencies**: `pip install -r requirements.txt`
- **Check OpenAI key**: Make sure `.env` file exists with `OPENAI_API_KEY=...`

### "Connection refused" in frontend
- **Make sure backend is running** on port 8000
- **Check the terminal** where you ran `uvicorn` for errors

### No estimate generated
- **Use plumbing-related words**: leak, pipe, toilet, sink, install, fix, repair
- **Be specific**: Include fixture types and what work needs to be done

### Voice not working
- **Check browser permissions**: Allow microphone access
- **Use Chrome/Edge**: Best browser support for Web Speech API
- **Check microphone**: Make sure it's working in other apps

## 📚 Additional Documentation

- **`VOICE_TO_ESTIMATE_INTEGRATION.md`** - Detailed technical documentation
- **`models/API_SUMMARY.md`** - API architecture and endpoints
- **`models/API_USAGE.md`** - Comprehensive API usage guide

## 🎉 Success Indicators

You'll know it's working when:
1. ✅ Backend shows "API is ready!" message
2. ✅ Frontend loads without errors
3. ✅ Microphone button responds to clicks
4. ✅ Voice/text input generates AI responses
5. ✅ Estimates appear with cost and time data

## 💡 Pro Tips

- **Be descriptive**: More details = better estimates
- **Use fixture names**: "wall-hung toilet" vs just "toilet"
- **Specify quality**: "luxury", "standard", "budget"
- **Ask questions**: The AI can have conversations!
- **Check estimates**: Review the detected features to ensure accuracy

---

**Need Help?** Check the documentation files or test the API with `test_chat.py`!
