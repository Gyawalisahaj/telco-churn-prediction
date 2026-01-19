from pydantic import BaseModel, Field, validator
from typing import Optional


class CustomerData(BaseModel):
    """Pydantic model for customer prediction data validation"""
    name: str = Field(..., min_length=1, description="Customer name")
    gender: str = Field(..., description="Male or Female")
    age: int = Field(..., ge=18, le=100, description="Customer age")
    num_dependents: int = Field(default=0, ge=0, le=10, description="Number of dependents")
    estimated_salary: float = Field(..., ge=0, description="Estimated salary in NPR")
    calls_made: int = Field(default=0, ge=0, description="Monthly calls made")
    sms_sent: int = Field(default=0, ge=0, description="Monthly SMS sent")
    data_used: float = Field(default=0, ge=0, description="Monthly data used in MB")
    tenure_months: int = Field(..., ge=0, le=72, description="Customer tenure in months")
    province: str = Field(..., description="Province from list of Nepal provinces")
    provider: str = Field(..., description="Telecom provider")
    
    @validator('gender')
    def validate_gender(cls, v):
        if v.upper() not in ['MALE', 'FEMALE', 'M', 'F']:
            raise ValueError('Gender must be Male, Female, M, or F')
        return v.upper()
    
    @validator('province')
    def validate_province(cls, v):
        valid_provinces = [
            "Bagmati", "Gandaki", "Karnali", "Koshi", 
            "Lumbini", "Madhesh", "Sudurpashchim"
        ]
        if v not in valid_provinces:
            raise ValueError(f'Province must be one of {valid_provinces}')
        return v
    
    @validator('provider')
    def validate_provider(cls, v):
        valid_providers = ["Ncell", "Nepal Telecom"]
        if v not in valid_providers:
            raise ValueError(f'Provider must be one of {valid_providers}')
        return v


class PredictionResponse(BaseModel):
    """Response model for predictions"""
    customer_name: str
    churn_prediction: str
    churn_probability: float
    risk_level: str
    recommendations: list = []
    
    
class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    model_loaded: bool
    version: str = "1.0.0"