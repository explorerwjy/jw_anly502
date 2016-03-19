#Join of MAXMIND and FORENSICSWIKI

import sys
from pyspark import SparkContext
import socket,struct
from weblog import Weblog
import bisect

def ip2long(ip):
	packedIP = socket.inet_aton(ip)
	return struct.unpack("!L",packedIP)[0]
def longtoip(long):
	return socket.inet_ntoa(struct.pack("!L",long))

def check(tmp):
    for i in tmp:
        print i
def get_ip_url(line):
    return 0
    
def bsearch(x,lookup):
    ip = x

    return 0    
def change_to_integer(x):
    #x[0] ip x[1] country
    integer,nn = x[0].split('/')
    integer = str(ip2long(integer))
    return integer+'/'+nn,x[1]

if __name__ == "__main__":
	wiki_path = 's3://gu-anly502/ps03/forensicswiki.2012-01.unzipped/access.log.2012-01-01'
	#wiki_path = 's3://gu-anly502/ps03/forensicswiki.2012.txt'
	path1 = 's3://gu-anly502/maxmind/GeoLite2-Country-Blocks-IPv4.csv'
	path2 = 's3://gu-anly502/maxmind/GeoLite2-Country-Locations-en.csv'
	sc = SparkContext(appName='IP Join')
	
	#Join The MaxMind Date
	ref1 = sc.textFile(path1).zipWithIndex().filter(lambda x:x[1] > 0).map(lambda x:x[0])#ip file
	ref2 = sc.textFile(path2).zipWithIndex().filter(lambda x:x[1] > 0).map(lambda x:x[0])#country
        pair1 = ref1.map(lambda x:(x.split(',')[1],x.split(',')[0]))#genoame_id,ip
	pair2 = ref2.map(lambda x:(x.split(',')[0],x.split(',')[-1]))#genoame_id,country_name
        pair3 = pair1.join(pair2)
	country_ip = pair3.map(lambda x:(x[1]))#ip,country_name
	#country_ip = country_ip.sortByKey(True)
        #country_ip = country_ip.map(lanbda x: "/".join(ip2long(x[0].split('/')[0]), x[0].split('/')[1]),x[1])
        country_ip = country_ip.map(lambda x:change_to_integer(x)).sortByKey(True)
        tmp = country_ip.collect()
        check(tmp)
        #check(tmp)
        #send this structure to all nodes
        lookup = sc.broadcast(tmp) 
        # print lookup.value
        
	#Forenisicswiki data for 2012
	wiki = sc.textFile(wiki_path)
        wiki_data = wiki.map(lambda x:x.split()[0])
        check(wiki_data.take(10))
        match_each_ip = wiki_data(lambda x : bsearch(x,lookup),1)
        




