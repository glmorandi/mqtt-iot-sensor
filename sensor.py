import random
import time
import numpy as np
from data_processor import DataProcessor

class Sensor:
    def __init__(self, device_id):
        self.device_id = device_id
        self.data_processor = DataProcessor()

    def read(self):
        pass

    def run(self, mqtt_client):
        while True:
            # Lê 5 valores dos sensores
            data = [self.read() for _ in range(5)]

            # Remove outliers
            data = self.data_processor.remove_outliers(data=data, threshold=3)

            # Calcula a média dos valores
            data_mean = np.mean(data)

            # Envie a média dos valores
            self.publish_data(mqtt_client, data_mean)
            time.sleep(10)

    def publish_data(self, mqtt_client, data):
        topic = f"devices/{self.get_sensor_type()}/{self.device_id}"
        mqtt_client.publish(topic, data)

    def get_sensor_type(self):
        pass

class TemperatureSensor(Sensor):
    def read(self):
        return random.uniform(-30, 30)

    def get_sensor_type(self):
        return "temperature"

class HumiditySensor(Sensor):
    def read(self):
        return random.uniform(0, 100)

    def get_sensor_type(self):
        return "humidity"

class VibrationSensor(Sensor):
    def read(self):
        num_points = 100
        vibration_values = [random.uniform(0, 1) for _ in range(num_points)]
        return vibration_values
    
    def get_sensor_type(self):
        return "vibration"

class LuminositySensor(Sensor):
    def read(self):
        return random.uniform(0, 1000)

    def get_sensor_type(self):
        return "luminosity"
