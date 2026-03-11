from pydantic import BaseModel, Field
from typing import Optional

class UserProfile(BaseModel):
    age: int = 30
    salary: float = 80000.0
    monthly_contribution: float = 5000.0
    risk_preference: str = "moderate"
    years_of_service: int = 5
    government_employee: bool = False
    retirement_age: int = 60
    expected_return: float = 0.10
    volatility: float = 0.15

class QueryRequest(BaseModel):
    query: str = Field(..., description="The question or intent query to send to the AI")
    user_profile: Optional[UserProfile] = None
