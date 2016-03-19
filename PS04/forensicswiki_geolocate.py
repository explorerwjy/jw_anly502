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
def get_var_nn(x):
    tmp = x.split('/')
    return tmp
def mask(a,nn):
    a >> 32-nn        

def compare(a,b):
    tmp = get_var_nn(b)
    var,nn=tmp[0],tmp[1]
    a = int(a)
    var = int(var)
    nn = int(nn)
    a = mask(a,nn)
    if a > var:
        return 'larger'
    if a < var:
        return 'small'
    if a == var:
        return 'match'
        
def bsearch(x,lookup):
    start = 0
    end = len(lookup)-1
    mid = (start+end)/2
    while start<end:
        flag = compare(x,lookup[mid][0])
        if flag == 'larger':
            start = mid
            end = end
        elif flag == "small":
            start = start
            end = mid
        elif flag == "match":
            return lookup[mid][1]
    return lookup[start][1]
    
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
        #check(tmp)
        print tmp
        #check(tmp)
        #send this structure to all nodes
        lookup = sc.broadcast(tmp) 
        # print lookup.value
        
	#Forenisicswiki data for 2012
	wiki = sc.textFile(wiki_path)
        wiki_data = wiki.map(lambda x:x.split()[0])
        match_each_ip = wiki_data.map(lambda x : (bsearch(x,lookup.value),1))
        match_2 = match_each_ip.reduceByKey(lambda x,y:x+y)
        counts = match_2.sortByKey(False).collect()
        check(counts)
        




