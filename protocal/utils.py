# -*- coding: utf-8 -*-

import os
import subprocess
import sys


def cmd_call(cmd):
    print 'Executing cmd:[%s]' % cmd
    p = subprocess.Popen(
        cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    (stdoutput, erroutput) = p.communicate()
    p.wait()
    rc = p.returncode
    if rc != 0:
        erroutput = erroutput.decode(sys.getfilesystemencoding())
        stdoutput = stdoutput.decode(sys.getfilesystemencoding())
        if erroutput == u'':
            raise Exception(stdoutput.encode('utf-8'))
        else:
            raise Exception(erroutput.encode('utf-8'))
    return (stdoutput, erroutput)


def get_file_list(find_path, suffix):
    findlist = []
    file_names = os.listdir(find_path)
    if (len(file_names) > 0):
        for fn in file_names:
            if (len(suffix) > 0):
                if fn.endswith(suffix):
                    fullfilename = os.path.join(find_path, fn)
                    findlist.append(fullfilename)
            else:
                fullfilename = os.path.join(find_path, fn)
                findlist.append(fullfilename)

    if (len(findlist) > 0):
        findlist.sort()

    return findlist
