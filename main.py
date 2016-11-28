# coding=utf-8
import urllib2
from subprocess import call
from config import *
from itertools import chain
import ipaddress
import codecs


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
        print>> flog, u"exclude (%s, %s) from %s" % (ip, name, src)
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
            for line in unicode(e).splitlines():
                log = src + u": " + line
                print >> flog, log


def main():
    table = {}
    try:
        fout = codecs.open(path, u"w", encoding=u"utf-8")
    except IOError as e:
        fout = codecs.open(u"out.txt", u"w", encoding=u"utf-8")
    flog = codecs.open(u"log.txt", u"w", encoding=u"utf-8")
    for (ip, name) in defaults:
        put_ip(table, ip, name, u"default", flog)
    for src, url, method in sources:
        try:
            resp = methods[method].open(url)
            charset = resp.headers.getparam(u'charset') or u"utf-8"
            for line in resp:
                parts = line.decode(charset).split(u'#', 2)
                if parts:
                    fields = [s for s in parts[0].split() if s]
                    if len(fields) >= 2:
                        ip = fields[0]
                        name = fields[1]
                        put_ip(table, ip, name, src, flog)
        except urllib2.URLError as e:
            for line in unicode(e).splitlines():
                log = src + u": " + line
                print >> fout, u"#", log
                print >> flog, log
    fsw = codecs.open(u"switch.txt", u"w", encoding=u"utf-8")
    print>> fsw, u"[SwitchyOmega Conditions]"
    for (name, version), (ip, src) in sorted(table.iteritems(), key=get_key):
        if version == 4:
            print>> fsw, name
        if version == 4 or allow_6_only or (name, 4) in table:
            print>> fout, ip, name, u"#", src + u",", u"IPv" + str(version)
        else:
            print>> flog, u"(%s, %s) from %s is IPv6 only." % (ip, name, src)
    fsw.close()
    fout.close()
    call(cmd)
    print>> flog, u"OK!"


if __name__ == "__main__":
    main()
