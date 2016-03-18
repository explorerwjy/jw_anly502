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

#import matplotlib.mlab as mlab
#import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    ##
    ## Parse the arguments
    ##

    infile =  's3://gu-anly502/ps03/freebase-wex-2009-01-12-articles.tsv'

    ## 
    ## Run WordCount on Spark
    ##

    sc     = SparkContext( appName="Wikipedia Count" )
    ## YOUR CODE GOES HERE
    lines = sc.textFile(infile)
    datetime = lines.map(lambda x:x.split('\t')[2])
    date = datetime.map(lambda x:'-'.join(x.split('-')[0:2]))
    pairs1 = date.map(lambda x:(x,1))
    pairs2 = pairs1.reduceByKey(lambda x,y:x+y)
    counts = pairs2.sortByKey(True).collect()
    ## PUT YOUR RESULTS IN counts

    #x = []
    #y = []
    with open("wikipedia_by_month.txt","w") as fout:
        for (date, count) in counts:
            fout.write("{}\t{}\n".format(date,count))
	    #x.append(date)
	    #y.append(count)
	##plot
    
    #plt.plot(x,y,'r--',linewidth=1)
    #plt.xlabel('Date')
    #plt.ylabel('Count')
    #plt.title('wikipedia monthly totals')
    #plt.grid(True)
    #plt.show()
   
    ## 
    ## Terminate the Spark job
    ##

    sc.stop()
