FROM ubuntu:18.04

RUN apt-get update && apt-get -y install software-properties-common python3-pip
RUN add-apt-repository ppa:kivy-team/kivy
RUN apt-get update && apt-get -y install python3-kivy
ADD requirements.txt /
RUN pip3 install -r requirements.txt
ADD * /
ENTRYPOINT python3 main.py
