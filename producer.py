import sys
import datetime
import cv2
from kafka import KafkaProducer
from json import dumps
import numpy as np
import base64

import random #for randomly generating camera_ids
topic = "hello"

def publish_camera():

    # Start up producer
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'],value_serializer=lambda x: x.encode('utf-8'))

    message = None
    camera = cv2.VideoCapture(-1)
    d=0
    while(True):
        success, frame = camera.read()
        #(640,480)
        frame = cv2.resize(frame,(300,200))
        rows = 480
        cols = 640
        cam_id = random.randint(1,30)
        ret, buffer = cv2.imencode('.jpg', frame)
        # mm = "string in caves"
        data = base64.b64encode(buffer)
        message = {
            "camera_id" : cam_id,
            "date" : str(datetime.date.today()),
            "time":datetime.datetime.now().strftime("%X"),
            "rows" : rows,
            "cols" : cols,
            "data" : str(data)
        }
        # print(message)
        json_data = dumps(message)
        print(json_data)
        producer.send(topic, value=json_data)
        producer.flush()
        print('Message published successfully.')        
        
        #break
    
    camera.release()


if __name__ == '__main__':
    print("publishing feed!")
    publish_camera()
