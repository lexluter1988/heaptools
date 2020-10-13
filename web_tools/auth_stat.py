import argparse
import re
import requests
from memory_profiler import profile

entry_pattern = r"(\s)*(?P<date>(\(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov)( \d{2} \d{2}:\d{2}:\d{2}))" \
                r"(.*)(\s)*(?P<ip>(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b))"

endpoint = "https://ipvigilante.com/"


@profile
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

@profile
def parse(log_file):
    for line in log_reader(log_file):
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
            date, ip, country = check.group('date'), check.group('ip'), response.get('data').get('country_name')
            print(date, ip, country)


@profile
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-file", type=str, help="Path to auth log file", required=True)
    args = parser.parse_args()
    parse(args.log_file)


if __name__ == '__main__':
    main()
