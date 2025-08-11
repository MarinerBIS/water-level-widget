# GitHub Actions + Python Water Level Scraper
# This script scrapes NB Power's dam safety site and pushes a JSON file to GitHub Pages

import requests
from bs4 import BeautifulSoup
import json
import datetime
import os

URL = "https://www.nbpower.com/en/safety/dam-safety"
DATA_FILE = "data.json"

# Function to extract water level
def get_current_water_level():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')

    # TODO: Update this selector based on the real site structure
    text = soup.get_text()
    match = re.search(r"(\d{2,3}\.\d{1,2}) ?m", text)
    if match:
        return float(match.group(1))
    else:
        raise ValueError("Water level not found")

# Load or create data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r") as f:
        data = json.load(f)
else:
    data = {"history": []}

# Append today's reading
today = datetime.date.today().isoformat()
level = get_current_water_level()

if not any(d["date"] == today for d in data["history"]):
    data["history"].append({"date": today, "level": level})

# Trim to last 7 days
data["history"] = data["history"][-7:]

# Calculate summary
data["current_level"] = data["history"][-1]["level"]
data["seven_day_average"] = round(sum(d["level"] for d in data["history"]) / len(data["history"]), 2)

# Write to file
with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)
