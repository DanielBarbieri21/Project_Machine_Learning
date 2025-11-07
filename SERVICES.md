# Serviços do Sistema

## Serviços Disponíveis

### 1. Kafka
- **Descrição**: Sistema de mensageria distribuída para streaming de dados
- **Porta**: 9092
- **UI**: http://localhost:8081
- **Uso**: Ingestão de dados em tempo real

### 2. Zookeeper
- **Descrição**: Coordenação de serviços distribuídos (requerido pelo Kafka)
- **Porta**: 2181
- **Uso**: Gerenciamento de configuração do Kafka

### 3. PostgreSQL
- **Descrição**: Banco de dados relacional (usado pelo Airflow e MLflow)
- **Porta**: 5432
- **Usuário**: airflow
- **Senha**: airflow
- **Uso**: Metadados do Airflow, tracking do MLflow

### 4. MongoDB
- **Descrição**: Banco de dados NoSQL
- **Porta**: 27017
- **Usuário**: admin
- **Senha**: admin
- **Uso**: Dados semiestruturados

### 5. Redis
- **Descrição**: Cache e armazenamento em memória
- **Porta**: 6379
- **Uso**: Cache, sessões, filas

### 6. Airflow
- **Descrição**: Plataforma de orquestração de workflows
- **Webserver**: http://localhost:8080
- **Usuário**: airflow
- **Senha**: airflow
- **Uso**: Orquestração de pipelines de dados e ML

### 7. MLflow
- **Descrição**: Plataforma para gerenciar o ciclo de vida de ML
- **UI**: http://localhost:5000
- **Uso**: Tracking de experimentos, versionamento de modelos

### 8. Prometheus
- **Descrição**: Sistema de monitoramento e alertas
- **UI**: http://localhost:9090
- **Uso**: Coleta de métricas do sistema

### 9. Grafana
- **Descrição**: Plataforma de visualização e análise
- **UI**: http://localhost:3000
- **Usuário**: admin
- **Senha**: admin
- **Uso**: Dashboards de métricas e visualizações

### 10. FastAPI
- **Descrição**: API RESTful para serviços ML
- **URL**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **Uso**: Predições, treinamento, gerenciamento de modelos

## Comandos Úteis

### Iniciar Todos os Serviços
```bash
docker-compose up -d
```

### Parar Todos os Serviços
```bash
docker-compose down
```

### Ver Logs de um Serviço
```bash
docker logs <container-name>
```

### Reiniciar um Serviço
```bash
docker-compose restart <service-name>
```

### Ver Status dos Serviços
```bash
docker-compose ps
```

## Verificação de Saúde

### Verificar se Kafka está rodando
```bash
docker ps | grep kafka
```

### Verificar se Airflow está acessível
```bash
curl http://localhost:8080/health
```

### Verificar se API está acessível
```bash
curl http://localhost:8000/health
```

## Portas Utilizadas

| Serviço | Porta | Protocolo |
|---------|-------|-----------|
| Kafka | 9092 | TCP |
| Kafka UI | 8081 | HTTP |
| Zookeeper | 2181 | TCP |
| PostgreSQL | 5432 | TCP |
| MongoDB | 27017 | TCP |
| Redis | 6379 | TCP |
| Airflow | 8080 | HTTP |
| MLflow | 5000 | HTTP |
| Prometheus | 9090 | HTTP |
| Grafana | 3000 | HTTP |
| FastAPI | 8000 | HTTP |

## Configuração

Todas as configurações podem ser ajustadas no arquivo `docker-compose.yml` ou através de variáveis de ambiente no arquivo `.env`.

## Troubleshooting

### Serviço não inicia
1. Verifique os logs: `docker logs <container-name>`
2. Verifique se a porta está disponível: `netstat -an | grep <port>`
3. Verifique recursos do sistema: `docker stats`

### Erro de conexão
1. Verifique se o serviço está rodando: `docker ps`
2. Verifique as configurações de rede: `docker network ls`
3. Verifique variáveis de ambiente no `.env`

### Problemas de performance
1. Ajuste recursos no `docker-compose.yml`
2. Verifique uso de recursos: `docker stats`
3. Considere aumentar memória/disco alocados

