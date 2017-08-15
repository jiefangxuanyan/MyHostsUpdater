# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import contextlib
import os
from subprocess import call

import cachecontrol
import cachecontrol.caches
import ipaddress
import requests
from requests_file import FileAdapter

from config import *


def get_key(tup):
    (name, version), (_, _) = tup
    res = name.split(".")
    res.reverse()
    return res, version


def put_ip(table, ip, name, src, flog):
    exclude = False
    for pat in excludes:
        if pat.search(name):
            exclude = True
            break
    if exclude:
        print("exclude (%s, %s) from %s" % (ip, name, src), file=flog)
    else:
        try:
            address = ipaddress.ip_address(ip)
            if isinstance(address, ipaddress.IPv4Address) and allow[4]:
                table.setdefault((name, 4), (ip, src))
            elif isinstance(address, ipaddress.IPv6Address) and allow[6]:
                table.setdefault((name, 6), (ip, src))
            else:
                raise ValueError
        except ValueError as e:
            for line in str(e).splitlines():
                log = src + ": " + line
                print(log, file=flog)


def nt_pem(func):
    import wincertstore
    def wrapped():
        with wincertstore.CertFile() as cert_file:
            cert_file.addstore("CA")
            cert_file.addstore("ROOT")
            return func(cert_file.name)

    return wrapped


def default_pem(func):
    from requests import certs
    def wrapped():
        return func(certs.where())

    return wrapped


def posix_pem(func):
    def wrapped():
        return func("/etc/ssl/certs")

    return wrapped


pem_getter = {
    "nt": nt_pem,
    "posix": posix_pem
}.get(os.name, default_pem)


@pem_getter
def main(pem):
    table = {}
    try:
        fout = open(path, "w", encoding="utf-8")
    except IOError as e:
        fout = open("out.txt", "w", encoding="utf-8")
    flog = open("log.txt", "w", encoding="utf-8")
    for (ip, name) in defaults:
        put_ip(table, ip, name, "default", flog)
    sess = requests.Session()
    sess.verify = pem
    sess.proxies = proxies
    cache = cachecontrol.CacheControlAdapter(cachecontrol.caches.FileCache(".cache"))
    sess.mount('http://', cache)
    sess.mount('https://', cache)
    sess.mount('file://', FileAdapter())
    for src, url in sources:
        try:
            with contextlib.closing(sess.get(url, stream=True)) as resp:
                for line in resp.text.splitlines():
                    parts = line.split("#", 2)
                    if parts:
                        fields = [s for s in parts[0].split() if s]
                        if len(fields) >= 2:
                            ip = fields[0]
                            name = fields[1]
                            put_ip(table, ip, name, src, flog)
        except requests.RequestException as e:
            for line in str(e).splitlines():
                log = src + ": " + line
                print("#", log, file=fout)
                print(log, file=flog)
    fsw = open("switch.txt", "w", encoding="utf-8")
    print("[SwitchyOmega Conditions]", file=fsw)
    for (name, version), (ip, src) in sorted(table.items(), key=get_key):
        if version == 4:
            print(name, file=fsw)
        if version == 4 or allow_6_only or (name, 4) in table:
            print(ip, name, "#", src + ",", "IPv" + str(version), file=fout)
        else:
            print("(%s, %s) from %s is IPv6 only." % (ip, name, src), file=flog)
    fsw.close()
    fout.close()
    call(cmd)
    print("OK!", file=flog)


if __name__ == "__main__":
    main()
