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
## Problems I Encountered

**1. No dataset exists for this problem**
Unlike my previous projects (Fraud Detection, Climate Risk), there 
is no Kaggle dataset for AI carbon footprints. I had to build the 
lookup table manually from published research — Strubell et al. 
(2019) for hardware energy values and Ember Climate for national 
carbon intensity figures. Deciding which sources to trust and how 
to represent them was harder than I expected.

**2. Defining meaningful thresholds**
What makes a job "High" carbon vs "Medium"? There is no agreed 
standard. I chose 1.0 kg and 10.0 kg as thresholds based on 
published estimates of typical ML training runs, but these are 
judgment calls. A more rigorous version would derive thresholds 
from a real distribution of HPC job data.

**3. Confidence was misleading at first**
My first version returned "High" confidence for every result 
regardless of input. That was dishonest — if a country isn't in 
my dataset I'm using a global average, which is much less reliable. 
I redesigned the confidence scoring to reflect actual data quality.

**4. Model complexity multipliers are estimated**
Mapping model types to complexity values (e.g. LLM = 8x, Neural 
Network = 2.5x) required reading multiple papers and making 
reasonable assumptions. These values are documented in 
carbon_data.py with comments explaining the reasoning. A future 
version would derive these empirically from real job telemetry.

**5. National averages hide real variation**
Carbon intensity varies by time of day and energy mix — a grid 
running on wind at 2am is very different from the same grid at 
peak demand. This prototype uses annual national averages because 
live carbon intensity APIs require commercial subscriptions. This 
is a known limitation, not an oversight.

## Author

Suditi Sharma
MSc Advanced Computer Science with Data Science — University of Strathclyde
github.com/SuditiSharma