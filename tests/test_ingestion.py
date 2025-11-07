"""
Testes para ingestão de dados.
"""
import pytest
import pandas as pd
from data_ingestion.etl.batch_ingestion import BatchDataIngestion


def test_ingest_from_csv(tmp_path):
    """Testa ingestão de CSV."""
    # Cria arquivo CSV temporário
    test_file = tmp_path / "test.csv"
    df = pd.DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
    df.to_csv(test_file, index=False)
    
    # Testa ingestão
    ingestor = BatchDataIngestion()
    result_df = ingestor.ingest_from_csv(str(test_file))
    
    assert len(result_df) == 3
    assert list(result_df.columns) == ["col1", "col2"]


def test_transform_data():
    """Testa transformação de dados."""
    ingestor = BatchDataIngestion()
    df = pd.DataFrame({"old_name": [1, 2, 3], "value": [10, 20, 30]})
    
    transformations = [
        {"type": "rename_columns", "mapping": {"old_name": "new_name"}},
        {"type": "filter", "condition": "value > 15"}
    ]
    
    result_df = ingestor.transform_data(df, transformations)
    
    assert "new_name" in result_df.columns
    assert len(result_df) == 2

