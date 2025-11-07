"""
DAG do Airflow para pipeline de dados.
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

default_args = {
    'owner': 'ml-team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'data_pipeline',
    default_args=default_args,
    description='Pipeline completo de dados: ingestão, processamento e ML',
    schedule_interval=timedelta(hours=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['data', 'etl', 'ml'],
)


def ingest_data(**context):
    """Tarefa de ingestão de dados."""
    from data_ingestion.etl.batch_ingestion import BatchDataIngestion
    
    ingestor = BatchDataIngestion()
    # Exemplo: ingerir dados
    # df = ingestor.ingest_from_csv('data/raw/data.csv')
    # ingestor.save_to_data_lake(df, 'data/lake/raw/', format='parquet')
    print("Dados ingeridos com sucesso")


def process_data(**context):
    """Tarefa de processamento de dados."""
    from data_processing.spark.batch_processing import SparkBatchProcessor
    
    processor = SparkBatchProcessor()
    # Exemplo: processar dados
    # df = processor.read_parquet('data/lake/raw/')
    # df_clean = processor.clean_data(df)
    # processor.save_parquet(df_clean, 'data/lake/processed/')
    print("Dados processados com sucesso")
    processor.stop()


def train_model(**context):
    """Tarefa de treinamento de modelo."""
    # Exemplo: treinar modelo
    # from ml.train import train_classification_model
    # train_classification_model('data/processed/train.csv', 'random_forest')
    print("Modelo treinado com sucesso")


def evaluate_model(**context):
    """Tarefa de avaliação de modelo."""
    print("Modelo avaliado com sucesso")


# Definir tarefas
ingest_task = PythonOperator(
    task_id='ingest_data',
    python_callable=ingest_data,
    dag=dag,
)

process_task = PythonOperator(
    task_id='process_data',
    python_callable=process_data,
    dag=dag,
)

train_task = PythonOperator(
    task_id='train_model',
    python_callable=train_model,
    dag=dag,
)

evaluate_task = PythonOperator(
    task_id='evaluate_model',
    python_callable=evaluate_model,
    dag=dag,
)

# Definir dependências
ingest_task >> process_task >> train_task >> evaluate_task

