#!/usr/bin/env python2
#
# Demonstrates how to parse URLs with Python Spark
# This version creates a Spark Row that holds weblog info.
# https://databricks.com/blog/2015/04/21/analyzing-apache-access-logs-with-databricks-cloud.html

import re              # bring in regular expression package
import dateutil, dateutil.parser
from pyspark.sql import Row

# Import pytest if we have it available
try:
    import pytest
except ImportError as e:
    pass


APPACHE_COMBINED_LOG_REGEX = '([(\d\.)]+) [^ ]+ [^ ]+ \[(.*)\] "(.*)" (\d+) [^ ]+ ("(.*)")? ("(.*)")?'
WIKIPAGE_PATTERN = "(index.php\?title=|/wiki/)([^ &]*)"

appache_re  = re.compile(APPACHE_COMBINED_LOG_REGEX)
wikipage_re = re.compile(WIKIPAGE_PATTERN)

def parse_apache_log_line(logline):
    m = appache_re.match(logline)
    if m==None:
        raise Error("Invalid logline: {}".format(logline))

    timestamp = m.group(2)
    request   = m.group(3)
    agent     = m.group(7).replace('"','') if m.group(7) else ''

    request_fields = request.split(" ")
    url         = request_fields[1] if len(request_fields)>2 else ""
    datetime    = dateutil.parser.parse(timestamp.replace(":", " ", 1)).isoformat()
    (date,time) = (datetime[0:10],datetime[11:])

    n = wikipage_re.search(url)
    wikipage = n.group(2) if n else ""

    return Row(
        ipaddr = m.group(1),
        timestamp = timestamp,
        request = request,
        result = int(m.group(4)),
        user = m.group(5),
        referrer = m.group(6),
        agent = agent,
        url = url,
        datetime = datetime,
        date = date,
        time = time,
        wikipage = wikipage)
        
# Tests
# test with pytest
demo_line1 = '172.16.0.3 - - [25/Sep/2002:14:04:19 +0200] "GET /hello.html HTTP/1.1" 401 - "" "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.1) Gecko/20020827"'
demo_line2 = '173.199.115.51 - - [01/Jan/2013:00:59:08 -0800] "GET /wiki/Special:WhatLinksHere/SQLite_Forensic_Reporter HTTP/1.1" 200 4614 "-" "Mozilla/5.0 (compatible; AhrefsBot/4.0; +http://ahrefs.com/robot/)"'
demo_line3 = '198.58.99.82 - - [01/Jan/2013:00:59:25 -0800] "GET /w/index.php?title=Special:RecentChanges&amp;feed=atom HTTP/1.1" 304 223 "-" "Superfeedr bot/2.0 http://superfeedr.com - Please get in touch if we are polling too hard."'
def test_weblog():
    p = parse_apache_log_line(demo_line1)
    assert p.ipaddr=="172.16.0.3"
    assert p.datetime==parser.parse("25-Sep-2002 14:04:19 +0200").isoformat()
    assert p.request=="GET /hello.html HTTP/1.1"
    assert p.url=="/hello.html"
    assert p.result==401
    assert p.referrer==""
    assert p.agent=="Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.1) Gecko/20020827"
    assert Weblog(demo_line1).wikipage()==None
    assert Weblog(demo_line2).wikipage()=="Special:WhatLinksHere/SQLite_Forensic_Reporter"
    assert Weblog(demo_line3).wikipage()=="Special:RecentChanges"
#        
#
# test the parser
if __name__=="__main__":
    p = parse_apache_log_line(demo_line2)
    print("url: %s  date: %s  time: %s  datetime: %s wikipage: %s" % (p.url,p.date,p.time,p.datetime,p.wikipage))
