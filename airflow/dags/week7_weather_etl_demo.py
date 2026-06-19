from __future__ import annotations

import pendulum
from airflow.decorators import dag, task


@dag(
    dag_id="week7_weather_etl_demo",
    start_date=pendulum.datetime(2026, 1, 1, tz="Europe/Helsinki"),
    schedule=None,
    catchup=False,
    tags=["week7", "etl", "demo"],
)
def week7_weather_etl_demo():

    @task
    def extract_and_load():
        print("Step 1: Python extract/load would run here.")

    @task
    def dbt_run():
        print("Step 2: dbt run would run here.")

    @task
    def dbt_test():
        print("Step 3: dbt test would run here.")

    extract_and_load() >> dbt_run() >> dbt_test()


week7_weather_etl_demo()
