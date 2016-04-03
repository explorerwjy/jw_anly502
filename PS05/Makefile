botstats.raw: botstats.hql
	beeline -u jdbc:hive2://localhost:10000 -n hadoop -p hadoop -f botstats.hql > botstats.raw

botstats.txt: botstats.raw
	grep '^[|\+] 2012' botstats.raw > botstats.txt

botstats.pdf: botstats.txt
	python2.7 botstats_plot.py

agents.raw: agents.hql
	beeline -u jdbc:hive2://localhost:10000 -n hadoop -p hadoop -f agents.hql > agents.raw	

agents.txt: agents.raw
	grep '^[|\+]' agents.raw > agents.txt

