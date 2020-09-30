#!/usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import sys, os
import numpy as np
import cv2
import time
import json
import base64
import requests

def send_image(img):
    # 画像を送信可能な形式に変換してJSONに格納
    _, encimg = cv2.imencode(".png", img)
    img_str = encimg.tostring()
    img_byte = base64.b64encode(img_str).decode("utf-8")
    img_json = json.dumps({'image': img_byte}).encode('utf-8')

    # HTTPリクエストを送信
    response = requests.post("http://172.26.16.6:8080/save", data=img_json) # 物理サーバ: 172.26.16.6 , docker: 172.17.0.2
    print('{0} {1}'.format(response.status_code, json.loads(response.text)["message"]))


cam = cv2.VideoCapture(0) # VideoCaptureのインスタンスを作成する。(複数のカメラがあるときは引数で識別)

count = 0
cascade_path = "/home/pi/.local/lib/python3.5/site-packages/cv2/data/haarcascade_frontalface_default.xml"
face_detector = cv2.CascadeClassifier(cascade_path)

while(True):
        ret, img = cam.read()
        img = cv2.flip(img, 1) # flip video image vertically
        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(img, 1.3, 5)
        print("detecting..")
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)
            count += 1
            # Save the captured image into the datasets folder
            cv2.imwrite("checkpic/" + str(count) + ".jpg", img[y:y+h,x:x+w])
            # cv2.imshow('image', img)
            send_image(img[y:y+h, x:x+w])

        if count >= 10:
            break
