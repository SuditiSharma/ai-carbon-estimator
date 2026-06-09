# AI Carbon Footprint Estimator API

A FastAPI-based tool that estimates the carbon footprint of AI and 
High-Performance Computing (HPC) research jobs.

Built as exploratory work ahead of a PhD application to the 
Decarb-AI programme at University of Galway (ICHEC), supervised 
by Dr. Venkatesh Kannan.

## Why I Built This

One of the core challenges in sustainable AI research is that nobody 
currently has a reliable way to connect computational resource usage 
to environmental cost. A researcher running a Large Language Model 
on a GPU cluster for 10 hours in India produces roughly 51 kg of CO₂ 
— equivalent to driving 200 km. Yet this cost is invisible to funders 
and institutions.

This API is a first-pass prototype exploring that question: can we 
make the carbon cost of AI research transparent and queryable?

## What It Does

Send a description of any AI or HPC job and get back:
- Estimated energy consumed (kWh)
- Estimated CO₂ produced (kg)
- Carbon label: Low / Medium / High
- A plain-English message explaining the result

## Example

**High carbon job:**
```json
{
  "model_type": "Large Language Model",
  "hardware": "Multi-GPU",
  "duration_hours": 10,
  "country": "India"
}
```
Returns: 🔴 HIGH CARBON — 50.976 kg CO₂

**Low carbon job:**
```json
{
  "model_type": "Linear Regression",
  "hardware": "CPU",
  "duration_hours": 1,
  "country": "France"
}
```
Returns: ✅ LOW CARBON — 0.005 kg CO₂

## Tech Stack

- Python 3.11
- FastAPI
- Uvicorn
- Carbon intensity data: Our World in Data / Ember Climate 2023
- Hardware energy data: Strubell et al. (2019)

## Run Locally
git clone https://github.com/SuditiSharma/ai-carbon-estimator.git
cd ai-carbon-estimator
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

uvicorn app.main:app --reload
Then open: http://127.0.0.1:8000/docs

## Limitations and Next Steps

- Carbon intensity values are national averages — real values vary 
  by time of day and energy mix
- Hardware energy values are estimates from published research
- A more sophisticated version would pull live grid carbon data
- Future work would integrate real ICHEC job telemetry data

## Author

Suditi Sharma
MSc Advanced Computer Science with Data Science — University of Strathclyde
github.com/SuditiSharma