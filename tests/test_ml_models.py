"""
Testes para modelos ML.
"""
import pytest
import pandas as pd
import numpy as np
from sklearn.datasets import make_classification, make_regression
from ml.models.classification_model import ClassificationModel
from ml.models.regression_model import RegressionModel


def test_classification_model():
    """Testa modelo de classificação."""
    X, y = make_classification(n_samples=100, n_features=10, n_classes=2, random_state=42)
    X_df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(10)])
    y_series = pd.Series(y)
    
    model = ClassificationModel(model_type='random_forest', n_estimators=10)
    metrics = model.train(X_df, y_series, mlflow_tracking=False)
    
    assert 'accuracy' in metrics
    assert metrics['accuracy'] > 0
    
    predictions = model.predict(X_df[:5])
    assert len(predictions) == 5


def test_regression_model():
    """Testa modelo de regressão."""
    X, y = make_regression(n_samples=100, n_features=10, random_state=42)
    X_df = pd.DataFrame(X, columns=[f'feature_{i}' for i in range(10)])
    y_series = pd.Series(y)
    
    model = RegressionModel(model_type='random_forest', n_estimators=10)
    metrics = model.train(X_df, y_series, mlflow_tracking=False)
    
    assert 'r2_score' in metrics
    assert metrics['r2_score'] > -1
    
    predictions = model.predict(X_df[:5])
    assert len(predictions) == 5

