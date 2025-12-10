import os

import json

import logging

from datetime import datetime, timezone
 
import boto3

from botocore.exceptions import BotoCoreError, ClientError

import requests

from dotenv import load_dotenv
 
# --------------------------

# Setup logging

# --------------------------

logging.basicConfig(

    level=logging.INFO,

    format="%(asctime)s [%(levelname)s] %(message)s"

)
 
# --------------------------

# Load environment variables

# --------------------------

load_dotenv()
 
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

AWS_REGION = os.getenv("AWS_REGION", "ap-south-1")

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

CITIES_ENV = os.getenv("CITIES", "")
 
if not OPENWEATHER_API_KEY:

    raise ValueError("OPENWEATHER_API_KEY is not set in environment/.env")
 
if not S3_BUCKET_NAME:

    raise ValueError("S3_BUCKET_NAME is not set in environment/.env")
 
if not CITIES_ENV:

    raise ValueError("CITIES is not set in environment/.env")
 
CITIES = [c.strip() for c in CITIES_ENV.split(",") if c.strip()]
 
# --------------------------

# AWS S3 client

# --------------------------

s3_client = boto3.client("s3", region_name=AWS_REGION)
 
# --------------------------

# OpenWeather API settings

# --------------------------

OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
 
 
def get_weather_for_city(city: str) -> dict | None:

    """

    Fetch real-time weather data for a single city from OpenWeather API.
 
    Returns a normalized dict with key fields or None on failure.

    """

    params = {

        "q": city,

        "appid": OPENWEATHER_API_KEY,

        "units": "imperial",  # Fahrenheit

    }
 
    try:

        response = requests.get(OPENWEATHER_BASE_URL, params=params, timeout=10)

        response.raise_for_status()

        data = response.json()

    except requests.exceptions.RequestException as e:

        logging.error(f"Error fetching weather data for {city}: {e}")

        return None
 
    # Defensive parsing

    try:

        main = data.get("main", {})

        weather_list = data.get("weather", [])

        weather_description = weather_list[0]["description"] if weather_list else "unknown"
 
        record = {

            "city": city,

            "temp_f": main.get("temp"),

            "humidity": main.get("humidity"),

            "condition": weather_description,

            "timestamp_utc": datetime.now(timezone.utc).isoformat(),

            "raw": data,  # keep full raw response for historical / debugging

        }

        return record

    except (KeyError, TypeError) as e:

        logging.error(f"Unexpected data format for {city}: {e} | raw={data}")

        return None
 
 
def collect_weather_for_cities(cities: list[str]) -> list[dict]:

    """

    Fetch weather data for a list of cities.

    Skips any city that fails and logs the error.

    """

    records: list[dict] = []
 
    for city in cities:

        logging.info(f"Fetching weather for: {city}")

        record = get_weather_for_city(city)

        if record:

            records.append(record)

            # Also display summary to console

            logging.info(

                f"{city}: {record['temp_f']}°F, "

                f"Humidity {record['humidity']}%, "

                f"Condition: {record['condition']}"

            )

        else:

            logging.warning(f"Skipping city due to error: {city}")
 
    return records
 
 
def upload_to_s3(data: list[dict]) -> str | None:

    """

    Uploads the collected weather data to S3 as a JSON file.
 
    Key format: weather-data/YYYY/MM/DD/weather-YYYYMMDD-HHMMSS.json

    Returns the S3 object key on success, None on failure.

    """

    if not data:

        logging.warning("No weather data to upload to S3.")

        return None
 
    now = datetime.now(timezone.utc)

    date_path = now.strftime("%Y/%m/%d")

    timestamp_str = now.strftime("%Y%m%d-%H%M%S")
 
    key = f"weather-data/{date_path}/weather-{timestamp_str}.json"
 
    body = json.dumps(

        {

            "generated_at_utc": now.isoformat(),

            "record_count": len(data),

            "records": data,

        },

        indent=2

    )
 
    try:

        s3_client.put_object(

            Bucket=S3_BUCKET_NAME,

            Key=key,

            Body=body.encode("utf-8"),

            ContentType="application/json",

        )

        logging.info(f"Uploaded weather data to s3://{S3_BUCKET_NAME}/{key}")

        return key

    except (BotoCoreError, ClientError) as e:

        logging.error(f"Failed to upload data to S3: {e}")

        return None
 
 
def main():

    logging.info("Starting Weather Data Collection System")
 
    logging.info(f"Tracking cities: {', '.join(CITIES)}")

    records = collect_weather_for_cities(CITIES)
 
    # Upload to S3

    upload_to_s3(records)
 
    logging.info("Weather data collection run completed.")
 
 
if __name__ == "__main__":

    main()

 