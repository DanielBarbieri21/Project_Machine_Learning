"""
Kafka Consumer para processar dados em tempo real.
"""
import json
import logging
from typing import Callable, Optional
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KafkaDataConsumer:
    """Consumer Kafka para receber e processar dados."""
    
    def __init__(
        self,
        bootstrap_servers: str = None,
        topic: str = None,
        group_id: str = None,
        auto_offset_reset: str = 'earliest'
    ):
        """
        Inicializa o consumer Kafka.
        
        Args:
            bootstrap_servers: Servidores Kafka
            topic: Nome do tópico Kafka
            group_id: ID do grupo de consumidores
            auto_offset_reset: Onde começar a ler ('earliest' ou 'latest')
        """
        self.bootstrap_servers = bootstrap_servers or os.getenv(
            'KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'
        )
        self.topic = topic or os.getenv(
            'KAFKA_TOPIC_DATA_INGESTION', 'data-ingestion'
        )
        self.group_id = group_id or 'ml-data-consumer-group'
        
        self.consumer = KafkaConsumer(
            self.topic,
            bootstrap_servers=self.bootstrap_servers,
            group_id=self.group_id,
            auto_offset_reset=auto_offset_reset,
            value_deserializer=lambda m: json.loads(m.decode('utf-8')),
            key_deserializer=lambda k: k.decode('utf-8') if k else None,
            enable_auto_commit=True,
            consumer_timeout_ms=1000
        )
        
        logger.info(f"Kafka Consumer inicializado: {self.topic}")
    
    def consume(self, callback: Callable = None, max_messages: Optional[int] = None):
        """
        Consome mensagens do tópico Kafka.
        
        Args:
            callback: Função para processar cada mensagem
            max_messages: Número máximo de mensagens a processar (None = ilimitado)
        """
        message_count = 0
        
        try:
            logger.info(f"Iniciando consumo do tópico {self.topic}")
            
            for message in self.consumer:
                try:
                    data = message.value
                    key = message.key
                    
                    logger.info(
                        f"Mensagem recebida - Tópico: {message.topic}, "
                        f"Partição: {message.partition}, "
                        f"Offset: {message.offset}, "
                        f"Key: {key}"
                    )
                    
                    # Processa a mensagem
                    if callback:
                        callback(data, key, message)
                    else:
                        self.default_callback(data, key, message)
                    
                    message_count += 1
                    
                    if max_messages and message_count >= max_messages:
                        logger.info(f"Processadas {max_messages} mensagens. Parando.")
                        break
                        
                except Exception as e:
                    logger.error(f"Erro ao processar mensagem: {e}", exc_info=True)
        
        except KafkaError as e:
            logger.error(f"Erro no consumer Kafka: {e}")
        
        finally:
            self.close()
    
    def default_callback(self, data: dict, key: str, message):
        """Callback padrão que apenas imprime os dados."""
        print(f"Key: {key}, Data: {json.dumps(data, indent=2)}")
    
    def close(self):
        """Fecha a conexão com o Kafka."""
        self.consumer.close()
        logger.info("Consumer Kafka fechado")


def main():
    """Exemplo de uso do consumer."""
    
    def process_message(data: dict, key: str, message):
        """Função de processamento personalizada."""
        print(f"Processando dados do sensor {key}: {data}")
        # Aqui você pode adicionar lógica de processamento
        # Por exemplo, salvar no banco de dados, processar com ML, etc.
    
    consumer = KafkaDataConsumer()
    consumer.consume(callback=process_message, max_messages=10)


if __name__ == "__main__":
    main()

