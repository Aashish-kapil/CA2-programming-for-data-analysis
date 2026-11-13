import pandas as pd

FILE = 'data/raw/firms/portugal_sample_2025.csv'

df = pd.read_csv(FILE)

# Expected Schema
expected_columns = [
    'latitude',
    'longitude', 
    'bright_ti4', 
    'scan', 
    'track', 
    'acq_date', 
    'acq_time', 
    'satellite', 
    'instrument', 
    'confidence', 
    'version', 
    'bright_ti5', 
    'frp', 
    'daynight', 
    'type'
]

print("Validating FIRMS data schema...")

missing_columns = set(expected_columns) - set(df.columns)
unexpected_columns = set(df.columns) - set(expected_columns)

print("Missing columns:", missing_columns)
print("Unexpected columns:", unexpected_columns)

assert not missing_columns, f"Missing columns: {missing_columns}"

# Check for null values

print("Null values per column:")
print(df.isnull().sum())

# Check for duplicates

print("Number of duplicate rows:", df.duplicated().sum())

# Check for geographical boundaries
print(f"Latitude range: {df['latitude'].min()} to {df['latitude'].max()}")
print(f"Longitude range: {df['longitude'].min()} to {df['longitude'].max()}")

assert df["latitude"].between(-90, 90).all()
assert df["longitude"].between(-180, 180).all()

# Check date range

print(f"Date range: {df['acq_date'].min()} to {df['acq_date'].max()}")

# 6. Check numeric columns
numeric_columns = [
    "latitude",
    "longitude",
    "bright_ti4",
    "bright_ti5",
    "scan",
    "track",
    "frp"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

print("\nNumeric conversion:")
print(df[numeric_columns].dtypes)

# 7. Check FRP
print("\nFRP summary:")
print(df["frp"].describe())

print(
    "Negative FRP values:",
    (df["frp"] < 0).sum()
)

# 8. Check categorical values
for column in [
    "satellite",
    "instrument",
    "confidence",
    "daynight"
]:
    print(f"\n{column}:")
    print(df[column].value_counts(dropna=False))

print("\nValidation completed.")