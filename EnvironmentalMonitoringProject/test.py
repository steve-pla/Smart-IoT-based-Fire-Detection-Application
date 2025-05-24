import pandas as pd
import numpy as np
import psycopg2
from psycopg2 import Error

# Set desired timeframe (one week)
start_date = pd.to_datetime("2024-02-11")  # Replace with your start date
end_date = start_date + pd.Timedelta(days=7)

# Generate timestamps at 5-minute intervals
timestamps = pd.date_range(start_date, end_date, freq="5T")

# Define realistic ranges and trends (adjust based on your forest environment)
min_co2 = 400
max_co2 = 500
trend_co2 = 0.01  # ppm per minute increase

min_temp = -5
max_temp = 45
amplitude_temp = 6  # degrees Celsius

min_humidity = 20
max_humidity = 950
amplitude_humidity = 15  # percentage

# Generate CO2 values with noise
co2_values = (
        min_co2
        + trend_co2 * (timestamps - start_date).total_seconds() / 60  # Convert timestamps to minutes
        + np.random.uniform(-1, 1, len(timestamps))
)

# Generate temperature values with daily fluctuations
temperature_values = (
        amplitude_temp
        * np.sin(timestamps.dayofyear / 365 * 2 * np.pi)
        + min_temp
        + np.random.normal(0, 1, len(timestamps))
)

# Generate humidity values with random fluctuations
humidity_values = (
        amplitude_humidity
        * np.random.normal(0, 1, len(timestamps))
        + min_humidity
        + np.random.normal(0, 5, len(timestamps))
)

# Ensure values stay within ranges
co2_values = np.clip(co2_values, min_co2, max_co2)
temperature_values = np.clip(temperature_values, min_temp, max_temp)
humidity_values = np.clip(humidity_values, min_humidity, max_humidity)

# Create DataFrame with realistic data
data = pd.DataFrame({"timestamp": timestamps, "co2": co2_values, "temperature": temperature_values,
                     "humidity": humidity_values})

print(data)

# Connect to PostgreSQL
try:
    connection = psycopg2.connect(user="postgres",
                                  password="smi21",
                                  host="localhost",
                                  port=5432,
                                  database="postgres")
    cursor = connection.cursor()
    # Assuming your DataFrame is named 'data'
    for index, row in data.iterrows():
        cursor.execute("""
            INSERT INTO measurements (timestamp, co2, temperature, humidity)
            VALUES (%s, %s, %s, %s)
        """, (row['timestamp'], row['co2'], row['temperature'], row['humidity']))

    # Commit the transaction
    connection.commit()
    print("Records inserted successfully")
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    # Close the cursor and connection
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
