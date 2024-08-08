import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

EXPORT_PATH = 'exported_assets'
CONFIG_FILE = 'config.json'

def load_config(config_file=CONFIG_FILE):
    """Load Superset instances configuration from JSON file."""
    with open(config_file, 'r') as file:
        return json.load(file)

def get_headers(api_token):
    """Return headers for API requests."""
    return {
        'Authorization': f'Bearer {api_token}',
        'Content-Type': 'application/json'
    }

def get_existing_objects(instance_url, api_token, object_type):
    """Fetch existing objects from a Superset instance API."""
    headers = get_headers(api_token)
    try:
        response = requests.get(f'{instance_url}/api/v1/{object_type}/', headers=headers)
        response.raise_for_status()
        data = response.json()
        if isinstance(data, dict) and 'result' in data:
            return data['result']
        else:
            print(f"Unexpected response format for {object_type}: {data}")
            return []
    except requests.RequestException as e:
        print(f"Failed to retrieve {object_type} from {instance_url}: {e}")
        return []

def import_or_update_objects(instance_url, api_token, object_type, objects):
    """Import or update objects in a Superset instance."""
    existing_objects = get_existing_objects(instance_url, api_token, object_type)
    if not isinstance(existing_objects, list):
        print(f"Error: existing_objects for {object_type} is not a list. Skipping.")
        return

    existing_ids = {obj.get('id') for obj in existing_objects if 'id' in obj}

    headers = get_headers(api_token)
    for obj in objects:
        if 'id' in obj and obj['id'] in existing_ids:
            # Update existing object
            response = requests.put(f'{instance_url}/api/v1/{object_type}/{obj["id"]}', headers=headers, json=obj)
            if response.status_code == 200:
                print(f"Successfully updated {object_type} with ID {obj['id']} in {instance_url}.")
            else:
                print(f"Failed to update {object_type} with ID {obj['id']} in {instance_url}: {response.status_code} - {response.text}")
        else:
            # Create new object
            response = requests.post(f'{instance_url}/api/v1/{object_type}/', headers=headers, json=obj)
            if response.status_code == 201:
                print(f"Successfully created {object_type} with ID {response.json().get('id')} in {instance_url}.")
            else:
                print(f"Failed to create {object_type} in {instance_url}: {response.status_code} - {response.text}")

def clean_up_objects(instance_url, api_token, object_type, current_ids):
    """Delete objects in a Superset instance that are not present in the current import."""
    existing_objects = get_existing_objects(instance_url, api_token, object_type)
    if not isinstance(existing_objects, list):
        print(f"Error: existing_objects for {object_type} is not a list. Skipping.")
        return

    headers = get_headers(api_token)
    for obj in existing_objects:
        if obj.get('id') not in current_ids:
            response = requests.delete(f'{instance_url}/api/v1/{object_type}/{obj["id"]}', headers=headers)
            if response.status_code == 204:
                print(f"Successfully deleted {object_type} with ID {obj['id']} in {instance_url}.")
            else:
                print(f"Failed to delete {object_type} with ID {obj['id']} in {instance_url}: {response.status_code} - {response.text}")

def import_assets():
    """Import assets from local files to multiple Superset instances."""
    config = load_config()
    instances = config['superset_instances']

    for instance in instances:
        instance_name = instance.get('name')
        instance_url = instance.get('url')
        api_token = instance.get('api_key')
        
        print(f"\nProcessing instance: {instance_name} ({instance_url})")

        for object_type in ['dataset', 'chart', 'dashboard']:
            file_path = os.path.join(EXPORT_PATH, f'{object_type}s.json')
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    try:
                        objects = json.load(f)
                        # Debugging: Print the type and content of objects
                        print(f"Type of {object_type}s: {type(objects)}")
                        print(f"Content of {object_type}s: {objects}")

                        if isinstance(objects, list):
                            filtered_objects = [obj for obj in objects if isinstance(obj, dict) and 'WIP' not in obj.get('name', '')]
                            current_ids = {obj['id'] for obj in filtered_objects if 'id' in obj}
                            import_or_update_objects(instance_url, api_token, object_type, filtered_objects)
                            clean_up_objects(instance_url, api_token, object_type, current_ids)
                        else:
                            print(f"Error: {object_type}s.json is not a list. Data: {objects}")
                    except json.JSONDecodeError as e:
                        print(f"Failed to read {object_type}s file: {e}")
            else:
                print(f"No {object_type}s file found for import.")

if __name__ == "__main__":
    import_assets()
