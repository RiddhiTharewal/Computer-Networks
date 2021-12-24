import sys
import struct
import socket
import string 
import common
import time
import argparse

#get proper url
def file(URL):
	global webpage
	response = ""
	file_name = ""
	SubURL = ""
	i = 0
	
	for n in URL.split('/'):
		i = i + 1
		if(i == 1):
			SubURL = SubURL + n
		if(i == len(URL.split('/'))):
			file_name = file_name + n

	webpage = SubURL
	
	
#construct query
def DNSquery(t,host, Class,rec):
	global response
	response = ""
	response = response+webpage+" "+common.types[t]+" "

	if(rec == "1"):
		B = "\x01\x00"
	else:
		B = "\x00\x00"
	
	q = bytes("\x12\x12"+B+"\x00\x01"+"\x00\x00"+"\x00\x00"+"\x00\x00", 'utf-8')
	question = bytes("", 'utf-8')
	for w in webpage.split('.'):
		question += struct.pack("!b" + str(len(w)) + "s", len(w), bytes(w, "utf-8"))
	
	q = q + question
	packet=q+struct.pack("!bHH",0,t,Class)
	return packet
#sending query to server and getting reply
def dnsresponse(q):
	server = None
	port = 53
	if server is None:
		server = common.default_nameserver()
	if server is None: raise Error("no server") 
	if server.split(".")[-1].isdigit():
		host = addr = server
	else:
		info = S.gethostbyname_ex(server)
		host, addr = webpage, server
	print("{:15} {}".format("Server:", server))
	print("{:15} {}#{}".format("Address:", addr, port))
	print()
	try:
		
		
		try:
			
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.settimeout(20)
			sock.sendto(q, (server,53))		
			reply, addr = sock.recvfrom(2048)
			reply = reply.decode('utf-8')
			sock.close()
			
		
		except:
			sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			sock.settimeout(10)
			sock.sendto(q, ('8.8.8.8',53))	
			
			reply, addr = sock.recvfrom(2048)
			reply = "".join(["{:02X}".format(c) for c in reply])
			sock.close()
				
	except Exception as e:
		print ("No response from server", server)
		print ("--------------------Timeout Occured----------------------------------")
		print ("")
		#sock.close()
		sys.exit()
		
	#reply = "".join(["{:02X}".format(c) for c in reply])
	res = handleresponse(q, reply)
	return res
	
