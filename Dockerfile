#Create our image from Ubuntu 16.04 Xenial Distribution
FROM merklescience/docker-blocksci 
MAINTAINER Nirmal AK <nirmal@merklescience.com>

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN mkdir /app && \
    chmod +x entrypoint.sh

COPY . /app

WORKDIR /app

RUN pip3 install flask==1.0.2 gunicorn==19.9.0

CMD ['./entrypoint.sh']
