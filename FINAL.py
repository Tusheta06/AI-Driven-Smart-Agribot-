import time
import threading
import math
import cv2
import cvzone
from ultralytics import YOLO
import paho.mqtt.client as mqtt
from Adafruit_IO import MQTTClient

# Adafruit IO Credentials
AIO_USERNAME = "B2112"
AIO_KEY = "aio_SXoc91Oyl0czDaXwtFqR8997qK7I"
AIO_FEED = "info"

def connected(client):
    print("Connected to Adafruit IO!")
    client.subscribe(AIO_FEED)

def disconnected(client):
    print("Disconnected from Adafruit IO! Reconnecting...")
    time.sleep(5)
    client.connect()

def message(client, feed_id, payload):
    print(f"Received data from {feed_id}: {payload}")

# Create MQTT client
client = MQTTClient(AIO_USERNAME, AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.connect()
client.loop_background()

def update_value(value):
    try:
        print(f"Sending value {value} to {AIO_FEED}")
        client.publish(AIO_FEED, value)
    except Exception as e:
        print("Error publishing data:", e)

class VideoStream:
    def __init__(self, src=0):
        self.stream = cv2.VideoCapture(src)
        self.ret, self.frame = self.stream.read()
        self.stopped = False

    def start(self):
        threading.Thread(target=self.update, args=()).start()
        return self

    def update(self):
        while not self.stopped:
            if not self.ret:
                self.stop()
            else:
                self.ret, self.frame = self.stream.read()

    def read(self):
        return self.frame

    def stop(self):
        self.stopped = True
        self.stream.release()

cap = VideoStream('http://192.168.190.82:8080/video').start()

model = YOLO('leaf.pt')
classnames = [
    "Apple Scab Leaf", "Apple leaf", "Apple rust leaf", "Bell_pepper leaf",
    "Bell_pepper leaf spot", "Blueberry leaf", "Cherry leaf", "Corn Gray leaf spot",
    "Corn leaf blight", "Corn rust leaf", "Peach leaf", "Potato leaf", "Potato leaf early blight",
    "Potato leaf late blight", "Raspberry leaf", "Soyabean leaf", "Soybean leaf",
    "Squash Powdery mildew leaf", "Strawberry leaf", "Tomato Early blight leaf",
    "Tomato Septoria leaf spot", "Tomato leaf", "Tomato leaf bacterial spot",
    "Tomato leaf late blight", "Tomato leaf mosaic virus", "Tomato leaf yellow virus",
    "Tomato mold leaf", "Tomato two spotted spider mites leaf", "grape leaf", "grape leaf black rot"
]

frame_skip = 5
frame_count = 0
display_width = 480
display_height = 360

while True:
    frame = cap.read()
    if frame is None:
        print("Failed to grab frame")
        break
    
    frame_count += 1
    if frame_count % frame_skip == 0:
        frame = cv2.resize(frame, (640, 480))
        result = model(frame, stream=True)
        for info in result:
            boxes = info.boxes
            for box in boxes:
                confidence = math.ceil(box.conf[0] * 100)
                Class = int(box.cls[0])

                if confidence > 30:
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 5)
                    label = f'{classnames[Class]} {confidence}%'
                    cvzone.putTextRect(frame, label, [x1 + 8, y1 + 100], scale=1.5, thickness=2)
                    print(f'Object: {classnames[Class]}, Confidence: {confidence}%')

                    # Fertilizer recommendations and Adafruit IO updates
                    if classnames[Class] == "Apple Scab Leaf":
                        recommendation = "Apple Scab Leaf detected: Apply NPK 10-10-10 fertilizer and fungicide"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Apple leaf":
                        recommendation = "Apple leaf detected: Apply NPK 15-5-10 fertilizer"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Apple rust leaf":
                        recommendation = "Apple rust leaf detected: Apply NPK 10-10-10 with sulfur-based fungicide"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Bell_pepper leaf":
                        recommendation = "Bell_pepper leaf detected: Apply NPK 5-10-10 fertilizer"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Bell_pepper leaf spot":
                        recommendation = "Bell_pepper leaf spot detected: Apply NPK 5-10-10 with copper fungicide"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Blueberry leaf":
                        recommendation = "Blueberry leaf detected: Apply NPK 12-4-8 fertilizer"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Cherry leaf":
                        recommendation = "Cherry leaf detected: Apply NPK 10-10-10 fertilizer"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Corn Gray leaf spot":
                        recommendation = "Corn Gray leaf spot detected: Apply NPK 20-10-10 with fungicide"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Corn leaf blight":
                        recommendation = "Corn leaf blight detected: Apply NPK 20-10-10 with systemic fungicide"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Corn rust leaf":
                        recommendation = "Corn rust leaf detected: Apply NPK 20-10-10 with rust-specific fungicide"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Peach leaf":
                        recommendation = "Peach leaf detected: Apply NPK 10-10-10 fertilizer"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Potato leaf":
                        recommendation = "Potato leaf detected: Apply NPK 5-10-15 fertilizer"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Potato leaf early blight":
                        recommendation = "Potato leaf early blight detected: Apply NPK 5-10-15 with chlorothalonil"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Potato leaf late blight":
                        recommendation = "Potato leaf late blight detected: Apply NPK 5-10-15 with systemic fungicide"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Raspberry leaf":
                        recommendation = "Raspberry leaf detected: Apply NPK 10-10-10 fertilizer"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Soyabean leaf" or classnames[Class] == "Soybean leaf":
                        recommendation = "Soybean leaf detected: Apply NPK 3-18-18 fertilizer"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Squash Powdery mildew leaf":
                        recommendation = "Squash Powdery mildew leaf detected: Apply NPK 5-10-10 with sulfur"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Strawberry leaf":
                        recommendation = "Strawberry leaf detected: Apply NPK 10-10-10 fertilizer"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Tomato Early blight leaf":
                        recommendation = "Tomato Early blight leaf detected: Apply NPK 5-10-10 with fungicide"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Tomato Septoria leaf spot":
                        recommendation = "Tomato Septoria leaf spot detected: Apply NPK 5-10-10 with chlorothalonil"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Tomato leaf":
                        recommendation = "Tomato leaf detected: Apply NPK 5-10-10 fertilizer"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Tomato leaf bacterial spot":
                        recommendation = "Tomato leaf bacterial spot detected: Apply NPK 5-10-10 with copper"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Tomato leaf late blight":
                        recommendation = "Tomato leaf late blight detected: Apply NPK 5-10-10 with systemic fungicide"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Tomato leaf mosaic virus":
                        recommendation = "Tomato leaf mosaic virus detected: Apply NPK 5-10-10 and remove infected plants"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Tomato leaf yellow virus":
                        recommendation = "Tomato leaf yellow virus detected: Apply NPK 5-10-10 and control whiteflies"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Tomato mold leaf":
                        recommendation = "Tomato mold leaf detected: Apply NPK 5-10-10 with fungicide"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "Tomato two spotted spider mites leaf":
                        recommendation = "Tomato spider mites detected: Apply NPK 5-10-10 with miticide"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "grape leaf":
                        recommendation = "grape leaf detected: Apply NPK 10-10-10 fertilizer"
                        print(recommendation)
                        update_value(recommendation)
                    elif classnames[Class] == "grape leaf black rot":
                        recommendation = "grape leaf black rot detected: Apply NPK 10-10-10 with fungicide"
                        print(recommendation)
                        update_value(recommendation)

        display_frame = cv2.resize(frame, (display_width, display_height))
        cv2.imshow('frame', display_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.stop()
cv2.destroyAllWindows()