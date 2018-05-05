FROM python:3.6
ENV PYTHONUNBUFFERED 1
ADD requirements.txt /tmp/requirements.txt
RUN apt-get update && \
    apt-get install -y python3-gdal postgis && \
    pip install -r /tmp/requirements.txt
