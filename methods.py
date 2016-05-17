# coding=utf-8
import urllib2

methods = {
    None: urllib2.build_opener(),
    u"XX-Net": urllib2.build_opener(urllib2.ProxyHandler({'http': 'localhost:8087', 'https': 'localhost:8087'})),
}
