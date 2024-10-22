import datetime
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from init_db_conn import InitDB
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class GetData(InitDB):
    def __init__(self):
        super().__init__()

    def write_data(self):
        for value in range(10):
            point = (
                Point("measurement1")
                .tag("tagname1", "tagvalue1")
                .field("field1", value)
            )
            self.write_api.write(bucket=self.bucket, org=self.org, record=point)
            time.sleep(1)

    def write_sin_data(self):
        for x in range(75):
            x *= 0.05 * np.pi
            value = round(np.sin(x), 2)
            point2 = (
                Point("sin_val1")
                .tag("tagname2", "tagvalue2")
                .field("field2", value)
                .time(datetime.datetime.now(datetime.UTC), WritePrecision.US)
            )
            self.write_api.write(bucket=self.bucket, org=self.org, record=point2)
            time.sleep(1)

    def get_values(self):
        query = f"""
        from(bucket: "{self.bucket}")
        |> range (start: -1m)
        """
        tables = self.query_api.query(query)

        data = []
        for table in tables:
            for record in table.records:
                data.append({"time": record.get_time(), "value": record.get_value()})

        df = pd.DataFrame(data)

        df['time'] = pd.to_datetime(df['time'])
        df['time_formatted'] = df['time'].dt.strftime('%H:%M:%S')

        plt.figure(figsize=(10, 6))
        plt.plot(df["time"], df["value"], marker='o', linestyle='-', color='b')
        plt.xlabel('Time')
        plt.ylabel('The value of the indicator')
        plt.title('Graph of indicator values over time')

        plt.xticks(df["time"][::len(df) // 10], df["time_formatted"][::len(df) // 10], rotation=45)
        plt.grid()

        plt.tight_layout()
        plt.show()
        print(df)
