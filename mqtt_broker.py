import paho.mqtt.client as mqtt
import requests


class MqttBroker:
    MQTT_BROKER = "localhost"
    MQTT_PORT = 1883
    TOPICS = "devices/+/+"

    def __init__(self):
        self.mqtt_server = mqtt.Client()
        self.mqtt_server.on_message = self.on_message

    def connect_to_broker(self):
        self.mqtt_server.connect(self.MQTT_BROKER, self.MQTT_PORT)

    def subscribe_to_topics(self):
        self.mqtt_server.subscribe(self.TOPICS)

    def start(self):
        self.connect_to_broker()    
        self.subscribe_to_topics()
        self.mqtt_server.loop_start()

    def on_message(self, client, userdata, msg):
        topic = msg.topic
        data = float(msg.payload)

        print(f'Recebido data: {data} de {msg.topic}')

        topic = msg.topic.split('/')

        # Sempre 1 pois dados estão no formato /device/topico/deviceid
        topic = topic[1]

        self.send_data(data, topic)

    def send_data(self, data, topic):
        payload = {
            'topic': topic,
            'data': data
        }
        print(payload)
        try:
            response = requests.post('http://localhost:5000/add_data', json=payload)
            if response.status_code == 200:
                print(f'Enviado dados para o tópico: {topic}')
            else:
                print(f'Falha em enviar dados para o tópico: {topic}')
        except Exception as e:
            print(f'Erro em enviar dados para o tópico {topic}: {str(e)}')
