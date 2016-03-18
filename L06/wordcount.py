#!/usr/bin/spark-submit
#
# wordcount as a pyspark

import sys
from operator import add
from pyspark import SparkContext

if __name__ == "__main__":
    
    ##
    ## Parse the arguments
    ##

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("file",help="file to wordcount")
    args = parser.parse_args()

    ## 
    ## Run WordCount on Spark
    ##

    sc     = SparkContext( appName="PythonWordCount" )
    lines  = sc.textFile( args.file, 1 )
    counts = lines.flatMap(lambda line: line.split(' ')) \
                  .map(lambda word: filter(unicode.isalpha,word)) \
                  .map(lambda x: (x, 1)) \
                  .reduceByKey(add)

    top20counts = counts.sortBy(lambda x: x[1], ascending=False) \
                  .take(20)
    for (word, count) in top20counts:
        print "%-10s: %i" % (word, count)
    
    ## 
    ## Terminate the Spark job
    ##

    sc.stop()
