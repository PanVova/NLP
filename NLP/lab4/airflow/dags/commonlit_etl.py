
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import psycopg2

DB_CONFIG = {
    'host': 'db',
    'dbname': 'commonlit',
    'user': 'user',
    'password': 'password'
}

API_URL = 'http://api:8000/predict'

def extract():
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id, text FROM input_texts WHERE id NOT IN (SELECT id FROM predicted_scores);")
            return cur.fetchall()

def transform_and_load(**context):
    rows = context['ti'].xcom_pull(task_ids='extract')
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            for row in rows:
                rid, text = row
                response = requests.post(API_URL, json={"text": text})
                pred = response.json()['predicted_score']
                cur.execute("INSERT INTO predicted_scores (id, text, predicted_score) VALUES (%s, %s, %s)", (rid, text, pred))
            conn.commit()

def extract_task():
    return extract()

def transform_and_load_task(**context):
    return transform_and_load(**context)

def create_dag():
    with DAG(
        dag_id="commonlit_etl",
        schedule_interval="@daily",
        start_date=datetime(2024, 1, 1),
        catchup=False
    ) as dag:
        t1 = PythonOperator(
            task_id="extract",
            python_callable=extract_task
        )
        t2 = PythonOperator(
            task_id="transform_and_load",
            python_callable=transform_and_load_task
        )
        t1 >> t2
    return dag

globals()["commonlit_etl"] = create_dag()
