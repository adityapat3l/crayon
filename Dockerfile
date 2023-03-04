FROM python:3.8

WORKDIR /app
ENV PYTHONPATH=/app
RUN apt-get update
RUN apt-get -y install git

COPY requirements.txt /requirements.txt

CMD python --version
