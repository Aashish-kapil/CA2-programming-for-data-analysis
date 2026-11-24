import os
from pathlib import Path
import requests
from dotenv import load_dotenv
import pandas as pd
import io

load_dotenv()
MAP_KEY = os.getenv("FIRMS_MAP_KEY")

if not MAP_KEY:
    raise ValueError("Missing NASA MAP_KEY")

SOURCE = "VIIRS_NOAA21_NRT"
AREA = "-9.6,36.8,-6.1,42.2"
START_DATE = "2026-11-20"
DAY_RANGE = 3
url = (
    "https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
    f"{MAP_KEY}/{SOURCE}/{AREA}/{DAY_RANGE}/{START_DATE}"
)

output_dir = Path('data/raw/firms')
output_dir.mkdir(parents=True, exist_ok=True)
output_file = output_dir / f"firms_{START_DATE}.csv"

# if output_file.exists():
#     raise SystemExit(f"Output file {output_file} already exists. Exiting to avoid overwriting.")


try:
    response = requests.get(url, timeout=60)
except requests.exceptions.RequestException:
    print("Error occurred while making the request:")
    raise SystemExit("Exiting due to request error.")


if response.status_code != 200:
    raise SystemExit("Exiting due to request error.")

expected_columns = [
    "latitude", "longitude", "bright_ti4", "scan", "track",
    "acq_date", "acq_time", "satellite", "instrument",
    "confidence", "version", "bright_ti5", "frp", "daynight",
]

try:
    df = pd.read_csv(io.BytesIO(response.content),dtype="string")
except(pd.errors.ParserError, pd.errors.EmptyDataError):
    raise SystemExit("Exiting due to CSV parsing error.")

missing_columns = set(expected_columns) - set(df.columns)
if missing_columns:
    print(f"Warning: Missing expected columns: {missing_columns}")
    print("Received columns:", df.columns.tolist())
    raise SystemExit("Exiting due to missing columns in the CSV data.")

output_file.write_bytes(response.content)
print(f"Successfully fetched data. Number of records: {len(df)}")

print('HTTP status:', response.status_code)
print('Response size:', len(response.content), 'bytes')
print('Content Type:', response.headers.get('Content-Type'))
print('Response Preview:')
print(response.text[:1000])