import socket
import math, re,random
import time

RESOLV_CONF       = "/etc/resolv.conf"
CACHE_FILE        = "cache.txt"

types = {
	1:"A",
	2:"NS",
	5:"CNAME",
	28:"AAAA",
	6:"SOA",
	15:"MX",
	16:"TXT",
	12:"PTR",
	}

#get first nameserver from resolv.conf file
def default_nameserver():
	servers = default_nameservers()
	if servers: return servers[0]
	return None
  
#get all nameservers from resolv.conf file
def default_nameservers(resolv_conf = RESOLV_CONF):            
  	servers = []
  	try:
    		with open(resolv_conf) as f:
      			for line in f.readlines():
        			m = re.match("nameserver\s+([0-9.]+)", line)
        			if m: servers.append(m.group(1))
  	except IOError as e:
    		if e.errno != 2: raise
    		else: return None   
  	return servers
#saving cached data 
def save_cache(q):
	with open(CACHE_FILE ,'a') as f:
		f.write(q)
		
#getting cached data from cache.txt		
def getcache(q,t):
	
	with open(CACHE_FILE ,'r') as f:
		line = f.readline()
		while(line):
			l = line.split()
			if(types[t] == l[1] and str(q) == l[0]):
				return str(l[4])
			line = f.readline()
	return 0
	
#loading the time in cached data if already present
def loadcache(q,t):
	re = ""
	with open(CACHE_FILE ,'r') as f:
		line = f.readline()
		while(line):
			l = line.split()
			
			if(q == l[0] and types[t] == l[1]):
				ti = str(int(time.time()))
				li = l[0]+" "+l[1]+" "+l[2]+" "+ti+" "+l[4]+"\n"
				#f.write(li)
				re = re+li
			else:
				re = re+line
			line = f.readline()
	with open(CACHE_FILE ,'w') as f:
		f.write(re)
	return
def cleancache():
	re = ""
	with open(CACHE_FILE ,'r') as f:
		line = f.readline()
		while(line):
			l = line.split()
			#print(type(date.today()))
			
			if((int(time.time())-int(l[3]))<=int(l[2])):
				re = re+line
			line = f.readline()
	with open(CACHE_FILE ,'w') as f:
		f.write(re)

