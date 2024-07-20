import paho.mqtt.client as mqtt
import re
import binascii
import requests
import psycopg2
from datetime import datetime, timezone
from config_files import mqtt_config as config

ttn_broker = config.MQTT_HOSTNAME
ttn_port = config.MQTT_PORT
ttn_username = config.MQTT_USERNAME
ttn_password = config.MQTT_PASSWORD
ttn_topic = config.MQTT_TOPIC

# Regular expression to extract data from payload
extract_data_regex = re.compile(r'(?<="frm_payload":")[^"]+')


def connect_to_mysql():
    mydb = psycopg2.connect(
        host="localhost",
        user="iot_postgres",
        password="smi21",
        database="postgres",
        port=5432
    )
    return mydb


# searches for payload to extract from received message
def extract_data_from_payload(payload):
    match = extract_data_regex.search(payload)
    if match:
        return match.group(0)
    return None


# converts and displays base64 payload to integer
def base64_to_unsigned_int32(base64_str):
    binary_str = binascii.a2b_base64(base64_str)
    decimal_values = [int(byte) for byte in binary_str]

    # Convert every four values to unsigned 32-bit integers
    uint32_values = []
    for i in range(0, len(decimal_values), 4):
        # here we perform a bitwise OR, in order to combine them into a single value. We shift them to them left, in order for the bits to occupy their correct position
        uint32 = (decimal_values[i] << 24) | (decimal_values[i + 1] << 16) | (decimal_values[i + 2] << 8) | \
                 decimal_values[i + 3]
        uint32_values.append(uint32)

    return uint32_values


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        # we should always subscribe from on_connect callback to be sure
        # our subscribed is persisted across reconnections.
        client.subscribe(ttn_topic)


def on_message(client, userdata, msg):  # every time we receive a message from the mqtt broker we do the following
    print(f"Received message on topic {msg.topic}: {msg.payload.decode()}")

    # we attempt to extract data using the regular expression
    extracted_data = extract_data_from_payload(msg.payload.decode())
    if extracted_data is not None:
        print("Extracted data (base64):", extracted_data)

        # Convert base64 to unsigned 32-bit integers
        uint32_values = base64_to_unsigned_int32(extracted_data)

        # Divide each value by 100 to get float numbers
        float_values = [value / 100.0 for value in uint32_values]

        if float_values[-1] < 25 or float_values[-1] > 100:
            # print("Humidity sensor is not working properly. Getting humidity from OpenWeather API.")
            float_values[-1] = get_humidity_for_open_weather()

        # Save Values to Database
        O2_value = float_values[0]
        CO_value = float_values[1]
        NO2_value = float_values[2]
        humidity_value = float_values[3]
        save_data_to_database(O2_value, CO_value, NO2_value, humidity_value)


def get_humidity_for_open_weather():
    # Enter your API key here
    api_key = "b94c15a1b0245a2c43c7c5365ac6c168"

    # base_url variable to store url
    base_url = "http://api.openweathermap.org/data/2.5/weather?"

    # Give city name
    city_name = "Samos"

    # complete url address
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name

    # Call the API
    response = requests.get(complete_url)
    # get the data in json format
    data = response.json()
    #get the status code
    if data["cod"] != "404":
        main_data = data["main"]
        current_humidity = main_data["humidity"]
        return current_humidity
    else:
        return 55


def save_data_to_database(O2_value, CO_value, NO2_value, humidity_value):
    mydb = connect_to_mysql()
    # Extract current timestamp to append to the current measurement
    int_timestamp = int(datetime.now(tz=timezone.utc).timestamp())
    timestamp = datetime.fromtimestamp(int_timestamp, tz=timezone.utc)
    #

    print("O2: ", O2_value)
    print("CO: ", CO_value)
    print("NO2: ", NO2_value)
    print("Humidity: ", humidity_value)
    print("Timestamp: ", timestamp)
    print("\n")

    mycursor = mydb.cursor()
    sql = "INSERT INTO public.measurements (timestamp, co2, humidity, o2, no2) VALUES (%s, %s, %s, %s, %s)"
    val = (timestamp, CO_value, humidity_value, O2_value, NO2_value)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")
    mycursor.close()


if __name__ == "__main__":
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.username_pw_set(ttn_username, password=ttn_password)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(ttn_broker, port=ttn_port, keepalive=60)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Disconnecting from TTN MQTT Broker")
        client.disconnect()
