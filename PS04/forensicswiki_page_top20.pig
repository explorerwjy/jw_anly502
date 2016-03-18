--
-- part2 problem 4
-- Create a Pig program that reports the number of URLs served each day in 2012 by the forensicswiki.org website

-- Clear the output directory location
--
rmf forensicswiki_count_by_date

--
-- Map locally defined functions to the Java functions in the piggybank
--
DEFINE EXTRACT       org.apache.pig.piggybank.evaluation.string.EXTRACT();

-- This URL uses just one day
raw_logs = load 's3://gu-anly502/ps03/forensicswiki.2012-01.unzipped/access.log.2012-01-01' as (line:chararray);
--
-- This URL reads a month:
-- raw_logs = load 's3://gu-anly502/ps03/forensicswiki.2012-01.unzipped/access.log.2012-01-??' as (line:chararray);
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
logs = foreach logs_base generate ToDate(SUBSTRING(datetime_str,0,11),'dd/MMM/yyyy') as date, host, url, size;
logs2 = foreach logs generate SUBSTRING(ToString(date),0,10) as date,host,url,size;
logs3 = foreach logs2 generate REGEX_EXTRACT_ALL(date, '(2012.*)') AS date,host,url,size;
logs4 = foreach logs2 generate REGEX_EXTRACT_ALL(url,'(index.php\\?title=|/wiki/)([^ &]*)') AS date,host,url,size;
by_wiki = GROUP logs4 BY url;
wiki_count = foreach by_wiki generate group as wikipage,COUNT(logs4);
forensicswiki_page = ORDER wiki_count BY $1 DESC;
my_output = limit forensicswiki_page 20;
-- dump my_output;
-- PUT YOUR RESULTS IN output

-- store output INTO 'forensicswiki_page_top20' USING PigStorage();
store my_output INTO 'forensicswiki_page_top20' USING PigStorage();

-- Get the results
--
fs -getmerge forensicswiki_page_top20 forensicswiki_page_top20.txt
