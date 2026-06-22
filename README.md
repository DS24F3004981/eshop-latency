# eShop Latency Monitoring

A Python-based latency monitoring and analysis system for e-commerce services across multiple global regions, built with FastAPI.

## Overview

This project provides a comprehensive latency monitoring solution that:
- Tracks API response times across global regions (APAC, EMEA, AMER)
- Monitors uptime percentages for critical services
- Collects performance metrics for multiple microservices
- Stores historical data in JSON format for analysis
- Provides insights into service performance and regional differences

## Features

- **Multi-Region Monitoring**: Tracks latency in APAC, EMEA, and AMER regions
- **Service Performance**: Monitors multiple services including:
  - Catalog Service
  - Checkout Service
  - Support Service
  - Recommendations Engine
  - Analytics Service
- **Uptime Tracking**: Maintains uptime percentage metrics for each service
- **Historical Data**: Stores performance data with timestamps for trend analysis
- **FastAPI Backend**: Modern async API framework for data serving
- **JSON Data Storage**: Easy-to-analyze JSON format for metrics

## Tech Stack

- **FastAPI**: Python web framework for building APIs
- **Python 3.7+**: Core language
- **JSON**: Data storage format
- **Vercel**: Deployment platform

## Project Structure

```
eshop-latency/
├── api/
│   └── (API endpoints for latency data)
├── q-vercel-latency.json    # Performance metrics dataset
├── requirements.txt         # Python dependencies
├── .github/                 # GitHub configuration
└── README.md               # This file
```

## Data Schema

### Latency Record Format

```json
{
  "region": "apac|emea|amer",
  "service": "catalog|checkout|support|recommendations|analytics",
  "latency_ms": 193.63,
  "uptime_pct": 97.52,
  "timestamp": 20250301
}
```

### Fields

| Field | Type | Description |
|-------|------|-------------|
| region | string | Geographic region: APAC, EMEA, or AMER |
| service | string | Microservice being monitored |
| latency_ms | float | Response time in milliseconds |
| uptime_pct | float | Service uptime percentage |
| timestamp | integer | Date in YYYYMMDD format |

## Sample Data

The repository includes sample data (`q-vercel-latency.json`) with:
- **Time Period**: March 1-12, 2025
- **Regions**: 3 (APAC, EMEA, AMER)
- **Services**: 5 (catalog, checkout, support, recommendations, analytics)
- **Records**: 36 data points for comprehensive analysis

### Regional Performance Summary

**APAC Region**:
- Latency Range: 124-215 ms
- Uptime Range: 97.4-99.2%
- Primary Services: Catalog, Recommendations, Analytics

**EMEA Region**:
- Latency Range: 137-226 ms
- Uptime Range: 97.2-99.1%
- Primary Services: Recommendations, Catalog, Checkout

**AMER Region**:
- Latency Range: 110-207 ms
- Uptime Range: 97.3-99.2%
- Primary Services: Support, Recommendations, Analytics

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone https://github.com/DS24F3004981/eshop-latency.git
cd eshop-latency
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running Locally

Start the FastAPI server:
```bash
uvicorn api.main:app --reload
```

The API will be available at `http://localhost:8000`

### API Documentation

FastAPI automatically generates interactive documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Sample API Endpoints

#### Get all latency records
```bash
curl http://localhost:8000/latency
```

#### Get metrics by region
```bash
curl http://localhost:8000/latency?region=apac
```

#### Get metrics by service
```bash
curl http://localhost:8000/latency?service=catalog
```

#### Get metrics by timestamp
```bash
curl http://localhost:8000/latency?timestamp=20250301
```

## Data Analysis

### Calculate Average Latency by Region

```python
import json

with open('q-vercel-latency.json') as f:
    data = json.load(f)

regions = {}
for record in data:
    region = record['region']
    if region not in regions:
        regions[region] = []
    regions[region].append(record['latency_ms'])

for region, latencies in regions.items():
    avg = sum(latencies) / len(latencies)
    print(f"{region}: {avg:.2f} ms")
```

