from datetime import timedelta

import pendulum

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator


with DAG(
    dag_id="bing_ad_pipeline",
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    schedule=None,
    catchup=False,
    tags=["radancy", "bing", "etl"],
    default_args={
        "retries": 1,
        "retry_delay": timedelta(minutes=2),
    },
) as dag:

    load_staging = BashOperator(
        task_id="load_staging",
        bash_command="python /opt/airflow/src/load_staging.py",
    )

    quality_check = BashOperator(
        task_id="quality_check",
        bash_command="python /opt/airflow/src/quality_check.py",
    )

    load_warehouse = BashOperator(
        task_id="load_warehouse",
        bash_command="python /opt/airflow/src/load_warehouse.py",
    )

    load_staging >> quality_check >> load_warehouse