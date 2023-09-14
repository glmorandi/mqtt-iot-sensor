# mqtt-iot-sensor

Collects and visualizes simulated IoT sensor data (temperature, humidity, vibration, luminosity) with real-time monitoring, a web interface, Discord webhook and MQTT.
  
## Installation

1. **Clone the Repository**

   Open your terminal/command prompt and run the following command:

   ```bash
   git clone https://github.com/glmorandi/mqtt-iot-sensor.git
   cd mqtt-iot-sensor
   ```

2. **Create a Virtual Environment (Optional)**

   Set up a virtual environment to isolate project dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Dependencies**

   Install the project's Python dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

4. **Configuration**

   Configure your MQTT broker, Discord webhook and Flask server by editing the appropriate files in the project.

## Running the Project

1. **Start the Server**

   Run the server by executing the following command:

   ```bash
   python server.py
   ```

2. **Start the Client**

   Run the client by executing the following command:

   ```bash
   python main.py
   ```

3. **Access the Web Interface**

   Open your web browser and navigate to [http://localhost:5000](http://localhost:5000) to access the web interface.
