* A simple tool to lookup domains, and their certs and aliases

```
usage: domain_checker.py [-h] --domain DOMAIN

optional arguments:
  -h, --help       show this help message and exit
  --domain DOMAIN  Do SSL lockup for provided domain
```

* Usage 

```
$ python domain_checker.py --domain www.google.com
OrderedDict([('domain', 'www.google.com'),
             ('alternative_names', ['www.google.com']),
             ('issued_to', 'www.google.com'),
             ('issued_by', 'GTS CA 1O1'),
             ('expired', 'Aug 18 15:30:03 2020 GMT')])
```
