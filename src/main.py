from paho.mqtt import client as mqtt_client
import json
import time

from schema.aggregated_data_schema import AccelerometerSchema, GpsSchema, ParkingSchema
from file_datasource import FileDatasource
import config

def connect_mqtt(broker, port):
    """Create MQTT client"""
    print(f"CONNECT TO {broker}:{port}")
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"Connected to MQTT Broker ({broker}:{port})!")
        else:
            print("Failed to connect {broker}:{port}, return code %d\n", rc)
            exit(rc)  # Stop execution
    client = mqtt_client.Client()
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()
    return client

def publish(client, topic, data, schema):
    """Publish data to MQTT topic"""
    msg = schema.dumps(data)
    result = client.publish(topic, msg)
    if result[0] != 0:
        print(f"Failed to send message to topic {topic}")

def run():
    # Connect to MQTT broker
    client = connect_mqtt(config.MQTT_BROKER_HOST, config.MQTT_BROKER_PORT)

    # Initialize data source
    data_source = FileDatasource("data/accelerometer.csv", "data/gps.csv", "data/parking.csv")
    data_source.startReading()

    try:
        while True:
            # Read data from data source
            data = data_source.read()

            # Publish accelerometer data
            publish(client, config.MQTT_ACCELEROMETER_TOPIC, data.accelerometer, AccelerometerSchema())

            # Publish GPS data
            publish(client, config.MQTT_GPS_TOPIC, data.gps, GpsSchema())

            # Publish parking data
            publish(client, config.MQTT_PARKING_TOPIC, data.parking, ParkingSchema())

            # Delay
            time.sleep(config.DELAY)

    finally:
        # Clean up resources
        data_source.stopReading()
        client.disconnect()

if __name__ == "__main__":
    run()