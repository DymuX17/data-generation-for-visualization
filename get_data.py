import datetime
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from init_db_conn import InitDB
import numpy as np
import pandas as pd
import snap7
from snap7.util import get_real
from threading import Lock


class GetData(InitDB):
    def __init__(self):
        super().__init__()
        self.running = True
        self.buffer = {"opcua_y": None, "opcua_w": None, "snap7_y": None, "snap7_w": None}
        self.lock = Lock()

    def synchronize_and_send(self, producer):
        """
        Synchronizuje dane z różnych źródeł i wysyła je razem z tym samym znacznikiem czasowym.
        """
        with self.lock:
            if all(value is not None for value in self.buffer.values()):  # Jeśli wszystkie dane są dostępne
                time_val = datetime.datetime.now(datetime.timezone.utc).isoformat()

                # Wysłanie danych do odpowiednich tematów
                self.send_message("test-topic", producer, {"value": self.buffer["opcua_y"], "time": time_val})
                self.send_message("test-topic2", producer, {"value": self.buffer["opcua_w"], "time": time_val})
                self.send_message("test-topic3", producer, {"value": self.buffer["snap7_y"], "time": time_val})
                self.send_message("test-topic4", producer, {"value": self.buffer["snap7_w"], "time": time_val})

                # Czyszczenie bufora
                self.buffer = {"opcua_y": None, "opcua_w": None, "snap7_y": None, "snap7_w": None}
            else:
                missing_keys = [key for key, value in self.buffer.items() if value is None]
                print(f"Bufor niekompletny. Brakujące dane: {missing_keys}")

    def write_sin_data(self):
        for x in range(20):
            x *= 0.05 * np.pi
            value = round(np.sin(x), 2)
            point2 = (
                Point("sin_val1")
                .tag("tagname2", "tagvalue2")
                .field("field2", value)
                .time(datetime.datetime.now(datetime.timezone.utc), WritePrecision.US)
            )
            print(f"Received message: {value}, time: {datetime.datetime.now(datetime.timezone.utc)}, topic: sin_val1")
            self.write_api.write(bucket=self.bucket, org=self.org, record=point2)
            time.sleep(1)

    def write_snap7_data(self, producer):
        while self.running:
            try:
                db_n = 1
                start_addr = 0
                size = 8

                data = self.plc_snap7.db_read(db_n, start_addr, size)

                y = get_real(data, 0)  # Offset 0 dla zmiennej y
                w = get_real(data, 4)  # Offset 4 dla zmiennej w

                # Pobranie znacznika czasowego
                time_val = datetime.datetime.now(datetime.timezone.utc).isoformat()

                # Buforowanie danych
                with self.lock:
                    self.buffer["snap7_y"] = y
                    self.buffer["snap7_w"] = w

                if all(self.buffer.values()):
                    self.synchronize_and_send(producer)
                    self.buffer = {"opcua_y": None, "opcua_w": None, "snap7_y": None, "snap7_w": None}
                else:
                    pass

                time.sleep(1)

            except Exception as e:
                print(f"Błąd podczas odczytu danych dla S7Conn: {e}")

    def write_opcua_data(self, producer):
        while self.running:
            try:
                self.node1 = self.client_opcua.get_node('ns=3;s="Data_PID"."y"')
                value1 = self.node1.get_value()
                self.node2 = self.client_opcua.get_node('ns=3;s="Data_PID"."w"')
                value2 = self.node2.get_value()

                # Pobranie znacznika czasowego
                time_val = datetime.datetime.now(datetime.timezone.utc).isoformat()

                # Buforowanie danych
                with self.lock:
                    self.buffer["opcua_y"] = value1
                    self.buffer["opcua_w"] = value2

                if all(self.buffer.values()):
                    self.synchronize_and_send(producer)
                    self.buffer = {"opcua_y": None, "opcua_w": None, "snap7_y": None, "snap7_w": None}
                else:
                    pass

                time.sleep(1)

            except Exception as e:
                print(f"Błąd podczas odczytu danych dla OPC UA: {e}")





