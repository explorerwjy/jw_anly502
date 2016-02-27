
import mrjob
import mrjob.compat
from mrjob.job import MRJob
from mrjob.step import MRStep
import sys

class wikipedia(MRJob):
    SORT_VALUES = True
    def mapper(self,_,line):
	try:
	    tmp = line.strip().split("\t")
	    date = tmp[2]
	    month = '-'.join(date.split('-')[0:2])
	    self.increment_counter("Status","record find",1)
	    yield month,1
	except IndexError:
	    self.increment_counter("Warn","bad record",1)
    def reducer(self,key,values):
	yield key,sum(values)
    def mapper2(self,key,values):
        yield "sort",(key,values)
    def reducer2_init(self):
        self.queue = []
    def reducer2(self,key,values):
        for (month,num) in values:
            self.queue.append((month,num))
            self.queue = sorted(self.queue)
    def reducer2_final(self):
        for (month,num) in sorted(self.queue):
            yield month,num

    def steps(self):
        return [
                MRStep(mapper=self.mapper,reducer=self.reducer),
                MRStep(mapper=self.mapper2,reducer_init=self.reducer2_init,reducer=self.reducer2,reducer_final=self.reducer2_final)    
                ]
    
if __name__ == "__main__":
    wikipedia.run()



