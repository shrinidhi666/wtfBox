#!/usr/bin/python
import os
import sys
import argparse



dirSelf = os.path.dirname(os.path.realpath(__file__))
libDir = dirSelf.rstrip(os.sep).rstrip("bin").rstrip(os.sep) + os.sep + "lib"
sys.path.append(libDir)
# print("lib : "+ libDir)

import dbOuiDevices

parser = argparse.ArgumentParser()
parser.add_argument("-i","--id",dest='id',help='id of the device')
parser.add_argument("-t","--idtype",dest='idtype',help='device id type.Use device_idType command to know more')
parser.add_argument("-m","--manufacturer",dest='manufacturer',help='device manufacturer.Use device_manufacturer command to know more')
parser.add_argument("-y","--type",dest='type',help='device type.Use device_type command to know more')
args = parser.parse_args()

