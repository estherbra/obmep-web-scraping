from airflow import DAG
from datetime import datetime
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from scraper import scraping_function
from local_to_s3 import local_to_s3


default_args = {
  "owner": "airflow",
  "depends_on_past": False,
  "start_date": datetime(2022, 4, 5),
  "retries": 0,
}

with DAG(
  "obmep_dag", 
  schedule_interval='@monthly',
  catchup=False,
  default_args=default_args
) as dag:
  
# Inicio do Pipeline
    start_of_data_pipeline = DummyOperator(task_id='start_of_data_pipeline', dag=dag)

    # Definindo a tarefa para realização de web scrapping
    web_scraping_stage = PythonOperator(
        task_id='web_scraping_stage',
        python_callable=scraping_function
    )

    # definindo a tarefa para enviar o arquivo para S3.
    s3_stage = PythonOperator(
        task_id='s3_stage',
        python_callable=local_to_s3,
        op_kwargs={
            'bucket_name': '1sti-bucket'
        },
    )
    
    # Fim da Pipeline
    end_of_data_pipeline = DummyOperator(task_id='end_of_data_pipeline', dag=dag)

# Definição do padrão de execução
start_of_data_pipeline >>web_scraping_stage >> s3_stage >> end_of_data_pipeline