import tldextract
import subprocess
import os
import sys
import json
import time


host = os.environ.get('CERTBOT_DOMAIN')
CERTBOT_VALIDATION = os.environ.get('CERTBOT_VALIDATION')
CLEAN_MODE = 'clean' in sys.argv
WAIT_FOR = 10

_ext = tldextract.extract(host)
subdomain, registered_domain = _ext.subdomain, _ext.registered_domain
RRKeyWord = '_acme-challenge'
if subdomain != '':
    RRKeyWord = RRKeyWord + '.' + subdomain
print(f'registered_domain: {registered_domain}, subdomain: {subdomain}, RRKeyWord: {RRKeyWord}')


def clean(ValueKeyWord=None):
    cmd = [
        'aliyun',

        'alidns',
        'DescribeDomainRecords',

        '--DomainName',
        registered_domain,

        '--RRKeyWord',
        RRKeyWord,

        '--Type',
        "TXT",
    ]
    if ValueKeyWord:
        cmd.extend([
            "--ValueKeyWord",
            ValueKeyWord
        ])
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    for i in json.loads(result.stdout)['DomainRecords']['Record']:
        result = i['RecordId']
        print(f'Got record existing: {result}')
        subprocess.run([
            'aliyun',

            'alidns',
            'DeleteDomainRecord',

            '--RecordId',
            result
        ], shell=True, capture_output=True, text=True)
        print(f'Delete record: {result}')


if CLEAN_MODE:
    print('Running in CLEAN_MODE')
    clean(CERTBOT_VALIDATION)
else:
    clean()
    result = subprocess.run([
        'aliyun',

        'alidns',
        'AddDomainRecord',

        '--DomainName',
        registered_domain,

        '--RR',
        RRKeyWord,

        '--Type',
        "TXT",

        "--Value",
        CERTBOT_VALIDATION
    ], shell=True, capture_output=True, text=True)
    print(f'Created record, waiting for 10 seconds')
    time.sleep(10)
