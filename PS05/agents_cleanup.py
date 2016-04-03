#!/usr/bin/env python2.7

"""
Read the file agents.raw and output agents.csv, a comma-separated file
"""

if __name__=="__main__":
    with open("agents.txt","r") as f:
        with open("agents.txt","w") as out:
            for line in f:
                if(line[0] in '+|'):
                    out.write(line)

            
