from pydantic import BaseModel, Field

class CollegeOnboardingRequest(BaseModel):
    name: str = Field(..., min_length=5, max_length=100)
    email_suffix: str = Field(..., min_length=3, max_length=100)
    description: str = Field(..., min_length=5, max_length=1000)
    
class CollegeOnboardingResponse(BaseModel):
    name: str 
    slug: str
    email_suffix: str
    description: str 