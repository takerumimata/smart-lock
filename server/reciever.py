import os
import json
import cv2
import base64
import numpy as np
from datetime import datetime
from flask import Flask, request, Response
app = Flask(__name__)
count = 0

# 画像を保存するフォルダの作成
image_dir = "./images"
if not os.path.isdir(image_dir):
  os.mkdir(image_dir)

def detect_face(img):
  # 顔検出モデル（'haarcascade_frontalface_default.xml'）は下記リンクからダウンロードできる
  # https://github.com/opencv/opencv/tree/master/data/haarcascades
  face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
  faces = face_cascade.detectMultiScale(img, 1.3, 5)
  return faces

@app.route('/save', methods=['POST'])
def save_image():
    # データの変換処理
    data = request.data.decode('utf-8')
    data_json = json.loads(data)
    image = data_json['image']
    image_dec = base64.b64decode(image)
    data_np = np.fromstring(image_dec, dtype='uint8')
    decimg = cv2.imdecode(data_np, 1)

    # 顔検出してボックスを描画
    gray_img = cv2.cvtColor(decimg, cv2.COLOR_BGR2GRAY)
    # faces = detect_face(gray_img)
    # for (x,y,w,h) in faces:
    #   decimg = cv2.rectangle(decimg,(x,y),(x+w,y+h),(255,0,0),2)

    # 画像ファイルを保存
    global count
    filename = "./images/image{}.png".format(count)
    cv2.imwrite(filename, decimg)
    count += 1

    # HTTPレスポンスを送信
    return Response(response=json.dumps({"message": "{} was saved".format(filename)}), status=200)

if __name__ == '__main__':
    app.run(host='172.17.0.2', port=8080)