"""
Kafka Producer para ingestão de dados em tempo real.
"""
import json
import time
import logging
from typing import Dict, Any
from kafka import KafkaProducer
from kafka.errors import KafkaError
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KafkaDataProducer:
    """Producer Kafka para envio de dados."""
    
    def __init__(
        self,
        bootstrap_servers: str = None,
        topic: str = None
    ):
        """
        Inicializa o producer Kafka.
        
        Args:
            bootstrap_servers: Servidores Kafka (ex: localhost:9092)
            topic: Nome do tópico Kafka
        """
        self.bootstrap_servers = bootstrap_servers or os.getenv(
            'KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'
        )
        self.topic = topic or os.getenv(
            'KAFKA_TOPIC_DATA_INGESTION', 'data-ingestion'
        )
        
        self.producer = KafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8') if k else None,
            acks='all',
            retries=3,
            max_in_flight_requests_per_connection=1
        )
        
        logger.info(f"Kafka Producer inicializado: {self.bootstrap_servers}")
    
    def send_data(self, data: Dict[Any, Any], key: str = None):
        """
        Envia dados para o tópico Kafka.
        
        Args:
            data: Dados a serem enviados (dict)
            key: Chave para particionamento (opcional)
        """
        try:
            future = self.producer.send(
                self.topic,
                value=data,
                key=key
            )
            
            # Aguarda confirmação
            record_metadata = future.get(timeout=10)
            
            logger.info(
                f"Dados enviados para tópico {record_metadata.topic} "
                f"partição {record_metadata.partition} "
                f"offset {record_metadata.offset}"
            )
            
            return True
            
        except KafkaError as e:
            logger.error(f"Erro ao enviar dados para Kafka: {e}")
            return False
    
    def send_batch(self, data_list: list, key_field: str = None):
        """
        Envia múltiplos registros em batch.
        
        Args:
            data_list: Lista de dados para enviar
            key_field: Campo a ser usado como chave (opcional)
        """
        success_count = 0
        for data in data_list:
            key = data.get(key_field) if key_field else None
            if self.send_data(data, key):
                success_count += 1
        
        logger.info(f"Enviados {success_count}/{len(data_list)} registros")
        return success_count
    
    def close(self):
        """Fecha a conexão com o Kafka."""
        self.producer.close()
        logger.info("Conexão Kafka fechada")


def main():
    """Exemplo de uso do producer."""
    producer = KafkaDataProducer()
    
    # Exemplo: enviar dados de sensores
    sensor_data = {
        "sensor_id": "sensor_001",
        "timestamp": time.time(),
        "temperature": 23.5,
        "humidity": 65.0,
        "location": "warehouse_A"
    }
    
    producer.send_data(sensor_data, key="sensor_001")
    
    # Exemplo: enviar batch
    batch_data = [
        {"id": i, "value": i * 2, "timestamp": time.time()}
        for i in range(10)
    ]
    producer.send_batch(batch_data, key_field="id")
    
    producer.close()


if __name__ == "__main__":
    main()

