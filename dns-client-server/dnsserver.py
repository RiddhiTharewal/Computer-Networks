import sys
import socket
import random
import common
import time


ROOT_SERVERS = dict(                                       
  a = "198.41.0.4",
  b = "192.228.79.201",
  c = "192.33.4.12",
  d = "199.7.91.13",
  e = "192.203.230.10",
  f = "192.5.5.241",
  g = "192.112.36.4",
  h = "128.63.2.53",
  i = "192.36.148.17",
  j = "192.58.128.30",
  k = "193.0.14.129",
  l = "199.7.83.42",
  m = "202.12.27.33",
)    

ips = common.default_nameserver()

def random_root_server():
  return random.choice(list(ROOT_SERVERS.values()))



def dnsserver(q):
	response = ""
	url = ""
	query = "".join(["{:02X}".format(c) for c in q])
	j = 26
	while(query[j:j+2]!="00"):
		n = int(query[j:j+2],16)
		if(n<=32):
			url = url+"."
		else:
			url = url + chr(n)
		j=j+2
	u = url[:]
	response = response+u
	print(type(u),u,len(u))
	t = query[len(query)-8:len(query)-4]
	t = int(t,16)
	response = response+" "+common.types[t]
	reply = common.getcache(u,t)
	if(reply!=0):
		return reply
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	server = random_root_server()
	sock.sendto(q, (server,53))
	reply,addr = sock.recvfrom(2048)
	try:
		sock.settimeout(5)
		for i in range(2):
			reply = "".join(["{:02X}".format(c) for c in reply])
			'''if(int(reply[13:17],16) !=0):
				return reply'''
			r = reply[2*len(q):]
			if(len(r)>=32):
				while(True):
				
					r = r[4:]
					t = r[:4]
					#t = int(t,16)
					r = r[16:]
					l = r[:4]
					l = int(l,16)
					r = r[4:]
					if(l == 4 and t == "0001"):
						b = r[:8]
						print(b)
						a = int(b,16)
						
						break
					else:
						r = r[2*l:]
							
					
				ip4 = a & 0xff
				a = a >> 8
				ip3 = a & 0xff
				a = a >> 8
				ip2 = a & 0xff
				a = a >> 8
				ip1 = a & 0xff
				ip = str(ip1) + "." + str(ip2) + "." + str(ip3) + "." + str(ip4)
				print(ip)
				sock.sendto(q, (ip,53))
				reply,addr = sock.recvfrom(1024)
		reply = "".join(["{:02X}".format(c) for c in reply])
		r = int(reply[8],16)
		if (r == 0):
			answer = reply[len(q)*2+4:]
			answer = answer[4:]
			c = answer[:4]		# get the CLASS from the answer
			answer = answer[4:]
			ttl = answer[:8]	# get the TTL from the answer
			answer = answer[8:]
			l = answer[:4]		# get the RDLENGTH from the answer
			answer = answer[4:]
			response = response + " "+str(int(ttl,16))+" "+str(int(time.time()))+" "+reply+"\n"
				
		
		common.save_cache(response)
		return reply
	except:
		return 
		
	

s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
s.bind((ips,53))
print("DNS Server is Listening ...........")
while(True):
	query,addr = s.recvfrom(2048)
	try:
		res = dnsserver(query)
		res = bytes(res,'utf-8')
		s.sendto(res,addr)
	except:
		print()
s.close()


