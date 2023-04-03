FROM apache/airflow:2.5.2-python3.9
USER root
RUN apt-get update && apt-get install git gcc libpq-dev build-essential -y

USER airflow
COPY requirements.txt /
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /requirements.txt
RUN airflow db upgrade