#resolving the obtained response from server
def handleresponse(q, reply):
	ttl = "0E10"
	prev = webpage
	nameserver = name = prev
	k =bin(int(reply[7]))
	if  k[-1]=='0':
		print("Non-authoritative answer:")
		

	r = int(reply[8],16)
	if (r == 0):	
		ancount = reply[:16]
		ancount = ancount[12:]
		count = int(ancount,16)
		responses = ""
		# get the answer from the server reply
		answer = reply[2*len(q):]
		name = webpage
		cname = webpage
		for i in range(0, count):
			n = answer[:4]		#get the Name from answer
			answer = answer[4:]
			t = answer[:4]		# get the TYPE from the answer
			answer = answer[4:]
			c = answer[:4]		# get the CLASS from the answer
			answer = answer[4:]
			ttl = answer[:8]	# get the TTL from the answer
			answer = answer[8:]
			l = answer[:4]		# get the RDLENGTH from the answer
			answer = answer[4:]
			
			rdata = answer[:int(l, 16)*2]	# get the RDATA from the answer
			TYPE = common.types[int(t,16)]
			
			
			if (t == "0001"): # get the IP from the RDATA if the TYPE is A			
				a = int(rdata, 16)		
				ip4 = a & 0xff
				a = a >> 8
				ip3 = a & 0xff
				a = a >> 8
				ip2 = a & 0xff
				a = a >> 8
				ip1 = a & 0xff
				print("Name: ",name)
				ip = str(ip1) + "." + str(ip2) + "." + str(ip3) + "." + str(ip4)
				print ("Address: " , ip)
				print ("")
				answer = answer[int(l, 16)*2:]
			
			elif(t == "0005"):# get the CNAME from the RDATA if the TYPE is CNAME
				cname = ""	
				rdata = rdata[2:]
				for i in range(int(l, 16)-3):					
					n = rdata[:2]
					n = int(n, 16)	
					rdata = rdata[2:]									
					if n <= 32:
						cname = cname + "."      							
					cname = cname + chr(n)	
					name = cname				
				print (prev , "\t canonical name ", name)
				
				answer = answer[int(l, 16)*2:]
				
			elif(t == "001C"):		# get the ipv6 from the RDATA if the TYPE is AAAA
				ans = answer[:32]
				ip = ""
				for j in range(0,16,1):
					ip = ip + ans[j] 
					if((j+1)%4 == 0):
						ip = ip + ":"
				print("Name: ",name)	
				print("Address : ",ip[:-1])
				answer = answer[int(l, 16)*2:]
				
			elif(t=="0002"):		# get the nameserver
				cn = ""
				ns = answer[:2]
				while(answer[:2]!="C0"):				
					n = answer[:2]
					n = int(n,16)
					answer = answer[2:]									
					if n <= 32:
						cn = cn + "."
				
					cn = cn + chr(n)
				if(i==0):
					if(len(cn)>int(ns,16)):
						nameserver = cn[:]+".com"
					else:
						nameserver = cn[:]+"."+prev
					#cn = nameserver
					
				#else:
				if(nameserver[int(l,16)-1:]!=".com"):
					cn = cn+nameserver[int(l,16)-1:]	
				else:
					cn = cn+"."+prev
				answer = answer[4:]		
				print (name,"\tnameserver = ", cn[1:])
				
			elif(t=="000F"):	#get mail exchanger data
				p = answer[:4]
				p = int(p,16)
				answer = answer[4:]
				cn = ""
				for j in range(int(l,16)-2):
					n = answer[:2]
					n = int(n,16)
					answer = answer[2:]
					if n<=32:
						cn = cn+"."
					cn = cn+chr(n)
				if(i==0):
					nameserver = cn[:-1]
					nameserver = nameserver[:-2]+"."+prev
					cn = nameserver
				else:
					cn = cn[:-2]+"."+nameserver[int(l,16)-1:]
				
				print(name,"\tmail exchanger = ",p,cn[1:])

			
			elif(t =="0006"):#SOA
				cn = "origin = "
				n = answer[:2]
				answer = answer[2:]
				while(answer[:2]!="C0"):
					ns = answer[:2]
					ns = int(ns,16)
					answer = answer[2:]
					if(ns<=32):
						cn = cn+"."
					cn = cn+chr(ns)
				cn = cn + "." + prev + "\n\tmail addr = "
				answer = answer[4:]
				n = answer[:2]
				answer = answer[2:]

				while(answer[:2]!="C0"):
					ns = answer[:2]
					ns = int(ns,16)
					answer = answer[2:]
					if(ns<=32):
						cn = cn+"."
					cn = cn+chr(ns)
				cn = cn + "." + prev + "\n\tserial = "
				answer = answer[4:]
				c = answer[:8]
				c = int(c,16)
				answer=answer[8:]
				cn = cn + str(c) + "\n\trefresh = "
				c = answer[:8]
				c = int(c,16)
				answer=answer[8:]
				cn = cn +str(c)+ "\n\tretry = "
				c = answer[:8]
				c = int(c,16)
				answer=answer[8:]
				cn = cn+str(c) + "\n\texpire = "
				c = answer[:8]
				c = int(c,16)
				answer=answer[8:]
				cn = cn+str(c) + "\n\tminimum = "
				c = answer[:8]
				c = int(c,16)
				cn = cn+str(c)
				print(name,"\t",cn)	
					
			elif(t =="000C" or t=="0010"):#PTR and txt
				cn = ""
				for i in range(int(l,16)):				
					n = answer[:2]
					n = int(n,16)
					answer = answer[2:]									
					if n <= 32:
						cn = cn + "."
					cn = cn + chr(n)
										
				print (name,"\t",TYPE," = ", '"',cn,'"')
			
			else:
				print("Not implemented")
				answer = answer[int(l, 16)*2:]
				
					
	elif (r == 1):
		# error
		print ("Format error: the name server was unable to interpret the query.")	
	elif (r == 2):
		print ("Server failure: the name server was unable to process this query due to a problem with the name server.")
	elif (r == 3):
		print ("None exist domains: server can not find answer.")
	elif (r == 4):
		print ("Not Implemented: the name server does not support the requested kind of query.")
	elif (r == 5):
		print ("Server Refused.")
	else:
		print ("Other errors")
	
	print ("----------------------------------------------------------------------")
	res = response+str(int(ttl,16))+" "+str(int(time.time()))+" "+reply+"\n"
	
	
	return res
	
	
def typequery(query_type):
    code = 0
    if query_type == "A":
        code = 1
    elif query_type == "NS":
        code = 2
    elif query_type == "CNAME":
        code = 5
    elif query_type == "SOA":
        code = 6
    elif query_type == "MX":
        code = 15
    elif query_type == "TXT":
        code = 16
    elif query_type == "PTR":
        code = 12
    elif query_type == "AAAA":
        code = 28
    else:
        exit(1)
    return code
	    
def main():
	a = argparse.ArgumentParser()
	a.add_argument("-type",default="A")
	a.add_argument("-rec",default="1")
	a.add_argument("url")
	args = a.parse_args()
	URL = args.url
	file(URL)
	t = typequery(args.type.upper())
	r = args.rec
	query = DNSquery(t,webpage,1,r)
	
	r = dnsresponse(query)
	q = "".join(["{:02X}".format(c) for c in query])
	if(not common.getcache(webpage,t)):
		common.save_cache(r)
	else:
		common.loadcache(webpage,t)
	#common.cleancache()
	
if __name__ == "__main__":
	main()

