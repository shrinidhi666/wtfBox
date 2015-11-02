import subprocess

p = subprocess.Popen(['dig','+short','myip.opendns.com','@resolver1.opendns.com'],stdout=subprocess.PIPE)
t = p.communicate()
p.wait()
print(t)