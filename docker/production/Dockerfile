FROM registry.lapig.iesa.ufg.br/lapig-images-prod/download-minio:base as python-base

LABEL maintainer="Jairo Matos da Rocha <jairo@geocodelabs.com>"

# Clone app and npm install on server

ENV URL_TO_APPLICATION_GITHUB="https://github.com/lapig-ufg/timeseries.git" \
    LAPIG_BRANCH="main" \
    LAPIG_APP_DEBUG=false  \
    LAPIG_API_NAME=timeseries-indexs-dev \
    ENV_FOR_DYNACONF=${LAPIG_BRANCH} \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv" \
    DOCKER_BASE_PATH="./docker/production"


###############################################
# Production Image
###############################################
FROM python-base as production

WORKDIR /APP

COPY ${DOCKER_BASE_PATH}/start.sh /APP
COPY ./version.jso* /APP



RUN apt-get update && \
    apt-get install -y  curl build-essential git make libpq-dev libpq5 figlet && \
    echo 'figlet -t "Lapig Docker Timeseries"' >> ~/.bashrc && \
    mkdir -p /APP && cd /APP && \
    git clone -b ${LAPIG_BRANCH} ${URL_TO_APPLICATION_GITHUB} && \
    cd /APP/timeseries && \
    pip3 install -r requirements.txt && \
    rm -rf /var/lib/apt/lists/* && chmod +x /APP/start.sh  && \
    mkdir -p /APP/timeseries/logs
        

CMD [ "sh", "/APP/start.sh" ]
