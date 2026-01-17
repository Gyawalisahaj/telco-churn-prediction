from pydantic import BaseModel


class CustomerData(BaseModel):
    name: str
    gender: str
    age: int
    num_dependents: int
    estimated_salary: float
    calls_made: int
    sms_sent: int
    data_used: float
    tenure_months: int
    province: str
    provider: str