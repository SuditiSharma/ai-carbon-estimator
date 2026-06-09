from data.carbon_data import CARBON_INTENSITY, HARDWARE_ENERGY, MODEL_COMPLEXITY

def calculate_carbon(model_type: str, hardware: str,
                     duration_hours: float, country: str):

    # Step 1 — get values from lookup table
    country_known = country in CARBON_INTENSITY
    intensity = CARBON_INTENSITY.get(country, CARBON_INTENSITY["Other"])
    energy_per_hour = HARDWARE_ENERGY.get(hardware, HARDWARE_ENERGY["CPU"])
    complexity = MODEL_COMPLEXITY.get(model_type, MODEL_COMPLEXITY["Random Forest"])

    # Step 2 — calculate energy (kWh)
    energy_kwh = energy_per_hour * complexity * duration_hours

    # Step 3 — calculate carbon (kg CO2)
    carbon_kg = energy_kwh * intensity

    # Step 4 — confidence based on data quality
    # Not everything is equally certain
    if not country_known:
        confidence = "Low"
        confidence_reason = "Country not in dataset — using global average"
    elif duration_hours > 24:
        confidence = "Medium"
        confidence_reason = "Long jobs may have variable energy draw"
    elif hardware == "Multi-GPU":
        confidence = "Medium"
        confidence_reason = "Multi-GPU configurations vary widely"
    else:
        confidence = "High"
        confidence_reason = "Known hardware and country values used"

    # Step 5 — carbon equivalencies
    # 1 kg CO2 = ~4 km driven (average car emits ~0.251 kg CO2/km)
    equivalent_km_driven = round(carbon_kg / 0.251, 1)

    # 1 phone charge = ~0.00822 kg CO2
    equivalent_phone_charges = int(carbon_kg / 0.00822)

    # Step 6 — label
    if carbon_kg < 1.0:
        label = "Low"
        message = f"✅ LOW CARBON — {carbon_kg:.4f} kg CO₂. Computationally efficient."
    elif carbon_kg < 10.0:
        label = "Medium"
        message = f"⚠️ MEDIUM CARBON — {carbon_kg:.4f} kg CO₂. Consider optimising."
    else:
        label = "High"
        message = f"🔴 HIGH CARBON — {carbon_kg:.4f} kg CO₂. Significant environmental cost."

    return (energy_kwh, carbon_kg, label, confidence,
            confidence_reason, equivalent_km_driven,
            equivalent_phone_charges, message)