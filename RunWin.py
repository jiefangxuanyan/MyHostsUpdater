# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals
from future.builtins import *

import os
import sys
from win32com.shell import shell

ASADMIN = "asadmin"

if __name__ == "__main__":
    if sys.argv[-1] != ASADMIN:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
        shell.ShellExecuteEx(lpVerb="runas", lpFile=sys.executable, lpParameters=params)
        sys.exit(0)

    from main import main

    main()
