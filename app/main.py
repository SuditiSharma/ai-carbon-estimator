from fastapi import FastAPI
from app.schemas import JobInput, JobOutput
from app.model import calculate_carbon

# Create the API — same as your Climate Risk API
app = FastAPI(
    title="AI Carbon Footprint Estimator",
    description="Estimates the carbon footprint of AI and HPC research jobs",
    version="1.0.0"
)

# Welcome endpoint — same pattern as before
@app.get("/")
def root():
    return {"message": "Welcome to the AI Carbon Footprint Estimator API"}

# Health check — same as before
@app.get("/health")
def health():
    return {"status": "healthy"}

# Options endpoint — tells user what values are valid
@app.get("/options")
def options():
    return {
        "model_types": [
            "Linear Regression",
            "Random Forest", 
            "Neural Network",
            "Large Language Model",
            "Computer Vision Model"
        ],
        "hardware": ["CPU", "GPU", "TPU", "Multi-GPU"],
        "countries": [
            "Ireland", "India", "UK", "USA", 
            "Germany", "France", "China", 
            "Australia", "Canada", "Other"
        ]
    }

# Main prediction endpoint
@app.post("/estimate", response_model=JobOutput)
def estimate_carbon(job: JobInput):
    
    energy_kwh, carbon_kg, label, confidence, message = calculate_carbon(
        model_type=job.model_type,
        hardware=job.hardware,
        duration_hours=job.duration_hours,
        country=job.country
    )
    
    return JobOutput(
        energy_kwh=round(energy_kwh, 4),
        carbon_kg=round(carbon_kg, 4),
        carbon_label=label,
        confidence=confidence,
        message=message
    )