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
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from services.feature_extractor import FeatureExtractor
from predict import PlumbingPredictor

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="Plumbing Cost Estimator API",
    description="Get cost and time estimates for plumbing jobs using natural language descriptions",
    version="1.0.0"
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
        example="I need a luxury bathroom with a wall-hung toilet, luxury shower, and a pedestal sink"
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
                    "showerCabinType": "Luxury_Enclosure"
                }
            }
        }


class ErrorResponse(BaseModel):
    """Error response model."""
    success: bool = False
    error: str = Field(description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")


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
            "GET /redoc": "API documentation (ReDoc)"
        }
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
            "services": {
                "feature_extractor": "ready",
                "predictor": "ready"
            }
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e)
        }


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
        cost_dzd = prediction['cost']
        cost_gbp = dzd_to_gbp(cost_dzd)
        time_days = prediction['time']

        # Return response
        return EstimateResponse(
            success=True,
            job_description=request.job_description,
            cost_dzd=round(cost_dzd, 2),
            cost_gbp=round(cost_gbp, 2),
            time_days=round(time_days, 1),
            features=features
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "success": False,
                "error": "Invalid input",
                "detail": str(e)
            }
        )
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": "Model not found",
                "detail": str(e)
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": "Estimation failed",
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
        print("  1. Model file exists at models/production/plumbing_model_v1.0.0.joblib")
        print("  2. OPENAI_API_KEY is set in .env file")
        print("  3. All dependencies are installed (pip install -r requirements.txt)")
        raise


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
