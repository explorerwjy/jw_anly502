#!/usr/bin/env python2

# This is a version of the wordcount that only prints the top10.
# It does so by maintaining a heap as an instance variable in the reducer object.
#
# The mapper outputs <word,1>
# The reducer_init() creates an empty heap
# The reducer inputs <word,(1,1,1...)> and outputs NOTHING.
#    Instead, it maintains the heap with <word,COUNT>, keeping only the TOPN
# The reducer_final outputs the heap, in reverse sort order

from mrjob.job import MRJob
import heapq

TOPN = 10
class WordCount(MRJob):
    def mapper(self, _, line):
        for word in line.strip().split():
            word = filter(str.isalpha,word.lower())
            yield word,1

    def reducer_init(self):
        self.heap = []

    def reducer(self, key, values):
        heapq.heappush(self.heap,(sum(values),key))
        if len(self.heap) > TOPN:
            heapq.heappop(self.heap)
        # Uncomment this print statement to monitor the top of the stack
        # print(self.heap)

    def reducer_final(self):
        for v in sorted(self.heap, reverse=True):
            yield v

if __name__=="__main__":
    WordCount.run()
