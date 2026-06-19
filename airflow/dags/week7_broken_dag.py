from __future__ import annotations

import pendulum
from airflow.decorators import dag, task


@dag(
    dag_id="week7_broken_dag",
    start_date=pendulum.datetime(2026, 1, 1, tz="Europe/Helsinki"),
    schedule=None,
    catchup=False,
    tags=["week7", "troubleshooting"],
)
def week7_broken_dag():

    @task
    def intentionally_failing_task():
        raise ValueError("This task is intentionally broken for troubleshooting practice.")

    intentionally_failing_task()


week7_broken_dag()
