
import os
import time
import svnhelper
import projecthelper
from synchelper import synchelper
from exporthelper import exporthelper
from synchelper.summary_tools import *

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

def exporter(project, branch):
    branch_path = projecthelper.get_branch_path(branch.id)
    if not os.path.exists(branch_path):
        os.makedirs(branch_path)
    export_path = branch_path + '/export/'
    if not os.path.exists(export_path):
        os.makedirs(export_path)
    exporthelper.export(branch, export_path)