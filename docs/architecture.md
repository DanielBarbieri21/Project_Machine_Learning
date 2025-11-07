# Arquitetura do Sistema

## Visão Geral

Este documento descreve a arquitetura completa do sistema integrado de Machine Learning e Big Data.

## Componentes Principais

### 1. Ingestão de Dados

#### Kafka
- **Propósito**: Ingestão de dados em tempo real (streaming)
- **Componentes**:
  - Producer: `data_ingestion/kafka/producer.py`
  - Consumer: `data_ingestion/kafka/consumer.py`
- **Uso**: Sensores IoT, logs de aplicação, eventos em tempo real

#### ETL Batch
- **Propósito**: Ingestão de dados em lote
- **Componentes**: `data_ingestion/etl/batch_ingestion.py`
- **Fontes Suportadas**:
  - CSV, JSON, Parquet
  - Bancos de dados relacionais (PostgreSQL, MySQL)
  - APIs REST

### 2. Armazenamento

#### Data Lake
- **Formato**: Parquet, CSV, JSON
- **Localização**: `data/lake/`
- **Propósito**: Armazenar dados brutos em formato original

#### Data Warehouse
- **Tecnologia**: PostgreSQL
- **Propósito**: Dados processados e agregados para análise

#### NoSQL
- **MongoDB**: Dados semiestruturados
- **Redis**: Cache e dados em memória

### 3. Processamento

#### Batch Processing (Spark)
- **Componente**: `data_processing/spark/batch_processing.py`
- **Uso**: Processamento de grandes volumes de dados
- **Operações**: Limpeza, transformação, agregação

#### Streaming Processing (Spark Streaming)
- **Componente**: `data_processing/spark/streaming_processing.py`
- **Uso**: Processamento em tempo real
- **Fonte**: Kafka topics
- **Operações**: Agregação por janela de tempo, detecção de anomalias

### 4. Machine Learning

#### Modelos
- **Classificação**: `ml/models/classification_model.py`
  - Random Forest
  - Gradient Boosting
  - Logistic Regression

- **Regressão**: `ml/models/regression_model.py`
  - Random Forest Regressor
  - Gradient Boosting Regressor
  - Linear Regression

#### MLOps
- **MLflow**: Tracking de experimentos
- **Componente**: `ml/mlops/mlflow_tracking.py`
- **Funcionalidades**:
  - Versionamento de modelos
  - Tracking de métricas
  - Model Registry

### 5. APIs

#### FastAPI
- **Componente**: `api/app.py`
- **Endpoints**:
  - `/predict`: Predições em tempo real
  - `/models`: Lista modelos disponíveis
  - `/train`: Treinamento assíncrono
  - `/metrics`: Métricas do sistema

### 6. Orquestração

#### Apache Airflow
- **DAGs**: `orchestration/dags/`
- **Pipelines**:
  - `data_pipeline.py`: Pipeline completo de dados
  - `ml_pipeline.py`: Pipeline de ML

### 7. Visualização

#### Dashboards
- **Dash**: `visualization/dashboards/ml_dashboard.py`
- **Funcionalidades**:
  - Métricas de modelos
  - Distribuição de predições
  - Visão geral dos dados

### 8. Monitoramento

#### Prometheus
- **Configuração**: `monitoring/prometheus/prometheus.yml`
- **Métricas**: Performance da API, uso de recursos

#### Grafana
- **Configuração**: `monitoring/grafana/`
- **Dashboards**: Visualização de métricas

## Fluxo de Dados

### Pipeline Batch
1. **Ingestão**: Dados são ingeridos via ETL batch
2. **Armazenamento**: Dados brutos salvos no Data Lake
3. **Processamento**: Spark processa dados em lote
4. **Transformação**: Dados limpos e transformados
5. **Armazenamento**: Dados processados salvos
6. **ML**: Modelos treinados com dados processados
7. **Deploy**: Modelos disponibilizados via API

### Pipeline Streaming
1. **Ingestão**: Dados chegam via Kafka
2. **Processamento**: Spark Streaming processa em tempo real
3. **Agregação**: Dados agregados por janela de tempo
4. **Ação**: Predições ou alertas em tempo real
5. **Armazenamento**: Resultados salvos para análise posterior

## Tecnologias Utilizadas

- **Linguagens**: Python 3.9+
- **Big Data**: Apache Spark, Apache Kafka
- **ML**: Scikit-learn, TensorFlow, PyTorch
- **APIs**: FastAPI
- **Orquestração**: Apache Airflow
- **Monitoramento**: Prometheus, Grafana
- **Containerização**: Docker, Kubernetes
- **MLOps**: MLflow

## Escalabilidade

O sistema foi projetado para escalar horizontalmente:
- **Kafka**: Particionamento de tópicos
- **Spark**: Cluster mode
- **APIs**: Múltiplas instâncias via load balancer
- **Storage**: Data Lake distribuído

## Segurança

- Autenticação e autorização nas APIs
- Criptografia em trânsito (TLS)
- Criptografia em repouso
- Controle de acesso baseado em roles (RBAC)

## Próximos Passos

1. Implementar autenticação JWT nas APIs
2. Adicionar mais modelos de ML (NLP, Computer Vision)
3. Implementar feature store
4. Adicionar testes de integração
5. Configurar CI/CD pipeline

