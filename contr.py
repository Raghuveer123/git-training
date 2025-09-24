import json

# Load the raw CJOC JSON file
with open("cjoc_raw.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Filter only ManagedMasters and convert name -> lowercase
controllers = [
    {
        "name": item.get("name", "").lower(),
        "url": item.get("url", "").rstrip("/")
    }
    for item in data.get("items", [])
    if item.get("_class", "").startswith("com.cloudbees.opscenter.server.model.ManagedMaster")
]

# Save to controllers.json
with open("controllers.json", "w", encoding="utf-8") as f:
    json.dump({"controllers": controllers}, f, indent=2)

print(f"Filtered {len(controllers)} ManagedMaster controllers saved to controllers.json (names lowercased).")
