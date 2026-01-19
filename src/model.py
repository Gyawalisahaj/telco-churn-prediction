"""
FastAPI Backend for Nepal Telco Churn Prediction
Production-ready API with comprehensive error handling and logging
"""

import logging
import sys
from pathlib import Path
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

try:
    # Try absolute imports (for local/Docker)
    from src.predmodel import CustomerData, PredictionResponse, HealthResponse
    from src.model_service import ChurnModelService
except ImportError:
    try:
        # Try relative imports
        from predmodel import CustomerData, PredictionResponse, HealthResponse
        from model_service import ChurnModelService
    except ImportError:
        # Add current directory to path and try again
        sys.path.insert(0, str(Path(__file__).parent))
        from predmodel import CustomerData, PredictionResponse, HealthResponse
        from model_service import ChurnModelService

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize model service
model_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    global model_service
    # Startup
    logger.info("🚀 Starting Nepal Telco Churn Prediction API...")
    model_service = ChurnModelService()
    logger.info("✅ Model service initialized")
    yield
    # Shutdown
    logger.info("🛑 Shutting down API...")

# Initialize FastAPI with lifespan
app = FastAPI(
    title="Nepal Telco Churn Prediction API",
    description="Advanced Deep Learning API for customer churn prediction in Nepalese Telecom sector",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware for cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc), "type": "validation_error"}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"❌ Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "type": "server_error"}
    )


# ==================== API Endpoints ====================

@app.get("/", response_model=HealthResponse, tags=["Health"])
def read_root():
    """Root endpoint - health check"""
    return HealthResponse(
        status="healthy",
        model_loaded=model_service.model_loaded if model_service else False
    )

@app.get("/health", response_model=HealthResponse, tags=["Health"])
def health_check():
    """Detailed health check endpoint"""
    if not model_service:
        raise HTTPException(status_code=503, detail="Model service not initialized")
    
    return HealthResponse(
        status="healthy" if model_service.model_loaded else "degraded",
        model_loaded=model_service.model_loaded
    )

@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
def predict_churn(data: CustomerData):
    """
    Predict customer churn probability
    
    ### Parameters:
    - **name**: Customer name
    - **gender**: Male or Female
    - **age**: Age (18-100)
    - **num_dependents**: Number of dependents (0-10)
    - **estimated_salary**: Estimated salary in NPR
    - **calls_made**: Monthly calls
    - **sms_sent**: Monthly SMS
    - **data_used**: Monthly data in MB
    - **tenure_months**: Customer tenure (0-72 months)
    - **province**: Nepal province
    - **provider**: Ncell or Nepal Telecom
    
    ### Response:
    - **churn_prediction**: CHURN or RETAIN
    - **churn_probability**: Probability as percentage (0-100)
    - **risk_level**: LOW, MEDIUM, or HIGH
    - **recommendations**: List of actionable recommendations
    """
    
    if not model_service or not model_service.model_loaded:
        logger.warning("⚠️ Prediction attempted with model not loaded")
        raise HTTPException(
            status_code=503,
            detail="Model not available. Please check server status."
        )
    
    try:
        # Convert Pydantic model to dictionary
        customer_dict = data.dict()
        
        # Get prediction from model service
        result = model_service.predict(customer_dict)
        
        if not result.get("success"):
            logger.error(f"Prediction failed: {result.get('error')}")
            raise HTTPException(
                status_code=500,
                detail=result.get("error", "Prediction failed")
            )
        
        logger.info(
            f"✅ Prediction successful for {data.name}: "
            f"{result['churn_prediction']} ({result['churn_probability']}%)"
        )
        
        return PredictionResponse(**result)
        
    except ValueError as e:
        logger.warning(f"⚠️ Validation error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"❌ Unexpected error during prediction: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/batch-predict", tags=["Prediction"])
def batch_predict(customers: list[CustomerData]):
    """
    Predict churn for multiple customers at once
    
    ### Parameters:
    - **customers**: List of customer data objects
    
    ### Response:
    - List of predictions for each customer
    """
    
    if not model_service or not model_service.model_loaded:
        raise HTTPException(
            status_code=503,
            detail="Model not available"
        )
    
    try:
        results = []
        for customer in customers:
            customer_dict = customer.dict()
            result = model_service.predict(customer_dict)
            if result.get("success"):
                results.append(PredictionResponse(**result))
            else:
                results.append({
                    "customer_name": customer.name,
                    "churn_prediction": "ERROR",
                    "churn_probability": 0,
                    "risk_level": "UNKNOWN",
                    "error": result.get("error")
                })
        
        logger.info(f"✅ Batch prediction successful for {len(customers)} customers")
        return {"total": len(customers), "predictions": results}
        
    except Exception as e:
        logger.error(f"❌ Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail="Batch prediction failed")


@app.get("/info", tags=["Info"])
def get_info():
    """Get API and model information"""
    return {
        "api_name": "Nepal Telco Churn Prediction API",
        "version": "1.0.0",
        "model_loaded": model_service.model_loaded if model_service else False,
        "features": {
            "single_prediction": True,
            "batch_prediction": True,
            "health_check": True
        },
        "provinces": [
            "Bagmati", "Gandaki", "Karnali", "Koshi",
            "Lumbini", "Madhesh", "Sudurpashchim"
        ],
        "providers": ["Ncell", "Nepal Telecom"]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)