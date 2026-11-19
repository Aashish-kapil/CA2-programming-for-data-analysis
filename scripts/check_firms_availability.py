import requests
from dotenv import load_dotenv
import os

load_dotenv()

MAP_KEY = os.getenv("FIRMS_MAP_KEY")

if not MAP_KEY:
    raise ValueError("Missing NASA MAP_KEY")

url = (
    "https://firms.modaps.eosdis.nasa.gov/"
    f"api/data_availability/csv/{MAP_KEY}/all"
)

response = requests.get(url, timeout=120)
response.raise_for_status()

print(response.text)

# The response of this data gives a table which shows the differect satellite data available on this api, with the given date ranges.
# As per this response, we are using the VIIRS_NOAA21_NRT data because it gives the latest data available till the current date.

