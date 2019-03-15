#!/usr/bin/env python
# -*- encoding:utf8 -*-

from protocol.helpers.panpbtool.data import middata
from protocol.helpers.panpbtool.conf import prototype

def translate():
    project = middata.Project()

    # for proto_file in raw_data.proto_file:
        # comments 
        # for location in proto_file.source_code_info.location:
        #     path = [str(proto_file.name)]
        #     for pathNode in location.path:
        #         path.append(pathNode)

        #     content = (location.leading_comments+' '+location.trailing_comments).strip().replace("\n", "")
        #     project.add_comment(str(path), content)
        
        # module = project.get_module(fullname = proto_file.package)
        # if module == None:
        #     module = project.add_module(
        #         name = proto_config.get_module_name(context, proto_file),
        #         fullname = proto_file.package,
        #         namespace = namespace,
        #         location = [str(proto_file.name)]
        #     )
    return project