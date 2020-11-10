from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pytz


def parse_datetime(date):
    dt = datetime.strptime(date[1:-7], '%d/%b/%Y:%H:%M:%S')
    dt_tz = int(date[-6:-3]) * 60 + int(date[-3:-1])
    return dt.replace(tzinfo=pytz.FixedOffset(dt_tz))


def parse_nginx(log_file):
    df = pd.read_csv(log_file,
                     sep=r'\s(?=(?:[^"]*"[^"]*")*[^"]*$)(?![^\[]*\])',
                     engine='python',
                     usecols=[0, 3, 4, 5, 6, 7, 8],
                     names=['ip', 'time', 'request', 'status', 'size', 'referer', 'user_agent'],
                     na_values='-',
                     header=None,
                     converters={
                         'time': parse_datetime}
                     )
    return df


def print_df(df):
    # examples
    #print(df['status'].value_counts())
    # print(df['user_agent'].value_counts())
    print(df['ip'].value_counts())
    # print(df['size'].value_counts())
    # print(df['time'].value_counts())
    #df.index = pd.to_datetime(df.pop('time'))
    print(df['time'].head())
    #print(df.describe())
    #print(df.groupby('status'))
    plt.close('all')
    #df_s = df['status'].value_counts()


    # working stuff
    #df_s.plot(kind='pie')

    #path = df['ip']
    #path.value_counts()[:5].plot(kind='bar')
    nums = df['time']



    plt.savefig('ngx.png')


df = parse_nginx('nginx.log')
print_df(df)