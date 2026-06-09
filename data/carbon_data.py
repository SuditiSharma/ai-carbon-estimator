# Carbon intensity by country (kg CO2 per kWh)
# Source: Our World in Data / Ember Climate 2023
CARBON_INTENSITY = {
    "Ireland": 0.295,
    "India": 0.708,
    "UK": 0.233,
    "USA": 0.386,
    "Germany": 0.385,
    "France": 0.085,
    "China": 0.681,
    "Australia": 0.656,
    "Canada": 0.150,
    "Other": 0.450
}

# Energy consumption per hardware type per hour (kWh)
# Source: Machine Learning CO2 Impact research (Strubell et al.)
HARDWARE_ENERGY = {
    "CPU": 0.120,
    "GPU": 0.300,
    "TPU": 0.200,
    "Multi-GPU": 0.900
}

# Model type complexity multiplier
# More complex models = more compute needed
MODEL_COMPLEXITY = {
    "Linear Regression": 0.5,
    "Random Forest": 1.0,
    "Neural Network": 2.5,
    "Large Language Model": 8.0,
    "Computer Vision Model": 3.0
}