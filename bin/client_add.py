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
parser.add_argument("-c","--company",dest='companyName',help='company name')
parser.add_argument("-f","--firstname",dest='firstname',help='first name')
parser.add_argument("-l","--lastname",dest='lastname',help='last name')
parser.add_argument("-t","--tin",dest='tin',help='tin number of the company')
parser.add_argument("-p","--pan",dest='pan',help='pan number of the company')
parser.add_argument("-o","--officeaddress",dest='officeaddress',help='office address')
parser.add_argument("-h","--homeaddress",dest='homeaddress',help='home address')
parser.add_argument("-m","--homephone",dest='homephone',help='home phone number')
parser.add_argument("-i","--officephone",dest='officephone',help='office phone number')


args = parser.parse_args()
