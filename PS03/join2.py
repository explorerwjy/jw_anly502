#!/usr/bin/env python2

# To get started with the join, 
# try creating a new directory in HDFS that has both the fwiki data AND the maxmind data.

import mrjob
from mrjob.job import MRJob
from mrjob.step import MRStep
from weblog import Weblog       # imports class defined in weblog.py
import os
import re
import sys

class FwikiMaxmindJoin(MRJob):
    def mapper(self, _, line):
        # Is this a weblog file, or a MaxMind GeoLite2 file?
        filename = mrjob.compat.jobconf_from_env("map.input.file")
        if "top1000ips_to_country.txt" in filename:
			self.increment_counter("Status","top1000_ips_to_country file found",1) 
			try:
				(ipaddr, country) =  line.strip().split("\t")
				yield ipaddr, "+"+country
			except ValueError as e:
				pass
        else:
			try:
				o = Weblog(line)
			except ValueError:
				sys.stderr.write("Invalid Logfile line :{}\n".format(line))
				return
			if o.wikipage() == "Main_Page":
				yield o.ipaddr, line

    def reducer(self, key, values):
		country = None
		for v in values:
			if v[0:1] == '+':
				country = v[1:]
				continue
			if not country:
				self.increment_counter("Warning","No Country Found", 1)
				continue
			o = Weblog(v)
			yield "Geolocated",[o.date,country,v]

    def mapper2(self,key,value):
		country = value[1]
		yield country,1
    def reducer2(self,key,values):
		yield key,sum(values)
    def steps(self):
		return [
				MRStep(mapper=self.mapper,reducer=self.reducer),

				MRStep(mapper=self.mapper2,reducer=self.reducer2)
				]
if __name__=="__main__":
	FwikiMaxmindJoin.run()
