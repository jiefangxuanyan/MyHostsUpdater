# coding=utf-8
import urllib2
from subprocess import call
from config import *
from itertools import chain


def get_key(tup):
    name, (_, _) = tup
    res = name.split(".")
    res.reverse()
    return res


def get_defaults():
    for ip, name in defaults:
        yield name, (ip, u"default")


def main():
    table = {}
    try:
        fout = open(path, "w")
    except IOError as e:
        fout = open(u"out.txt", "w")
    flog = open(u"log.txt", "w")
    for src, url, method in sources:
        try:
            resp = methods[method].open(url)
            for line in resp:
                parts = line.split('#', 2)
                if parts:
                    fields = [s for s in parts[0].split() if s]
                    if len(fields) >= 2:
                        ip = fields[0]
                        name = fields[1]
                        exclude = False
                        for pat in excludes:
                            if pat.search(name):
                                exclude = True
                                break
                        if exclude:
                            print>> flog, "exclude (%s, %s) from %s" % (ip, name, src)
                        elif name not in table:
                            table[name] = (ip, src)
        except urllib2.URLError as e:
            for line in unicode(e).splitlines():
                log = src + ":", line
                print >> fout, "#", log
                print >> flog, log
    for _, name in defaults:
        table.pop(name, None)
    for name, (ip, src) in chain(get_defaults(), sorted(table.iteritems(), key=get_key)):
        print>> fout, ip, name, "#", src
    fout.close()
    call(cmd)
    print>> flog, "OK!"


if __name__ == "__main__":
    main()
