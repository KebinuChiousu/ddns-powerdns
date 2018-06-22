from flask import Flask
from flask import request
from flask import jsonify

import dns.update
import dns.query
import dns.resolver


import argparse
# PowerDNS CLI tool
from pdns import *

import logging
import sys

root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(module)-12s %(levelname)-8s %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

app = Flask(__name__)

def_api_key='changeme'
def_web_port="9190"

@app.route('/query/<t>/<fqdn>')
def query(t, fqdn):
    resolver = dns.resolver.Resolver(configure=False)
    resolver.nameservers = ['127.0.0.1']
    try:
        answer = dns.resolver.query(fqdn, t)
        if t == 'a':
            return '{0}\n'.format(answer.rrset[0].address)
    except dns.resolver.NXDOMAIN:
        logging.debug("NXDOMAIN: {0}".format(fqdn))
        return 'NXDOMAIN\n'

@app.route("/get_my_ip", methods=["GET"])
def get_my_ip():
     return '{0}\n'.format(request.headers.get('X-Forwarded-For', request.remote_addr))

@app.route("/update/<domain>/<host>/<ip>", methods=['POST'])
def update(domain, host, ip):

    args = set_pdns_args('{0}.'.format(domain),host,'A',ip,'add_record')
    PDNSControl(args)

    return "update with {0}\n".format(ip)

def set_pdns_args(domain, name, recordType, content, action):

    parser = argparse.ArgumentParser(description='PDNS Controls...')
    parser.add_argument('action', help='Define action to take',
                        choices=['add_record', 'add_zone', 'delete_record',
                                 'delete_zone', 'query_config', 'query_stats', 'query_zone'])
    parser.add_argument('--apikey', help='PDNS API Key', default=def_api_key)
    parser.add_argument('--apihost', help='PDNS API Host', default='127.0.0.1')
    parser.add_argument('--apiport', help='PDNS API Port', default=def_web_port)
    parser.add_argument('--content', help='DNS Record content, can be specified multiple times', action='append')
    parser.add_argument('--disabled', help='Define if Record is disabled',
                        action='store_true', default=False)
    parser.add_argument('--master', help='DNS zone master, can be specified multiple times', action='append')
    parser.add_argument('--name', help='DNS record name')
    parser.add_argument('--nameserver', help='DNS nameserver for zone, can be specified multiple times', action='append')
    parser.add_argument('--priority', help='Define priority', default=0)
    parser.add_argument('--recordType', help='DNS record type',
                        choices=['A', 'AAAA', 'CNAME', 'MX', 'NS', 'PTR', 'SOA', 'SRV', 'TXT', 'NAPTR'])
    parser.add_argument('--setPTR', help='Define if PTR record is created',
                        action='store_true', default=False)
    parser.add_argument('--ttl', help='Define TTL', default=3600)
    parser.add_argument('--zone', help='DNS zone')
    parser.add_argument('--zoneType', help='DNS Zone Type',
                        choices=['MASTER', 'NATIVE', 'SLAVE'])
    parser.add_argument('--debug', help='Enable debug', action='store_true', default=False)

    if content is None:
        args = parser.parse_args(['--debug', 
                                  '--zone={0}'.format(domain), 
                                  '--name={0}'.format(name), 
                                  '--recordType={0}'.format(recordType), 
                                  '{0}'.format(action)])
    else:
        args = parser.parse_args(['--debug', 
                                  '--zone={0}'.format(domain), 
                                  '--name={0}'.format(name), 
                                  '--recordType={0}'.format(recordType), 
                                  '--content={0}'.format(content), 
                                  '{0}'.format(action)])

    return args


if __name__ == "__main__":
    app.run()
