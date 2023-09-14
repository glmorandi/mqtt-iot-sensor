import paho.mqtt.client as mqtt
from sensor import TemperatureSensor, HumiditySensor, VibrationSensor, LuminositySensor
from mqtt_broker import MqttBroker
from threading import Thread
from discord_bot import DiscordWebhook

WEBHOOK_URL = "https://discord.com/api/webhooks/"

if __name__ == "__main__":
    # Inicialização do bot do Discord
    disc_bot = DiscordWebhook(WEBHOOK_URL, username='IOT - Info')

    # Cria threads para executar os métodos diretamente
    disc_bot_img_thread = Thread(target=disc_bot.send_plots, args=(120,))
    disc_bot_alert_thread = Thread(target=disc_bot.alert_handler)

    disc_bot_img_thread.start()
    disc_bot_alert_thread.start()

    # Inicialização do cliente MQTT
    mqtt_client = mqtt.Client()
    mqtt_client.connect("localhost", 1883)

    # Inicialização dos sensores
    num_devices = 5
    all_sensors = []
    sensor_threads = []

    # Crie e inicialize sensores para cada tipo
    for sensor_class in [TemperatureSensor, HumiditySensor, VibrationSensor, LuminositySensor]:
        sensors = [sensor_class(device_id=f'device{i}') for i in range(num_devices)]
        all_sensors.extend(sensors)

    # Inicialização do broker MQTT
    broker = MqttBroker()
    broker.start()

    # Iniciar threads para os sensores
    for sensor in all_sensors:
        sensor_thread = Thread(target=sensor.run, args=(mqtt_client,))
        sensor_threads.append(sensor_thread)
        sensor_thread.start()

    # Aguarde até que todas as threads dos sensores terminem
    for sensor_thread in sensor_threads:
        sensor_thread.join()

    # Manter o cliente MQTT em execução
    mqtt_client.loop_forever()