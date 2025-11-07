"""
MLflow tracking para experimentos de ML.
"""
import logging
import mlflow
import mlflow.sklearn
import mlflow.pytorch
import mlflow.tensorflow
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MLflowTracker:
    """Classe para tracking de experimentos MLflow."""
    
    def __init__(self, tracking_uri: str = None, experiment_name: str = None):
        """
        Inicializa o tracker MLflow.
        
        Args:
            tracking_uri: URI do servidor MLflow
            experiment_name: Nome do experimento
        """
        self.tracking_uri = tracking_uri or os.getenv(
            'MLFLOW_TRACKING_URI', 'http://localhost:5000'
        )
        mlflow.set_tracking_uri(self.tracking_uri)
        
        if experiment_name:
            mlflow.set_experiment(experiment_name)
        
        logger.info(f"MLflow tracking inicializado: {self.tracking_uri}")
    
    def start_run(self, run_name: str = None):
        """Inicia um novo run."""
        return mlflow.start_run(run_name=run_name)
    
    def log_params(self, params: dict):
        """Registra parâmetros."""
        mlflow.log_params(params)
        logger.info(f"Parâmetros registrados: {params}")
    
    def log_metrics(self, metrics: dict, step: int = None):
        """Registra métricas."""
        mlflow.log_metrics(metrics, step=step)
        logger.info(f"Métricas registradas: {metrics}")
    
    def log_model(self, model, artifact_path: str, model_type: str = 'sklearn'):
        """
        Registra modelo.
        
        Args:
            model: Modelo a ser registrado
            artifact_path: Caminho do artefato
            model_type: Tipo do modelo ('sklearn', 'pytorch', 'tensorflow')
        """
        if model_type == 'sklearn':
            mlflow.sklearn.log_model(model, artifact_path)
        elif model_type == 'pytorch':
            mlflow.pytorch.log_model(model, artifact_path)
        elif model_type == 'tensorflow':
            mlflow.tensorflow.log_model(model, artifact_path)
        else:
            raise ValueError(f"Tipo de modelo não suportado: {model_type}")
        
        logger.info(f"Modelo registrado: {artifact_path}")
    
    def log_artifact(self, local_path: str, artifact_path: str = None):
        """Registra artefato."""
        mlflow.log_artifact(local_path, artifact_path)
        logger.info(f"Artefato registrado: {local_path}")
    
    def register_model(self, model_uri: str, model_name: str):
        """
        Registra modelo no Model Registry.
        
        Args:
            model_uri: URI do modelo
            model_name: Nome do modelo
        """
        mlflow.register_model(model_uri, model_name)
        logger.info(f"Modelo registrado no Model Registry: {model_name}")
    
    def load_model(self, model_uri: str):
        """Carrega modelo."""
        model = mlflow.pyfunc.load_model(model_uri)
        logger.info(f"Modelo carregado: {model_uri}")
        return model


def main():
    """Exemplo de uso."""
    tracker = MLflowTracker(experiment_name="test_experiment")
    
    with tracker.start_run(run_name="test_run"):
        tracker.log_params({"param1": "value1", "param2": 42})
        tracker.log_metrics({"metric1": 0.95, "metric2": 0.87})


if __name__ == "__main__":
    main()

