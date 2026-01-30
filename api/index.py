from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

# Load telemetry data
df = pd.read_csv("telemetry.csv")

class RequestBody(BaseModel):
    regions: list[str]
    threshold_ms: int

@app.post("/api")
def analyze_latency(body: RequestBody):
    result = []

    for region in body.regions:
        region_df = df[df["region"] == region]

        if len(region_df) == 0:
            continue

        avg_latency = region_df["latency_ms"].mean()
        p95_latency = np.percentile(region_df["latency_ms"], 95)
        avg_uptime = region_df["uptime"].mean()
        breaches = (region_df["latency_ms"] > body.threshold_ms).sum()

        result.append({
            "region": region,
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": int(breaches)
        })

    return result
