FROM --platform=linux/amd64 python:3.9

# set working directory
WORKDIR /usr/src/app
ENV PYTHONPATH=/usr/src/app:/usr/src/app/project

RUN apt-get -y update
RUN apt-get -y install git

# add and install requirements
COPY /services/scraper/requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# add entrypoint.sh
COPY /services/scraper/entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# add app
COPY /services/scraper /usr/src/app

RUN chmod +x /usr/src/app/entrypoint.sh
CMD ["/usr/src/app/entrypoint.sh"]