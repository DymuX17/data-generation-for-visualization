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
import datetime
import snap7
from snap7.util import get_real


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
            self.node1 = None
            self.node2 = None
            self.plc_snap7 = None
            self.url_opcua = "opc.tcp://192.168.1.105:4840"
            self.client_opcua = Client(self.url_opcua)
            self.admin_client = None

            self.KAFKA_BROKER = '127.0.0.1:9092'

            self.connect()
            self.opcua_connect()
            self.snap7_connect()
            InitDB._conn_init = True

    def connect(self):
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

    def opcua_connect(self):
        try:
            self.client_opcua.connect()
            print("Connected with OPC UA server")

        except Exception as e:
            print('Error: ', e)

    def snap7_connect(self):
        self.plc_snap7 = snap7.client.Client()
        self.plc_snap7.connect('192.168.1.110', 0, 1)
        if self.plc_snap7.get_connected():
            print("Połączono z PLC!")
        else:
            print("Nie udało się połączyć.")
            exit()

    def create_topic(self, topic_name):
        try:
            self.admin_client = KafkaAdminClient(bootstrap_servers=self.KAFKA_BROKER)
            topic = NewTopic(name=topic_name, num_partitions=1, replication_factor=1)
            self.admin_client.create_topics([topic])
        except Exception as e:
            if "TopicExistsException" in str(e):
                print(f"Temat {topic_name} już istnieje.")
            else:
                print(f"Błąd podczas tworzenia tematu {topic_name}: {e}")

    def check_and_create_topics(self, admin_client, topics):

        existing_topics = admin_client.list_topics()  # Pobranie listy istniejących tematów
        for topic in topics:
            if topic not in existing_topics:
                print(f"Tworzenie tematu: {topic}")
                self.create_topic(topic)

            else:
                print(f"Temat {topic} już istnieje.")

    def create_producer(self):
        return KafkaProducer(
            bootstrap_servers=self.KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def create_consumer(self, topic_name, group_id):
        return KafkaConsumer(
            topic_name,
            bootstrap_servers=self.KAFKA_BROKER,
            group_id=group_id,
            enable_auto_commit=True,  # Automatyczne zatwierdzanie offsetów
            auto_commit_interval_ms=1000,  # Zatwierdzaj offsety co 1 sekundę
            auto_offset_reset='latest',  # Pobieraj tylko nowe wiadomości
            fetch_max_wait_ms=500,  # Czekaj maksymalnie 0.5s na wiadomości
            fetch_min_bytes=1,  # Pobierz nawet najmniejszą wiadomość
            session_timeout_ms=30000,  # Timeout sesji
            heartbeat_interval_ms=10000,  # Interwał heartbeat
            value_deserializer=lambda m: json.loads(m.decode('utf-8'))
        )

    def send_message(self, topic_name, producer, message):
        producer.send(topic_name, message)
        producer.flush()

    def write_to_influx(self, value, time_val, point_name):
        point = (
            # Point("opc_val1")
            Point(point_name)
            .tag("opcua", "plc")
            .field("field3", value)
            .time(time_val, WritePrecision.NS)
        )
        self.write_api.write(bucket=self.bucket, org=self.org, record=point)

    def receive_message(self, topic_name, consumer):
        for message in consumer:
            try:
                message_data = message.value
                if isinstance(message_data, dict):
                    value = message_data.get('value')
                    time_val = message_data.get('time')
                    time_val = datetime.datetime.fromisoformat(time_val)
                    topic_name = str(topic_name)
                    print(f"Received message: {value}, time: {time_val}, topic: {topic_name}")

                    self.write_to_influx(value, time_val, topic_name)
                    print('data sent to influx...')

            except Exception as e:
                print(e)

            time.sleep(1)







