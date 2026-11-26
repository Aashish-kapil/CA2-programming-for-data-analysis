from fetch_firms_recent import fetch_firms_data
from load_firms_data import load_firms_data
from datetime import timedelta, datetime, timezone

def main() -> None:
    day_range = 3
    end_date = datetime.now(timezone.utc).date()
    start_date = end_date - timedelta(days=day_range - 1)

    print("Request window:", start_date, "through", end_date)

    saved_path = fetch_firms_data(
        start_date=start_date.isoformat(),
        day_range=day_range,
    )
    load_firms_data(saved_path)

if __name__ == '__main__':
    main()