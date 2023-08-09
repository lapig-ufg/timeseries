FROM python:3.10.12-alpine3.17

LABEL maintainer="Jairo Matos da Rocha <rjairo@geocodelabs.com>"

# Clone app and npm install on server
ENV URL_TO_APPLICATION_GITHUB="https://github.com/lapig-ufg/timeseries.git"
ENV LAPIG_BRANCH="develop"

ENV LAPIG_APP_DEBUG=true  \
    LAPIG_API_NAME=timeseries-indexs-dev \
    ENV_FOR_DYNACONF=${LAPIG_BRANCH}

RUN /bin/sh -c "apk add --no-cache bash" && \
    apk update && apk add figlet git curl wget  && \
    mkdir -p /APP && cd /APP && git clone -b ${LAPIG_BRANCH} ${URL_TO_APPLICATION_GITHUB} && \
    cd timeseries/ && pip3 install -r requirements.txt && \
    echo 'figlet -t "Lapig Docker Timeseries"' >> ~/.bashrc && \
    chmod +x /APP/timeseries/api.py

WORKDIR /APP

CMD [ "/bin/bash", "-c", "gunicorn -c gunicorn_conf.py  app.server:app"]
