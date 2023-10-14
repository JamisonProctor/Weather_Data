import requests
import sqlite3
import datetime
from creds import url, db_path
from inspection_functions import get_update, get_current_weather, get_forecast, update_forecast, update_current_weather

def main():
    response = get_update(url)

    weathercode_forecast, temperature_forecast, windspeed_forecast = get_forecast(response)
    current_weather = get_current_weather(response)

    update_forecast('weathercode', weathercode_forecast)
    update_forecast('temperature', temperature_forecast)
    update_forecast('windspeed', windspeed_forecast)
    update_current_weather('current_weather', current_weather)

if __name__ == '__main__':
    main()
