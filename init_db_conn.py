import influxdb_client, os, time
import json
from kafka import KafkaProducer, KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
import threading
import opcua
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from dotenv import load_dotenv
from opcua import Client


class InitDB:
    _conn_init = False
    load_dotenv()

    def __init__(self):
        if not InitDB._conn_init:
            self.token = os.getenv("INFLUX_TOKEN")
            self.org = os.getenv("INFLUX_ORG")
            self.url = os.getenv("INFLUX_URL")
            self.bucket = os.getenv("INFLUX_BUCKET")
            self.client = None
            self.write_api = None
            self.query_api = None
            self.node = None
            self.url_opcua = "opc.tcp://192.168.1.100:4840"
            # self.url_opcua = "opc.tcp://192.168.1.100:4840"
            self.client_opcua = Client(self.url_opcua)

            self.KAFKA_BROKER = "127.0.0.1:9092"
            self.TOPIC = 'ttopic'

            self.connect()
            self.opcua_connect()
            InitDB._conn_init = True

    def connect(self):
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

    def opcua_connect(self):
        try:
            self.client_opcua.connect()
            print("Connected with OPC UA server")
            # self.node = self.client_opcua.get_node("ns=3;s=a")
            # value = self.node.get_value()
            # print('value: ', value)
        except Exception as e:
            print('Error: ', e)
        # finally:
        #     self.client_opcua.disconnect()
        #     print('Disconnected from OPC UA server...')

    def create_topic(self):
        try:
            admin_client = KafkaAdminClient(bootstrap_servers=self.KAFKA_BROKER)
            topic = NewTopic(name=self.TOPIC, num_partitions=1, replication_factor=1)
            admin_client.create_topics([topic])
        except Exception:
            pass

    def create_producer(self):
        return KafkaProducer(
            bootstrap_servers=self.KAFKA_BROKER,
            # Ensure self.KAFKA_BROKER is set correctly (e.g., '192.168.100.3:9092')
            api_version=(3, 9, 0),  # Ensure this matches the broker's version
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            metadata_max_age_ms=60000,  # Refresh metadata every 60 seconds
            request_timeout_ms=30000,  # Timeout for producer requests
            retries=5,  # Retry sending messages up to 5 times
            max_in_flight_requests_per_connection=5,  # Limit in-flight requests
            linger_ms=10,  # Add a small delay to batch messages
            compression_type='gzip'  # Compress messages for efficiency
        )

    def create_consumer(self):
        return KafkaConsumer(
            self.TOPIC,
            bootstrap_servers=self.KAFKA_BROKER,
            api_version=(3, 9, 0),
            group_id='test-group',
            auto_offset_reset='earliest',
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

    def send_message(self, producer, message):
        producer.send(self.TOPIC, message)
        producer.flush()

    def receive_message(self, consumer):
        print(f"Listening for messages on topic '{self.TOPIC}'...")
        for message in consumer:
            print(f"Received message: {message.value}")