from pydantic import BaseModel

# What the user sends TO the API
class JobInput(BaseModel):
    model_type: str        # e.g. "Random Forest"
    hardware: str          # e.g. "GPU"
    duration_hours: float  # e.g. 2.5
    country: str           # e.g. "Ireland"

# What the API sends BACK to the user
class JobOutput(BaseModel):
    energy_kwh: float
    carbon_kg: float
    carbon_label: str
    confidence: str
    message: str