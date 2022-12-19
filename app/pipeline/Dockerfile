FROM python:3.9-alpine
LABEL Data Research Jobs Team 

ENV PIP_NO_CACHE_DIR 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH "${PYTHONPATH}:/app/"

WORKDIR /app

COPY ./Pipfile /app
COPY ./Pipfile.lock /app

RUN pip install pipenv
RUN pipenv install --ignore-pipfile --system

COPY . /app