# -*- coding: utf-8 -*-

import os
import time
import svnhelper
import projecthelper
import zipfile

from synchelper import synchelper
from exporthelper import exporthelper
from synchelper.summary_tools import *
from protocol.helpers.panpbtool.utils import utils

def __getDir(branch):
    branch_path = projecthelper.get_branch_path(branch.id)
    if not os.path.exists(branch_path):
        os.makedirs(branch_path)
    proto_sync_path = branch_path + '/proto/'
    return proto_sync_path

def __getURL(project, branch):
    url = project.urlbase
    if not url.endswith('/'):
        url += '/'
    url += branch.proto_url
    return url

#------------------------------------------------------------------------

def testSync(project, branch):
    sync_dir = __getDir(branch)
    sync_url = __getURL(project, branch)
    svnhelper.doupdate(sync_url, sync_dir)

    file_summary = generate_file_summary(sync_dir, ['proto', 'go'])
    summary_path = sync_dir + "/summary.txt"
    last_file_summary = read_file_summary(summary_path)
    summary_diff = compare_file_summary(file_summary,last_file_summary)
    
    if summary_diff["updated"]:
        return True

    return False

def syncer(project, branch, force):
    start = time.time()
    if testSync(project, branch) or force:
        sync_dir = __getDir(branch)
        try:
            synchelper.sync(project, branch, sync_dir)

            file_summary = generate_file_summary(sync_dir, ['proto', 'go'])
            summary_path = sync_dir + "/summary.txt"
            write_file_summary(file_summary, summary_path)
        except Exception, e:
            raise e
    
    end = time.time()
    print "sync cost time", end-start

def exporter(project, branch, version):
    branch_path = projecthelper.get_branch_path(branch.id)
    if not os.path.exists(branch_path):
        os.makedirs(branch_path)
    export_path = branch_path + '/export/'
    if not os.path.exists(export_path):
        os.makedirs(export_path)
    exporthelper.export(branch, export_path)
    
    file_version = open(export_path + '/lua/'+ 'protocol_version.txt','w')    
    file_version.write(version)
    file_version.close()

def zipExporter(project, branch):
    the_zip_file = "config_lua.zip"
    branch_path = projecthelper.get_branch_path(branch.id)
    the_export_path = branch_path + '/export/'

    zip_archive_path = the_export_path + '/archive/'
    if not os.path.exists(zip_archive_path):
        os.mkdir(zip_archive_path) 
    
    file_zip = zipfile.ZipFile(zip_archive_path+the_zip_file,'w',zipfile.ZIP_DEFLATED) 

    the_lua_path = str(the_export_path + '/lua/')
    filenames = utils.get_file_list(the_lua_path, ['lua'])
    for filename in filenames: 
        tozipfile = os.path.relpath(filename, the_lua_path)  
        file_zip.write(filename, tozipfile) 
     
    file_zip.write(the_lua_path + 'protocol_version.txt', 'protocol_version.txt') 
    file_zip.close()

    return zip_archive_path+the_zip_file