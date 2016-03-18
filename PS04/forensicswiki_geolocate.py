#Join of MAXMIND and FORENSICSWIKI

import sys
from pyspark import SparkCountext
import socket,struct
from weblog import Weblog

def ip2long(ip):
	packedIP = socket.inet_aton(ip)
	return struct.unpack("!L",packedIP)[0]
def longtoip(long):
	return socket.inet_ntoa(struct.pack("!L",long))

if __name__ == "__main__":
	wiki_path = 's3://gu-anly502/ps03/forensicswiki.2012-01.unzipped/access.long.2012-01-01'
	#wiki_path = 's3://gu-anly502/ps03/forensicswiki.2012.txt'
	path1 = 's3://gu-anly502/maxmind/GeoLite2-Country-Blocks-IPv4.csv'
	path2 = 's3://gu-anly502/maxmind/GeoLite2-Country-Locations-en.csv'
	sc = SparkContext(appName='IP Join')
	
	#Join The MaxMind Date
	ref1 = sc.textFile(path1).zipWithIndex().filter(lambda x:x[1] > 0)
	ref2 = sc.textFile(path2).zipWithIndex().filter(lambda x:x[1] > 0)
	"""
	head1,head2 = ref1.first(),ref2.first()
	ref1 = ref1.filter(lambda x:x !=head1)
	ref2 = ref2.filter(lambda x:x !=head2)
	"""
	pair1 = ref1.map(lambda x:(x.split(',')[0],x.split(',')[-1]))#genoame_id,country_name
	pair2 = ref2.map(lambda x:(x.split(',')[1],x.split(',')[0].split('/')[0]))#genoame_id,ip
	pair3 = pair.join(pair2)
	country_ip = pair3.map(lambda x:(ip2long(x[1][1]),x[1][0]))#ip,country_name
	#send this structure to all nodes



	#Forenisicswiki data for 2012
	wiki = sc.textFile(wiki_path)
	wiki_data = wiki.map(lambda x:Weblog(x))
	wiki_pair = wiki_data.map(lambda x:x.ipaddr,x.)





