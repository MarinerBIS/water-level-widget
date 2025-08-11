import requests
from bs4 import BeautifulSoup
import json
import datetime
import os

URL = "https://www.nbpower.com/en/safety/dam-safety"
DATA_FILE = "data.json"

# Scrape function
def get_current_water_level():
    res = requests.get(URL)
    soup = BeautifulSoup(res.text, 'html.parser')

    # This selector depends on NB Power’s site structure — update as needed
    value = soup.find("div", class_="water-level").text.strip()
    level = float(value.split()[0])  # assumes something like "75.3 m"

    return level

# Load previous data
if os.path.exists(DATA_FILE):
    with open(DATA_FILE) as f:
        data = json.load(f)
else:
    data = {"history": []}

# Update with today's value
today = datetime.date.today().isoformat()
level = get_current_water_level()

data["history"].append({"date": today, "level": level})
data["history"] = data["history"][-7:]  # Keep last 7 days

# Compute current/avg
levels = [d["level"] for d in data["history"]]
data["current_level"] = levels[-1]
data["seven_day_average"] = sum(levels) / len(levels)

# Save updated file
with open(DATA_FILE, "w") as f:
    json.dump(data, f, indent=2)
