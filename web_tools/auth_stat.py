# -*- encoding: utf-8 -*-

import argparse
from datetime import datetime

from db import DB, visitors, ip_location
from parsers import AuthParser

DATE_FORMAT = '%b %d %H:%M:%S'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-file", type=str, help="Path to auth log file", required=True)
    args = parser.parse_args()

    logs_parser = AuthParser()
    parsed_logs = logs_parser.parse(args.log_file)

    db = DB()
    engine = db.engine

    conn = engine.connect()
    for date, ip, country in parsed_logs:
        ins = visitors.insert().values(ip=ip, country=country, visit_at=datetime.strptime(date, DATE_FORMAT))
        conn.execute(ins)


if __name__ == '__main__':
    main()
