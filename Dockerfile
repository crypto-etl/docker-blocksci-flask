#Create our image from Ubuntu 16.04 Xenial Distribution
FROM allenday/blocksci-docker:v0.6
MAINTAINER Nirmal AK <nirmal@merklescience.com>

WORKDIR /app
# Commit Hash for Latest Release - 48db2c208303fadabaf6bf50c78221087797e326

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

COPY docker-entrypoint.sh /usr/bin/

RUN chmod +x /usr/bin/docker-entrypoint.sh

COPY . /app

RUN pip3 install flask==1.0.2 gunicorn==19.9.0 mock==2.0.0 python-dateutil==2.6.1 pytz==2017.2

ENTRYPOINT ["/bin/bash"]

CMD ["/usr/bin/docker-entrypoint.sh"]
