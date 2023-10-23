FROM postgres:14
ENV LANG C.UTF-8
RUN apt-get update -y
RUN apt-get install -y nano cifs-utils ssh rsync cron
ADD init.sql /docker-entrypoint-initdb.d
