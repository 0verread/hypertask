# pull official base image
FROM python:3.10-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create the app directory - and switch to it
RUN mkdir -p /app
WORKDIR /app

# install dependencies
COPY requirements.txt /tmp/requirements.txt
RUN set -ex && \
    pip3 install --upgrade pip && \
    pip3 install -r /tmp/requirements.txt

# copy project
COPY . /app/

# expose port 8000
EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "2", "config.wsgi:application"]