#!/usr/bin/env python3

from dnslib import RCODE, RR, CNAME, QTYPE
from dnslib.server import DNSServer, BaseResolver
from time import sleep
import json
import argparse


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", required=True, help="Input with json config")
    args = parser.parse_args()
    return args


class Resolver(BaseResolver):
    def __init__(self, config):
        self.config = config

    def resolve(self,request,handler):
        reply = request.reply()
        segements = request.q.qname.label[0:4]
        ip = ".".join(reversed([str(i, 'utf-8') for i in segements]))
        if ip in self.config.keys():
            url = self.config[ip]
            reply.add_answer(RR(request.q.qname, QTYPE.CNAME, ttl=60, rdata=CNAME(url)))
            reply.header.rcode = getattr(RCODE, "NOERROR")
        else:
            reply.header.rcode = getattr(RCODE,'NXDOMAIN')
        return reply


def main():
    args = arg_parse()

    # Read config content
    configPath = args.config
    with open(configPath, 'r') as f:
        config = json.load(f)
    if not config:
        return -1

    resolver = Resolver(config)
    servers = [
        DNSServer(resolver, port=5053, address="0.0.0.0", tcp=True),
        DNSServer(resolver, port=5053, address="0.0.0.0", tcp=False)
    ]

    for server in servers:
        server.start_thread()

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        for server in servers:
            server.stop()


if __name__ == '__main__':
    main()
