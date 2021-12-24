## dns-client-server

**DNS Server**: supporting all types of queries and replies. Should be able to do both recursive and iterative queries. Caching to be implemented. 

**Client like nslookup**: as close as possible to the existing nslookup, all options, all functionality, use of the file /etc/resolv.conf 

## To run program

First go to terminal and type **$sudo gedit /etc/resolv.conf** and add nameserver with the ip address(in my case I used 127.0.0.1).

Then run dnsserver.py using command 

**$sudo python3 dnsserver.py**

**# To Run Client**

**$python3 dnsclient.py [-h] [-type TYPE] [-rec 0/1] url**

**# To run the test**

First Run server and the run test.sh

**$sudo python3 dnssserver.py**

**$bash test.sh**

**# Output**

![](https://raw.githubusercontent.com/RiddhiTharewal/Computer-Networks/main/dns-client-server/output.png)


