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

latitude = pd.to_numeric(df['latitude'], errors='coerce')
longitude = pd.to_numeric(df['longitude'], errors='coerce')

valid_latitude = latitude.between(-90, 90)
valid_longitude = longitude.between(-180, 180)

invalid_coordinates = ~(valid_latitude & valid_longitude)

print('invalid coordinates:', invalid_coordinates.sum())
print('latitude range:', latitude.min(), latitude.max())
print('longitude range:', longitude.min(), longitude.max())

print('Satellite', df['satellite'].value_counts(dropna=False))
print('Instrument', df['instrument'].value_counts(dropna=False))

print('Confidence', df['confidence'].value_counts(dropna=False))

# checking skewed data by histogram.
# frp = pd.to_numeric(df['frp'], errors='coerce')
# print(frp.describe())
# plt.hist(frp.dropna(), bins=30)
# plt.show()

acquisition_time = df["acq_time"].str.zfill(4)

df["acquired_at"] = pd.to_datetime(df['acq_date'] + " " + acquisition_time, format="%Y-%m-%d %H%M", errors='coerce', utc=True)

print(df[["acq_date", "acq_time", "acquired_at"]])
print("Invalid timestamps:", df["acquired_at"].isna().sum())