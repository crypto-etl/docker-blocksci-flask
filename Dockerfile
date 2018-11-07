#Create our image from Ubuntu 16.04 Xenial Distribution
FROM merklescience/docker-blocksci 
MAINTAINER Nirmal AK <nirmal@merklescience.com>

RUN mkdir /app

COPY . /app

WORKDIR /app

RUN pip3 install -r flask==1.0.2
