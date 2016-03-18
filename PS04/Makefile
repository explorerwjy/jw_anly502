wordcount_shakespeare1.txt: wordcount_shakespeare1.pig
	pig -x mapreduce -stop_on_failure $^ 

wordcount_shakespeare2.txt: wordcount_shakespeare2.pig
	pig -x mapreduce -stop_on_failure $^ 

wordcount_shakespeare3.txt: wordcount_shakespeare3.pig
	pig -x mapreduce -stop_on_failure $^ 

forensicswiki_count_by_date.txt: forensicswiki_count_by_date.pig
	pig -x mapreduce -stop_on_failure $^

forensicswiki_page_top20.pig: forensicswiki_count_by_date.txt
	pig -x mapreduce -stop_on_failure $^

wordcount_shakespeare4.txt: wordcount_shakespeare4.py
	spark-submit $^

wikipedia_by_month.txt: wikipedia_by_month.py
	spark-submit $^


