import sqlite3
from inspection_functions import get_column_names, create_table

# set column names for tables
weathercode_forecast_columns = get_column_names(data_type='INT')
temperature_forecast_columns = get_column_names()
windspeed_forecast_columns = get_column_names()
current_weather_columns = ', '.join(['time_stamp', 'temperature', 'windspeed', 'weathercode', 'is_day', 'time'])

# create tables 
create_table('weathercode', weathercode_forecast_columns)
create_table('temperature', temperature_forecast_columns)
create_table('windspeed', windspeed_forecast_columns)
create_table('current_weather', current_weather_columns)