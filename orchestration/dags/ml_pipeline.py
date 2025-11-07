"""
DAG do Airflow para pipeline de Machine Learning.
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'ml-team',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=10),
}

dag = DAG(
    'ml_pipeline',
    default_args=default_args,
    description='Pipeline de Machine Learning completo',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['ml', 'training', 'evaluation'],
)


def prepare_data(**context):
    """Prepara dados para treinamento."""
    print("Preparando dados para treinamento...")


def train_classification(**context):
    """Treina modelo de classificação."""
    print("Treinando modelo de classificação...")


def train_regression(**context):
    """Treina modelo de regressão."""
    print("Treinando modelo de regressão...")


def evaluate_models(**context):
    """Avalia todos os modelos."""
    print("Avaliando modelos...")


def deploy_best_model(**context):
    """Faz deploy do melhor modelo."""
    print("Fazendo deploy do melhor modelo...")


# Definir tarefas
prepare_task = PythonOperator(
    task_id='prepare_data',
    python_callable=prepare_data,
    dag=dag,
)

train_class_task = PythonOperator(
    task_id='train_classification',
    python_callable=train_classification,
    dag=dag,
)

train_reg_task = PythonOperator(
    task_id='train_regression',
    python_callable=train_regression,
    dag=dag,
)

evaluate_task = PythonOperator(
    task_id='evaluate_models',
    python_callable=evaluate_models,
    dag=dag,
)

deploy_task = PythonOperator(
    task_id='deploy_best_model',
    python_callable=deploy_best_model,
    dag=dag,
)

# Definir dependências
prepare_task >> [train_class_task, train_reg_task] >> evaluate_task >> deploy_task

