-- wordcount_shakespeare3.pig
--
-- Find the top-20 most popular words beginning with a "h",
-- ignoring case.
--
-- Clear the output directory location
--
rmf sorted_words3

--
-- Run the script

shakespeare = LOAD 's3://gu-anly502/ps04/Shakespeare.txt' as (line:chararray);

-- YOUR CODE GOES HERE
words = foreach shakespeare generate flatten(TOKENIZE(line)) as word;
lower_words = foreach words generate LOWER(word) as low_word;
h_words = FILTER lower_words BY (low_word MATCHES '^h.*');
grouped = GROUP h_words BY low_word;
wordcount = foreach grouped generate group, COUNT(h_words);
sorted_words = ORDER wordcount BY $1 DESC;
sorted_words20 = limit sorted_words 20;
-- PUT YOUR RESULTS IN sorted_words20

STORE sorted_words20 INTO 'sorted_words3' USING PigStorage();
 
-- Get the results
--
fs -getmerge sorted_words3 wordcount_shakespeare3.txt
