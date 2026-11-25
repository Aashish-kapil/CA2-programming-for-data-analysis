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
    df = raw_df.copy()
    numeric_columns = ["latitude", "longitude", "bright_ti4", "scan", "track", "bright_ti5", "frp"]

    for column in numeric_columns:
        converted = pd.to_numeric(df[column], errors='coerce')
        conversion_failures = df[column].notna() & converted.isna()
        print(f"Column '{column}': {conversion_failures.sum()} conversion failures")
        df[column] = converted

    acquisition_time = df["acq_time"].str.zfill(4)
    df["acquired_at"] = pd.to_datetime(df['acq_date'] + " " + acquisition_time, format="%Y-%m-%d %H%M", errors='coerce', utc=True)

    return df

raw_df = pd.read_csv(CSV_PATH, dtype="string")
missing_columns = set(EXPECTED_COLUMNS) - set(raw_df.columns)
if missing_columns:
    raise SystemExit(f"Exiting due to missing columns in the CSV data: {missing_columns}")

df = transform_firms_data(raw_df)
# Lat & Log validation
invalid_coordinates = ~(df['latitude'].between(-90, 90).fillna(False) & df['longitude'].between(-180, 180).fillna(False))

# negative frp
negative_frp = df['frp'] < 0

# invalid confidence values
invalid_confidence = ~df['confidence'].isin(['l', 'n', 'h'])

# invalid DayNight
invalid_daynight = ~df['daynight'].isin(['D', 'N'])

# invalid satellite values
invalid_satellite = ~df['satellite'].isin(['N21'])

# invalid instrument values
invalid_instrument = ~df['instrument'].isin(['VIIRS'])

print('shape',df.shape)
print('columns',df.columns.to_list())
print('missing values',df.isna().sum())
print('Duplicates:',df.duplicated().sum())
print('Satellite', df['satellite'].value_counts(dropna=False))
print('Instrument', df['instrument'].value_counts(dropna=False))
print('Confidence', df['confidence'].value_counts(dropna=False))
print(df[["acq_date", "acq_time", "acquired_at"]])
print("Invalid timestamps:", df["acquired_at"].isna().sum())
print("Invalid coordinates:", invalid_coordinates.sum())
print("Negative FRP values:", negative_frp.sum())
print("Invalid confidence values:", invalid_confidence.sum())
print("Invalid DayNight values:", invalid_daynight.sum())
print("Invalid satellite values:", invalid_satellite.sum())
print("Invalid instrument values:", invalid_instrument.sum())

empty_raw_df = raw_df.iloc[:0].copy()
empty_df = transform_firms_data(empty_raw_df)

print("Empty input shape:", empty_raw_df.shape)
print("Empty transformed shape:", empty_df.shape)
print("Timestamp type:", empty_df["acquired_at"].dtype)