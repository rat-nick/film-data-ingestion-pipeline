import os
import json
from psycopg2.extras import execute_values
from airflow import DAG
from airflow.operators.python import PythonOperator
from logging import getLogger
from datetime import datetime, timedelta
from airflow.providers.postgres.hooks.postgres import PostgresHook
from utils.films import fetch_films_this_week, fetch_genres


logger = getLogger(__name__)

def discover_films_task(**kwargs):
    logical_date = kwargs['logical_date'] 
    logical_date -= timedelta(days=14) # for more complete info
    
    logger.info(f"Fetching films for {logical_date}")
    films = fetch_films_this_week(logical_date)
    logger.info(f"Discovered {len(films)} films")

    file_path = f"/tmp/shared/films-{logical_date.strftime('%Y-%m-%d')}.json"
    logger.info(f"Saving films to file {file_path}")
    try:    
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    except OSError as e:
        logger.error(f"Error creating directory: {e}")
    
    try:
        with open(file_path, "w") as f:
            json.dump(films, f)
    except Exception as e:
        logger.error(f"Error saving file: {e}")
    
    ti = kwargs['ti']
    ti.xcom_push(key='file_path', value=file_path)
    
def load_films_into_db_task(**kwargs):
    postgres_hook = PostgresHook(postgres_conn_id='media-metadata-db')
    conn = postgres_hook.get_conn()
    cursor = conn.cursor()

    ti = kwargs['ti']
    file_path = ti.xcom_pull(task_ids='discover', key='file_path')
    with open(file_path, 'r') as f:
        films = json.load(f)
    
    genres = fetch_genres()

    for film in films:
        film['genre_ids'] = [genres.get(genre_id) for genre_id in film.get('genre_ids', [])]

    execute_values(
        cursor,
        """
        INSERT INTO film_metadata (
            is_adult, genres, external_id, source, original_language, 
            original_title, title, backdrop_path, overview, poster_path, release_date
        ) VALUES %s
        ON CONFLICT (source, external_id) DO NOTHING
        """,
        [
            (
                film.get('adult'),
                ','.join(film.get('genre_ids', [])),
                film['id'],
                "TMDB",
                film.get('original_language'),
                film.get('original_title'),
                film['title'],
                film.get('backdrop_path'),
                film.get('overview'),
                film.get('poster_path'),
                film['release_date']
            )
            for film in films
        ]
    )
    conn.commit()
    cursor.close()
    conn.close()

def clean_up_task(**kwargs):
    ti = kwargs['ti']
    file_path = ti.xcom_pull(task_ids='discover', key='file_path')
    os.remove(file_path)

default_args = {
    "owner": "rat-nick",
    "retrires": 3,
    "retry_delay": timedelta(hours=2),
    "start_date" : datetime(2000, 1, 1),
}

with DAG(
    dag_id="weekly_film_discovery",
    default_args=default_args,
    schedule_interval="@weekly",
    catchup=True,
    tags=["weekly", "external"],
) as dag:
    
    discover_films = PythonOperator(
        task_id="discover",
        python_callable=discover_films_task,
        provide_context=True,
    )

    load_films_into_db = PythonOperator(
        task_id="load_into_db",
        python_callable=load_films_into_db_task,
        provide_context=True,
    )

    clean_up = PythonOperator(
        task_id="clean_up",
        python_callable=clean_up_task,
        provide_context=True,
    )
    
    discover_films >> load_films_into_db >> clean_up