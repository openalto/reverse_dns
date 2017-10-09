# Reverse DNS

It's a simple reverse dns server written in Python 3.

## Start

```sh
pip3 install dnslib
python3 reverse_dns.py -c record.json
```

## Edit
Please edit ```record.json```.

## Test
```sh
nslookup 1.2.3.4 -port=5053 localhost
```
