import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt

def get_table(database, tablename):
    conn = sqlite3.connect(database)
    df = pd.read_sql_query(f'SELECT * FROM {tablename}', conn)
    conn.close()
    return df

def format_data(df):
    df = df.set_index('time_stamp')
    df.index = pd.to_datetime(df.index)
    df = df[df.index >= '2023-04-30 23:00:01']
    df.index = df.index.shift(1, freq="H") #move index up one period so that index represents the target forecast date.
    return df

def pivot_forecast(df):
    df['hour'] = df.index.hour
    num_columns_to_shift = df['hour']
    num_columns_to_shift %= 24 - (num_columns_to_shift % 24)
    df.drop(columns=['hour'], inplace=True)
    df = df.apply(lambda row: row.shift(-num_columns_to_shift[row.name]), axis=1)
    for i in range(df.shape[1]):
        df.iloc[:,i] = df.iloc[:,i].shift(i)
    df = df.iloc[:, :-48] #remove farthest out forecasts as they contain many null points. 
    df = df.replace('None', np.nan)
    df = df.fillna(np.nan)
    df = df.dropna()
    df = df.astype(float) #some of the weather codes remained in int format. 
    return df

def summary_statistics(df):
    df['mean'] = df.mean(axis=1, numeric_only=True)
    df['std'] = df.std(axis=1, numeric_only=True)    
    df['min'] = df.min(axis=1, numeric_only=True)    
    df['max'] = df.max(axis=1, numeric_only=True)    
    df['median'] = df.median(axis=1, numeric_only=True) 
    return df

def preprocess_forecast(database, tablename):
    df = get_table(database, tablename)
    df = format_data(df)
    df = pivot_forecast(df)
    return df

def preprocess_lables(database, tablename):
    df = get_table(database, tablename)
    df = format_data(df)
    return df

def combine_forecast_current(forecast_df, labels_df, label_column):
    labels_df = labels_df[labels_df.index >= forecast_df.index[0]]
    labels_df = labels_df[[label_column]]
    forecast_df['Label'] = labels_df[label_column]
    combined_df = forecast_df
    return combined_df


def label_difs(df):
    df_labels = pd.DataFrame(df['Label'])
    df_forecasts = df.drop('Label', axis=1)
    diff_df = df_forecasts.subtract(df_labels['Label'], axis=0)
    return diff_df


def stat_report(df):
    df = summary_statistics(df)
    print(f"Dataframe Shape: {df.shape}")
    print(f"minimum std: {round(df['std'].min(numeric_only=True), 2)}")
    print(f"maximum std: {round(df['std'].max(numeric_only=True), 2)}")
    print(f"mean std: {round(df['std'].mean(numeric_only=True), 2)}")
    print(f"min minimum: {round(df['min'].min(numeric_only=True), 2)}")
    print(f"max minimum: {round(df['min'].max(numeric_only=True), 2)}")
    print(f"min maximum: {round(df['max'].min(numeric_only=True), 2)}")
    print(f"max maximum: {round(df['max'].max(numeric_only=True), 2)}")
    print(f"min max range: {round(df['max'].max(numeric_only=True) - df['min'].min(numeric_only=True), 2)}")

def print_nans(df):
    nan_counts = df.isna().sum()
    nan_counts.plot(kind='bar')
    plt.xlabel('Colmuns')
    plt.ylabel('Number of NaN Values')
    plt.show()


