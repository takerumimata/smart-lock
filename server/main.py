import os
import json
import cv2
import base64
import numpy as np
import keras
from keras.models import load_model
from datetime import datetime
from flask import Flask, request, Response
from PIL import Image
from flask import Flask, request, Response
import json
import urllib.request
app = Flask(__name__)
count = 0

imsize = (226,226)
model = load_model('./cte_facedetect3.h5')

def cv2pil(image):
    ''' OpenCV型 -> PIL型 '''
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image

@app.route('/unlock', methods=['POST'])
def predict_and_open():
    # データの変換処理
    data = request.data.decode('utf-8')
    data_json = json.loads(data)
    image = data_json['image']
    image_dec = base64.b64decode(image)
    data_np = np.fromstring(image_dec, dtype='uint8')
    decimg = cv2.imdecode(data_np, 1)

    # pillowに変換
    img_pil = cv2pil(decimg)
    img = img_pil.resize(imsize)
    # 画像データをnumpy配列の形式に変更
    img = np.asarray(img)
    img = img / 255.0
    prd = model.predict(np.array([img]))
    is_accept = prd[0][0]
    if is_accept > 0.9:
        url = 'https://api.candyhouse.co/public/sesame/{device_id}'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': '{our_api_key}',
        }

        data = {
            "command": "unlock",
        }

        req = urllib.request.Request(url, json.dumps(data).encode(), headers)
        with urllib.request.urlopen(req) as res:
            body = res.read()
    # HTTPレスポンスを送信
    return Response(response=json.dumps({"message": "{} is prediction".format(prd)}), status=200)

# pic = "./images/tanahashi.jpg"
# img = load_image(pic)

if __name__ == '__main__':
    app.run(host='172.17.0.2', port=8080)