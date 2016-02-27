#!/usr/bin/env python2
#
# 
# Small program to display the first 50 lines of a web log (chronically)
# Creates a single mapper that maps every line to the same key, with the values
# being the datetime and the original weblog line.
# The reducer counts 50

# The one problem with this approach is that all of the keys need to go through the same reducer.
# We can do it better with a distributed first50.

import sys

from mrjob.job import MRJob

from weblog import Weblog  # imports class defined in weblog.py


# First50 is just Top-10 in reverse

class First50(MRJob):
    # The mapper separates out the datetime from the line
    # and builds a list of the lowest 50 dates
    # (We don't use Python's heap, because it is a maxheap)
    # mapper_final sends them to the reducer
    # The mapper runs on all of the nodes, finding the first 50 of all the splits
    
    def mapper_init(self):
        self.lowest = []
    
    def mapper(self, _, line):
        try:
            o = Weblog(line)
        except ValueError:
            sys.stderr.write("Invalid logfile line: {}\n".format(line))
            return
            

        # See if this is the desired URL
        if o.wikipage() == "Main_Page":
            self.lowest.append((o.datetime, line))
            self.lowest = sorted(self.lowest)[0:50]  # keep just the first 50
            #yield "First50",line
    
    def mapper_final(self):
        for (datetime, line) in self.lowest:
            yield "First50", (datetime, line)
    
    # The reducer maintains also uses a list to get the first 50
    # Because all of the lines come through with the same key,
    # mapreduce guarentees that only a single reducer will run
    def reducer_init(self):
        self.lowest = []
	
    # reducer adds to the heap. Notice we use
    def reducer(self, _, values):
        for (datetime, line) in values:
            self.lowest.append((datetime, line))
            self.lowest = sorted(self.lowest)[0:50]  # keep just the first 50

    def reducer_final(self):
        for (datetime, line) in sorted(self.lowest)[0:50]:
            yield "First50", line
    #SORT_VALUES = True

if __name__ == "__main__":
    First50.run()