### Identify Service Performance Issues

```python
import json

with open('q-vercel-latency.json') as f:
    data = json.load(f)

# Services with latency > 200ms
slow_services = [r for r in data if r['latency_ms'] > 200]
print(f"Slow service records: {len(slow_services)}")
for record in slow_services:
    print(f"  {record['service']} in {record['region']}: {record['latency_ms']}ms")
```

### Regional Comparison

```python
import json

with open('q-vercel-latency.json') as f:
    data = json.load(f)

# Average uptime by region
regions_uptime = {}
for record in data:
    region = record['region']
    if region not in regions_uptime:
        regions_uptime[region] = []
    regions_uptime[region].append(record['uptime_pct'])

for region, uptimes in regions_uptime.items():
    avg = sum(uptimes) / len(uptimes)
    print(f"{region} Average Uptime: {avg:.3f}%")
```

## Key Insights

1. **Latency Distribution**:
   - Lowest latency: Americas region with recommendations service (110.33 ms)
   - Highest latency: EMEA region with catalog service (226.26 ms)
   - Average across all: ~170 ms

2. **Uptime Performance**:
   - Most services maintain 97-99% uptime
   - Support services generally have higher uptime
   - All services above 97% SLA threshold

3. **Regional Patterns**:
   - AMER consistently shows best performance
   - APAC has good balance between latency and uptime
   - EMEA shows highest latency but acceptable uptime

## Deployment

### Deploy to Vercel

1. Install Vercel CLI:
```bash
npm i -g vercel
```

2. Deploy:
```bash
vercel
```

3. Configuration will use any existing `vercel.json`

## Data Management

### Adding New Records

```python
import json
from datetime import datetime

new_record = {
    "region": "apac",
    "service": "catalog",
    "latency_ms": 195.5,
    "uptime_pct": 98.2,
    "timestamp": int(datetime.now().strftime("%Y%m%d"))
}

with open('q-vercel-latency.json', 'r') as f:
    data = json.load(f)

data.append(new_record)

with open('q-vercel-latency.json', 'w') as f:
    json.dump(data, f, indent=2)
```

### Archiving Old Data

```bash
# Archive data older than 90 days
cp q-vercel-latency.json q-vercel-latency-$(date +%Y%m%d).json
```

## Monitoring & Alerts

### Set Performance Thresholds

- **Critical**: Latency > 300ms or Uptime < 95%
- **Warning**: Latency > 250ms or Uptime < 97%
- **Healthy**: Latency < 200ms and Uptime > 99%

### Create Alerts

```python
def check_performance(record):
    alerts = []
    
    if record['latency_ms'] > 300:
        alerts.append(f"CRITICAL: {record['service']} latency {record['latency_ms']}ms")
    elif record['latency_ms'] > 250:
        alerts.append(f"WARNING: {record['service']} latency {record['latency_ms']}ms")
    
    if record['uptime_pct'] < 95:
        alerts.append(f"CRITICAL: {record['service']} uptime {record['uptime_pct']}%")
    elif record['uptime_pct'] < 97:
        alerts.append(f"WARNING: {record['service']} uptime {record['uptime_pct']}%")
    
    return alerts
```

## Best Practices

1. **Data Collection**: Implement automated metric collection from your services
2. **Regular Archiving**: Archive data older than 6 months
3. **Alerts**: Set up monitoring alerts for threshold violations
4. **Backup**: Maintain backups of historical data
5. **Analysis**: Perform regular trend analysis to identify patterns

## Contributing

To contribute improvements:

1. Add new latency records following the schema
2. Implement new API endpoints for analysis
3. Enhance data visualization capabilities
4. Improve monitoring and alerting features

## License

This project is open source and available under the MIT License.

## Author

Created by DS24F3004981

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Vercel Documentation](https://vercel.com/docs)
- [JSON Schema Validator](https://jsonschema.net/)
