import os
import yaml
from datetime import datetime, timezone
from superset import app, db
from superset.commands.chart.export import ExportChartsCommand
from superset.commands.dashboard.export import ExportDashboardsCommand
from superset.commands.dataset.export import ExportDatasetsCommand
from superset.utils.dict_import_export import EXPORT_VERSION

# Define the output directory
output_dir = "extracted_data"
os.makedirs(output_dir, exist_ok=True)

# Helper function to save data to files
def save_to_file(file_name: str, content: str):
    file_path = os.path.join(output_dir, file_name)
    with open(file_path, 'w') as file:
        file.write(content)
    print(f"Saved {file_name} to {file_path}")

def export_assets():
    # Initialize Superset app context
    app.app_context().push()

    # Metadata
    metadata = {
        "version": EXPORT_VERSION,
        "type": "assets",
        "timestamp": datetime.now(tz=timezone.utc).isoformat(),
    }
    save_to_file("metadata.yaml", yaml.safe_dump(metadata, sort_keys=False))

    # Export datasets
    dataset_command = ExportDatasetsCommand
    dataset_ids = [model.id for model in dataset_command.dao.find_all()]
    for file_name, file_content in dataset_command(dataset_ids, export_related=False).run():
        save_to_file(file_name, file_content)

    # Export charts
    chart_command = ExportChartsCommand
    chart_ids = [model.id for model in chart_command.dao.find_all()]
    for file_name, file_content in chart_command(chart_ids, export_related=False).run():
        save_to_file(file_name, file_content)

    # Export dashboards
    dashboard_command = ExportDashboardsCommand
    dashboard_ids = [model.id for model in dashboard_command.dao.find_all()]
    for file_name, file_content in dashboard_command(dashboard_ids, export_related=False).run():
        save_to_file(file_name, file_content)

if __name__ == "__main__":
    export_assets()
