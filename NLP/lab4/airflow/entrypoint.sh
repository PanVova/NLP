#!/bin/bash
airflow db init

airflow users create \
    --username admin2 \
    --firstname Admin \
    --lastname Two \
    --role Admin \
    --email admin2@example.com \
    --password 123456 || true

airflow scheduler &

exec airflow webserver
