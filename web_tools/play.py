from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pytz


# TODO: always write timeframe, from to, period
# TODO: plt close decorator
# TODO: basic nginx doesn't have execution time logged
# TODO: savefig as decorator with file name as parameter of decorator
# TODO: html hable as decorator, maybe, with file name as parameter of decorator
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


def pie_chart_of_codes(df):
    plt.close('all')
    df['status'].value_counts().plot(kind='pie', figsize=(11, 6), autopct='%1.0f%%')
    plt.savefig('codes.png')


def total_requests_by_time(df):
    plt.close('all')
    df.groupby('time').size().plot(kind='line', stacked=True, xlabel='time', ylabel='requests', figsize=(11, 6))
    plt.savefig('requests_total.png')


def total_requests_by_ip(df):
    urls = df.ip.value_counts().to_frame().to_html()
    with open('ips.html', 'w') as f:
        f.write(urls)


def urls_to_html_tables(df):
    urls = df.request.value_counts().to_frame().to_html()
    with open('urls.html', 'w') as f:
        f.write(urls)


def error_requests_by_time(df):
    pass


def good_requests_by_time(df):
    pass


def build_report():
    """
    main funciton, creates html page sceleton, calls pandas to get stats
    and build html page with images, tables and report by needed time
    :return:
    """
    pass



df = parse_nginx('nginx.log')
#pie_chart_of_codes(df)


# good parts

#df = df.set_index('time').sort_index()
#df.groupby('time').size()