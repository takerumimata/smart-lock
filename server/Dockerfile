FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y tzdata
# timezone setting
ENV TZ=Asia/Tokyo
# pythonとpipちゃん
RUN apt update && apt install -y python3-pip
RUN apt install python3
RUN apt-get remove python-pip python3-pip -y && apt-get install -y wget
# opencv-devのインストール
RUN apt-get update -y && apt-get install -y libopencv-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN apt update -y  && apt install curl -y
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py
# TensorflowとOpencvのインストール
RUN pip3 install numpy tensorflow-gpu opencv-python

# kerasとsklearnのインストール
RUN pip3 install keras
RUN pip3 install scikit-learn
RUN pip3 install pillow
