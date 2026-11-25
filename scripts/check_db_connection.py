import psycopg
from dotenv import load_dotenv

load_dotenv()

with psycopg.connect(connect_timeout=10) as conn:
    with conn.cursor() as cursor:
        cursor.execute("SELECT current_database(), current_user;")
        result = cursor.fetchone()
        print(f"Connected to database: {result[0]}, as user: {result[1]}")

        cursor.execute("SELECT COUNT(*) FROM public.fire_detections;")
        detection_count = cursor.fetchone()
        print(f"Number of fire detections: {detection_count[0]}")

        cursor.execute("SELECT %s::text, %s::double precision;", ("VIIRS_NOAA21_NRT", 0.6))
        result = cursor.fetchone()
        print(f"Test query result: {result[0]}, {result[1]}")