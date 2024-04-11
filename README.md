# Hand Movement Recognition and Control System

## Overview
This project captures hand movement using Python scripts, stores the data in a MongoDB cluster, and controls servo motors based on the captured finger angles using an Arduino. It consists of three main components:

1. **host.py**: Python script to capture hand movement data and send it to the MongoDB cluster.
2. **client.py**: Python script to extract the data from the MongoDB cluster and control servo motors.
3. **servo.ino**: Arduino sketch to receive data from the MongoDB cluster and move servo motors accordingly.

## Instructions

### Prerequisites
- Install Python 3.x: [Download Python](https://www.python.org/downloads/)
- Install MongoDB: [Download MongoDB](https://www.mongodb.com/try/download/community)
- Install Arduino IDE: [Download Arduino IDE](https://www.arduino.cc/en/software)

### Setting up MongoDB Cluster
1. Sign up for a MongoDB Atlas account: [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster and obtain the connection string.
3. Replace the connection string in `host.py` and `client.py` with your MongoDB cluster connection string.

### Running the Host Script
1. Open a terminal and navigate to the project directory.
2. Run the following command to install required Python dependencies:
   ```
   pip install pymongo
   ```
3. Run the `host.py` script to capture hand movement data and send it to the MongoDB cluster:
   ```
   python host.py
   ```

### Running the Client Script
1. Open another terminal window and navigate to the project directory.
2. Run the following command to install required Python dependencies:
   ```
   pip install pymongo
   ```
3. Run the `client.py` script to extract data from the MongoDB cluster and control servo motors:
   ```
   python client.py
   ```

### Uploading Arduino Sketch
1. Open the `servo.ino` sketch in the Arduino IDE.
2. Connect your Arduino board to your computer via USB.
3. Select the appropriate board and port in the Arduino IDE.
4. Upload the sketch to your Arduino board.

## Additional Notes
- Ensure that your MongoDB cluster is properly configured and accessible from both the host and client machines.
- Adjust the servo motor pins in the Arduino sketch (`servo.ino`) to match your hardware setup.

## License
This project is licensed under the [MIT License](LICENSE).


