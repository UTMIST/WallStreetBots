FROM python:3.10-buster
ENV PYTHONUNBUFFERED=1
RUN pip install --upgrade pip
# required for psycopg2 if using alpine base image
# RUN apk update && apk add g++ postgresql-dev gcc python3-dev musl-dev libffi-dev jpeg-dev zlib-dev
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY . /app
# RUN python manage.py migrate