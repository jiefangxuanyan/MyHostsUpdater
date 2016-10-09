# coding=utf-8
import urllib2
import re

path = u"C:\\Windows\\System32\\drivers\\etc\\hosts"
cmd = ["ipconfig", "/flushdns"]

methods = {
    None: urllib2.build_opener(),
    u"XX-Net": urllib2.build_opener(urllib2.ProxyHandler({'http': 'localhost:8087', 'https': 'localhost:8087'})),
}

defaults = [
    (u"127.0.0.1", u"localhost"),
    (u"::1", u"localhost"),
]

sources = [
    (u"laod", u"file:///G:/software/Windows系列跟苹果系列/hosts", None),
    (u"racaljk", u"https://raw.githubusercontent.com/racaljk/hosts/master/hosts", None),
    (u"txthinking", u"https://raw.githubusercontent.com/txthinking/google-hosts/master/hosts", None),
    (u"yadgen", u"http://blog.yadgen.com/wp-content/uploads/2013/01/hosts_69.2.txt", None),
]

excludes = [
    re.compile(ur"github\.com$"),
]
