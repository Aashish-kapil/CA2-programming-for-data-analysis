from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]

CSV_PATH = PROJECT_ROOT / "data/raw/firms/firms_2026-11-20.csv"
EXPECTED_COLUMNS = [
    "latitude", "longitude", "bright_ti4", "scan", "track", "acq_date",
    "acq_time", "satellite", "instrument", "confidence", "version",
    "bright_ti5", "frp", "daynight",
]

def transform_firms_data(raw_df: pd.DataFrame) -> pd.DataFrame:
    missing_columns = set(EXPECTED_COLUMNS) - set(raw_df.columns)
    if missing_columns:
        raise ValueError(f"Exiting due to missing columns in the CSV data: {missing_columns}")

    df = raw_df.copy()
    numeric_columns = ["latitude", "longitude", "bright_ti4", "scan", "track", "bright_ti5", "frp"]

    for column in numeric_columns:
        converted = pd.to_numeric(df[column], errors='coerce')
        conversion_failures = df[column].notna() & converted.isna()
        if conversion_failures.any():
            raise ValueError(f"Invalid Numeric values in column {column}")
        print(f"Column '{column}': {conversion_failures.sum()} conversion failures")
        df[column] = converted

    acquisition_time = df["acq_time"].str.zfill(4)
    df["acquired_at"] = pd.to_datetime(df['acq_date'] + " " + acquisition_time, format="%Y-%m-%d %H%M", errors='coerce', utc=True)

    return df

def validate_firms_data(df: pd.DataFrame) -> None:
    valid_rows = (
        df["latitude"].between(-90, 90).fillna(False)
        & df["longitude"].between(-180, 180).fillna(False)
        & df["acquired_at"].notna()
        & df["satellite"].isin(["N21"])
        & df["instrument"].isin(["VIIRS"])
        & df["confidence"].isin(["l", "n", "h"])
        & df["daynight"].isin(["D", "N"])
        & (df["frp"].isna() | df["frp"].ge(0)).fillna(False)
    )
    invalid_count = int((~valid_rows).sum())

    if invalid_count:
        raise ValueError(f"Validation failed for {invalid_count} observations.")



def main() -> None:
    raw_df = pd.read_csv(CSV_PATH, dtype="string")

    df = transform_firms_data(raw_df)
    validate_firms_data(df)

    print("Validation passed.")
    print("Shape:", df.shape)
    print("Missing values:")
    print(df.isna().sum())
    print("Exact duplicates:", df.duplicated().sum())
    print(df[["satellite", "acquired_at", "latitude", "longitude", "frp"]])

if __name__ == "__main__":
    main()