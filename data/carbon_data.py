# =============================================================
# CARBON INTENSITY BY COUNTRY (kg CO2 per kWh)
# Source: Ember Climate / Our World in Data (2023)
# https://ourworldindata.org/grapher/carbon-intensity-electricity
# =============================================================
CARBON_INTENSITY = {
    "Ireland": 0.295,    # Ember Climate 2023
    "India": 0.708,      # Ember Climate 2023 — coal-heavy grid
    "UK": 0.233,         # Ember Climate 2023
    "USA": 0.386,        # Ember Climate 2023 — varies by state
    "Germany": 0.385,    # Ember Climate 2023
    "France": 0.085,     # Ember Climate 2023 — ~70% nuclear
    "China": 0.681,      # Ember Climate 2023 — coal-heavy grid
    "Australia": 0.656,  # Ember Climate 2023
    "Canada": 0.150,     # Ember Climate 2023 — hydro-heavy grid
    "Other": 0.450       # Global average — used when country unknown
}

# =============================================================
# ENERGY CONSUMPTION PER HARDWARE TYPE PER HOUR (kWh)
# Source: Strubell et al. (2019) "Energy and Policy Considerations
# for Deep Learning in NLP" — https://arxiv.org/abs/1906.02629
# and Patterson et al. (2021) "Carbon Emissions and Large
# Neural Network Training"
# =============================================================
HARDWARE_ENERGY = {
    "CPU": 0.120,       # Typical server CPU — Strubell et al.
    "GPU": 0.300,       # NVIDIA V100 — Strubell et al.
    "TPU": 0.200,       # Google TPU v3 — Patterson et al.
    "Multi-GPU": 0.900  # 3x GPU estimate — assumed linear scaling
}

# =============================================================
# MODEL COMPLEXITY MULTIPLIER
# Baseline: Random Forest = 1.0
# Values estimated from relative compute requirements
# reported across Strubell et al. (2019), Patterson et al.
# (2021), and Lannelongue et al. (2021) "Green Algorithms"
# https://arxiv.org/abs/2007.07610
# =============================================================
MODEL_COMPLEXITY = {
    "Linear Regression": 0.5,        # Very low compute — single pass
    "Random Forest": 1.0,            # Baseline
    "Neural Network": 2.5,           # Estimated from typical MLP training
    "Large Language Model": 8.0,     # Based on GPT-scale training estimates
    "Computer Vision Model": 3.0     # Based on ResNet/VGG training estimates
}