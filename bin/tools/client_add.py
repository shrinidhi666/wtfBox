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
parser.add_argument("-n","--name",dest='name',help='company name')
parser.add_argument("-f","--firstname",dest='firstname',help='first name')
parser.add_argument("-l","--lastname",dest='lastname',help='last name')
parser.add_argument("-t","--tin",dest='tin',help='tin number of the company')
parser.add_argument("-p","--pan",dest='pan',help='pan number of the company')
parser.add_argument("-o","--officeaddress",dest='officeaddress',help='office address')
parser.add_argument("-h","--homeaddress",dest='homeaddress',help='home address')
parser.add_argument("-m","--homephone",dest='homephone',help='home phone number')
parser.add_argument("-e","--officephone",dest='officephone',help='office phone number')
parser.add_argument("-c","--country",dest='country',help='country')
parser.add_argument("-s","--state",dest='state',help='state')
parser.add_argument("-y","--city",dest='city',help='city')
parser.add_argument("-l","--list",dest='islist',action='store_true',help='list all the cities')

args = parser.parse_args()

dbconn = dbOuiDevices.db()

if(args.islist):
  #print("listing all the id types for devices")
  raw = dbconn.execute("select * from clients",dictionary=True)
  if(not isinstance(raw,int)):
    for x in raw:
      print(x['id'] +":"+ x['name'] +":"+ x['firstName'] +":"+ x['lastName'] +":"+ x['country'] +":"+ x['state'] +":"+ x['city'] +":"+ x['officeAddress'] +":"+ x['officePhone'] +":"+ x['homeAddress'] +":"+ x['homePhone'] +":"+ x['tinNo'] +":"+ x['panNo'])
  sys.exit(0)

fields = []
values = []

if(not (args.name or (args.firstname and args.lastname))):
  print('please give a name or first and last name')
  sys.exit(1)




if(args.name):
  fields.append('name')
  values.append("'"+ args.name +"'")
if(args.firstname):
  fields.append('firstName')
  values.append("'"+ args.firstname +"'")
if(args.lastname):
  fields.append('lastName')
  values.append("'"+ args.lastname +"'")
if(args.country):
  fields.append('country')
  values.append("'"+ args.country +"'")
if(args.state):
  fields.append('state')
  values.append("'"+ args.state +"'")
if(args.city):
  fields.append('city')
  values.append("'"+ args.city +"'")
if(args.officeaddress):
  fields.append('officeAddress')
  values.append("'"+ args.officeaddress +"'")
if(args.homeaddress):
  fields.append('homeAddress')
  values.append("'"+ args.homeaddress +"'")
if(args.officephone):
  fields.append('officePhone')
  values.append("'"+ args.officephone +"'")
if(args.homephone):
  fields.append('homePhone')
  values.append("'"+ args.homephone +"'")
if(args.tin):
  fields.append('tinNo')
  values.append("'"+ args.tin +"'")
if(args.pan):
  fields.append('panNo')
  values.append("'"+ args.pan +"'")

try:
  dbconn.execute("insert into clients ("+ ",".join(fields) +") values ("+ ",".join(values) +")" )
except:
  print(str(sys.exc_info()))
  sys.exit(1)



