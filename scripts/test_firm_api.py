import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

firms_map_key = os.getenv("FIRMS_MAP_KEY")

if not firms_map_key:
    raise ValueError("FIRMS_MAP_KEY is not set in the environment variables.")

url = 'https://firms.modaps.eosdis.nasa.gov/mapserver/mapkey_status/?MAP_KEY=' + firms_map_key # For checking the status of the map key
da_url = 'https://firms.modaps.eosdis.nasa.gov/api/data_availability/csv/' + firms_map_key + '/all' # For checking the data used per sensor

try: 
    response = requests.get(url)
    data = response.json()
    df = pd.Series(data)
    print(df)
    # df = pd.read_csv(da_url)
    # print(df)
except requests.exceptions.RequestException as e:
    print(f"An error occurred while making the request: {e}")