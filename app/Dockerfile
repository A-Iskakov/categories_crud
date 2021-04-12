FROM python:3.9.4-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/

COPY . /code/
RUN cd /code;pip install -r requirements.txt; python manage.py makemigrations; python manage.py migrate; python manage.py collectstatic;
