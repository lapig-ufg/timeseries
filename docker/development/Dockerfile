FROM python:3.10.12-alpine3.17

LABEL maintainer="Jairo Matos da Rocha <jairo@geocodelabs.com>"

# Clone app and npm install on server
ENV URL_TO_APPLICATION_GITHUB="https://github.com/lapig-ufg/timeseries.git"
ENV LAPIG_BRANCH="develop"

ENV LAPIG_APP_DEBUG=true  \
    LAPIG_API_NAME=timeseries-indexs-dev \
    ENV_FOR_DYNACONF=${LAPIG_BRANCH}

WORKDIR /APP

COPY ./ssh /root/.ssh 


COPY ./start.sh /APP
COPY ./version.jso* /APP
COPY ./.env /APP/.env

RUN /bin/sh -c "apk add --no-cache bash" && \
    apk update && apk add figlet git curl wget  && \
    mkdir -p /APP && cd /APP && git clone -b ${LAPIG_BRANCH} ${URL_TO_APPLICATION_GITHUB} && \
    cd timeseries/ && pip3 install -r requirements.txt && \
    echo 'figlet -t "Lapig Docker Timeseries"' >> ~/.bashrc && \
    chmod +x /APP/start.sh



CMD [ "sh", "/var/www/start.sh" ]
