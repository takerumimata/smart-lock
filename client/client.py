# client側のプログラム
# 画像を読み込んでサーバにPOSTメソッドで送信するだけ
import socket

PORT = 50000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 第一引数でアドレスファミリ（IPv4）を指定し、第二引数でソケットタイプ（TCP）を指定
client.connect(('127.0.0.1', PORT)) # ipアドレスとport番号を指定して通信する
data = "hello!" # dataを定義
client.send(data.encode()) # dataを送信

response = client.recv(4096)
print(response)
