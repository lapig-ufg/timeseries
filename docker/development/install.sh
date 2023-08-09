#!/bin/bash
FOLDER=~/.ssh


if [ -f "pyproject.toml" ]; then
    rm requirements.txt
fi
if [ -d "$FOLDER" ]; then
    cp -rvp ~/.ssh ssh/
else
    echo "Directory ./ssh does not exist!"
fi


cp -rvp ../../requirements.txt .

docker-compose build 

docker-compose up -d 