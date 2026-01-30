from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json
import os
from statistics import mean

app = FastAPI()

# ✅ STRONG CORS CONFIG
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],   # IMPORTANT
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "q-vercel-latency.json")

with open(DATA_PATH) as f:
    data = json.load(f)

class RequestBody(BaseModel):
    regions: list[str]
    threshold_ms: int

def p95(values):
    values = sorted(values)
    if not values:
        return 0
    return values[int(0.95 * (len(values) - 1))]

@app.options("/api")
def options_handler():
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": "*",
        },
    )

@app.post("/api")
def analyze_latency(body: RequestBody):
    response = {}

    for region in body.regions:
        rows = [r for r in data if r["region"] == region]
        if not rows:
            continue

        latencies = [r["latency_ms"] for r in rows]
        uptimes = [r["uptime_pct"] for r in rows]

        response[region] = {
            "avg_latency": round(mean(latencies), 2),
            "p95_latency": round(p95(latencies), 2),
            "avg_uptime": round(mean(uptimes), 2),
            "breaches": sum(1 for l in latencies if l > body.threshold_ms),
        }

    return JSONResponse(
        content=response,
        headers={"Access-Control-Allow-Origin": "*"},
    )
