# -*- encoding: utf-8 -*-
import os

from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, DateTime, Boolean

from datetime import datetime

DB_PATH = 'sqlite:///auth.db'

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


class DB:
    def __init__(self, reinit=False):
        self.engine = create_engine(DB_PATH, echo=False)

        if not os.path.exists(DB_PATH) or reinit:
            if os.path.exists('./auth.db'):
                os.remove('./auth.db')
            meta.create_all(self.engine)
        print('db already created!')
