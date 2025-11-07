"""
ETL Batch para ingestão de dados em lote.
Suporta múltiplas fontes: databases, arquivos, APIs.
"""
import logging
import pandas as pd
import os
from typing import List, Dict, Any, Optional
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BatchDataIngestion:
    """Classe para ingestão de dados em lote."""
    
    def __init__(self):
        """Inicializa o ingestor batch."""
        self.postgres_engine = self._create_postgres_engine()
    
    def _create_postgres_engine(self):
        """Cria conexão com PostgreSQL."""
        try:
            host = os.getenv('POSTGRES_HOST', 'localhost')
            port = os.getenv('POSTGRES_PORT', '5432')
            user = os.getenv('POSTGRES_USER', 'airflow')
            password = os.getenv('POSTGRES_PASSWORD', 'airflow')
            database = os.getenv('POSTGRES_DB', 'airflow')
            
            connection_string = (
                f"postgresql://{user}:{password}@{host}:{port}/{database}"
            )
            engine = create_engine(connection_string)
            logger.info("Conexão PostgreSQL criada")
            return engine
        except Exception as e:
            logger.error(f"Erro ao conectar PostgreSQL: {e}")
            return None
    
    def ingest_from_csv(
        self,
        file_path: str,
        chunk_size: int = 10000,
        **kwargs
    ) -> pd.DataFrame:
        """
        Ingere dados de um arquivo CSV.
        
        Args:
            file_path: Caminho do arquivo CSV
            chunk_size: Tamanho do chunk para leitura (None = tudo de uma vez)
            **kwargs: Argumentos adicionais para pd.read_csv
        
        Returns:
            DataFrame com os dados
        """
        try:
            logger.info(f"Ingerindo dados de {file_path}")
            
            if chunk_size:
                chunks = []
                for chunk in pd.read_csv(file_path, chunksize=chunk_size, **kwargs):
                    chunks.append(chunk)
                df = pd.concat(chunks, ignore_index=True)
            else:
                df = pd.read_csv(file_path, **kwargs)
            
            logger.info(f"Dados ingeridos: {len(df)} registros")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao ingerir CSV: {e}")
            raise
    
    def ingest_from_json(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Ingere dados de um arquivo JSON.
        
        Args:
            file_path: Caminho do arquivo JSON
            **kwargs: Argumentos adicionais para pd.read_json
        
        Returns:
            DataFrame com os dados
        """
        try:
            logger.info(f"Ingerindo dados de {file_path}")
            df = pd.read_json(file_path, **kwargs)
            logger.info(f"Dados ingeridos: {len(df)} registros")
            return df
        except Exception as e:
            logger.error(f"Erro ao ingerir JSON: {e}")
            raise
    
    def ingest_from_database(
        self,
        query: str,
        connection_engine = None
    ) -> pd.DataFrame:
        """
        Ingere dados de um banco de dados usando SQL.
        
        Args:
            query: Query SQL para executar
            connection_engine: Engine SQLAlchemy (usa PostgreSQL padrão se None)
        
        Returns:
            DataFrame com os dados
        """
        try:
            engine = connection_engine or self.postgres_engine
            if not engine:
                raise ValueError("Nenhuma conexão de banco de dados disponível")
            
            logger.info(f"Executando query: {query[:100]}...")
            df = pd.read_sql(query, engine)
            logger.info(f"Dados ingeridos: {len(df)} registros")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao ingerir do banco de dados: {e}")
            raise
    
    def ingest_from_parquet(self, file_path: str, **kwargs) -> pd.DataFrame:
        """
        Ingere dados de um arquivo Parquet.
        
        Args:
            file_path: Caminho do arquivo Parquet
            **kwargs: Argumentos adicionais para pd.read_parquet
        
        Returns:
            DataFrame com os dados
        """
        try:
            logger.info(f"Ingerindo dados de {file_path}")
            df = pd.read_parquet(file_path, **kwargs)
            logger.info(f"Dados ingeridos: {len(df)} registros")
            return df
        except Exception as e:
            logger.error(f"Erro ao ingerir Parquet: {e}")
            raise
    
    def save_to_data_lake(
        self,
        df: pd.DataFrame,
        destination: str,
        format: str = 'parquet',
        partition_by: Optional[List[str]] = None
    ):
        """
        Salva dados no Data Lake.
        
        Args:
            df: DataFrame para salvar
            destination: Caminho de destino
            format: Formato de arquivo ('parquet', 'csv', 'json')
            partition_by: Colunas para particionamento
        """
        try:
            os.makedirs(os.path.dirname(destination), exist_ok=True)
            
            if format == 'parquet':
                df.to_parquet(destination, partition_cols=partition_by, index=False)
            elif format == 'csv':
                df.to_csv(destination, index=False)
            elif format == 'json':
                df.to_json(destination, orient='records', lines=True)
            else:
                raise ValueError(f"Formato não suportado: {format}")
            
            logger.info(f"Dados salvos em {destination}")
            
        except Exception as e:
            logger.error(f"Erro ao salvar no Data Lake: {e}")
            raise
    
    def transform_data(
        self,
        df: pd.DataFrame,
        transformations: List[Dict[str, Any]]
    ) -> pd.DataFrame:
        """
        Aplica transformações aos dados.
        
        Args:
            df: DataFrame a ser transformado
            transformations: Lista de transformações a aplicar
                Cada transformação é um dict com 'type' e parâmetros
        
        Returns:
            DataFrame transformado
        """
        result_df = df.copy()
        
        for transformation in transformations:
            transform_type = transformation.get('type')
            
            if transform_type == 'rename_columns':
                result_df = result_df.rename(columns=transformation.get('mapping', {}))
            
            elif transform_type == 'filter':
                condition = transformation.get('condition')
                if condition:
                    result_df = result_df.query(condition)
            
            elif transform_type == 'add_column':
                column = transformation.get('column')
                value = transformation.get('value')
                if column:
                    result_df[column] = value
            
            elif transform_type == 'drop_columns':
                columns = transformation.get('columns', [])
                result_df = result_df.drop(columns=columns, errors='ignore')
            
            elif transform_type == 'fillna':
                method = transformation.get('method', 'forward')
                result_df = result_df.fillna(method=method)
            
            logger.info(f"Transformação '{transform_type}' aplicada")
        
        return result_df


def main():
    """Exemplo de uso do ingestor batch."""
    ingestor = BatchDataIngestion()
    
    # Exemplo: ingerir CSV
    # df = ingestor.ingest_from_csv('data/sample.csv')
    
    # Exemplo: aplicar transformações
    sample_data = pd.DataFrame({
        'id': range(100),
        'value': range(100, 200),
        'category': ['A', 'B', 'C'] * 33 + ['A']
    })
    
    transformations = [
        {'type': 'rename_columns', 'mapping': {'id': 'identifier'}},
        {'type': 'filter', 'condition': 'value > 150'},
        {'type': 'add_column', 'column': 'processed', 'value': True}
    ]
    
    transformed_df = ingestor.transform_data(sample_data, transformations)
    print(transformed_df.head())


if __name__ == "__main__":
    main()

