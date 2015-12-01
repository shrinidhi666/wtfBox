import MySQLdb
import MySQLdb.cursors
import sys
import os
import time
import json



dbHostname = "localhost"
dbPort = "3306"
dbDatabase = "ouiDevices"

try:
  dbHostname = os.environ['ouiDevices_dbHostname']
except:
  pass
try:
  dbPort = os.environ['ouiDevices_dbPort']
except:
  pass
try:
  dbDatabase = os.environ['ouiDevices_dbDatabase']
except:
  pass

if(sys.platform.find("win") >= 0):
  try:
    username = os.environ['USERNAME']
  except:
    username = "nobody"
if(sys.platform.find("linux") >= 0):
  try:
    username = os.environ['USER']
  except:
    username = "nobody"

class db:
  """database querying class for rbhus"""
  def __init__(self):
    f = open("/etc/oui/mysql.json","r")
    a = json.loads(f.read())
    f.close()
    self.password = str(a['password'])

    self.__conn = self._connect()

  def __del__(self):
    try:
      self.__conn.close()
    except:
      print(str(sys.exc_info()))
    #print("Db connection closed" +"\n")
  
  def _connDb(self,hostname,port,dbname):
    try:
      conn = MySQLdb.connect(host = hostname,port=port,db = dbname,passwd=self.password)
      conn.autocommit(1)
    except:
      raise
    return(conn)
    
  def _connect(self):
    while(1):
      try:
        con = self._connDb(hostname=dbHostname,port=int(dbPort),dbname=dbDatabase)
        #print("Db connected")
        return(con)
      except:
        print("Db not connected : "+ str(sys.exc_info()))
      time.sleep(1)
      
       
  def execute(self,query,dictionary=False):
    while(1):
      try:
        if(dictionary):
          cur = self.__conn.cursor(MySQLdb.cursors.DictCursor)
        else:
          cur = self.__conn.cursor()
        cur.execute(query)
        #print(query)
        if(dictionary):
          try:
            rows = cur.fetchall()
          except:
            print("fetching failed : "+ str(sys.exc_info()))
          
          cur.close()
          if(rows):
            return(rows)
          else:
            return(0)
        else:
          cur.close()
          return(1)
      except:
        print("Failed query : "+ str(query) +" : "+ str(sys.exc_info()))
        if(str(sys.exc_info()).find("OperationalError(2003") >= 0):
          time.sleep(1)
          try:
            cur.close()
          except:
            pass
          try:
            self.__conn.close()
          except:
            pass
          self.__conn = self._connect()
          continue
        else:
          try:
            cur.close()
          except:
            pass
          raise