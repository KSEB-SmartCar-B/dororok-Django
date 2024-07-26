FROM python:3.9

WORKDIR /var/jenkins_home/workspace/Django/dororok-Django

COPY requriements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DJANGO_SETTINGS_MODULE=dororok-Django.settingspy

EXPOSE 9999

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:9999"]