# Documentação da API

## Endpoints

### Health Check

#### GET /health
Retorna o status de saúde da API.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0"
}
```

### Predições

#### POST /predict
Faz predições usando um modelo ML.

**Request:**
```json
{
  "features": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]],
  "model_type": "classification",
  "model_name": "random_forest"
}
```

**Response:**
```json
{
  "predictions": [0, 1],
  "probabilities": [[0.9, 0.1], [0.2, 0.8]]
}
```

### Modelos

#### GET /models
Lista todos os modelos disponíveis.

**Response:**
```json
{
  "models": ["classification_random_forest", "regression_gradient_boosting"]
}
```

### Treinamento

#### POST /train
Inicia treinamento de um modelo (assíncrono).

**Request:**
```
POST /train?model_type=classification&model_name=random_forest
```

**Response:**
```json
{
  "status": "training_started",
  "message": "Treinamento do modelo classification_random_forest iniciado"
}
```

### Métricas

#### GET /metrics
Retorna métricas do sistema.

**Response:**
```json
{
  "active_models": 2,
  "total_predictions": 1500
}
```

## Autenticação

Atualmente, a API não requer autenticação. Para produção, implemente autenticação JWT.

## Rate Limiting

A API não possui rate limiting por padrão. Para produção, implemente rate limiting.

## Erros

A API retorna erros no seguinte formato:

```json
{
  "detail": "Mensagem de erro"
}
```

Códigos de status HTTP:
- 200: Sucesso
- 400: Bad Request
- 404: Not Found
- 500: Internal Server Error

