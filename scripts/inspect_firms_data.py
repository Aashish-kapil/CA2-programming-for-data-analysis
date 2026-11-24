from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[1]
print(Path(__file__).resolve())
print(Path(__file__).resolve().parents)
CSV_PATH = PROJECT_ROOT / "data/raw/firms/firms_2026-11-16.csv"
EXPECTED_COLUMNS = [
    "latitude", "longitude", "bright_ti4", "scan", "track", "acq_date",
    "acq_time", "satellite", "instrument", "confidence", "version",
    "bright_ti5", "frp", "daynight",
]

df = pd.read_csv(CSV_PATH, dtype="string")

print('shape',df.shape)
print('columns',df.columns.to_list())

print('missing values',df.isna().sum())
print('Duplicates:',df.duplicated().sum())

print('Satellite', df['satellite'].value_counts(dropna=False))
print('Instrument', df['instrument'].value_counts(dropna=False))

print('Confidence', df['confidence'].value_counts(dropna=False))

# checking skewed data by histogram.
# frp = pd.to_numeric(df['frp'], errors='coerce')
# print(frp.describe())
# plt.hist(frp.dropna(), bins=30)
# plt.show()

# Converting acq_date and acq_time to a single datetime column
acquisition_time = df["acq_time"].str.zfill(4)
df["acquired_at"] = pd.to_datetime(df['acq_date'] + " " + acquisition_time, format="%Y-%m-%d %H%M", errors='coerce', utc=True)

print(df[["acq_date", "acq_time", "acquired_at"]])
print("Invalid timestamps:", df["acquired_at"].isna().sum())

# Convertig measurement columns to numeric types
numeric_columns = ["latitude", "longitude", "bright_ti4", "scan", "track", "bright_ti5", "frp"]

for column in numeric_columns:
    converted = pd.to_numeric(df[column], errors='coerce')

    conversion_failed = df[column].notna() & converted.isna()
    print(f"Conversion failed for {conversion_failed.sum()} values in column '{column}'")

    df[column] = converted

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

print("Invalid coordinates:", invalid_coordinates.sum())
print("Negative FRP values:", negative_frp.sum())
print("Invalid confidence values:", invalid_confidence.sum())
print("Invalid DayNight values:", invalid_daynight.sum())
print("Invalid satellite values:", invalid_satellite.sum())
print("Invalid instrument values:", invalid_instrument.sum())