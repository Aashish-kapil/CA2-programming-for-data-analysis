# Mediterranean Wildfire Intelligence

The project investigates how environmental and geographical conditions relate to satellite-detected fire activity in **Portugal, Spain, and Greece**, with a planned study period of **2018–2025**.

## Data and approach

The workflow will acquire data directly from official sources, validate and transform it, store it in a database, and perform exploratory and statistical analysis.

- **NASA FIRMS:** VIIRS Suomi-NPP standard-processing active fire observations (`VIIRS_SNPP_SP`).
- **Planned sources:** Copernicus ERA5-Land weather data, ESA WorldCover land cover, and authoritative country boundaries, subject to access and coverage checks.

## Current progress

- Acquired a five-day FIRMS sample for a bounding box around mainland Portugal: **1–5 August 2025**.
- Inspected **885 observations across 15 columns**; found no missing values or exact duplicate rows.
- Separated API acquisition from local CSV inspection. Raw observations remain unchanged.

Next steps are to review detection classifications, design reproducible historical acquisition, apply country boundaries, and develop the database and environmental-data integration.

## Local setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Acquisition requires a NASA FIRMS key stored locally in `.env` as `FIRMS_MAP_KEY`. Credentials and local data are excluded from Git.

To inspect the sample after acquiring it:

```bash
python scripts/inspect_firms_data.py
```

The inspection script reads `data/raw/firms/portugal_sample_2025.csv` without making an API request. The CSV is not included in the repository.

