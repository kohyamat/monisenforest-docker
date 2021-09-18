FROM python:3.9-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# RUN apk add --no-cache postgresql-libs \
#  && apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev \
#  && python3 -m pip install -r /backend/requirements.txt --no-cache-dir \
#  && apk --purge del .build-deps

COPY . .
