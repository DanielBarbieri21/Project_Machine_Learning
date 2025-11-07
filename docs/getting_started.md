# Guia de Início Rápido

## Instalação Rápida

### 1. Clone o Repositório
```bash
git clone <repository-url>
cd Projeto_Machine_Learning
```

### 2. Configure o Ambiente
```bash
# Linux/Mac
bash scripts/setup.sh

# Windows
# Execute os comandos manualmente ou use WSL
```

### 3. Configure Variáveis de Ambiente
```bash
cp env.example .env
# Edite o arquivo .env com suas configurações
```

### 4. Inicie os Serviços
```bash
docker-compose up -d
```

### 5. Verifique os Serviços
- Kafka UI: http://localhost:8081
- Airflow: http://localhost:8080 (usuário: airflow, senha: airflow)
- MLflow: http://localhost:5000
- Grafana: http://localhost:3000 (usuário: admin, senha: admin)
- Prometheus: http://localhost:9090
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Primeiros Passos

### 1. Ingerir Dados

#### Via Kafka
```python
from data_ingestion.kafka.producer import KafkaDataProducer

producer = KafkaDataProducer()
data = {"sensor_id": "sensor_001", "temperature": 23.5}
producer.send_data(data, key="sensor_001")
```

#### Via ETL Batch
```python
from data_ingestion.etl.batch_ingestion import BatchDataIngestion

ingestor = BatchDataIngestion()
df = ingestor.ingest_from_csv('data/raw/data.csv')
```

### 2. Processar Dados

#### Batch Processing
```python
from data_processing.spark.batch_processing import SparkBatchProcessor

processor = SparkBatchProcessor()
df = processor.read_csv('data/raw/data.csv')
df_clean = processor.clean_data(df)
processor.save_parquet(df_clean, 'data/processed/')
```

### 3. Treinar Modelo

```python
from ml.models.classification_model import ClassificationModel
import pandas as pd

# Preparar dados
X = pd.DataFrame(...)  # Features
y = pd.Series(...)     # Target

# Treinar modelo
model = ClassificationModel(model_type='random_forest')
metrics = model.train(X, y)

# Fazer predições
predictions = model.predict(X_new)
```

### 4. Usar API

```python
import requests

# Fazer predição
response = requests.post(
    'http://localhost:8000/predict',
    json={
        'features': [[1.0, 2.0, 3.0]],
        'model_type': 'classification',
        'model_name': 'random_forest'
    }
)
print(response.json())
```

### 5. Executar Pipeline Airflow

1. Acesse http://localhost:8080
2. Faça login (airflow/airflow)
3. Encontre o DAG `data_pipeline`
4. Ative e execute o DAG

## Exemplos

### Exemplo Completo: Pipeline de ML

```python
# 1. Ingerir dados
from data_ingestion.etl.batch_ingestion import BatchDataIngestion
ingestor = BatchDataIngestion()
df = ingestor.ingest_from_csv('data/raw/train.csv')

# 2. Processar dados
from data_processing.spark.batch_processing import SparkBatchProcessor
processor = SparkBatchProcessor()
df_processed = processor.clean_data(df)

# 3. Treinar modelo
from ml.models.classification_model import ClassificationModel
X = df_processed.drop('target', axis=1)
y = df_processed['target']
model = ClassificationModel(model_type='random_forest')
metrics = model.train(X, y)

# 4. Salvar modelo
model.save('models/classification_model.pkl')
```

## Próximos Passos

1. Leia a [Documentação da Arquitetura](architecture.md)
2. Explore os [Exemplos de Código](../examples/)
3. Consulte a [Documentação da API](api_documentation.md)
4. Veja o [Guia de Desenvolvimento](development_guide.md)

## Problemas Comuns

### Kafka não conecta
- Verifique se o Kafka está rodando: `docker ps | grep kafka`
- Verifique as configurações em `.env`

### Erro ao importar módulos
- Certifique-se de que o ambiente virtual está ativado
- Instale as dependências: `pip install -r requirements.txt`

### Airflow DAGs não aparecem
- Verifique os logs: `docker logs airflow-webserver`
- Verifique se os arquivos estão em `orchestration/dags/`

## Suporte

Para mais ajuda, consulte:
- [Documentação Completa](../README.md)
- [Issues do GitHub](<repository-url>/issues)
- [Guia de Contribuição](../CONTRIBUTING.md)

