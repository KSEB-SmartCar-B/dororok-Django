FROM python:3.8.10

LABEL maintainer="a1932a@naver.com"

RUN pip install --upgrade pip

WORKDIR /usr/src/app

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8080"]

EXPOSE 8080
