import pymongo
import serial
import time
import urllib.parse

username = urllib.parse.quote_plus('Client laptop username')
password = urllib.parse.quote_plus('Client laptop @ password')

# Connect to MongoDB Atlas

client = pymongo.MongoClient('mongodb+srv://' + username + ':' + password +
                             '@cluster_name.mongodb.net/?retryWrites=true&w=majority&appName=Cluster name')
db = client.get_database('hand_tracking_database')
collection = db.get_collection('hand_angle_readings')

# Connect to Arduino

ser = serial.Serial('COMX', 9600)  # Replace 'COMX' with the appropriate port

while True:
    # Retrieve latest finger angle readings from MongoDB
    latest_data = collection.find_one(sort=[('_id', pymongo.DESCENDING)])
    thumb_angle = latest_data['thumb_angle']
    index_angle = latest_data['index_angle']
    middle_angle = latest_data['middle_angle']
    ring_angle = latest_data['ring_angle']
    pinky_angle = latest_data['pinky_angle']

    # Send angle data to Arduino
    command = f"{thumb_angle},{index_angle},{middle_angle},{ring_angle},{pinky_angle}\n"
    ser.write(command.encode())
    print("Sent data:", command.strip())

    time.sleep(0.1)  # Wait for 1 second before fetching the next reading

