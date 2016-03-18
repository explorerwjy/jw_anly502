#!/usr/bin/spark-submit
#
# Problem Set #4
# Implement wordcount on the shakespeare plays as a spark program that:
# a.Removes characters that are not letters, numbers or spaces from each input line.
# b.Converts the text to lowercase.
# c.Splits the text into words.
# d.Reports the 40 most common words, with the most common first.

# Note:
# You'll have better luck debugging this with ipyspark

import sys
from operator import add
from pyspark import SparkContext

def isokay(ch):
    return ch in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 '

if __name__ == "__main__":
    
    ##
    ## Parse the arguments
    ##

    infile =  's3://gu-anly502/ps04/Shakespeare.txt'

    ## 
    ## Run WordCount on Spark
    ##

    sc     = SparkContext( appName="Shakespeare Count" )
    ## YOUR CODE GOES HERE
    lines  = sc.textFile( infile )
	lines2 = lines.filter(isokay)
	lines3 = lines2.map(lambda x:x.lower())
	words = lines3.flatMap(lambda x:x.split(" "))
	result = words.map(lambda x :(x,1)).reduceByKey(lambda x,y :x+y)
	tmp_top40counts = result.map(lambda x:(x[1],x[0])).sortByKey(False).take(40)
	top40counts = result.map(lambda x:(x[1],x[0]))
    ## PUT YOUR RESULTS IN top40counts

    with open("wordcount_shakespeare4.txt","w") as fout:
        for (word, count) in top40counts:
            fout.write("{}\t{}\n".format(word,count))
    
    ## 
    ## Terminate the Spark job
    ##

    sc.stop()
