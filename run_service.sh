#!/bin/sh
pip install -r requirements.txt
docker-compose up -d
echo "waiting for containers..."

until [ "`docker inspect -f {{.State.Running}} kafka_kafka_1`"=="true" ]; do
    sleep 5;
done;
sleep 5
docker exec -d kafka_db_1 sh populate_db.sh

sleep 5

python consumer.py