#FROM python:3.8.10
#
#LABEL maintainer="a1932a@naver.com"
#
#RUN pip install --upgrade pip
#
#WORKDIR /usr/src/app
#apt-get -y update
#RUN apt install wget
#RUN apt install unzip
#RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN apt -y install ./google-chrome-stable_current_amd64.deb
#RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
#RUN mkdir chrome
#RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/src/chrome
#
#COPY . .
#COPY .env /usr/src/app/dororok-django/.env
#
#RUN pip install -r requirements.txt
#WORKDIR /usr/src/app/dororok-django
#
#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]
#
#EXPOSE 8080

FROM python:3.8.10

LABEL maintainer="a1932a@naver.com"

RUN pip install --upgrade pip

WORKDIR /usr/src/app

RUN apt-get -y update && apt-get -y install wget unzip

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt -y install ./google-chrome-stable_current_amd64.deb

RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip
RUN mkdir -p /usr/src/chrome
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/src/chrome

COPY . .
COPY .env /usr/src/app/dororok-django/.env

RUN pip install -r requirements.txt

WORKDIR /usr/src/app/dororok-django

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]

EXPOSE 8080
