import re
from abc import ABC, abstractmethod

import requests


class AbstractLogsParser(ABC):
    @abstractmethod
    def log_reader(self, log_file):
        pass

    @abstractmethod
    def parse(self, log_file):
        pass


class AuthParser(AbstractLogsParser):
    entry_pattern = r"(\s)*(?P<date>(\(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov)( \d{2} \d{2}:\d{2}:\d{2}))" \
                    r"(.*)(\s)*(?P<ip>(\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b))"
    endpoint = "https://ipvigilante.com/"

    def log_reader(self, log_file):
        """
        Generator approach to read files
        :param log_file: path to log file
        :return: one line at the time
        """
        with open(log_file) as f:
            # version with yield from
            # yield from f.readlines()
            # version where we return one line at the time
            while True:
                line = f.readline()
                if not line:
                    break
                yield line

    def parse(self, log_file):
        result = []

        for line in self.log_reader(log_file):
            # TODO: support records like "Invalid user admin from"
            if 'Failed password for root from' in line:
                check = re.match(self.entry_pattern, line)

                response = {
                    'data':
                        {
                            'country_name': None
                        }
                }
                try:
                    response = requests.get(("{}{}".format(self.endpoint, check.group('ip')))).json()
                except:
                    pass
                date, ip, country = check.group('date'), check.group('ip'), response.get('data').get('country_name')
                result.append((date, ip, country))
        return result


class NginxParser(AbstractLogsParser):
    def log_reader(self, log_file):
        with open(log_file) as f:
            # version with yield from
            # yield from f.readlines()
            # version where we return one line at the time
            while True:
                line = f.readline()
                if not line:
                    break
                yield line

    def parse(self, log_file):
        result = []
        # TODO: code
        return result
