import json
from database import session
from models import Dataset, Chart, Dashboard  # Import your SQLAlchemy models


def import_objects(file_path, model_class):
    with open(file_path, 'r') as f:
        data = json.load(f)
        for item in data:
            # Import objects only if their names do not contain 'WIP'
            if 'WIP' in item.get('name', ''):
                continue

            # Assuming the `id` field determines whether to update or insert
            existing_item = session.query(model_class).filter_by(id=item['id']).first()
            if existing_item:
                # Update existing record
                for key, value in item.items():
                    setattr(existing_item, key, value)
            else:
                # Create new record
                new_item = model_class(**item)
                session.add(new_item)
        session.commit()

def import_assets():
    import_objects('exported_assets/datasets.json', Dataset)
    import_objects('exported_assets/charts.json', Chart)
    import_objects('exported_assets/dashboards.json', Dashboard)

if __name__ == "__main__":
    import_assets()
