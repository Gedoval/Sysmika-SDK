# syntax=docker/dockerfile:1
FROM ubuntu:20.04
ENV DEBIAN_FRONTEND noninteractive
RUN export FLASK_APP='run:run_app()'

WORKDIR /sysmika
RUN apt update -y && apt upgrade -y && apt-get update -y && apt install git python3.9 python3-venv python3-pip -y

RUN pip install pipenv
RUN git clone https://github.com/Gedoval/Sysmika-SDK.git
RUN cd Sysmika-SDK && pipenv install --system
RUN cd Sysmika-SDK/src/integrations/mercadolibre/inbound && flask run