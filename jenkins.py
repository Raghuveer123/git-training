import os
import json
import csv
import requests
from requests.auth import HTTPBasicAuth

# Load controller URLs from controllers.json
with open("controllers.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    controllers = data.get("controllers", [])

# Load credentials from environment
username = os.getenv("CLOUDBEES_USERNAME", "your_username")
api_token = os.getenv("CLOUDBEES_API_TOKEN", "your_api_token")

# If your CloudBees setup requires Bearer tokens, set this to True
USE_BEARER = False

# Headers for Bearer mode
headers = {"Content-Type": "application/json"}
if USE_BEARER:
    headers["Authorization"] = f"Bearer {api_token}"

# Collect AD group data
ad_group_data = []

for url in controllers:
    endpoint = f"{url}/groups/api/json?tree=groups[name,description,users,groups]"
    try:
        if USE_BEARER:
            response = requests.get(endpoint, headers=headers, verify=False, timeout=10)
        else:
            response = requests.get(
                endpoint,
                headers=headers,
                auth=HTTPBasicAuth(username, api_token),
                verify=False,
                timeout=10
            )

        if response.status_code == 200:
            groups = response.json().get("groups", [])
            for group in groups:
                ad_group_data.append({
                    "controller": url,
                    "name": group.get("name", ""),
                    "description": group.get("description", ""),
                    "users": ",".join(group.get("users", [])),  # flatten list
                    "nested_groups": ",".join(group.get("groups", []))  # flatten list
                })
        else:
            ad_group_data.append({
                "controller": url,
                "name": "",
                "description": "",
                "users": "",
                "nested_groups": "",
                "error": f"HTTP {response.status_code} - {response.text}"
            })

    except requests.exceptions.RequestException as e:
        ad_group_data.append({
            "controller": url,
            "name": "",
            "description": "",
            "users": "",
            "nested_groups": "",
            "error": str(e)
        })

# Save results to CSV
csv_file = "ad_groups.csv"
fieldnames = ["controller", "name", "description", "users", "nested_groups", "error"]

with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for entry in ad_group_data:
        # Ensure "error" key exists in all rows
        if "error" not in entry:
            entry["error"] = ""
        writer.writerow(entry)

print(f"AD group data collection complete. Results saved in {csv_file}")
