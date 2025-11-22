"""
FastAPI Application for Plumbing Cost and Time Estimation
==========================================================
This API accepts natural language job descriptions and returns cost and time estimates.

Usage:
    uvicorn api:app --reload

Endpoints:
    POST /estimate - Get cost and time estimate from job description
    GET /health - Health check endpoint
"""

import os
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from predict import PlumbingPredictor
from pydantic import BaseModel, Field
from services.feature_extractor import FeatureExtractor

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Plumbing Cost Estimator API",
    description="Get cost and time estimates for plumbing jobs using natural language descriptions",
    version="1.0.0",
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Currency conversion rate
DZD_TO_GBP_RATE = 0.0056


def dzd_to_gbp(dzd_amount: float, exchange_rate: float = DZD_TO_GBP_RATE) -> float:
    """Convert Algerian Dinar to British Pounds."""
    return dzd_amount * exchange_rate


# Initialize services (singleton pattern)
class Services:
    """Singleton class to hold initialized services."""

    _extractor: Optional[FeatureExtractor] = None
    _predictor: Optional[PlumbingPredictor] = None

    @classmethod
    def get_extractor(cls) -> FeatureExtractor:
        """Get or create feature extractor instance."""
        if cls._extractor is None:
            cls._extractor = FeatureExtractor()
        return cls._extractor

    @classmethod
    def get_predictor(cls) -> PlumbingPredictor:
        """Get or create predictor instance."""
        if cls._predictor is None:
            model_path = "models/production/plumbing_model_v1.0.0.joblib"
            if not os.path.exists(model_path):
                raise FileNotFoundError(
                    f"Model file not found at {model_path}. "
                    "Please run 'python model.py' to train the model first."
                )
            cls._predictor = PlumbingPredictor(model_path)
        return cls._predictor


# Pydantic models for request/response validation
class EstimateRequest(BaseModel):
    """Request model for job estimation."""

    job_description: str = Field(
        ...,
        min_length=10,
        max_length=1000,
        description="Natural language description of the plumbing job",
        example="I need a luxury bathroom with a wall-hung toilet, luxury shower, and a pedestal sink",
    )


class EstimateResponse(BaseModel):
    """Response model for job estimation."""

    success: bool = Field(description="Whether the estimation was successful")
    job_description: str = Field(description="Original job description")
    cost_dzd: float = Field(description="Estimated cost in Algerian Dinar")
    cost_gbp: float = Field(description="Estimated cost in British Pounds")
    time_days: float = Field(description="Estimated time in days")
    features: dict = Field(description="Extracted features from job description")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "job_description": "Install luxury bathroom with wall-hung toilet",
                "cost_dzd": 450000.00,
                "cost_gbp": 2520.00,
                "time_days": 12.5,
                "features": {
                    "toilet": 1,
                    "toileType": "Wall-Hung",
                    "showerCabin": 1,
                    "showerCabinType": "Luxury_Enclosure",
                },
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""

    success: bool = False
    error: str = Field(description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User message describing the plumbing job"
    )


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(description="AI response text")
    estimate: Optional[dict] = Field(None, description="Cost and time estimate if job was described")
    features: Optional[dict] = Field(None, description="Extracted features if applicable")
    materials: Optional[list] = Field(None, description="Suggested materials list with names and quantities")
    tasks: Optional[list] = Field(None, description="Labor tasks with estimated hours")


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Plumbing Cost Estimator API",
        "version": "1.0.0",
        "description": "Get cost and time estimates for plumbing jobs",
        "endpoints": {
            "POST /estimate": "Get estimate from job description",
            "GET /health": "Health check",
            "GET /docs": "API documentation (Swagger UI)",
            "GET /redoc": "API documentation (ReDoc)",
        },
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        # Check if services can be initialized
        Services.get_extractor()
        Services.get_predictor()
        return {
            "status": "healthy",
            "services": {"feature_extractor": "ready", "predictor": "ready"},
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}


