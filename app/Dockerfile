FROM python:3.9.4-alpine
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/

COPY . /code/
RUN apk update  && apk add postgresql-dev gcc python3-dev musl-dev
RUN cd /code;pip install -r requirements.txt;  python manage.py collectstatic;
ENTRYPOINT ["sh", "/code/entrypoint.sh"]