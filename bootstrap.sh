#!/bin/sh -e

# Up Container
docker-compose \
        --project-name fast-api-klasifikasi-stenografi-cnn \
        --file docker-compose.yaml \
        up --detach --remove-orphans

# Init Database
docker-compose \
        --project-name fast-api-klasifikasi-stenografi-cnn \
        --file docker/docker-compose.yml \
        exec dbs /docker-entrypoint-initdb.d/init-db.sh