from asyncio import tasks
import json
from textwrap import dedent
import pendulum
import os
from airflow import DAG
from airflow.operators.python import PythonOperator

#defining DAG
with DAG(
    'sensor_training',  #name
    default_args={'retries': 2},  # if 1st fail to run pipeline it will atomatically run 2nd time(re try again and again)
    # [END default_args]
    description='Sensor Fault Detection',
    schedule_interval="@weekly",
    start_date=pendulum.datetime(2022, 12, 11, tz="UTC"),
    catchup=False,##optional
    tags=['example'],
) as dag:

    
    def training(**kwargs): #create a function called as training
        from sensor.pipeline.training_pipeline import start_training_pipeline
        start_training_pipeline() #calling function
    
    def sync_artifact_to_s3_bucket(**kwargs):
        bucket_name = os.getenv("BUCKET_NAME")
        os.system(f"aws s3 sync /app/artifact s3://{bucket_name}/artifacts")
        os.system(f"aws s3 sync /app/saved_models s3://{bucket_name}/saved_models")
    
    # Importing pythonoperator from airflow(Creating operator in airflow)
    training_pipeline  = PythonOperator(
            task_id="train_pipeline",
            python_callable=training

    )
    
    # Importing pythonoperator from airflow(Creating operator in airflow)
    sync_data_to_s3 = PythonOperator(
            task_id="sync_data_to_s3",
            python_callable=sync_artifact_to_s3_bucket

    )
    #first we will run training pipeline ,then we will sync data t0 s3 bucket
    training_pipeline >> sync_data_to_s3