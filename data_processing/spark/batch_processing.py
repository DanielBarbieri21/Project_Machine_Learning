"""
Processamento de dados em batch usando Apache Spark.
"""
import logging
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when, count, avg, sum as spark_sum
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SparkBatchProcessor:
    """Classe para processamento batch com Spark."""
    
    def __init__(self, app_name: str = None, master: str = None):
        """
        Inicializa a sessão Spark.
        
        Args:
            app_name: Nome da aplicação Spark
            master: URL do master Spark (local[*], spark://host:port, etc.)
        """
        self.app_name = app_name or os.getenv('SPARK_APP_NAME', 'ML-Processing')
        self.master = master or os.getenv('SPARK_MASTER', 'local[*]')
        
        self.spark = SparkSession.builder \
            .appName(self.app_name) \
            .master(self.master) \
            .config("spark.sql.warehouse.dir", "/tmp/spark-warehouse") \
            .config("spark.driver.memory", os.getenv('SPARK_DRIVER_MEMORY', '4g')) \
            .config("spark.executor.memory", os.getenv('SPARK_EXECUTOR_MEMORY', '4g')) \
            .getOrCreate()
        
        logger.info(f"Sessão Spark criada: {self.app_name}")
    
    def read_csv(self, path: str, schema: StructType = None, **kwargs):
        """
        Lê arquivo CSV.
        
        Args:
            path: Caminho do arquivo CSV
            schema: Schema do DataFrame (opcional)
            **kwargs: Argumentos adicionais para read.csv
        
        Returns:
            DataFrame Spark
        """
        try:
            logger.info(f"Lendo CSV: {path}")
            df = self.spark.read.csv(path, schema=schema, header=True, **kwargs)
            logger.info(f"CSV lido: {df.count()} registros")
            return df
        except Exception as e:
            logger.error(f"Erro ao ler CSV: {e}")
            raise
    
    def read_parquet(self, path: str, **kwargs):
        """
        Lê arquivo Parquet.
        
        Args:
            path: Caminho do arquivo Parquet
            **kwargs: Argumentos adicionais
        
        Returns:
            DataFrame Spark
        """
        try:
            logger.info(f"Lendo Parquet: {path}")
            df = self.spark.read.parquet(path, **kwargs)
            logger.info(f"Parquet lido: {df.count()} registros")
            return df
        except Exception as e:
            logger.error(f"Erro ao ler Parquet: {e}")
            raise
    
    def read_json(self, path: str, **kwargs):
        """
        Lê arquivo JSON.
        
        Args:
            path: Caminho do arquivo JSON
            **kwargs: Argumentos adicionais
        
        Returns:
            DataFrame Spark
        """
        try:
            logger.info(f"Lendo JSON: {path}")
            df = self.spark.read.json(path, **kwargs)
            logger.info(f"JSON lido: {df.count()} registros")
            return df
        except Exception as e:
            logger.error(f"Erro ao ler JSON: {e}")
            raise
    
    def clean_data(self, df, drop_na: bool = False, fill_na: dict = None):
        """
        Limpa os dados.
        
        Args:
            df: DataFrame Spark
            drop_na: Se True, remove linhas com valores nulos
            fill_na: Dict com valores para preencher nulos
        
        Returns:
            DataFrame limpo
        """
        result_df = df
        
        if drop_na:
            result_df = result_df.dropna()
            logger.info("Linhas com valores nulos removidas")
        
        if fill_na:
            for column, value in fill_na.items():
                result_df = result_df.fillna({column: value})
            logger.info(f"Valores nulos preenchidos: {fill_na}")
        
        return result_df
    
    def aggregate_data(self, df, group_by: list, aggregations: dict):
        """
        Agrega dados.
        
        Args:
            df: DataFrame Spark
            group_by: Lista de colunas para agrupar
            aggregations: Dict com agregações (ex: {'value': 'avg', 'count': 'count'})
        
        Returns:
            DataFrame agregado
        """
        try:
            agg_exprs = []
            for column, func in aggregations.items():
                if func == 'avg':
                    agg_exprs.append(avg(column).alias(f'{column}_avg'))
                elif func == 'sum':
                    agg_exprs.append(spark_sum(column).alias(f'{column}_sum'))
                elif func == 'count':
                    agg_exprs.append(count(column).alias(f'{column}_count'))
                elif func == 'min':
                    agg_exprs.append(min(column).alias(f'{column}_min'))
                elif func == 'max':
                    agg_exprs.append(max(column).alias(f'{column}_max'))
            
            result_df = df.groupBy(*group_by).agg(*agg_exprs)
            logger.info(f"Dados agregados por: {group_by}")
            return result_df
            
        except Exception as e:
            logger.error(f"Erro na agregação: {e}")
            raise
    
    def save_parquet(self, df, path: str, mode: str = 'overwrite', partition_by: list = None):
        """
        Salva DataFrame como Parquet.
        
        Args:
            df: DataFrame Spark
            path: Caminho de destino
            mode: Modo de escrita ('overwrite', 'append', 'ignore', 'error')
            partition_by: Lista de colunas para particionamento
        """
        try:
            logger.info(f"Salvando Parquet: {path}")
            writer = df.write.mode(mode)
            if partition_by:
                writer = writer.partitionBy(*partition_by)
            writer.parquet(path)
            logger.info("Parquet salvo com sucesso")
        except Exception as e:
            logger.error(f"Erro ao salvar Parquet: {e}")
            raise
    
    def save_csv(self, df, path: str, mode: str = 'overwrite', header: bool = True):
        """
        Salva DataFrame como CSV.
        
        Args:
            df: DataFrame Spark
            path: Caminho de destino
            mode: Modo de escrita
            header: Se True, inclui cabeçalho
        """
        try:
            logger.info(f"Salvando CSV: {path}")
            df.write.mode(mode).option("header", header).csv(path)
            logger.info("CSV salvo com sucesso")
        except Exception as e:
            logger.error(f"Erro ao salvar CSV: {e}")
            raise
    
    def stop(self):
        """Para a sessão Spark."""
        self.spark.stop()
        logger.info("Sessão Spark encerrada")


def main():
    """Exemplo de uso do processador batch."""
    processor = SparkBatchProcessor()
    
    # Exemplo: criar DataFrame de exemplo
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("value", DoubleType(), True),
        StructField("category", StringType(), True)
    ])
    
    data = [(1, 10.5, "A"), (2, 20.3, "B"), (3, 15.7, "A"), (4, 25.1, "C")]
    df = processor.spark.createDataFrame(data, schema)
    
    # Limpar dados
    df_clean = processor.clean_data(df, fill_na={'value': 0.0})
    
    # Agregar dados
    df_agg = processor.aggregate_data(
        df_clean,
        group_by=['category'],
        aggregations={'value': 'avg', 'id': 'count'}
    )
    
    df_agg.show()
    
    processor.stop()


if __name__ == "__main__":
    main()

