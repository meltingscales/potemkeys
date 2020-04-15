#!/usr/bin/env python2
import argparse
import datetime
import os
import socket
import time
from typing import Tuple
from time import gmtime, strftime
from ping3 import ping


class PingEvent:

    @staticmethod
    def ping_now(host: str):
        return PingEvent(host, datetime.datetime.now(), (ping(args.host) * 1000))

    @staticmethod
    def get_rows() -> Tuple[str, str, str]:
        return 'host', 'time', 'ping_time'

    @staticmethod
    def get_csv_rows() -> str:
        return ','.join(PingEvent.get_rows())

    def __init__(self, host: str, time: datetime.datetime, ms: float):
        self.host = host
        self.time = time
        self.ping_time = ms

    def __str__(self):
        return (f"{self.time}\n"
                f"PING {args.host}\n"
                f"{r * 1000:.2f}ms")

    def get_csv_value(self, column_name: str) -> str:

        if column_name not in self.get_rows():
            raise Exception(f"No column name called {column_name}!")

        if column_name == 'host':
            return str(self.host)
        if column_name == 'time':
            return str(self.time)
        if column_name == 'ping_time':
            return str(self.ping_time)

    def as_csv_row(self, rows=None):

        rows = self.get_rows()

        rowValues = []
        for row in rows:
            rowValues.append(self.get_csv_value(row))

        return ','.join(rowValues)


parser = argparse.ArgumentParser(description='Conduct a ping test and save a log.')

parser.add_argument('--host', help='Host to ping.', required=True)
parser.add_argument('--ping_delay', help='Delay between pings in ms', default=1000.0)
parser.add_argument('--ping_amount', help='Amount of pings to do.', default=10)  # 86400 seconds or is 1 hour
parser.add_argument('--csv_name', help='Name of CSV file.', default='defaultCsvName')
parser.add_argument('--output_folder', help='Path of output folder.', default='pingstatsoutput.out')
parser.add_argument('--comment', help='Comment for .info.txt file.', default=socket.gethostname())

args = parser.parse_args()

OUTPUT_FOLDER = args.output_folder
CSV_NAME = args.csv_name
HOST = args.host
PING_AMOUNT = args.ping_amount
PING_DELAY = args.ping_delay

if __name__ == '__main__':

    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    START_TIME = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    csv_filename = 'pingstats-' + CSV_NAME + START_TIME + '.csv'
    info_filename = 'pingstats-' + CSV_NAME + START_TIME + '.info.txt'

    with open(os.path.join(OUTPUT_FOLDER, info_filename), 'w') as f:
        f.write('STARTED ON ' + START_TIME + '\n')
        f.write('HOST IS ' + HOST + '\n')
        f.write(
            f'PINGING {PING_AMOUNT} TIMES, WAITING {PING_DELAY}ms BETWEEN PINGS, FOR A TOTAL OF '
            f'{PING_AMOUNT * (PING_DELAY / 1000)} SECONDS' + "\n")

    with open(os.path.join(OUTPUT_FOLDER, csv_filename), 'w') as f:

        f.write(PingEvent.get_csv_rows() + '\n')
        for i in range(0, PING_AMOUNT):
            pingEvent = PingEvent.ping_now(host=HOST)
            print(pingEvent.as_csv_row())
            f.write(pingEvent.as_csv_row() + "\n")
            time.sleep(PING_DELAY / 1000.0)
