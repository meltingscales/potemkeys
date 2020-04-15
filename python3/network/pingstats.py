#!/usr/bin/env python2
import os
import time
from typing import Any

from ping3 import ping, verbose_ping
import datetime

import argparse


class PingEvent:
    def __init__(self, host: str, time: datetime.datetime, ms: float):
        self.host = host
        self.time = time
        self.ping_time = ms

    def __str__(self):
        return f"""{self.time}
PING {args.host}
{r * 1000:.2f}ms"""

    def get_csv_value(self, column_name: str) -> str:
        if column_name == 'host':
            return str(self.host)
        if column_name == 'time':
            return str(self.time)
        if column_name == 'ping_time':
            return str(self.ping_time)
        raise Exception(f"No column name called {column_name}!")

    def as_csv_row(self, rows=('host', 'time', 'ping_time')):

        rowValues = []
        for row in rows:
            rowValues.append(self.get_csv_value(row))

        return ','.join(rowValues)


parser = argparse.ArgumentParser(description='Conduct a ping test and save a log.')

parser.add_argument('--host', help='Host to ping.', required=True)
parser.add_argument('--ping_delay', help='Delay between pings in ms', default=1000.0)
parser.add_argument('--ping_amount', help='Amount of pings to do.', default=10)  # 86400 seconds or is 1 hour

args = parser.parse_args()

if __name__ == '__main__':

    for i in range(0, args.ping_amount):
        r = ping(args.host)
        pingEvent = PingEvent(args.host, datetime.datetime.now(), (r * 1000))
        print(pingEvent.as_csv_row())
        time.sleep(args.ping_delay / 1000.0)
