# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.builtins import *

import re

path = r"C:\Windows\System32\drivers\etc\hosts"
cmd = ["ipconfig", "/flushdns"]

proxies = {
    # 'http': 'http://localhost:8087',
    # 'https': 'http://localhost:8087'
}

defaults = [
    ("127.0.0.1", "localhost"),
    ("::1", "localhost"),
]

sources = [
    ("lennylxx", "https://raw.githubusercontent.com/lennylxx/ipv6-hosts/master/hosts"),
    # ("laod", "file:///F:/software/Windows系列跟苹果系列/hosts"),
    ("racaljk", "https://raw.githubusercontent.com/racaljk/hosts/master/hosts"),
    ("txthinking", "https://raw.githubusercontent.com/txthinking/google-hosts/master/hosts"),
    # ("yadgen", "http://blog.yadgen.com/wp-content/uploads/2013/01/hosts_71.txt"),
]

excludes = [
    re.compile(r"(?<!gist\.)github\.com$"),
    re.compile(r"\*"),
    re.compile(r"amazon(?:aws)?\.com$"),
    re.compile(r"googleusercontent\.com$"),
    re.compile(r"^fonts\.googleapis\.com$"),
    re.compile(r"^fonts\.gstatic\.com$"),
    re.compile(r"^www\.tensorflow\.org$")
]

allow = {
    4: True,
    6: True,
}

allow_6_only = True
