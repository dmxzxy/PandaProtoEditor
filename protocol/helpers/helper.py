
import os
import svnhelper
import projecthelper
from synchelper import synchelper
from exporthelper import exporthelper

def syncer(project, branch):
    branch_path = projecthelper.get_branch_path(branch.id)
    if not os.path.exists(branch_path):
        os.makedirs(branch_path)

    proto_sync_path = branch_path + '/proto/'

    url = project.urlbase
    if not url.endswith('/'):
        url += '/'
    url += branch.proto_url

    svnhelper.doupdate(url, proto_sync_path)

    synchelper.sync(project, branch, proto_sync_path)