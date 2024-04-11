import pymongo
import cv2
import numpy as np
import time
import mediapipe as mp
import urllib.parse



username = urllib.parse.quote_plus('Host Laptop username')
password = urllib.parse.quote_plus('Host laptop password')


# MongoDB configuration
client = pymongo.MongoClient('mongodb+srv://' + username + ':' + password +
                             '@Cluster_name.mongodb.net/?retryWrites=true&w=majority&appName=ClusterFrstPrjct')
db = client['hand_tracking_database']
collection = db['hand_angle_readings']

# Mediapipe configuration
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)

# Define closest and farthest distances for each finger
thumb_closest = 0.055
thumb_farthest = 0.235

index_closest = 0.055
index_farthest = 0.312

middle_closest = 0.06
middle_farthest = 0.345

ring_closest = 0.06
ring_farthest = 0.325

pinky_closest = 0.055
pinky_farthest = 0.240

# Function to map distance to angle for each finger
def map_distance_to_angle(distance, closest, farthest):
    flexion_angle = 180 - (distance - closest) / (farthest - closest) * 180
    return min(180, max(0, flexion_angle))

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5, max_num_hands=1) as hands:
    prev_time = 0
    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        # BGR 2 RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)

        height, width, _ = image.shape
        border_size = 185
        cv2.rectangle(image, (width // 2 - border_size, height // 2 - border_size),
                      (width // 2 + border_size, height // 2 + border_size), (255, 0, 0), 2)

        # Set flag
        image.flags.writeable = False

        # Detections
        results = hands.process(image)

        # Set flag to true
        image.flags.writeable = True

        # RGB 2 BGR
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                thumb_distance = np.linalg.norm(np.array([hand_landmarks.landmark[4].x, hand_landmarks.landmark[4].y]) -
                                                np.array([hand_landmarks.landmark[5].x, hand_landmarks.landmark[5].y]))
                index_distance = np.linalg.norm(np.array([hand_landmarks.landmark[8].x, hand_landmarks.landmark[8].y]) -
                                                np.array([hand_landmarks.landmark[5].x, hand_landmarks.landmark[5].y]))
                middle_distance = np.linalg.norm(
                    np.array([hand_landmarks.landmark[12].x, hand_landmarks.landmark[12].y]) -
                    np.array([hand_landmarks.landmark[9].x, hand_landmarks.landmark[9].y]))
                ring_distance = np.linalg.norm(np.array([hand_landmarks.landmark[16].x, hand_landmarks.landmark[16].y]) -
                                               np.array([hand_landmarks.landmark[13].x, hand_landmarks.landmark[13].y]))
                pinky_distance = np.linalg.norm(
                    np.array([hand_landmarks.landmark[20].x, hand_landmarks.landmark[20].y]) -
                    np.array([hand_landmarks.landmark[17].x, hand_landmarks.landmark[17].y]))

                # Map distances to angles
                thumb_angle = map_distance_to_angle(thumb_distance, thumb_closest, thumb_farthest)
                index_angle = map_distance_to_angle(index_distance, index_closest, index_farthest)
                middle_angle = map_distance_to_angle(middle_distance, middle_closest, middle_farthest)
                ring_angle = map_distance_to_angle(ring_distance, ring_closest, ring_farthest)
                pinky_angle = map_distance_to_angle(pinky_distance, pinky_closest, pinky_farthest)

                # Store finger angle readings in MongoDB
                current_time = time.time()
                if current_time - prev_time >= 0.1:
                    data = {
                        "thumb_angle": thumb_angle,
                        "index_angle": index_angle,
                        "middle_angle": middle_angle,
                        "ring_angle": ring_angle,
                        "pinky_angle": pinky_angle,
                        "timestamp": current_time
                    }
                    collection.insert_one(data)
                    print("Inserted data:", data)
                    prev_time = current_time

        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
