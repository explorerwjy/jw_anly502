
import mrjob
import mrjob.compat
from mrjob.job import MRJob
from mrjob.setp import MRStep
import sys
from weblog import Weblog
import matplotlib

class wikipedia(MRJob):
	def mapper(self,_,line):
		try:
			tmp = line.strip().split("")
			date = tmp[2]
			month = '-'.join(date.split('-')[0:1])
			self.increment_counter("Status","record find",1)i
			yield month,1
		except IndexError:
			self.increment_counter("Warn","bad record",1)
	def reducer(self,key,values):
		yield key,sum(values)
	SORT_VALUES = True

if __name__ == "__main__":
	wikipedia.run()



