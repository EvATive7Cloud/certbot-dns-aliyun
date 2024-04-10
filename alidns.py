import tldextract
import subprocess
import os
import sys
import json
import time


host = os.environ.get('CERTBOT_DOMAIN')
CERTBOT_VALIDATION = os.environ.get('CERTBOT_VALIDATION')
CLEAN_MODE = 'clean' in sys.argv

_ext = tldextract.extract(host)
subdomain, registered_domain = _ext.subdomain, _ext.registered_domain
ValueKeyWord = '_acme-challenge'
if subdomain != '':
    ValueKeyWord = ValueKeyWord + '.' + subdomain
print(f'registered_domain: {registered_domain}, subdomain: {subdomain}, ValueKeyWord: {ValueKeyWord}')

if CLEAN_MODE:
    print('Running in CLEAN_MODE')
    result = subprocess.run([
        'aliyun',

        'alidns',
        'DescribeDomainRecords',

        '--DomainName',
        registered_domain,

        '--RRKeyWord',
        ValueKeyWord,

        '--Type',
        "TXT",

        "--ValueKeyWord",
        CERTBOT_VALIDATION
    ], shell=True, capture_output=True, text=True)
    result = json.loads(result.stdout)['DomainRecords']['Record'][0]['RecordId']
    print(f'Got record existing: {result}')
    subprocess.run([
        'aliyun',

        'alidns',
        'DeleteDomainRecord',

        '--RecordId',
        result
    ], shell=True, capture_output=True, text=True)
    print(f'Delete record: {result}')
else:
    result = subprocess.run([
        'aliyun',

        'alidns',
        'AddDomainRecord',

        '--DomainName',
        registered_domain,

        '--RR',
        ValueKeyWord,

        '--Type',
        "TXT",

        "--Value",
        CERTBOT_VALIDATION
    ], shell=True, capture_output=True, text=True)
    print(f'Created record, waiting for 20 seconds')
    time.sleep(20)
