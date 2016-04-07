#!/usr/bin/env python2

#import pytest
from pyspark import SparkContext,HiveContext

################################################################
## Code for parsing Apache weblogs
## This is an improved parser that's tolerant of bad data.
## Instead of throwing an error, it return a Row() object
## with all NULLs
from pyspark.sql import Row
import dateutil, dateutil.parser, re

APPACHE_COMBINED_LOG_REGEX = '([(\d\.)]+) [^ ]+ [^ ]+ \[(.*)\] "(.*)" (\d+) [^ ]+ ("(.*)")? ("(.*)")?'
WIKIPAGE_PATTERN = "(index.php\?title=|/wiki/)([^ &]*)"

appache_re  = re.compile(APPACHE_COMBINED_LOG_REGEX)
wikipage_re = re.compile(WIKIPAGE_PATTERN)


def parse_apache_log(logline):
    from dateutil import parser
    m = appache_re.match(logline)
    if m==None: return Row(ipaddr=None, timestamp = None, request = None, result = None,
                           user=None, referrer = None, agent = None, url = None, datetime = None,
                           date = None, time = None, wikipage = None)
                           
    timestamp = m.group(2)
    request   = m.group(3)
    agent     = m.group(7).replace('"','') if m.group(7) else ''

    request_fields = request.split(" ")
    url         = request_fields[1] if len(request_fields)>2 else ""
    datetime    = parser.parse(timestamp.replace(":", " ", 1)).isoformat()
    (date,time) = (datetime[0:10],datetime[11:])

    n = wikipage_re.search(url)
    wikipage = n.group(2) if n else ""

    return Row( ipaddr = m.group(1), timestamp = timestamp, request = request,
        result = int(m.group(4)), user = m.group(5), referrer = m.group(6),
        agent = agent, url = url, datetime = datetime, date = date,
        time = time, wikipage = wikipage)


def raw_logs(sc):
    return sc.textFile("s3://gu-anly502/ps05/forensicswiki/2012/??/*")

def logs(sc):
    """Return a RDD with the parsed logs"""
    return sc.textFile("s3://gu-anly502/ps05/forensicswiki/2012/??/*").\
        map(lambda line:parse_apache_log(line))

#
# try this from the command line:
# ipyspark --py-files=fwiki.py
# import fwiki
# char_logs = fwiki.raw_logs(sc).filter(lambda line:"CHAR" in line)
# char_df   = sqlCtx.createDataFrame(char_logs.map(fwiki.parse_apache_log))
# char_df.cache()
# char_df.registerTempTable("logs")
# sqlCtx.sql("select count(*) from logs").collect()
