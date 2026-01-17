import fastapi as FastApi
from pydantic import BaseModel


class PredModel(BaseModel):
    gender : str	
    age	: int    
    num_dependent	: int
    date_of_registration	: str
    num_dependents	: int
    estimated_salary	: float
    calls_made	: int
    sms_sent	: int
    data_used	: float
    churn	: int
    province	: str
    provider_nepal	: str