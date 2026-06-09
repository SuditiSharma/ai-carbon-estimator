from pydantic import BaseModel, Field

# What the user sends TO the API
class JobInput(BaseModel):
    model_type: str
    hardware: str
    duration_hours: float = Field(
        gt=0,
        description="Must be greater than 0"
    )
    country: str

# What the API sends BACK
class JobOutput(BaseModel):
    energy_kwh: float
    carbon_kg: float
    carbon_label: str
    confidence: str
    confidence_reason: str
    equivalent_km_driven: float
    equivalent_phone_charges: int
    message: str