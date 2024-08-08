import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Use environment variables for Superset A
SUP_SECRET_API_URL_A = os.getenv('SUP_SECRET_API_URL_A')
SUP_SECRET_API_TOKEN_A = os.getenv('SUP_SECRET_API_TOKEN_A')
EXPORT_PATH = 'exported_assets'

headers = {
    'Authorization': f'Bearer {SUP_SECRET_API_TOKEN_A}',
    'Content-Type': 'application/json'
}

def fetch_objects(object_type):
    """Fetch objects of a specific type from Superset A."""
    try:
        response = requests.get(f'{SUP_SECRET_API_URL_A}/api/v1/{object_type}/', headers=headers)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and 'result' in data:
            return data['result']
        else:
            print(f"Unexpected response format for {object_type}: {data}")
            return []
    except requests.RequestException as e:
        print(f"Failed to retrieve {object_type}: {e}")
        return []

def export_objects():
    """Export datasets, charts, and dashboards from Superset A."""
    datasets = fetch_objects('dataset')
    charts = fetch_objects('chart')
    dashboards = fetch_objects('dashboard')

    os.makedirs(EXPORT_PATH, exist_ok=True)

    with open(f'{EXPORT_PATH}/datasets.json', 'w') as f:
        json.dump([dataset for dataset in datasets if 'WIP' not in dataset.get('name', '')], f)

    with open(f'{EXPORT_PATH}/charts.json', 'w') as f:
        json.dump([chart for chart in charts if 'WIP' not in chart.get('name', '')], f)

    with open(f'{EXPORT_PATH}/dashboards.json', 'w') as f:
        json.dump([dashboard for dashboard in dashboards if 'WIP' not in dashboard.get('name', '')], f)

if __name__ == "__main__":
    export_objects()
