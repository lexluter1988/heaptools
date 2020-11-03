# -*- encoding: utf-8 -*-
# !/usr/bin/env python
import argparse
import re
import requests
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Boolean
import os
from datetime import datetime


DB_PATH = 'sqlite:///auth.db'
DATE_FORMAT = '%b %d %H:%M:%S'


meta = MetaData()

visitors = Table(
    'visitors', meta,
    Column('id', Integer, primary_key=True),
    Column('country', String),
    Column('ip', String),
    Column('visit_at', DateTime, default=datetime.now()),
)

ip_location = Table(
    'ip_location', meta,
    Column('id', Integer, primary_key=True),
    Column('ip', String, unique=True),
    Column('country', String)
)


def _init_db(reinit=False):
    engine = create_engine(DB_PATH, echo=True)
    if not os.path.exists(DB_PATH) or reinit:
        if os.path.exists('./auth.db'):
            os.remove('./auth.db')
        meta.create_all(engine)
    print('db, already created!')
    return engine


engine = _init_db()
conn = engine.connect()


entry_pattern = r"(\s)*(?P<date>(\(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov)( \d{2} \d{2}:\d{2}:\d{2}))" \
                r"(.*)(\s)*(?P<ip>(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b))"

# this site already blocked
# TODO: need other options and endpoints
endpoint = "https://ipvigilante.com/"


#@profile
def log_reader(log_file):
    """
    Generator approach to read files
    :param log_file: path to log file
    :return: one line at the time
    """
    with open(log_file) as f:
        # version with yield from
        #yield from f.readlines()
        # version where we return one line at the time
        while True:
           line = f.readline()
           if not line:
               break
           yield line

#@profile
def parse(log_file):
    for line in log_reader(log_file):
        # TODO: support records like "Invalid user admin from"
        if 'Failed password for root from' in line:
            check = re.match(entry_pattern, line)

            response = {
                'data':
                    {
                        'country_name': None
                    }
            }
            try:
                response = requests.get(("{}{}".format(endpoint, check.group('ip')))).json()
            except:
                pass
            # this is spagetty code, we get results of parser and also here
            # we insert in DB, while purpose of parser is to parse
            date, ip, country = check.group('date'), check.group('ip'), response.get('data').get('country_name')
            ins = visitors.insert().values(ip=ip, country=country, visit_at=datetime.strptime(date, DATE_FORMAT))
            conn.execute(ins)


#@profile
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-file", type=str, help="Path to auth log file", required=True)
    args = parser.parse_args()
    parse(args.log_file)


if __name__ == '__main__':
    main()
