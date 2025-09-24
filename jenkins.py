import requests
import json

# Load controller URLs from controllers.json
with open("controllers.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    controllers = data.get("controllers", [])

# Load API token from environment variable
api_token = os.getenv("CLOUDBEES_API_TOKEN", "your_personal_access_token")

# Headers for REST API requests
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/json"
}

# Collect AD group data
ad_group_data = []

for url in controllers:
    endpoint = f"{url}/groups/api/json?tree=groups[name,description,users,groups]"
    try:
        response = requests.get(endpoint, headers=headers, verify=False, timeout=10)
        if response.status_code == 200:
            groups = response.json().get("groups", [])
            for group in groups:
                ad_group_data.append({
                    "controller": url,
                    "name": group.get("name", ""),
                    "description": group.get("description", ""),
                    "users": group.get("users", []),
                    "nested_groups": group.get("groups", [])
                })
        else:
            ad_group_data.append({"controller": url, "error": f"HTTP {response.status_code}"})
    except requests.exceptions.RequestException as e:
        ad_group_data.append({"controller": url, "error": str(e)})

# Print the collected AD group data
for entry in ad_group_data:
    print(entry)

print("AD group data collection complete.")
