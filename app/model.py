from data.carbon_data import CARBON_INTENSITY, HARDWARE_ENERGY, MODEL_COMPLEXITY

def calculate_carbon(model_type: str, hardware: str, 
                     duration_hours: float, country: str):
    
    # Step 1 — get values from lookup table
    # If country not found, use "Other"
    intensity = CARBON_INTENSITY.get(country, CARBON_INTENSITY["Other"])
    
    # If hardware not found, use CPU
    energy_per_hour = HARDWARE_ENERGY.get(hardware, HARDWARE_ENERGY["CPU"])
    
    # If model not found, use Random Forest complexity
    complexity = MODEL_COMPLEXITY.get(model_type, MODEL_COMPLEXITY["Random Forest"])
    
    # Step 2 — calculate energy used (kWh)
    # Energy = hardware energy × complexity multiplier × hours run
    energy_kwh = energy_per_hour * complexity * duration_hours
    
    # Step 3 — calculate carbon produced (kg CO2)
    # Carbon = energy × how dirty the country's electricity is
    carbon_kg = energy_kwh * intensity
    
    # Step 4 — assign a label
    # These thresholds are based on research literature
    if carbon_kg < 1.0:
        label = "Low"
        confidence = "High"
        message = f"✅ LOW CARBON — This job produced {carbon_kg:.3f} kg CO₂. Computationally efficient."
    elif carbon_kg < 10.0:
        label = "Medium"
        confidence = "High"
        message = f"⚠️ MEDIUM CARBON — This job produced {carbon_kg:.3f} kg CO₂. Consider optimising."
    else:
        label = "High"
        confidence = "High"
        message = f"🔴 HIGH CARBON — This job produced {carbon_kg:.3f} kg CO₂. Significant environmental cost."
    
    return energy_kwh, carbon_kg, label, confidence, message