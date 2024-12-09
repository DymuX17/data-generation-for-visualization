import influxdb_client, os, time
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
            self.Client = Client(self.url_opcua)

            self.connect()
            InitDB._conn_init = True

    def connect(self):
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()


'''
        try:
            self.Client.connect()
            print("Connected with OPC UA server")
            self.node = Client.get_node("ns=3;s=a")
            value = self.node.get_value()
            print('value: ', value)
        except Exception as e:
            print('Error: ', e)
        finally:
            self.Client.disconnect()
            print('Disconnected from OPC UA server...')

'''