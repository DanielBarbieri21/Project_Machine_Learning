# Guia de Desenvolvimento

## Configuração do Ambiente

### Pré-requisitos
- Python 3.9+
- Docker e Docker Compose
- Java 8+ (para Spark)
- Git

### Setup Inicial

1. Clone o repositório
```bash
git clone <repository-url>
cd Projeto_Machine_Learning
```

2. Execute o script de setup
```bash
bash scripts/setup.sh
```

3. Configure as variáveis de ambiente
```bash
cp env.example .env
# Edite o arquivo .env
```

4. Inicie os serviços
```bash
bash scripts/start_services.sh
```

## Estrutura do Projeto

```
Projeto_Machine_Learning/
├── data_ingestion/        # Ingestão de dados
│   ├── kafka/            # Kafka producer/consumer
│   └── etl/              # ETL batch
├── data_processing/       # Processamento
│   └── spark/            # Spark batch e streaming
├── ml/                   # Machine Learning
│   ├── models/           # Modelos ML
│   └── mlops/            # MLOps
├── api/                  # APIs RESTful
│   └── routes/           # Rotas da API
├── orchestration/        # Airflow
│   └── dags/             # DAGs do Airflow
├── visualization/        # Dashboards
├── monitoring/           # Prometheus, Grafana
├── infrastructure/       # Docker, Kubernetes
├── tests/                # Testes
└── docs/                 # Documentação
```

## Desenvolvimento

### Adicionar Novo Modelo ML

1. Crie o modelo em `ml/models/`
2. Adicione métodos de treinamento e predição
3. Integre com MLflow para tracking
4. Adicione testes em `tests/`

### Adicionar Nova Rota API

1. Crie a rota em `api/routes/`
2. Importe no `api/app.py`
3. Adicione documentação Swagger
4. Adicione testes

### Criar Novo DAG Airflow

1. Crie o DAG em `orchestration/dags/`
2. Defina tarefas e dependências
3. Teste localmente
4. Deploy no Airflow

## Testes

Execute os testes:
```bash
pytest tests/
```

Com cobertura:
```bash
pytest --cov=. tests/
```

## Código de Estilo

Use Black para formatação:
```bash
black .
```

Use Flake8 para linting:
```bash
flake8 .
```

## Git Workflow

1. Crie uma branch para sua feature
```bash
git checkout -b feature/nova-feature
```

2. Faça commits frequentes
```bash
git add .
git commit -m "Descrição da mudança"
```

3. Push e crie Pull Request
```bash
git push origin feature/nova-feature
```

## Deploy

### Desenvolvimento
```bash
docker-compose up -d
```

### Produção
1. Configure variáveis de ambiente de produção
2. Build das imagens Docker
3. Deploy no Kubernetes (se aplicável)

## Troubleshooting

### Kafka não conecta
- Verifique se o Kafka está rodando: `docker ps`
- Verifique as configurações de conexão no `.env`

### Spark não inicia
- Verifique se Java está instalado
- Verifique as variáveis de ambiente do Spark

### Airflow DAGs não aparecem
- Verifique os logs do Airflow
- Verifique se os arquivos estão em `orchestration/dags/`

## Recursos Úteis

- [Documentação do Spark](https://spark.apache.org/docs/latest/)
- [Documentação do Kafka](https://kafka.apache.org/documentation/)
- [Documentação do Airflow](https://airflow.apache.org/docs/)
- [Documentação do FastAPI](https://fastapi.tiangolo.com/)
- [Documentação do MLflow](https://mlflow.org/docs/latest/)

