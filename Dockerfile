FROM python:3.10

LABEL maintainer="a1932a@naver.com"

RUN pip install --upgrade pip

WORKDIR /usr/src/app

COPY . .
COPY .env /usr/src/app/dororok-django/.env

RUN pip install -r requirements.txt
WORKDIR /usr/src/app/dororok-django

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]

EXPOSE 8080
