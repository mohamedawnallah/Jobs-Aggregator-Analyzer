FROM python:3.9-alpine
LABEL Data Research Jobs Team 

ENV PIP_NO_CACHE_DIR 1

# Keeps python from the generating .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app/"

COPY ./Pipfile /app
COPY ./Pipfile.lock /app

RUN pip install pipenv
RUN pipenv uninstall --all-dev
RUN pipenv install --ignore-pipfile --system

COPY ./app /app