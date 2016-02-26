import pylab as pl
import matplotlib.pyplot as plt

def plotit(x,y):
	pl.plot(x,y)
	
	return

if __name__ == "__main__":
	hand = open("wikipedia_stats.txt")
	x = []
	y = []
	for l in hand:
		t1,t2 = l.strip().split()
		x.append(''.join(t1.split('-')))
		y.append(t2)
	plotit(x,y)


