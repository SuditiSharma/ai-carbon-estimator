import time
import psutil
import os
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier

# =========================================================
# Real experiment: measure CPU usage and runtime of
# different ML models on the same dataset
# Goal: compare actual compute to our estimated multipliers
# =========================================================

def measure_job(name, model, X, y):
    process = psutil.Process(os.getpid())
    
    # CPU and memory before
    cpu_before = process.cpu_percent(interval=0.1)
    mem_before = process.memory_info().rss / 1024 / 1024  # MB
    
    # Time the training
    start = time.time()
    model.fit(X, y)
    duration = time.time() - start
    
    # CPU and memory after
    cpu_after = psutil.cpu_percent(interval=0.5)
    mem_after = process.memory_info().rss / 1024 / 1024  # MB
    
    print(f"\n{'='*50}")
    print(f"Model: {name}")
    print(f"Training time: {duration:.3f} seconds")
    print(f"CPU usage: {cpu_after:.1f}%")
    print(f"Memory used: {mem_after - mem_before:.1f} MB")
    print(f"Relative time vs Linear Regression: will calculate after")
    
    return duration, cpu_after, mem_after - mem_before

# Generate synthetic dataset
# 10,000 samples, 20 features
print("Generating dataset...")
np.random.seed(42)
X = np.random.rand(10000, 20)
y = (X[:, 0] + X[:, 1] > 1).astype(int)

results = {}

# Run each model
print("\nRunning experiments...")

duration, cpu, mem = measure_job(
    "Linear Regression",
    LinearRegression(),
    X, y
)
results["Linear Regression"] = duration

duration, cpu, mem = measure_job(
    "Random Forest (100 trees)",
    RandomForestClassifier(n_estimators=100, random_state=42),
    X, y
)
results["Random Forest"] = duration

duration, cpu, mem = measure_job(
    "Neural Network (2 hidden layers)",
    MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=50, random_state=42),
    X, y
)
results["Neural Network"] = duration

# Calculate relative multipliers
print(f"\n{'='*50}")
print("RESULTS — Relative compute multipliers")
print(f"{'='*50}")
baseline = results["Linear Regression"]
for name, duration in results.items():
    multiplier = duration / baseline
    print(f"{name}: {duration:.3f}s — {multiplier:.1f}x baseline")

print(f"\nOur estimated multipliers were:")
print(f"Linear Regression: 0.5x")
print(f"Random Forest: 1.0x")
print(f"Neural Network: 2.5x")
print(f"\nHow close were we?")