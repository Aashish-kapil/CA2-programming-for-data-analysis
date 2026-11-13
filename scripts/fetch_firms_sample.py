
import os
import io
import requests
import pandas as pd

from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

MAP_KEY = os.getenv("FIRMS_MAP_KEY")

if not MAP_KEY:
    raise ValueError("Missing NASA MAP_KEY")

SOURCE = "VIIRS_SNPP_SP"

# Small test area: Portugal
AREA = "-9.6,36.8,-6.1,42.2"

START_DATE = "2025-08-01"
DAY_RANGE = 5

BASE_URL = (
    "https://firms.modaps.eosdis.nasa.gov/"
    "api/area/csv"
)

url = (
    f"{BASE_URL}/{MAP_KEY}/"
    f"{SOURCE}/{AREA}/{DAY_RANGE}/{START_DATE}"
)

print("Requesting NASA FIRMS data...")

response = requests.get(
    url,
    timeout=120
)

response.raise_for_status()

print("HTTP status:", response.status_code)
print("Response size:", len(response.content), "bytes")

# Save original response before processing
output_dir = Path("data/raw/firms")
output_dir.mkdir(parents=True, exist_ok=True)

raw_file = output_dir / "portugal_sample_2025.csv"

raw_file.write_bytes(response.content)

print("Raw CSV saved:", raw_file)

# Load actual response into Pandas
df = pd.read_csv(
    io.BytesIO(response.content)
)

print("\nDataset shape:", df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nFirst five observations:")
print(df.head())

print("\nDataset information:")
df.info()

print("\nSummary statistics:")
print(df.describe(include="all"))

print("\nMissing values:")
print(df.isnull().sum())
