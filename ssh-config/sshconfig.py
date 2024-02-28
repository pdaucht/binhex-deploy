import json
import sys

with open('/var/lib/jenkins/binhex-deploy/ssh-config/nodes.json') as user_file:
  jsonfile = user_file.read()

fileName = "/var/lib/jenkins/.ssh/config"

data = json.loads(jsonfile)
   
sshconfig = open(fileName, "a")

sshconfig.write("Host * \n")
sshconfig.write("   StrictHostKeyChecking accept-new \n\n")

for cluster in data:
    for nodes in cluster:
        sshconfig.write("#--------"+nodes["nodename"]+"----------------\n")
        sshconfig.write("Host "+nodes["nodeproxy"]+"\n")
        sshconfig.write("   HostName "+nodes["nodeproxy"]+"\n\n")

        for containers in nodes["data"]:
            if "-pr."  not in containers["name"] and "10." in containers["ip"] :
                sshconfig.write("Host "+containers["name"]+"\n")
                sshconfig.write("   HostName "+containers["ip"]+"\n")
                sshconfig.write("   User root\n")
                sshconfig.write("   ProxyJump "+nodes["nodeproxy"]+"\n\n")
        
sshconfig.close()