import requests
import sqlite3
import datetime
from creds import db_path

# Table creation

def get_column_names(num_of_days=16, num_of_hours=24, key_type='DATETIME', data_type='DECIMAL'):
    column_names_list = [f'time_stamp {key_type.upper()} NOT NULL PRIMARY KEY', ]
    for day in range(num_of_days):
        for hour in range(num_of_hours):
            column_names_list.append(f'day{day}_{hour:02d}00 {data_type.upper()}')
    column_names_str = ', '.join(column_names_list)
    return column_names_str

def create_table(table_title, column_names):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    command = f'CREATE TABLE {table_title} ({column_names})'
    c.execute(command)
    conn.commit()
    conn.close()

# Getting data and updateing database
def get_update(url):
    response = requests.get(url)
    update = response.json()
    return update

def get_current_weather(update):
    response_json = update
    time_stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temperature = response_json['current_weather']['temperature']
    windspeed = response_json['current_weather']['windspeed']
    weathercode = response_json['current_weather']['weathercode']
    is_day = response_json['current_weather']['is_day']
    time = response_json['current_weather']['time']
    current_weather = [time_stamp, temperature, windspeed, weathercode, is_day, time]
    return current_weather

def update_current_weather(table, current_weather):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    command = f"INSERT INTO {table} VALUES(?,?,?,?,?,?)"
    c.execute(command, current_weather)
    conn.commit()
    conn.close()

def get_forecast(update):
    response_json = update
    time_stamp = [datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')]
    weathercode_forecast = time_stamp + [str(x) for x in response_json['hourly']['weathercode']]
    temperature_forecast = time_stamp + [str(x) for x in response_json['hourly']['temperature_2m']]
    windspeed_forecast = time_stamp + [str(x) for x in response_json['hourly']['windspeed_10m']]
    return weathercode_forecast, temperature_forecast, windspeed_forecast

def update_forecast(table, forecast):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute(f"PRAGMA table_info({table})")
    columns = [col[1] for col in c.fetchall()]
    command = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?' for col in columns])})"
    c.execute(command, forecast)
    conn.commit()
    conn.close()
