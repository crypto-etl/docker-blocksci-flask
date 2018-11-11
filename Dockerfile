#Create our image from Ubuntu 16.04 Xenial Distribution
FROM merklescience/docker-blocksci 
MAINTAINER Nirmal AK <nirmal@merklescience.com>

WORKDIR /app

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY docker-entrypoint.sh /usr/bin/

RUN chmod +x /usr/bin/docker-entrypoint.sh

COPY . /app

RUN pip3 install flask==1.0.2 gunicorn==19.9.0

ENTRYPOINT ["/bin/bash"]

CMD ["/usr/bin/docker-entrypoint.sh"]
