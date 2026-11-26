import pandas as pd
import psycopg
from inspect_firms_data import transform_firms_data, validate_firms_data
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

def load_firms_data(csv_path: Path) -> dict[str, int]:
    raw_df = pd.read_csv(csv_path, dtype="string")
    df = transform_firms_data(raw_df)
    validate_firms_data(df)


    if df.empty:
        print("Zero observations received. Nothing to load.")
        return {
        "records_received": 0,
        "records_inserted": 0,
        "records_skipped": 0,
    }

    columns = [
    "satellite", "instrument", "acquired_at", "latitude", "longitude",
    "bright_ti4", "bright_ti5", "frp", "track", "scan",
    "confidence", "version", "daynight",
    ]

    numeric_columns= [
        "latitude", "longitude", "bright_ti4", "bright_ti5",
        "frp", "track", "scan",
    ]

    inserted_count = 0
    skipped_count = 0

    with psycopg.connect(connect_timeout=10) as conn:
        with conn.cursor() as cursor:
            for _, observation in df.iterrows():
                values = []
                for column in columns:
                    value = observation[column]
            
                    if pd.isna(value):
                        value = None
                    elif column == 'acquired_at':
                        value = value.to_pydatetime()
                    elif column in numeric_columns:
                        value = float(value)
            
                    values.append(value)
                cursor.execute(
                    """
                    INSERT INTO public.fire_detections (
                        source_product, satellite, instrument, acquired_at,
                        latitude, longitude, bright_ti4, bright_ti5, frp,
                        track, scan, confidence, version, daynight
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s, %s
                    )
                    ON CONFLICT ON CONSTRAINT unique_fire_observation
                    DO NOTHING
                    RETURNING id;
                    """,
                    ("VIIRS_NOAA21_NRT", *values),
                )

                inserted = cursor.fetchone()
                if inserted is None:
                    skipped_count += 1
                else:
                    inserted_count += 1

    print("Inserted observations:", inserted_count)
    print("Already stored observations:", skipped_count)

    return {
        "records_received": len(df),
        "records_inserted": inserted_count,
        "records_skipped": skipped_count,
    }

if __name__ == "__main__":
    project_root = Path(__file__).resolve().parents[1]
    csv_path = project_root / "data/raw/firms/firms_2026-11-20.csv"
    load_firms_data(csv_path)