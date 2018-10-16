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


def is_sub_string(SubStrList, Str):
    flag = True
    for substr in SubStrList:
        if not (substr in Str):
            flag = False

    return flag


def get_file_list(FindPath, FlagStr=[]):
    FileList = []
    FileNames = os.listdir(FindPath)
    if (len(FileNames) > 0):
        for fn in FileNames:
            if (len(FlagStr) > 0):
                if (is_sub_string(FlagStr, fn)):
                    fullfilename = os.path.join(FindPath, fn)
                    FileList.append(fullfilename)
            else:
                fullfilename = os.path.join(FindPath, fn)
                FileList.append(fullfilename)

    if (len(FileList) > 0):
        FileList.sort()

    return FileList
