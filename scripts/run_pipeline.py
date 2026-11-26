import psycopg
from fetch_firms_recent import fetch_firms_data, SOURCE, AREA
from load_firms_data import load_firms_data
from datetime import timedelta, datetime, timezone
from dotenv import load_dotenv

def main() -> None:
    day_range = 3
    end_date = datetime.now(timezone.utc).date()
    start_date = end_date - timedelta(days=day_range - 1)

    print("Request window:", start_date, "through", end_date)

    load_dotenv()

    with psycopg.connect(connect_timeout=10) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO public.pipeline_runs (
                    source_product,
                    requested_area,
                    request_start,
                    request_end
                )
                VALUES (%s, %s, %s, %s)
                RETURNING id;
                """,
                (SOURCE, AREA, start_date, end_date),
            )

            row = cursor.fetchone()

            if row is None:
                raise RuntimeError("Creating the pipeline run returned no ID.")

            run_id = row[0]

    print("Pipeline run ID:", run_id)


    try:
        saved_path = fetch_firms_data(
            start_date=start_date.isoformat(),
            day_range=day_range,
        )

        counts = load_firms_data(saved_path)

    except Exception as error:
        # Store only the error class to avoid recording credentials.
        error_type = type(error).__name__

        try:
            with psycopg.connect(connect_timeout=10) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE public.pipeline_runs
                        SET status = 'failed',
                            finished_at = clock_timestamp(),
                            error_message = %s
                        WHERE id = %s;
                        """,
                        (error_type, run_id),
                    )

        except psycopg.Error:
            print("Could not record the failed status in PostgreSQL.")

        raise RuntimeError(
            f"Pipeline run {run_id} failed ({error_type})."
        ) from None

    with psycopg.connect(connect_timeout=10) as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE public.pipeline_runs
                SET status = 'succeeded',
                    finished_at = clock_timestamp(),
                    records_received = %s,
                    records_inserted = %s,
                    records_skipped = %s
                WHERE id = %s;
                """,
                (
                    counts["records_received"],
                    counts["records_inserted"],
                    counts["records_skipped"],
                    run_id,
                ),
            )

    print("Pipeline succeeded. Final counts:", counts)

if __name__ == '__main__':
    main()