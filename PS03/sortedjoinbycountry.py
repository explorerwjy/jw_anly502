#!/usr/bin/env python2
#
# 
#

import mrjob
import mrjob.compat
from mrjob.job import MRJob
import sys
from mrjob.step import MRStep

from weblog import Weblog  # imports class defined in weblog.py


class First50Join(MRJob):
    SORT_VALUES = True
    def mapper(self, _, line):
        # Is this a weblog file, or a MaxMind GeoLite2 file?
        filename = mrjob.compat.jobconf_from_env("map.input.file")
        import sys
        if "top1000ips_to_country.txt" in filename:
            # Handle as a GeoLite2 file
            #
            self.increment_counter("Status", "top1000_ips_to_country file found", 1)
            try:
                (ipaddr, country) = line.strip().split("\t")
                yield ipaddr, "+" + country
            except ValueError as e:
                pass
        else:
            # Handle as a weblog file
            try:
                o = Weblog(line)
            except ValueError:
                sys.stderr.write("Invalid logfile line: {}\n".format(line))
                return
            if o.wikipage() == "Main_Page":
                yield o.ipaddr, line


    def reducer(self, key, values):
        # values has all the lines for this key
        country = None
        for v in values:
            if v[0:1] == "+":  # found the location!
                country = v[1:]
                continue
            if not country:  #
                self.increment_counter("Warning", "No Country Found", 1)
                continue
            # If we get here, v is a logfile line. Parse it again
            o = Weblog(v)
            yield "Geolocated",[o.date,country,v]

    # Let MapReduce do the sorting this time!
    # All of the keys are the same, so just take the first 50 values...
    #SORT_VALUES = True
	

    def mapper2(self,key,values):
	country = values[1]
	yield country,1
    
    def reducer2(self,key,values):
        yield key,sum(values)
    
    def mapper3(self,key,values):
        yield "sort",(key,values)

    def reducer3_init(self):
        self.lowest = []
    
    def reducer3(self,key,values):
        for (country,num) in values:
            self.lowest.append((country,num))
            #self.lowest = sorted(self.lowest)
    
    def reducer3_final(self):
        for (country,num) in sorted(self.lowest):
            yield country,num 
    #SORT_VALUES = True	
	#def mapper3(self,key,values):

    def steps(self):
		return [
				MRStep(mapper=self.mapper,reducer=self.reducer),
				MRStep(mapper=self.mapper2,reducer=self.reducer2),
                                MRStep(mapper=self.mapper3,reducer_init=self.reducer3_init,reducer=self.reducer3,reducer_final=self.reducer3_final),
			]


if __name__ == "__main__":
    First50Join.run()
