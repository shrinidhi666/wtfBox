#!/usr/bin/python
import os
import sys
import argparse



dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("syncserver").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)
# print("lib : "+ libDir)

import dbOuiDevices
import dbOuiSync

dbconnDevices = dbOuiDevices.db()
dbconnSync = dbOuiSync.db()
rawBoxes = dbconnDevices.execute("select * from theBox",dictionary=True)
rawTasks = dbconnSync.execute("select * from tasks",dictionary=True)
rawTaskJobs = dbconnSync.execute("select * from taskJobs",dictionary=True)





rsync = "rsync -v --relative --recursive --append --inplace --checksum --copy-links --xattrs --perms --progress --delete-after --rsh=/usr/bin/ssh" + " testinglinks blue0002:/tmp/"

