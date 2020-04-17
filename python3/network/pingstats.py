#!/usr/bin/env python3
import argparse
import datetime
import os
import socket
import time
from typing import Tuple
from time import gmtime, strftime
from ping3 import ping


def datetime_now() -> datetime.datetime:
    return datetime.datetime.now()


def datetime_to_excelDatetime(d: datetime.datetime) -> str:
    """4/15/2020 08:56:58 PM"""
    return d.strftime('%m/%d/%Y %I:%M:%S %p')


assert (datetime_to_excelDatetime(datetime.datetime(2020, 4, 16, 4 + 12, 49, 20)) == '04/16/2020 04:49:20 PM')


def datetime_to_datetimeStr(d: datetime.datetime) -> str:
    return d.strftime('%Y-%m-%d_%H-%M-%S')


assert (datetime_to_datetimeStr(datetime.datetime(2020, 4, 16, 4 + 12, 49, 20)) == '2020-04-16_16-49-20')


def datetimeStr_to_datetime(s: str) -> datetime.datetime:
    return datetime.datetime.strptime(s, '%Y-%m-%d_%H-%M-%S')


class PingEvent:

    @staticmethod
    def ping_now(host: str, sequence_number: int = 0):

        try:
            ping_time_sec = ping(args.host)
            if ping_time_sec is None:  # fix for when ping() returns None
                ping_time_ms = 0
            else:
                ping_time_ms = 1000 * ping_time_sec
        except OSError as e:
            ping_time_ms = -abs(e.errno)

        return PingEvent(host, datetime.datetime.now(), ping_time_ms, sequence_number)

    @staticmethod
    def get_rows() -> Tuple[str, str, str, str, str]:
        return 'sequence_number', 'host', 'time', 'excel_time', 'ping_time'

    @staticmethod
    def get_csv_rows() -> str:
        return ','.join(PingEvent.get_rows())

    def __init__(self, host: str, time: datetime.datetime, ms: float, sequence_number: int):
        self.host = host
        self.time = time
        self.ping_time = ms
        self.sequence_number = sequence_number

    def __str__(self):
        return (f"{self.time}\n"
                f"PING {args.host}\n"
                f"{self.ping_time * 1000:.2f}ms")

    def get_csv_value(self, column_name: str) -> str:

        if column_name not in self.get_rows():
            raise Exception(f"No column name called {column_name}!")

        property_map = {
            'sequence_number': self.sequence_number,
            'host': self.host,
            'time': self.time,
            'excel_time': self.excel_time(),
            'ping_time': self.ping_time,
        }

        return str(property_map[column_name])

    def as_csv_row(self, rows=None):

        rows = self.get_rows()

        rowValues = []
        for row in rows:
            rowValues.append(self.get_csv_value(row))

        return ','.join(rowValues)

    def excel_time(self) -> str:
        """Get excel-friendly time"""
        return datetime_to_excelDatetime(self.time)


parser = argparse.ArgumentParser(description='Conduct a ping test and save a log.')

parser.add_argument('--host', help='Host to ping.',
                    default='google.com')

# 86400 seconds is 24 hours
parser.add_argument('--ping_delay', help='Delay between pings in ms',
                    default=1000.0)

parser.add_argument('--ping_amount', help='Amount of pings to do.',
                    default=10)

parser.add_argument('--csv_name', help='Name of CSV file.',
                    default=socket.gethostname())

parser.add_argument('--output_folder', help='Path of output folder.',
                    default='pingstatsoutput.out')

parser.add_argument('--comment', help='Comment for .info.txt file.',
                    default=f"comment: started by host {socket.gethostname()}")

args = parser.parse_args()

OUTPUT_FOLDER = args.output_folder
CSV_NAME = args.csv_name
HOST = args.host
PING_AMOUNT = float(args.ping_amount)
PING_DELAY = args.ping_delay
COMMENT = args.comment

if __name__ == '__main__':

    if not os.path.exists(OUTPUT_FOLDER):
        os.mkdir(OUTPUT_FOLDER)

    START_TIME = datetime_now()
    START_TIME_STR = datetime_to_datetimeStr(START_TIME)
    csv_filename = 'pingstats-' + HOST + "-" + CSV_NAME + "-" + START_TIME_STR + '.csv'
    info_filename = 'pingstats-' + HOST + "-" + CSV_NAME + "-" + START_TIME_STR + '.info.txt'

    print("Writing INFO to " + os.path.join(OUTPUT_FOLDER, info_filename))
    with open(os.path.join(OUTPUT_FOLDER, info_filename), 'w') as f:
        f.write(f'STARTED ON {START_TIME_STR}\n')
        f.write(f'HOST IS {HOST}\n')
        f.write(f"COMMENT: {COMMENT}\n")
        f.write(
            f'PINGING {PING_AMOUNT} TIMES, WAITING {PING_DELAY}ms BETWEEN PINGS,'
            f' FOR A TOTAL OF {PING_AMOUNT * (PING_DELAY / 1000)} SECONDS\n')
        f.flush()

    with open(os.path.join(OUTPUT_FOLDER, csv_filename), 'w') as f:

        print('Writing CSV DATA to ' + os.path.join(OUTPUT_FOLDER, csv_filename))
        f.write(PingEvent.get_csv_rows() + '\n')
        print(PingEvent.get_csv_rows())
        for i in range(0, int(PING_AMOUNT)):
            pingEvent = PingEvent.ping_now(host=HOST, sequence_number=i)
            print(pingEvent.as_csv_row())
            f.write(pingEvent.as_csv_row() + "\n")
            time.sleep(PING_DELAY / 1000.0)
