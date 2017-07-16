FROM python:2.7
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y netcat
RUN mkdir -p /app
WORKDIR /app
ADD requirements.txt /app/
RUN pip install --exists-action s -r requirements.txt
ADD . /app/
