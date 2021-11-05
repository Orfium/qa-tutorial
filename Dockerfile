FROM python:3.8-slim-buster

MAINTAINER konstantinos.konstantakopoulos@orfium.com


# Create a new user. Password is not required
RUN adduser --disabled-password --gecos '' testuser \
  &&  apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /qa-project

COPY requirements.txt requirements.txt

COPY wait_for_local_server.sh /wait_for_local_server.sh
RUN chmod +x /wait_for_local_server.sh

RUN pip install --no-cache-dir -r requirements_dev.txt

COPY . .

RUN chown -R testuser .

USER testuser

WORKDIR /qa-project/api_tests/tests
