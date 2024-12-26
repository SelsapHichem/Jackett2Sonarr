# config.py
JACKETT_URL = "http://127.0.0.1:9117"
JACKETT_API_KEY = "your_jackett_api_key"

SONARR_URL = "http://127.0.0.1:8989"
SONARR_API_KEY = "your_sonarr_api_key"

SONARR_INDEXER_SETTINGS = {
    "enableRss": True,
    "enableSearch": True,
    "priority": 25
}

# main.py
import requests
from config import JACKETT_URL, JACKETT_API_KEY, SONARR_URL, SONARR_API_KEY, SONARR_INDEXER_SETTINGS

def fetch_jackett_indexers():
    """Fetch the list of indexers from Jackett."""
    response = requests.get(f"{JACKETT_URL}/api/v2.0/indexers", headers={"X-Api-Key": JACKETT_API_KEY})
    response.raise_for_status()
    return response.json()

def add_indexer_to_sonarr(indexer):
    """Add a single indexer to Sonarr."""
    payload = {
        "name": indexer["title"],
        "implementation": "Torznab",
        "configContract": "TorznabSettings",
        "fields": [
            {"name": "baseUrl", "value": f"{JACKETT_URL}/api/v2.0/indexers/{indexer['id']}/results/torznab/"},
            {"name": "apiKey", "value": JACKETT_API_KEY}
        ],
        **SONARR_INDEXER_SETTINGS
    }
    headers = {"X-Api-Key": SONARR_API_KEY}
    response = requests.post(f"{SONARR_URL}/api/v3/indexer", json=payload, headers=headers)
    if response.status_code == 201:
        print(f"Successfully added indexer: {indexer['title']}")
    else:
        print(f"Failed to add indexer: {indexer['title']} - {response.status_code} {response.text}")

def main():
    """Main script to fetch and add indexers."""
    print("Fetching indexers from Jackett...")
    indexers = fetch_jackett_indexers()
    print(f"Found {len(indexers)} indexers. Adding them to Sonarr...")
    for indexer in indexers:
        add_indexer_to_sonarr(indexer)

if __name__ == "__main__":
    main()
