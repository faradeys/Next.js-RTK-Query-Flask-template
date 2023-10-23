FROM ubuntu:18.04
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev python3-pip python3-dev build-essential libpq-dev iputils-ping git cron
ADD . /srv/flask_api
WORKDIR /srv/flask_api
RUN pip install -r python2_requirements.txt
RUN python3 -m pip install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install -r requirements.txt
ENV LANG C.UTF-8
