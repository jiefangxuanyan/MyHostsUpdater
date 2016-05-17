# coding=utf-8
import urllib2
from sources import sources
from methods import methods
from subprocess import call
from system import path, cmd

if __name__ == "__main__":
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
                        if name not in table:
                            table[name] = (ip, src)
        except urllib2.URLError as e:
            for line in unicode(e).splitlines():
                log = src + ":", line
                print >> fout, "#", log
                print >> flog, log
    for name, (ip, src) in table.iteritems():
        print>> fout, ip, name, "#", src
    fout.close()
    call(cmd)
