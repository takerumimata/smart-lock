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

# if __name__ == '__main__':
#   cap = cv2.VideoCapture(0)
#   cap.set(cv2.CAP_PROP_FPS, 30)
#   i = 0
#   while True:
#     _, img = cap.read()
#     if i % 5 == 0:
#       send_image(img)
#     i += 1

image = "logo.png"
img = cv2.imread('logo.png')
send_image(img)
