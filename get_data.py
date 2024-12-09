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



    def write_sin_data(self):
        for x in range(75):
            x *= 0.05 * np.pi
            value = round(np.sin(x), 2)
            point2 = (
                Point("sin_val1")
                .tag("tagname2", "tagvalue2")
                .field("field2", value)
                .time(datetime.datetime.now(datetime.timezone.utc), WritePrecision.US)
            )
            self.write_api.write(bucket=self.bucket, org=self.org, record=point2)
            time.sleep(1)


