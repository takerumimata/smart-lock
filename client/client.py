# client側のプログラム
# 画像を読み込んでサーバにPOSTメソッドで送信するだけ
import socket

PORT = 50000

image = "logo.png"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 第一引数でアドレスファミリ（IPv4）を指定し、第二引数でソケットタイプ（TCP）を指定
client.connect(('172.26.16.6', PORT)) # ipアドレスとport番号を指定して通信する
data = "sending data..." # dataを定義
client.send(data.encode()) # dataを送信


try:

    # open image
    myfile = open(image, 'rb')
    bytes = myfile.read()
    size = len(bytes)

    # send image size to server
    client.sendall("SIZE %s" % size)
    answer = client.recv(4096)

    print 'answer = %s' % answer

    # send image to server
    if answer == 'GOT SIZE':
        client.sendall(bytes)

        # check what server send
        answer = client.recv(4096)
        print 'answer = %s' % answer

        if answer == 'GOT IMAGE' :
            client.sendall("BYE BYE ")
            print 'Image successfully send to server'

    myfile.close()

    data = "sending complete!" # dataを定義
    client.send(data.encode()) # dataを送信
finally:
    client.close()


# response = client.recv(4096)
# print(response)
