import json
from database import session
from models import Dataset, Chart, Dashboard  # Import your SQLAlchemy models


def export_objects():
    # Query all objects from the database, including only those without 'WIP' in their name
    datasets = session.query(Dataset).filter(~Dataset.name.ilike('%WIP%')).all()
    charts = session.query(Chart).filter(~Chart.name.ilike('%WIP%')).all()
    dashboards = session.query(Dashboard).filter(~Dashboard.name.ilike('%WIP%')).all()

    # Convert objects to dictionaries and export to JSON files
    with open('exported_assets/datasets.json', 'w') as f:
        json.dump([dataset.to_dict() for dataset in datasets], f)

    with open('exported_assets/charts.json', 'w') as f:
        json.dump([chart.to_dict() for chart in charts], f)

    with open('exported_assets/dashboards.json', 'w') as f:
        json.dump([dashboard.to_dict() for dashboard in dashboards], f)

if __name__ == "__main__":
    export_objects()
