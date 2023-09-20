import os
import threading
import time
from io import BytesIO
from collections import deque
import numpy as np
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, jsonify, Response

app = Flask(__name__)
app.config['STATIC_FOLDER'] = 'static'

# Classe para receber e armazenar dados com limite de quantidade de dados
class DataReceiver:
    def __init__(self, max_data_points=100):
        self.data = {}
        self.max_data_points = max_data_points
        self.lock = threading.Lock()

    def receive_data(self, topic, value):
        # Use deque para armazenar os dados
        with self.lock:
            topic_data = self.data.setdefault(topic, deque(maxlen=self.max_data_points))
            topic_data.append(value)

data_receiver = DataReceiver()

# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Rota para adicionar dados
@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.get_json()
    topic, value = data.get('topic'), data.get('data')

    if topic is not None and value is not None:
        data_receiver.receive_data(topic, value)
        return jsonify(status='Data received successfully'), 200
    else:
        return jsonify(error='Invalid data format'), 400

# Rota para obter dados por tópico
@app.route('/get_data', methods=['GET'])
def get_data():
    topic = request.args.get('topic')
    
    if topic is not None:
        with data_receiver.lock:
            data = list(data_receiver.data.get(topic, []))
        return jsonify(data=data), 200
    else:
        return jsonify(error='Topic not specified'), 400

# Rota para obter todos os dados
@app.route('/get_all_data', methods=['GET'])
def get_all_data():
    with data_receiver.lock:
        all_data = {topic: list(data) for topic, data in data_receiver.data.items()}
    return jsonify(all_data=all_data), 200

# Função para gerar o gráfico
def generate_plot(data, topic, smoothing=5):
    plt.figure(figsize=(10, 6))  # Ajuste o tamanho da figura

    # Se a suavização estiver ativada
    if smoothing > 0:
        smooth_data = np.convolve(data, np.ones(smoothing)/smoothing, mode='same')  # Suavização
        plt.plot(smooth_data, color='b', linewidth=2, marker='o', markersize=6, label='Smooth value')
        plt.plot(data, linestyle='--', alpha=0.5, linewidth=2, label='Real value')
    else:
        plt.plot(data, color='b', linewidth=2, marker='o', markersize=6, label='Real value')

    plt.xlabel('Tempo', fontsize=12)
    plt.ylabel('Valor', fontsize=12)
    plt.title(f'Gráfico para {topic}', fontsize=14)

    plt.grid(True, linestyle='--', alpha=0.6, which='both', axis='both', color='gray')

    plt.xticks(fontsize=10)  # Tamanho da fonte dos rótulos do eixo x
    plt.yticks(fontsize=10)  # Tamanho da fonte dos rótulos do eixo y

    plt.legend(fontsize=12)  # Adicione a legenda ao gráfico

    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=300)
    buffer.seek(0)

    return buffer


# Rota para gerar e enviar gráficos
@app.route('/plot/<topic>')
def plot_data(topic):
    if topic in data_receiver.data:
        data = data_receiver.data[topic]
        buffer = generate_plot(data, topic)
        
        def generate():
            yield buffer.read()

        return Response(generate(), mimetype='image/png')
    else:
        return jsonify(error='Tópico não encontrado'), 404

# Função para atualizar periodicamente os gráficos
def update_plots():
    while True:
        time.sleep(5)
        with data_receiver.lock:
            for topic, data in data_receiver.data.items():
                buffer = generate_plot(data, topic)
                filename = os.path.join(app.config['STATIC_FOLDER'], f'plot_{topic}.png')
                plt.savefig(filename, format='png')

if __name__ == '__main__':
    # Iniciar thread de atualização de gráficos em segundo plano
    update_thread = threading.Thread(target=update_plots)
    update_thread.daemon = True
    update_thread.start()
    
    # Garantir que o folder static existe
    if not os.path.exists(app.config['STATIC_FOLDER']):
        os.makedirs(app.config['STATIC_FOLDER'])

    # Iniciar o aplicativo Flask em modo de depuração
    app.run(debug=True)
