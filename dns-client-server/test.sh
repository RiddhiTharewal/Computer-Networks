#!/bin/bash

echo --------------------------------------------------------
echo www.google.com with query type text
python3 dnsclient.py -type=txt -rec=1 google.com
echo --------------------------------------------------------
echo www.google.com with query type A 
python3 dnsclient.py -type=A www.google.com
echo --------------------------------------------------------
echo www.youtube.com with query type CNAME
python3 dnsclient.py -type=CNAME www.youtube.com
echo --------------------------------------------------------
echo www.youtube.com with query type A
python3 dnsclient.py -type=A www.youtube.com
echo --------------------------------------------------------
echo www.google.com with query type AAAA 
python3 dnsclient.py -type=AAAA www.google.com
echo --------------------------------------------------------
echo google.com with query type ns
python3 dnsclient.py -type=ns google.com
echo --------------------------------------------------------
echo google.com with query type mx
python3 dnsclient.py -type=mx google.com
echo --------------------------------------------------------
echo google.com with query type SOA
python3 dnsclient.py -type=soa google.com
echo --------------------------------------------------------
echo www.shakthimaan.com with default query type 
python3 dnsclient.py -rec=1 www.shakthimaan.com

