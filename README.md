# AI Carbon Footprint Estimator API

A FastAPI-based tool that estimates the carbon footprint of AI and 
High-Performance Computing (HPC) research jobs.

Built as exploratory work ahead of a PhD application to the 
Decarb-AI programme at University of Galway (ICHEC), supervised 
by Dr. Venkatesh Kannan.

## Why I Built This

Several tools already exist for estimating the carbon footprint 
of computational workloads — CodeCarbon, Green Algorithms, 
CarbonTracker. But most of them stop at measurement. 

What they don't do is connect that cost to research outcomes — 
whether the computation actually led to useful findings, policy 
change, or environmental benefit. That linkage is what this 
project starts to explore.

I built this as preliminary work before applying to the Decarb-AI 
PhD programme at University of Galway (ICHEC), supervised by 
Dr. Venkatesh Kannan. The prototype helped me understand the 
problem hands-on — and, more importantly, helped me discover 
where simple estimation breaks down.

One thing I want to explore further is how HPC scheduler logs, 
resource allocation records, and hardware utilisation telemetry 
from real clusters like ICHEC could replace the estimated 
multipliers I used here. That's a more honest and accurate 
approach than lookup tables.

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

## Design Decisions

**Why use national averages instead of live grid data?**
Live carbon intensity APIs (like Electricity Maps) require 
commercial subscriptions and many HPC clusters do not expose 
real-time grid information. This prototype prioritises 
transparency and reproducibility over precision. A production 
version would pull live data.

**Why no trained ML model?**
Unlike my Climate Risk and Fraud Detection APIs, this project 
does not use a trained model — it uses documented calculations 
from published research. This is intentional. The goal is 
transparency: every number is traceable to a source. A black-box 
model would undermine the accountability purpose of the tool.

**Why three carbon labels instead of a continuous score?**
Continuous scores (e.g. "this job is in the 67th percentile") 
require a reference distribution of real HPC jobs — which I 
don't have. Labels are a defensible starting point that 
communicate meaning clearly to non-technical stakeholders, 
which is central to the research governance problem this 
project addresses.

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

## Future Research Questions

These are the questions this prototype cannot answer but the 
PhD would address:

1. How do carbon costs vary within a single country by time 
   of day and energy mix?
2. Can real ICHEC job telemetry data replace these estimated 
   multipliers?
3. Is there a meaningful relationship between carbon cost and 
   research output quality?
4. How should research funders weight computational efficiency 
   against research ambition?
5. What governance frameworks would make researchers accountable 
   for their computational footprint?

## What I Got Wrong

### My complexity multipliers were significantly off

Before running any experiments, I assigned complexity multipliers
based on general intuition and published estimates:

| Model | My estimate | Measured reality |
|---|---|---|
| Linear Regression | 0.5x | 1.0x (baseline) |
| Random Forest | 1.0x | 143.6x |
| Neural Network | 2.5x | 127.0x |

I assumed Neural Networks would be the most expensive and Random
Forests somewhere in the middle. The experiment showed the opposite —
Random Forest and Neural Network were comparable in runtime, and both
were roughly 130x more expensive than Linear Regression, not 2-5x.

This matters because my carbon estimates for Random Forest jobs are
currently around 130x too low.

### Why the gap exists

Random Forests train hundreds of decision trees in parallel —
on a 10,000 sample dataset with 100 trees, that's a lot of work.
Linear Regression is a single matrix operation. The difference is
much larger than I expected on real data.

The Neural Network also threw a ConvergenceWarning — it did not
fully converge in 50 iterations, meaning it stopped early. A fully
trained neural network would likely take even longer.

### What this means for the research

Single lookup-table multipliers are too blunt an instrument.
The actual compute cost depends heavily on:
- Dataset size (I only tested 10,000 samples)
- Number of trees / layers / parameters
- Whether the model converged

A more honest estimator would ask for these details rather than
assuming a single number per model type. This is exactly the kind
of finding that motivates more rigorous research — which is what
the Decarb-AI PhD is designed to do.

### What I would do differently

Rather than hardcoded multipliers, a better approach would derive
compute estimates from model parameters directly — number of trees,
hidden layer sizes, training iterations — and validate against real
measured job data from ICHEC. That is a core part of what this PhD
proposes to build.

## Author

Suditi Sharma
MSc Advanced Computer Science with Data Science — University of Strathclyde
github.com/SuditiSharma