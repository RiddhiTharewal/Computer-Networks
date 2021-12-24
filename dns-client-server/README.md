## dns-client-server

DNS Server: supporting all types of queries and replies. Should be able to do both recursive and iterative queries. Caching to be implemented. 

Client like nslookup: as close as possible to the existing nslookup, all options, all functionality, use of the file /etc/resolv.conf 

#To run program

First run dnsserver.py

$python3 dnsserver.py 

#To Run Client

$python3 dnsclient.py [-h] [-type TYPE] [-rec 0/1] url

#To run the test 

first Run server and the run test.sh

$python3 dnssserver.py

$bash test.sh 



https://raw.githubusercontent.com/RiddhiTharewal/Computer-Networks/main/dns-client-server/output.png


