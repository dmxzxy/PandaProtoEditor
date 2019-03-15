from stat import ST_MTIME

import os
import pickle


class summary_info:
    def __init__(self):
        self.path = ""
        self.time = 0

    def __repr__(self):
        return "[time = %d,path = %s]\n" % (self.time, self.path)


def write_file_summary(summary, summary_path):
    f = file(summary_path, 'w')
    pickle.dump(summary, f)
    f.close()


def read_file_summary(summary_path):
    file_summary = {}
    if not os.path.exists(summary_path):
        print "File[" + summary_path + "] not exits."
    else:
        f = file(summary_path, 'r')
        file_summary = pickle.load(f)
        f.close()
    return file_summary


def generate_file_sumary(folder_path, suffixs):
    file_sumary = {}
    onlyfiles = [
        f for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f))
    ]
    for f in onlyfiles:
        file_path = os.path.join(folder_path, f)
        file_name = os.path.basename(f)
        file_name, file_suffix = os.path.splitext(file_name)
        for suffix in suffixs:
            if file_suffix == suffix:
                info = summary_info()
                info.time = os.stat(file_path)[ST_MTIME]
                info.path = file_path
                file_sumary[file_name] = info

    return file_sumary


def compare_file_summary(cur_summary, last_summary):
    summary_diff = {}
    updated = {}
    unused = {}

    for k, v in cur_summary.iteritems():
        if k not in last_summary:
            updated[k] = v
        else:
            if last_summary[k].time != v.time:
                updated[k] = v
    summary_diff["updated"] = updated

    for k, v in last_summary.iteritems():
        if k not in cur_summary:
            unused[k] = v
    summary_diff["unused"] = unused

    return summary_diff
