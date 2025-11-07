# Estrutura do Projeto

## Visão Geral da Estrutura

```
Projeto_Machine_Learning/
│
├── 📁 data_ingestion/              # Ingestão de dados
│   ├── __init__.py
│   ├── 📁 kafka/                   # Kafka producer/consumer
│   │   ├── producer.py
│   │   └── consumer.py
│   └── 📁 etl/                     # ETL batch
│       ├── __init__.py
│       └── batch_ingestion.py
│
├── 📁 data_storage/                # Armazenamento de dados
│   ├── __init__.py
│   └── config.py
│
├── 📁 data_processing/             # Processamento de dados
│   ├── __init__.py
│   └── 📁 spark/                   # Apache Spark
│       ├── __init__.py
│       ├── batch_processing.py
│       └── streaming_processing.py
│
├── 📁 ml/                          # Machine Learning
│   ├── __init__.py
│   ├── train.py                    # Script de treinamento
│   ├── 📁 models/                  # Modelos ML
│   │   ├── __init__.py
│   │   ├── classification_model.py
│   │   └── regression_model.py
│   └── 📁 mlops/                   # MLOps
│       ├── __init__.py
│       └── mlflow_tracking.py
│
├── 📁 api/                         # APIs RESTful
│   ├── __init__.py
│   ├── app.py                      # Aplicação FastAPI principal
│   └── 📁 routes/                  # Rotas da API
│       ├── __init__.py
│       └── predictions.py
│
├── 📁 orchestration/               # Orquestração
│   ├── __init__.py
│   └── 📁 dags/                    # Airflow DAGs
│       ├── data_pipeline.py
│       └── ml_pipeline.py
│
├── 📁 visualization/               # Visualização
│   ├── __init__.py
│   └── 📁 dashboards/
│       └── ml_dashboard.py
│
├── 📁 monitoring/                  # Monitoramento
│   ├── 📁 prometheus/
│   │   └── prometheus.yml
│   └── 📁 grafana/
│       ├── 📁 datasources/
│       │   └── prometheus.yml
│       └── 📁 dashboards/
│           └── default.json
│
├── 📁 infrastructure/              # Infraestrutura
│   └── 📁 docker/
│       └── api.Dockerfile
│
├── 📁 tests/                       # Testes
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_ingestion.py
│   └── test_ml_models.py
│
├── 📁 scripts/                     # Scripts utilitários
│   ├── setup.sh
│   ├── start_services.sh
│   ├── stop_services.sh
│   └── run_tests.sh
│
├── 📁 docs/                        # Documentação
│   ├── architecture.md
│   ├── development_guide.md
│   ├── getting_started.md
│   └── api_documentation.md
│
├── 📄 README.md                    # Documentação principal
├── 📄 LICENSE                      # Licença MIT
├── 📄 CONTRIBUTING.md              # Guia de contribuição
├── 📄 PROJECT_STRUCTURE.md         # Este arquivo
├── 📄 requirements.txt             # Dependências Python
├── 📄 docker-compose.yml           # Configuração Docker Compose
├── 📄 env.example                  # Exemplo de variáveis de ambiente
├── 📄 .gitignore                   # Arquivos ignorados pelo Git
└── 📄 Makefile                     # Comandos Make
```

## Descrição dos Módulos

### 1. data_ingestion/
Módulo responsável pela ingestão de dados de diversas fontes.

**Componentes:**
- `kafka/`: Producer e Consumer Kafka para dados em tempo real
- `etl/`: ETL batch para ingestão de dados em lote (CSV, JSON, Parquet, databases)

### 2. data_storage/
Configurações e utilitários para armazenamento de dados.

**Componentes:**
- `config.py`: Configurações de conexão com bancos de dados e storage

### 3. data_processing/
Processamento de dados em batch e streaming.

**Componentes:**
- `spark/batch_processing.py`: Processamento batch com Spark
- `spark/streaming_processing.py`: Processamento streaming com Spark

### 4. ml/
Machine Learning: modelos, treinamento e MLOps.

**Componentes:**
- `models/`: Modelos de classificação e regressão
- `mlops/`: Tracking de experimentos com MLflow
- `train.py`: Script principal de treinamento

### 5. api/
APIs RESTful para exposição de serviços.

**Componentes:**
- `app.py`: Aplicação FastAPI principal
- `routes/`: Rotas da API (predições, modelos, etc.)

### 6. orchestration/
Orquestração de workflows com Apache Airflow.

**Componentes:**
- `dags/`: DAGs do Airflow (pipelines de dados e ML)

### 7. visualization/
Dashboards e visualizações.

**Componentes:**
- `dashboards/ml_dashboard.py`: Dashboard Dash para métricas ML

### 8. monitoring/
Monitoramento com Prometheus e Grafana.

**Componentes:**
- `prometheus/`: Configuração do Prometheus
- `grafana/`: Dashboards e datasources do Grafana

### 9. infrastructure/
Configurações de infraestrutura.

**Componentes:**
- `docker/`: Dockerfiles para containers

### 10. tests/
Testes unitários e de integração.

**Componentes:**
- Testes para API, ingestão e modelos ML

### 11. scripts/
Scripts utilitários para setup e gerenciamento.

**Componentes:**
- `setup.sh`: Setup inicial do projeto
- `start_services.sh`: Inicia serviços Docker
- `stop_services.sh`: Para serviços Docker
- `run_tests.sh`: Executa testes

### 12. docs/
Documentação completa do projeto.

**Componentes:**
- `architecture.md`: Arquitetura do sistema
- `development_guide.md`: Guia de desenvolvimento
- `getting_started.md`: Guia de início rápido
- `api_documentation.md`: Documentação da API

## Fluxo de Dados

1. **Ingestão**: Dados são ingeridos via Kafka (streaming) ou ETL (batch)
2. **Armazenamento**: Dados brutos são salvos no Data Lake
3. **Processamento**: Spark processa dados (batch ou streaming)
4. **Transformação**: Dados são limpos e transformados
5. **ML**: Modelos são treinados com dados processados
6. **Deploy**: Modelos são disponibilizados via API
7. **Visualização**: Dashboards mostram métricas e resultados
8. **Monitoramento**: Prometheus e Grafana monitoram o sistema

## Tecnologias por Módulo

- **Ingestão**: Kafka, ETL (Pandas, SQLAlchemy)
- **Processamento**: Apache Spark (PySpark)
- **ML**: Scikit-learn, TensorFlow, PyTorch
- **APIs**: FastAPI
- **Orquestração**: Apache Airflow
- **Monitoramento**: Prometheus, Grafana
- **Visualização**: Dash, Plotly
- **Containerização**: Docker, Docker Compose
- **MLOps**: MLflow

## Próximos Passos

1. Configure as variáveis de ambiente em `.env`
2. Execute `make setup` para configurar o ambiente
3. Execute `make run` para iniciar os serviços
4. Consulte `docs/getting_started.md` para exemplos

