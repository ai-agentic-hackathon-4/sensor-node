from pydantic import BaseModel, Field

class PumpRequest(BaseModel):
    volume_ml: float = Field(..., description="Target water volume in milliliters", gt=0)
