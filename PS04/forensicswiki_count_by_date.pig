--
-- part2 problem 4
-- Create a Pig program that reports the number of URLs served each day in 2012 by the forensicswiki.org website

-- Clear the output directory location
--
rmf count_by_date

--
-- Map locally defined functions to the Java functions in the piggybank
--
DEFINE EXTRACT       org.apache.pig.piggybank.evaluation.string.EXTRACT();

--
-- Uncomment the data source you wish to use:
-- This URL uses just one day
-- raw_logs = load 's3://gu-anly502/ps03/forensicswiki.2012-01.unzipped/access.log.2012-01-01' as (line:chararray);
--
-- This URL uses another day:
-- raw_logs = load 's3://gu-anly502/ps03/forensicswiki/access.log.2012-12-31.gz' as (line:chararray);

-- This URL reads a month:
raw_logs = load 's3://gu-anly502/ps03/forensicswiki.2012-01.unzipped/access.log.2012-01-??' as (line:chararray);
--
-- This URL reads all of 2012:
-- raw_logs = load 's3://gu-anly502/ps03/forensicswiki.2012.txt' as (line:chararray);

 
-- logs_base processes each of the lines 
-- FLATTEN takes the extracted values and flattens them into a single tupple
--
logs_base = 
  FOREACH
   raw_logs
  GENERATE
   FLATTEN ( EXTRACT( line,
     '^(\\S+) (\\S+) (\\S+) \\[([^\\]]+)\\] "(\\S+) (\\S+) \\S+" (\\S+) (\\S+) "([^"]*)" "([^"]*)"'
     ) ) AS (
     host: chararray, identity: chararray, user: chararray, datetime_str: chararray, verb: chararray, url: chararray, request: chararray, status: int,
     size: int, referrer: chararray, agent: chararray
     );

-- YOUR CODE GOES HERE
logs = foreach logs_base generate ToDate(datetime_str,'dd/MMM/yyyy:HH:mm:ss Z') as date,host,url,size;
logs2 = foreach logs generate SUBSTRING(ToString(date),0,10) as date,host,url,size;
by_date = GROUP logs2 BY (date);
date_counts = foreach by_date generate group as date,COUNT(logs_base);
date_counts_sorted = ORDER date_counts BY $1 DESC;
dump date_counts_sorted;
-- YOUR CODE SHOULD PUT THE RESULTS IN date_counts_sorted

--store date_counts_sorted INTO 'count_by_date' USING PigStorage();


-- Get the results
--
--fs -getmerge count_by_date forensicswiki_count_by_date.txt

