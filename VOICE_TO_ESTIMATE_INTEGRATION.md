# Voice Recorder to ML Model Integration

## 🎯 What Was Changed

The VoiceRecorder component now integrates with the plumbing estimation ML models to:
1. Accept voice or text descriptions of plumbing jobs
2. Send them to the backend ML model for analysis
3. Extract job features using AI
4. Generate cost and time estimates
5. Display the estimates in a beautiful UI

## 🔧 Changes Made

### Backend (`models/api.py`)

#### Added New Endpoint: `/chat`
- **Purpose**: Handles conversational interactions and generates estimates
- **How it works**:
  1. Receives user messages about plumbing jobs
  2. Detects if message describes actual work (using keywords)
  3. Extracts features using ChatGPT (via `FeatureExtractor`)
  4. Predicts cost and time using trained ML models
  5. Returns conversational response with estimate data

#### New Models Added:
- `ChatRequest` - for incoming messages
- `ChatResponse` - includes response text, estimate data, and extracted features

### Frontend (`frontend/src/components/VoiceRecorder.jsx`)

#### Key Updates:
1. **Added `onEstimateReceived` prop** - callback to notify parent when estimate is generated
2. **Enhanced message handling** - now captures estimate and features data from API
3. **Visual estimate display** - shows cost and time estimates inline with conversation
4. **Improved UI** - estimate boxes with color-coded highlights

### Frontend (`frontend/src/App.jsx`)

#### Key Updates:
1. **New state: `aiEstimate`** - stores estimate generated from voice/chat
2. **New handler: `handleAiEstimate`** - receives estimate from VoiceRecorder
3. **New UI section** - large, beautiful estimate card showing:
   - Cost in GBP
   - Cost in DZD (Algerian Dinar)
   - Estimated time in days
   - Detected features (fixtures, types, quantities)
   - Clear button to dismiss

## 🚀 How to Use

### 1. Start the Backend API

```powershell
cd models
python -m uvicorn api:app --reload
```

The API will run at `http://localhost:8000`

### 2. Start the Frontend

```powershell
cd frontend
npm run dev
```

### 3. Try It Out

**Voice Input:**
1. Click the microphone button
2. Say something like: "I need to fix a leaking pipe under my kitchen sink"
3. Watch as the AI:
   - Transcribes your speech
   - Analyzes the job description
   - Generates a cost estimate
   - Displays the estimate with conversation

**Text Input:**
1. Type a job description like: "Install a luxury shower and wall-hung toilet"
2. Click the send button (➤)
3. Get the same AI-powered estimate

## 💡 Example Interactions

### Example 1: Simple Repair
**User:** "Fix a leaking pipe"

**AI Response:**
```
I understand you need help with: Fix a leaking pipe

Based on my analysis, here's what I estimate:
💰 Cost: £2,250.00 (DZD 401,785.71)
⏱️ Time: 3.5 days

This estimate is based on the specific details you provided...
```

### Example 2: Installation
**User:** "Install a luxury bathroom with wall-hung toilet and premium shower"

**AI Response:**
```
I understand you need help with: Install a luxury bathroom...

Based on my analysis, here's what I estimate:
💰 Cost: £2,520.00 (DZD 450,000.00)
⏱️ Time: 12.5 days

Detected Features:
- toilet: 1
- toiletType: Wall-Hung
- shower: 1
- showerType: Luxury_Enclosure
```

### Example 3: General Conversation
**User:** "What can you do?"

**AI Response:**
```
I can help you with plumbing job estimates! Just describe your plumbing needs:
- Repairs (leaks, clogs, etc.)
- Installations (toilets, sinks, showers, etc.)
- Replacements or upgrades

I'll analyze your description and provide cost and time estimates!
```

## 🎨 UI Features

### Conversation History
- Shows full conversation with user and AI
- Color-coded messages (blue for user, green for AI)
- Voice indicator for spoken messages
- Auto-scrolls to latest message

### Inline Estimates
- Small estimate preview in conversation
- Shows cost in both currencies
- Shows estimated time

### Large Estimate Card
- Prominent display below conversation
- Three panels: GBP cost, DZD cost, time
- Feature detection badges
- Clear button to remove

## 🔑 Key Features

1. **Conversational AI**: Natural back-and-forth dialogue
2. **Smart Detection**: Automatically detects when user describes a job
3. **ML-Powered**: Uses trained XGBoost and Ridge regression models
4. **Feature Extraction**: Uses ChatGPT to understand job details
5. **Dual Currency**: Shows costs in both GBP and DZD
6. **Voice & Text**: Works with both input methods
7. **Text-to-Speech**: Reads responses aloud for voice interactions

## 🛠 Technical Details

### API Flow
```
User Message
    ↓
VoiceRecorder.jsx
    ↓
POST /chat (api.py)
    ↓
Keyword Detection
    ↓
FeatureExtractor (ChatGPT)
    ↓
PlumbingPredictor (ML Models)
    ↓
Response + Estimate
    ↓
Display in UI
```

### Models Used
- **Feature Extraction**: OpenAI ChatGPT-3.5-turbo
- **Cost Prediction**: XGBoost Regressor
- **Time Prediction**: Ridge Regressor
- **Model Version**: v1.0.0

### Extracted Features
The system can detect:
- Fixtures: toilet, sink, shower, bath, bidet
- Types: Wall-Hung, Floor-Mounted, Luxury, Standard
- Quantities: 1, 2, 3, etc.
- Additional features: mirrors, cabinets, tiling

## 📝 Notes

- The backend requires an OpenAI API key for feature extraction
- Models are pre-trained and stored in `models/production/`
- Currency conversion uses a fixed rate: 1 DZD = 0.0056 GBP
- The system is optimized for plumbing jobs but can be adapted for other trades

## 🐛 Troubleshooting

**"Connection refused" error:**
- Make sure the backend API is running on port 8000
- Check that `uvicorn api:app --reload` is running

**"Model not found" error:**
- Ensure models exist at `models/production/plumbing_model_v1.0.0.joblib`
- Run `python save_models.py` if needed

**No estimate generated:**
- Make sure your description includes plumbing-related keywords
- Try being more specific about fixtures and work needed

## 🎉 Success!

Your voice recorder now uses real ML models to generate accurate plumbing estimates! The system combines:
- Natural language understanding (ChatGPT)
- Machine learning predictions (XGBoost + Ridge)
- Beautiful UI presentation
- Conversational interaction

Users can now simply describe their plumbing needs and get instant, AI-powered cost and time estimates!
