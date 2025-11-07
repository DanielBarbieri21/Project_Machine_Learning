# Sistema Integrado de Machine Learning e Big Data

Sistema moderno, robusto e completo que integra Machine Learning (ML), Big Data e outras tecnologias de dados.

## 📋 Arquitetura

### 1. Coleta e Ingestão de Dados
- **Streaming**: Apache Kafka para dados em tempo real
- **ETL/ELT**: Apache NiFi, Apache Flink
- **Fontes**: Bancos relacionais, logs, JSON, XML, dados não estruturados

### 2. Armazenamento de Dados (Big Data)
- **Data Lake**: HDFS, S3, Azure Data Lake, GCS
- **Data Warehouse**: Snowflake, BigQuery, Redshift, Synapse Analytics
- **NoSQL**: Cassandra, MongoDB, Redis

### 3. Processamento de Dados
- **Batch Processing**: Apache Spark, Databricks
- **Stream Processing**: Apache Flink, Spark Streaming, Kafka Streams

### 4. Machine Learning
- **Frameworks**: TensorFlow, PyTorch, Scikit-learn
- **MLOps**: MLflow, Kubeflow
- **Plataformas**: AWS SageMaker, Azure ML, Google AI Platform

### 5. Orquestração
- Apache Airflow para workflows
- Apache NiFi para fluxos de dados

### 6. APIs e Serviços
- APIs RESTful (FastAPI, Flask)
- Microserviços

### 7. Visualização
- BI: Tableau, Power BI, Looker, Metabase
- Custom: D3.js, Plotly, Matplotlib

### 8. Infraestrutura
- **Cloud**: AWS, Azure, GCP
- **Containerização**: Docker, Kubernetes
- **CI/CD**: Jenkins, GitLab CI/CD, GitHub Actions
- **Monitoramento**: Prometheus, Grafana, ELK Stack

## 🚀 Estrutura do Projeto

```
Projeto_Machine_Learning/
├── data_ingestion/        # Ingestão de dados (Kafka, NiFi, ETL)
├── data_storage/          # Configurações de armazenamento
├── data_processing/       # Processamento batch e streaming (Spark, Flink)
├── ml/                    # Machine Learning (modelos, treinamento)
├── mlops/                 # MLOps (MLflow, pipelines)
├── api/                   # APIs RESTful
├── orchestration/         # Airflow DAGs
├── visualization/         # Dashboards e visualizações
├── infrastructure/        # Docker, Kubernetes, Terraform
├── monitoring/            # Prometheus, Grafana
├── tests/                 # Testes unitários e de integração
├── scripts/               # Scripts utilitários
└── docs/                  # Documentação
```

## 📦 Instalação

### Pré-requisitos
- Python 3.9+
- Docker e Docker Compose
- Java 8+ (para Spark, Kafka)
- Kubernetes (opcional, para produção)

### Setup Inicial

1. Clone o repositório:
```bash
git clone <repository-url>
cd Projeto_Machine_Learning
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

5. Inicie os serviços com Docker Compose:
```bash
docker-compose up -d
```

## 🔧 Configuração

### Variáveis de Ambiente
Veja `.env.example` para todas as variáveis configuráveis.

### Configuração do Kafka
Verifique `data_ingestion/kafka/config/` para configurações do Kafka.

### Configuração do Spark
Verifique `data_processing/spark/config/` para configurações do Spark.

## 📚 Uso

### Ingestão de Dados
```bash
python data_ingestion/kafka/producer.py
python data_ingestion/etl/batch_ingestion.py
```

### Processamento de Dados
```bash
python data_processing/spark/batch_processing.py
python data_processing/spark/streaming_processing.py
```

### Treinamento de Modelos ML
```bash
python ml/train.py --model-type classification
python ml/train.py --model-type regression
```

### Executar APIs
```bash
python api/app.py
```

### Executar DAGs do Airflow
Acesse http://localhost:8080 após iniciar o Airflow.

## 🧪 Testes

```bash
pytest tests/
```

## 📊 Monitoramento

- **Grafana**: http://localhost:3000
- **Prometheus**: http://localhost:9090
- **Airflow UI**: http://localhost:8080
- **MLflow UI**: http://localhost:5000

## 🤝 Contribuição

1. Crie uma branch para sua feature
2. Faça commit das mudanças
3. Abra um Pull Request



## 🔗 Links Úteis

- [Documentação Completa](docs/)
- [Guia de Desenvolvimento](docs/development_guide.md)
- [Arquitetura Detalhada](docs/architecture.md)


## 👨‍💻 Desenvolvedor

**Daniel Barbieri Dev**
- 🎮 Desenvolvedor de Jogos
- 💻 Especialista em C/C++
- 🚀 Entusiasta de Tecnologia
- 📧 Contato: [Daniel Barbieri](mailto:dibarbieri21@gmail.com)


# Project_Machine_Learning
