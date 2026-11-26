import os
from pathlib import Path
import requests
from dotenv import load_dotenv
import pandas as pd
import io

SOURCE = "VIIRS_NOAA21_NRT"
AREA = "-9.6,36.8,-6.1,42.2"


def fetch_firms_data(start_date: str, day_range: int) -> Path:
    load_dotenv()
    MAP_KEY = os.getenv("FIRMS_MAP_KEY")

    if not MAP_KEY:
        raise ValueError("Missing NASA MAP_KEY")
    url = (
        "https://firms.modaps.eosdis.nasa.gov/api/area/csv/"
        f"{MAP_KEY}/{SOURCE}/{AREA}/{day_range}/{start_date}"
    )

    project_root = Path(__file__).resolve().parents[1]
    output_dir = project_root / "data/raw/firms"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / f"{SOURCE}_{start_date}_{day_range}days.csv"

    if output_file.exists():
        raise FileExistsError(f"Output already exists: {output_file}")

    try:
        response = requests.get(url, timeout=60)
    except requests.exceptions.RequestException:
        raise RuntimeError("NASA Firms request failed.") from None


    if response.status_code != 200:
        raise RuntimeError(f"NASA Firms returned status code {response.status_code}")

    expected_columns = [
        "latitude", "longitude", "bright_ti4", "scan", "track",
        "acq_date", "acq_time", "satellite", "instrument",
        "confidence", "version", "bright_ti5", "frp", "daynight",
    ]

    try:
        df = pd.read_csv(io.BytesIO(response.content),dtype="string")
    except(pd.errors.ParserError, pd.errors.EmptyDataError):
        raise ValueError("NASA response could not be parsed as CSV.") from None

    missing_columns = set(expected_columns) - set(df.columns)
    if missing_columns:
        raise ValueError(
            f"Response is missing columns: {sorted(missing_columns)}"
        )

    output_file.write_bytes(response.content)
    print(f"Successfully fetched data. Number of records: {len(df)}")

    print('HTTP status:', response.status_code)
    print('Response size:', len(response.content), 'bytes')
    print('Content Type:', response.headers.get('Content-Type'))
    print('Response Preview:')
    print(response.text[:1000])
    return output_file

if __name__ == "__main__":
    saved_path = fetch_firms_data(
        start_date="2026-11-22",
        day_range=3,
    )
    print("Saved to:", saved_path)