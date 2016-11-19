#! /usr/bin/env python2
import os
import sys
import win32com.shell.shell as shell

ASADMIN = 'asadmin'

if __name__ == '__main__':
    if sys.argv[-1] != ASADMIN:
        script = os.path.abspath(sys.argv[0])
        params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
        sys.exit(0)

    from main import main

    main()
