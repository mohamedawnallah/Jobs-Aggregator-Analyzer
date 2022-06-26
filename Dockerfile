FROM python:3.9-alpine
LABEL Data Research Jobs Team 

# Do not cache python packages
ENV PIP_NO_CACHE_DIR 1

# Keeps python from the generating .pyc files
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Intialize the current working directory in the container
WORKDIR /app

# Set the PYTHONPATH to the app directory
ENV PYTHONPATH "${PYTHONPATH}:/app/"

# Transfering the dependencies to the container
COPY ./Pipfile /app
COPY ./Pipfile.lock /app

# Ignore Pipfile when installing, using the Pipfile.lock
RUN pip install pipenv
RUN pipenv install --ignore-pipfile --system

# Transfering the code to the container
COPY ./app /app