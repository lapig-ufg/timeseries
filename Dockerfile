FROM python:alpine3.15

LABEL maintainer="Renato Gomes <renatogomessilverio@gmail.com>"

# Clone app and npm install on server
ENV URL_TO_APPLICATION_GITHUB="https://github.com/lapig-ufg/timeseries.git"
ENV BRANCH="main"

RUN /bin/sh -c "apk add --no-cache bash" && \
    apk update && apk add figlet git  && \
    mkdir -p /APP && cd /APP && git clone -b ${BRANCH} ${URL_TO_APPLICATION_GITHUB} && \
    cd timeseries/ && pip3 install -r requirements.txt && \
    echo 'figlet -t "Lapig Docker Timeseries"' >> ~/.bashrc && \
    chmod +x /APP/timeseries/start.sh

WORKDIR /APP

ENTRYPOINT [ "/bin/bash", "-c", "python3 /APP/timeseries/api.py; tail -f /dev/null"]