"""
Fetch daily weather data from Open-Meteo Historical Weather API for the predefined locations.

Usage:
    python open_meteo_fetch_weather.py --locations ../data/locations.csv --start 2024-05-01 --end 2024-05-31 --out ../data/weather_api_raw.csv
"""
from __future__ import annotations
import argparse
import time
from pathlib import Path
import pandas as pd
import requests

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"

def fetch_one(latitude: float, longitude: float, start_date: str, end_date: str) -> dict:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join([
            "temperature_2m_mean",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "relative_humidity_2m_mean",
            "wind_speed_10m_mean",
        ]),
        "timezone": "auto",
    }
    response = requests.get(BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locations", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    locations = pd.read_csv(args.locations)
    rows = []

    for _, loc in locations.iterrows():
        payload = fetch_one(float(loc["latitude"]), float(loc["longitude"]), args.start, args.end)
        daily = payload.get("daily", {})
        dates = daily.get("time", [])
        for i, dt in enumerate(dates):
            rows.append({
                "location_id": loc["location_id"],
                "city": loc["city"],
                "country_code": loc["country_code"],
                "weather_date": dt,
                "avg_temp_c": daily.get("temperature_2m_mean", [None] * len(dates))[i],
                "max_temp_c": daily.get("temperature_2m_max", [None] * len(dates))[i],
                "min_temp_c": daily.get("temperature_2m_min", [None] * len(dates))[i],
                "total_precip_mm": daily.get("precipitation_sum", [None] * len(dates))[i],
                "avg_humidity_pct": daily.get("relative_humidity_2m_mean", [None] * len(dates))[i],
                "avg_wind_speed_kmh": daily.get("wind_speed_10m_mean", [None] * len(dates))[i],
                "source_system": "open_meteo_api",
            })
        time.sleep(0.2)

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(out_path, index=False)
    print(f"Wrote {len(rows)} rows to {out_path}")

if __name__ == "__main__":
    main()
