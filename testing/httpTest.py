#!/usr/bin/python
import requests

a = requests.get("http://github.com",timeout=1)
print(a.content)
