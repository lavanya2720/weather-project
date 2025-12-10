import json
import os
from datetime import datetime

def save_json(data, city):
    """Save weather data to a local JSON file."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"../data/{city}_{timestamp}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    return filename
