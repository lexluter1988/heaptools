import argparse
import re
import requests


entry_pattern = r"(\s)*(?P<date>(\(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov)( \d{2} \d{2}:\d{2}:\d{2}))" \
                r"(.*)(\s)*(?P<ip>(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b))"

endpoint = "https://ipvigilante.com/"


def parse(log_file):
    with open(log_file) as f:
        for line in f.readlines():
            if 'Failed password for root from' in line:
                check = re.match(entry_pattern, line)
                response = requests.get(("{}{}".format(endpoint, check.group('ip')))).json()
                date, ip, country = check.group('date'), check.group('ip'), response.get('data').get('country_name')
                print(date, ip, country)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-file", type=str, help="Path to auth log file", required=True)
    args = parser.parse_args()
    parse(args.log_file)


if __name__ == '__main__':
    main()
