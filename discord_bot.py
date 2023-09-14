import requests
import time
import numpy as np
import os

class DiscordWebhook:
    def __init__(self, webhook_url, username=None, avatar_url=None):
        self.webhook_url = webhook_url
        self.username = username
        self.avatar_url = avatar_url

    def request_plot_update(self, topic):
        # Solicita uma atualização do gráfico para um tópico específico no servidor local.
        url = f"http://localhost:5000/plot/{topic}"
        response = requests.get(url)
        
        return response.status_code

    def send_message(self, content):
        # Envia uma mensagem de texto para o webhook do Discord.
        payload = {
            'content': content,
            'username': self.username,
            'avatar_url': self.avatar_url
        }
        self._send_request(payload)
            
    def send_image(self, image_path, content=None):
        # Verifica se o arquivo de imagem existe
        if not os.path.exists(image_path):
            print(f"Imagem não existe: {image_path}")
            if self.request_plot_update(image_path.split("_")[1].split(".")[0]) == 200:
                print("Imagem gerada")
            else:
                print("Erro ao gerar a imagem")
                return

        with open(image_path, 'rb') as image_file:
            image_data = image_file.read()

        files = {'file': ('image.png', image_data)}

        payload = {
            'content': content,
            'username': self.username,
            'avatar_url': self.avatar_url
        }

        self._send_request(payload, files)

    def _send_request(self, payload, files=None):
        # Envia uma solicitação POST para o webhook do Discord.
        try:
            response = requests.post(self.webhook_url, data=payload, files=files)
            response.raise_for_status()
            print('Mensagem enviada com sucesso!')
        except requests.exceptions.RequestException as e:
            print(f'Erro ao enviar a mensagem: {str(e)}')
    
    def get_all_data(self):
        # Obtém todos os dados do servidor local.
        url = f"http://localhost:5000/get_all_data"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json().get('all_data', {})
            return data
        else:
            return None
        
    def alert_handler(self):
        # Monitora os dados e envia alertas se condições específicas forem atendidas.
        while True:
            all_data = self.get_all_data()
            if all_data:
                for topic, data in all_data.items():
                    # Consideramos a média dos últimos 5 valores
                    data = np.mean(data[-5:])
                    if topic.endswith("humidity") and data < 10.0:
                        self.send_message(f'Umidade está abaixo do valor de 10, valor atual: {int(data)}')
                    elif topic.endswith("temperature") and data > 50.0:
                        self.send_message(f'Temperatura está acima do valor de 50, valor atual: {int(data)}')
                    elif topic.endswith("vibration") and data > 1.5:
                        self.send_message(f'Vibração está acima do valor de 1.5, valor atual: {round(data, 1)}')
                    elif topic.endswith("luminosity") and data > 800:
                        self.send_message(f'Luminosidade está acima do valor de 800, valor atual: {int(data)}')
            else:
                print("Falha ao ler os dados do servidor.")
            time.sleep(1)

    def send_plots(self, interval):
        # Envia gráficos periodicamente para o webhook do Discord.
        while True:
            self.send_image("static/plot_humidity.png")
            self.send_image("static/plot_temperature.png")
            self.send_image("static/plot_vibration.png")
            self.send_image("static/plot_luminosity.png")
            time.sleep(int(interval))
