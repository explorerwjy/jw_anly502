import pylab

def plotit(x,y):
	pylab.plot([x,y])


if __name__ == "__main__":
	hand = open("wikipedia_stats.txt")
	x = []
	y = []
	for l in hand:
		t1,t2 = l.strip().split()
		x.append(t1)
		y.append(t2)
	plotit(x,y)


