#!/usr/bin/env python2.7
#
# A little program to make a plot of the botstats from the botstats.txt file.
# See http://matplotlib.org/examples/api/barchart_demo.html for worked example

import numpy as np
import matplotlib.pyplot as plt

if __name__=="__main__":
    months = []
    nonbots = []
    bots    = []
    for line in open("botstats.txt"):
        line = line.replace(" ","")
        vals = line.split("|")
        (month,nonbot,bot) = vals[1:4]
        months.append(month)
        nonbots.append(int(nonbot))
        bots.append(int(bot))

    count = len(months)         # number of bar groups to plot
    ind   = np.arange(count)    # The X locations for the groups
    width = 0.35                # the width of each bar
    fig, ax = plt.subplots()
    print("ind=",ind)
    print("nonbot=",nonbots)
    rects1 = ax.bar(ind, nonbots, width, color='y')
    rects2 = ax.bar(ind+width, bots, width, color='r')
    
    # add some text
    ax.set_ylabel("Number of hits")
    ax.set_title("Bots and Non-Bots per Month")
    ax.set_xticks(ind + width)   # where the tics go
    ax.set_xticklabels(months)  # the are strings
    ax.legend((rects1[0],rects2[0]), ("Bots","Non-Bots"))

    # Rotate the labels ( you need to rotate them separately)
    for label in ax.get_xticklabels():
        label.set_rotation(45)
    

    # Saving the figure causes all of the plot commands to be executed
    plt.savefig("botstats.pdf")



