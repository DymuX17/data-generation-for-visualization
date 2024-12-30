import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic

class KafkaManager:
    def __init__(self, kafka_broker, topic):
        self.KAFKA_BROKER = kafka_broker
        self.TOPIC = topic

    def create_topic(self):
        """
        Creates a Kafka topic if it does not already exist.
        """
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=self.KAFKA_BROKER)
            topic = NewTopic(name=self.TOPIC, num_partitions=1, replication_factor=1)
            admin_client.create_topics([topic], validate_only=False)
            print(f"Topic '{self.TOPIC}' created successfully.")
        except Exception as e:
            print(f"Error creating topic '{self.TOPIC}': {e}")

    def create_producer(self):
        """
        Creates a Kafka producer.
        """
        return KafkaProducer(
            bootstrap_servers=self.KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def create_consumer(self):
        """
        Creates a Kafka consumer.
        """
        return KafkaConsumer(
            self.TOPIC,
            bootstrap_servers=self.KAFKA_BROKER,
            group_id='test-group',
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

    def send_message(self, producer, message):
        """
        Sends a message to the Kafka topic.
        """
        try:
            producer.send(self.TOPIC, message)
            producer.flush()
            print(f"Message sent: {message}")
        except Exception as e:
            print(f"Error sending message: {e}")

    def receive_message(self, consumer):
        """
        Listens for messages on the Kafka topic.
        """
        print(f"Listening for messages on topic '{self.TOPIC}'...")
        try:
            for message in consumer:
                print(f"Received message: {message.value}")
        except Exception as e:
            print(f"Error receiving message: {e}")
