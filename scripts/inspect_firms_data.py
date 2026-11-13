"""Inspect the existing FIRMS sample without fetching or changing data."""

from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
print(Path(__file__).resolve())
print(Path(__file__).resolve().parents)
CSV_PATH = PROJECT_ROOT / "data/raw/firms/portugal_sample_2025.csv"
EXPECTED_COLUMNS = [
    "latitude", "longitude", "bright_ti4", "scan", "track", "acq_date",
    "acq_time", "satellite", "instrument", "confidence", "version",
    "bright_ti5", "frp", "daynight",
]


def main() -> None:
    # Strings preserve original field representations, including time zeroes.
    df = pd.read_csv(CSV_PATH, dtype="string")
    print("File:", CSV_PATH)
    print("Shape (rows, columns):", df.shape)
    print("Columns:", df.columns.tolist())
    print("Missing expected columns:", sorted(set(EXPECTED_COLUMNS) - set(df.columns)))
    print("Additional columns:", sorted(set(df.columns) - set(EXPECTED_COLUMNS)))
    print("\nMissing values per column:")
    print(df.isna().sum().to_string())

    required = {"frp", "confidence", "latitude", "longitude", "acq_date",
                "satellite", "instrument", "daynight"}
    if not required.issubset(df.columns):
        raise ValueError(f"Cannot complete inspection; missing: {sorted(required - set(df.columns))}")

    missing_frp = df["frp"].isna()
    missing_confidence = df["confidence"].isna()
    print("\nRows missing both FRP and confidence:", int((missing_frp & missing_confidence).sum()))
    print("Rows missing either (zero-based DataFrame index shown):")
    print(df.loc[missing_frp | missing_confidence].to_string())
    print("\nExact duplicate rows beyond first occurrence:", int(df.duplicated().sum()))
    print("All members of exact duplicate groups:")
    print(df.loc[df.duplicated(keep=False)].to_string())

    for column, lower, upper in [("latitude", -90, 90), ("longitude", -180, 180)]:
        numeric = pd.to_numeric(df[column], errors="coerce")
        invalid = ~numeric.between(lower, upper)
        print(f"\n{column} numeric range: {numeric.min()} to {numeric.max()}")
        print("Nonmissing values that failed numeric conversion:", int((df[column].notna() & numeric.isna()).sum()))
        print("Invalid or missing coordinates:", int(invalid.sum()))
        print(df.loc[invalid].to_string())

    for column in ["confidence", "satellite", "instrument", "daynight", "type"]:
        if column in df.columns:
            print(f"\n{column} values (including missing):")
            print(df[column].value_counts(dropna=False).to_string())

    frp = pd.to_numeric(df["frp"], errors="coerce")
    print("\nFRP summary (MW):")
    print(frp.describe().to_string())
    print("Nonmissing FRP values that failed numeric conversion:", int((df["frp"].notna() & frp.isna()).sum()))
    print("Negative FRP values:", int((frp < 0).sum()))
    dates = pd.to_datetime(df["acq_date"], format="%Y-%m-%d", errors="coerce")
    print("\nAcquisition date range:", dates.min(), "to", dates.max())
    print("Invalid or missing acquisition dates:", int(dates.isna().sum()))


if __name__ == "__main__":
    main()
