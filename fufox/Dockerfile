# pull official base image
FROM python:3.7.4-buster

USER root

# set work directory
WORKDIR /home

RUN wget http://sourceforge.net/projects/netcat/files/netcat/0.7.1/netcat-0.7.1.tar.gz
RUN tar -xzvf netcat-0.7.1.tar.gz
WORKDIR /home/netcat-0.7.1
RUN ./configure
RUN make
RUN make install
WORKDIR /home
RUN rm -rf netcat-*


# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# get the contents
COPY . /home/fufox/

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv

# install psycopg2
RUN apt-get install libpq-dev
RUN pip install psycopg2

# set the work directory inside fufox
WORKDIR /home/fufox

RUN pipenv install --skip-lock --system --dev

# copy entrypoint.sh
COPY ./entrypoint.sh /home/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/home/entrypoint.sh"]


