"""
API FastAPI principal para exposição de serviços ML.
"""
import logging
import os
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import pandas as pd
import joblib
import numpy as np
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ML & Big Data API",
    description="API para serviços de Machine Learning e Big Data",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Models
class PredictionRequest(BaseModel):
    """Request para predição."""
    features: List[List[float]]
    model_type: Optional[str] = "classification"
    model_name: Optional[str] = "random_forest"


class PredictionResponse(BaseModel):
    """Response de predição."""
    predictions: List[Any]
    probabilities: Optional[List[List[float]]] = None


class HealthResponse(BaseModel):
    """Response de health check."""
    status: str
    version: str


# Global model cache
model_cache: Dict[str, Any] = {}


def load_model(model_type: str, model_name: str):
    """Carrega modelo do cache ou do disco."""
    cache_key = f"{model_type}_{model_name}"
    
    if cache_key not in model_cache:
        model_path = f"models/{model_type}_{model_name}.pkl"
        if os.path.exists(model_path):
            model_cache[cache_key] = joblib.load(model_path)
            logger.info(f"Modelo carregado: {model_path}")
        else:
            raise FileNotFoundError(f"Modelo não encontrado: {model_path}")
    
    return model_cache[cache_key]


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check."""
    return HealthResponse(status="healthy", version="1.0.0")


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="1.0.0")


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Endpoint para fazer predições.
    
    Args:
        request: Request com features e tipo de modelo
    
    Returns:
        Predições
    """
    try:
        # Carrega modelo
        model_data = load_model(request.model_type, request.model_name)
        model = model_data['model']
        
        # Converte para DataFrame
        df = pd.DataFrame(
            request.features,
            columns=[f'feature_{i}' for i in range(len(request.features[0]))]
        )
        
        # Faz predição
        predictions = model.predict(df)
        
        # Probabilidades (se disponível)
        probabilities = None
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(df).tolist()
        
        return PredictionResponse(
            predictions=predictions.tolist(),
            probabilities=probabilities
        )
        
    except Exception as e:
        logger.error(f"Erro na predição: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/models")
async def list_models():
    """Lista modelos disponíveis."""
    models_dir = "models"
    if not os.path.exists(models_dir):
        return {"models": []}
    
    models = []
    for file in os.listdir(models_dir):
        if file.endswith('.pkl'):
            models.append(file.replace('.pkl', ''))
    
    return {"models": models}


@app.post("/train")
async def train_model(
    model_type: str,
    model_name: str,
    background_tasks: BackgroundTasks
):
    """
    Endpoint para treinar modelo (assíncrono).
    
    Args:
        model_type: Tipo de modelo (classification/regression)
        model_name: Nome do modelo
        background_tasks: Tarefas em background
    """
    # Aqui você pode adicionar lógica para treinar modelos
    # Por enquanto, apenas retorna uma resposta
    background_tasks.add_task(train_model_task, model_type, model_name)
    
    return {
        "status": "training_started",
        "message": f"Treinamento do modelo {model_type}_{model_name} iniciado"
    }


def train_model_task(model_type: str, model_name: str):
    """Tarefa de treinamento em background."""
    logger.info(f"Treinando modelo: {model_type}_{model_name}")
    # Implementar lógica de treinamento aqui
    pass


@app.get("/metrics")
async def get_metrics():
    """Retorna métricas do sistema."""
    # Aqui você pode integrar com Prometheus, etc.
    return {
        "active_models": len(model_cache),
        "total_predictions": 0  # Implementar contador
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8000)),
        reload=os.getenv("API_RELOAD", "True").lower() == "true"
    )