@app.post("/estimate", response_model=EstimateResponse)
async def estimate_job(request: EstimateRequest):
    """
    Estimate cost and time for a plumbing job.

    This endpoint:
    1. Extracts features from the natural language job description using ChatGPT
    2. Predicts cost (in DZD and GBP) and time using trained ML models
    3. Returns the estimates along with extracted features

    Args:
        request: EstimateRequest containing job_description

    Returns:
        EstimateResponse with cost, time, and extracted features

    Raises:
        HTTPException: If estimation fails
    """
    try:
        # Get services
        extractor = Services.get_extractor()
        predictor = Services.get_predictor()

        # Extract features from job description
        features = extractor.extract_features(request.job_description)

        # Make prediction
        prediction = predictor.predict(features)

        # Convert currency
        cost_dzd = prediction["cost"]
        cost_gbp = dzd_to_gbp(cost_dzd)
        time_days = prediction["time"]

        # Return response
        return EstimateResponse(
            success=True,
            job_description=request.job_description,
            cost_gbp=round(cost_gbp, 2),
            time_days=round(time_days / 15, 0),
            features=features,
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={"success": False, "error": "Invalid input", "detail": str(e)},
        )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Model not found", "detail": str(e)},
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"success": False, "error": "Estimation failed", "detail": str(e)},
        )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Chat endpoint that handles conversational interactions and generates estimates.
    
    This endpoint:
    1. Accepts a natural language message
    2. Attempts to extract job features if the message describes work
    3. Returns a conversational response with optional estimate
    
    Args:
        request: ChatRequest containing user message
        
    Returns:
        ChatResponse with conversational response and optional estimate
    """
    try:
        message = request.message.lower()
        
        # Check if message seems to describe a job
        job_keywords = ['fix', 'repair', 'install', 'replace', 'leak', 'pipe', 'drain', 
                       'toilet', 'sink', 'shower', 'bath', 'faucet', 'water', 'plumbing']
        
        is_job_description = any(keyword in message for keyword in job_keywords)
        
        if is_job_description:
            try:
                # Get services
                extractor = Services.get_extractor()
                predictor = Services.get_predictor()
                
                # Extract features from message
                features = extractor.extract_features(request.message)
                
                # Make prediction
                prediction = predictor.predict(features)
                
                # Convert currency
                cost_dzd = prediction['cost']
                cost_gbp = dzd_to_gbp(cost_dzd)
                time_days = prediction['time']
                
                estimate = {
                    'cost_dzd': round(cost_dzd, 2),
                    'cost_gbp': round(cost_gbp, 2),
                    'time_days': round(time_days, 1),
                }
                
                # Generate materials and tasks from features
                materials = []
                tasks = []
                
                # Map features to materials
                if features.get('toilet', 0) > 0:
                    toilet_type = features.get('toileType', 'One-Piece')
                    materials.append({'name': f"{toilet_type} Toilet", 'qty': features['toilet'], 'unitPrice': 350 if toilet_type == 'Wall-Hung' else 250 if toilet_type == 'One-Piece' else 150})
                    tasks.append({'title': f"Install {toilet_type} Toilet", 'hours': features['toilet'] * 3})
                
                if features.get('washbasin', 0) > 0:
                    basin_type = features.get('washbasinType', 'Standard')
                    materials.append({'name': f"{basin_type} Washbasin", 'qty': features['washbasin'], 'unitPrice': 180 if 'Luxury' in basin_type else 120})
                    tasks.append({'title': 'Install Washbasin', 'hours': features['washbasin'] * 2})
                
                if features.get('showerCabin', 0) > 0:
                    shower_type = features.get('showerCabinType', 'Standard')
                    materials.append({'name': f"{shower_type} Shower Cabin", 'qty': features['showerCabin'], 'unitPrice': 800 if 'Luxury' in shower_type else 450})
                    tasks.append({'title': 'Install Shower Cabin', 'hours': features['showerCabin'] * 5})
                
                if features.get('bathhub', 0) > 0:
                    bath_type = features.get('bathhubType', 'Standard')
                    materials.append({'name': f"{bath_type} Bathtub", 'qty': features['bathhub'], 'unitPrice': 1200 if 'Luxury' in bath_type else 600})
                    tasks.append({'title': 'Install Bathtub', 'hours': features['bathhub'] * 6})
                
                if features.get('Bidet', 0) > 0:
                    bidet_type = features.get('BidetType', 'Standard')
                    materials.append({'name': f"{bidet_type} Bidet", 'qty': features['Bidet'], 'unitPrice': 200})
                    tasks.append({'title': 'Install Bidet', 'hours': features['Bidet'] * 2})
                
                if features.get('radiator', 0) > 0:
                    rad_type = features.get('radiatorType', 'Standard Radiator')
                    materials.append({'name': rad_type, 'qty': features['radiator'], 'unitPrice': 150})
                    tasks.append({'title': 'Install Radiators', 'hours': features['radiator'] * 1.5})
                
                if features.get('waterHeater', 0) > 0:
                    heater_type = features.get('waterHeaterType', 'Standard')
                    materials.append({'name': f"{heater_type} Water Heater", 'qty': features['waterHeater'], 'unitPrice': 400})
                    tasks.append({'title': 'Install Water Heater', 'hours': features['waterHeater'] * 4})
                
                if features.get('boilerSize') and features['boilerSize'] not in ['none', '0', 0]:
                    size = features['boilerSize']
                    price = 1500 if size == 'big' else 1000 if size == 'medium' else 600
                    materials.append({'name': f"{size.capitalize()} Boiler", 'qty': 1, 'unitPrice': price})
                    tasks.append({'title': 'Install Boiler', 'hours': 8})
                
                # Add common materials if we have any fixtures
                if materials:
                    materials.extend([
                        {'name': 'PVC Pipes & Fittings', 'qty': 1, 'unitPrice': 150},
                        {'name': 'Plumbing Hardware Kit', 'qty': 1, 'unitPrice': 80},
                        {'name': 'Sealants & Adhesives', 'qty': 1, 'unitPrice': 40}
                    ])
                
                response_text = (
                    f"I understand you need help with: {request.message}\n\n"
                    f"Based on my analysis, here's what I estimate:\n"
                    f"💰 Cost: £{estimate['cost_gbp']:.2f} (DZD {estimate['cost_dzd']:.2f})\n"
                    f"⏱️ Time: {estimate['time_days']} days\n\n"
                    f"This estimate is based on the specific details you provided. "
                    f"Would you like me to explain any part of this estimate or do you have additional questions?"
                )
                
                return ChatResponse(
                    response=response_text,
                    estimate=estimate,
                    features=features,
                    materials=materials,
                    tasks=tasks
                )
                
            except Exception as e:
                # If estimation fails, still provide a helpful response
                return ChatResponse(
                    response=(
                        f"I understand you're describing a plumbing job, but I need a bit more detail to provide "
                        f"an accurate estimate. Could you tell me more about:\n"
                        f"- The specific fixtures involved (toilet, sink, shower, etc.)\n"
                        f"- The type/quality level you're looking for (standard, luxury, etc.)\n"
                        f"- Any other relevant details about the work?"
                    ),
                    estimate=None,
                    features=None
                )
        else:
            # General conversation response
            if any(word in message for word in ['hello', 'hi', 'hey']):
                response_text = (
                    "Hello! I'm your AI plumbing assistant. I can help you estimate costs and time "
                    "for plumbing jobs. Just describe what you need done!"
                )
            elif any(word in message for word in ['help', 'what can you do']):
                response_text = (
                    "I can help you with plumbing job estimates! Just describe your plumbing needs:\n"
                    "- Repairs (leaks, clogs, etc.)\n"
                    "- Installations (toilets, sinks, showers, etc.)\n"
                    "- Replacements or upgrades\n\n"
                    "I'll analyze your description and provide cost and time estimates!"
                )
            elif any(word in message for word in ['thank', 'thanks']):
                response_text = "You're welcome! Let me know if you need help with anything else!"
            else:
                response_text = (
                    "I'm here to help with plumbing estimates! Could you describe the plumbing work "
                    "you need done? Include details like fixtures, repairs, or installations you're considering."
                )
            
            return ChatResponse(
                response=response_text,
                estimate=None,
                features=None
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Chat processing failed",
                "detail": str(e)
            }
        )


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    print("=" * 80)
    print("PLUMBING COST ESTIMATOR API")
    print("=" * 80)
    print("\nInitializing services...")

    try:
        # Preload services
        Services.get_extractor()
        print("✓ Feature extractor initialized")

        Services.get_predictor()
        print("✓ Predictor initialized")

        print("\n" + "=" * 80)
        print("API is ready!")
        print("=" * 80)
        print("\nEndpoints:")
        print("  - POST http://localhost:8000/estimate")
        print("  - GET  http://localhost:8000/health")
        print("  - GET  http://localhost:8000/docs (Swagger UI)")
        print("\n" + "=" * 80 + "\n")

    except Exception as e:
        print(f"\n❌ Error initializing services: {e}")
        print("\nPlease ensure:")
        print(
            "  1. Model file exists at models/production/plumbing_model_v1.0.0.joblib"
        )
        print("  2. OPENAI_API_KEY is set in .env file")
        print("  3. All dependencies are installed (pip install -r requirements.txt)")
        raise


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
