"""
Script principal para treinamento de modelos ML.
"""
import argparse
import logging
import pandas as pd
import os
from dotenv import load_dotenv
from ml.models.classification_model import ClassificationModel
from ml.models.regression_model import RegressionModel

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_classification_model(data_path: str, model_type: str = 'random_forest'):
    """Treina um modelo de classificação."""
    logger.info(f"Treinando modelo de classificação: {model_type}")
    
    # Carregar dados
    df = pd.read_csv(data_path)
    
    # Assumindo que a última coluna é o target
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    
    # Criar e treinar modelo
    model = ClassificationModel(model_type=model_type)
    metrics = model.train(X, y)
    
    # Salvar modelo
    model_path = f"models/classification_{model_type}.pkl"
    os.makedirs("models", exist_ok=True)
    model.save(model_path)
    
    logger.info(f"Modelo salvo em: {model_path}")
    return metrics


def train_regression_model(data_path: str, model_type: str = 'random_forest'):
    """Treina um modelo de regressão."""
    logger.info(f"Treinando modelo de regressão: {model_type}")
    
    # Carregar dados
    df = pd.read_csv(data_path)
    
    # Assumindo que a última coluna é o target
    X = df.iloc[:, :-1]
    y = df.iloc[:, -1]
    
    # Criar e treinar modelo
    model = RegressionModel(model_type=model_type)
    metrics = model.train(X, y)
    
    # Salvar modelo
    model_path = f"models/regression_{model_type}.pkl"
    os.makedirs("models", exist_ok=True)
    model.save(model_path)
    
    logger.info(f"Modelo salvo em: {model_path}")
    return metrics


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(description='Treinar modelos de ML')
    parser.add_argument(
        '--model-type',
        type=str,
        choices=['classification', 'regression'],
        required=True,
        help='Tipo de modelo a treinar'
    )
    parser.add_argument(
        '--algorithm',
        type=str,
        default='random_forest',
        choices=['random_forest', 'gradient_boosting', 'logistic_regression', 'linear'],
        help='Algoritmo a usar'
    )
    parser.add_argument(
        '--data-path',
        type=str,
        required=True,
        help='Caminho do arquivo de dados'
    )
    
    args = parser.parse_args()
    
    if args.model_type == 'classification':
        train_classification_model(args.data_path, args.algorithm)
    elif args.model_type == 'regression':
        train_regression_model(args.data_path, args.algorithm)


if __name__ == "__main__":
    main()

