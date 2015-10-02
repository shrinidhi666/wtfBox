#!/usr/bin/python
import os
import sys
import argparse



dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("toolsSync").rstrip(os.sep).rstrip("bin").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)
# print("lib : "+ libDir)

import dbOuiDevices
import dbOuiSync

rsync = "rsync -v --relative --recursive --append --inplace --checksum --copy-links --xattrs --perms --progress --delete-after --rsh=/usr/bin/ssh" + " testinglinks blue0002:/tmp/"
