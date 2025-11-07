"""
Processamento de dados em streaming usando Apache Spark Streaming.
"""
import logging
import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json, window, count, avg
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SparkStreamingProcessor:
    """Classe para processamento streaming com Spark."""
    
    def __init__(self, app_name: str = None, master: str = None):
        """
        Inicializa a sessão Spark Streaming.
        
        Args:
            app_name: Nome da aplicação Spark
            master: URL do master Spark
        """
        self.app_name = app_name or os.getenv('SPARK_APP_NAME', 'ML-Streaming')
        self.master = master or os.getenv('SPARK_MASTER', 'local[*]')
        
        self.spark = SparkSession.builder \
            .appName(self.app_name) \
            .master(self.master) \
            .config("spark.sql.streaming.checkpointLocation", "/tmp/checkpoint") \
            .getOrCreate()
        
        logger.info(f"Sessão Spark Streaming criada: {self.app_name}")
    
    def read_from_kafka(
        self,
        kafka_bootstrap_servers: str,
        topics: str,
        starting_offsets: str = 'latest'
    ):
        """
        Lê dados do Kafka.
        
        Args:
            kafka_bootstrap_servers: Servidores Kafka
            topics: Tópicos Kafka (separados por vírgula)
            starting_offsets: Offset inicial ('earliest' ou 'latest')
        
        Returns:
            DataFrame de streaming
        """
        try:
            logger.info(f"Conectando ao Kafka: {topics}")
            
            df = self.spark \
                .readStream \
                .format("kafka") \
                .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
                .option("subscribe", topics) \
                .option("startingOffsets", starting_offsets) \
                .load()
            
            logger.info("Conexão Kafka estabelecida")
            return df
            
        except Exception as e:
            logger.error(f"Erro ao conectar ao Kafka: {e}")
            raise
    
    def parse_json_stream(self, df, schema: StructType, value_column: str = 'value'):
        """
        Parse JSON do stream.
        
        Args:
            df: DataFrame de streaming
            schema: Schema do JSON
            value_column: Nome da coluna com JSON
        
        Returns:
            DataFrame parseado
        """
        try:
            parsed_df = df.select(
                col("key").cast("string"),
                from_json(col(value_column).cast("string"), schema).alias("data"),
                col("timestamp")
            ).select("key", "data.*", "timestamp")
            
            return parsed_df
            
        except Exception as e:
            logger.error(f"Erro ao parsear JSON: {e}")
            raise
    
    def aggregate_stream(
        self,
        df,
        window_duration: str,
        slide_duration: str,
        group_by: list,
        aggregations: dict
    ):
        """
        Agrega dados do stream por janela de tempo.
        
        Args:
            df: DataFrame de streaming
            window_duration: Duração da janela (ex: '5 minutes')
            slide_duration: Duração do slide (ex: '1 minute')
            group_by: Colunas para agrupar
            aggregations: Dict com agregações
        
        Returns:
            DataFrame agregado
        """
        try:
            windowed_df = df.withWatermark("timestamp", window_duration) \
                .groupBy(window(col("timestamp"), window_duration, slide_duration), *group_by)
            
            # Adiciona agregações
            from pyspark.sql.functions import sum as spark_sum
            agg_exprs = []
            for column, func in aggregations.items():
                if func == 'count':
                    agg_exprs.append(count(column).alias(f'{column}_count'))
                elif func == 'avg':
                    agg_exprs.append(avg(column).alias(f'{column}_avg'))
                elif func == 'sum':
                    agg_exprs.append(spark_sum(column).alias(f'{column}_sum'))
            
            result_df = windowed_df.agg(*agg_exprs)
            return result_df
            
        except Exception as e:
            logger.error(f"Erro na agregação do stream: {e}")
            raise
    
    def write_to_console(self, df, output_mode: str = 'complete', truncate: bool = False):
        """
        Escreve stream no console (para debug).
        
        Args:
            df: DataFrame de streaming
            output_mode: Modo de saída ('append', 'complete', 'update')
            truncate: Se True, trunca strings longas
        
        Returns:
            StreamingQuery
        """
        query = df.writeStream \
            .outputMode(output_mode) \
            .format("console") \
            .option("truncate", truncate) \
            .start()
        
        return query
    
    def write_to_parquet(
        self,
        df,
        path: str,
        output_mode: str = 'append',
        checkpoint_location: str = None
    ):
        """
        Escreve stream em Parquet.
        
        Args:
            df: DataFrame de streaming
            path: Caminho de destino
            output_mode: Modo de saída
            checkpoint_location: Localização do checkpoint
        
        Returns:
            StreamingQuery
        """
        checkpoint = checkpoint_location or f"/tmp/checkpoint/{path}"
        
        query = df.writeStream \
            .outputMode(output_mode) \
            .format("parquet") \
            .option("path", path) \
            .option("checkpointLocation", checkpoint) \
            .start()
        
        return query
    
    def write_to_kafka(
        self,
        df,
        kafka_bootstrap_servers: str,
        topic: str,
        checkpoint_location: str = None
    ):
        """
        Escreve stream no Kafka.
        
        Args:
            df: DataFrame de streaming
            kafka_bootstrap_servers: Servidores Kafka
            topic: Tópico de destino
            checkpoint_location: Localização do checkpoint
        
        Returns:
            StreamingQuery
        """
        checkpoint = checkpoint_location or f"/tmp/checkpoint/kafka/{topic}"
        
        query = df.writeStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
            .option("topic", topic) \
            .option("checkpointLocation", checkpoint) \
            .start()
        
        return query
    
    def stop(self):
        """Para a sessão Spark."""
        self.spark.stop()
        logger.info("Sessão Spark Streaming encerrada")


def main():
    """Exemplo de uso do processador streaming."""
    processor = SparkStreamingProcessor()
    
    # Exemplo: ler do Kafka
    kafka_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
    topics = os.getenv('KAFKA_TOPIC_DATA_INGESTION', 'data-ingestion')
    
    # Schema do JSON esperado
    schema = StructType([
        StructField("sensor_id", StringType(), True),
        StructField("temperature", DoubleType(), True),
        StructField("timestamp", TimestampType(), True)
    ])
    
    # Lê stream do Kafka
    kafka_df = processor.read_from_kafka(kafka_servers, topics)
    
    # Parse JSON
    parsed_df = processor.parse_json_stream(kafka_df, schema)
    
    # Agrega por janela
    aggregated_df = processor.aggregate_stream(
        parsed_df,
        window_duration='5 minutes',
        slide_duration='1 minute',
        group_by=['sensor_id'],
        aggregations={'temperature': 'avg', 'sensor_id': 'count'}
    )
    
    # Escreve no console
    query = processor.write_to_console(aggregated_df)
    
    # Aguarda processamento
    query.awaitTermination()


if __name__ == "__main__":
    main()

