SET mapred.input.dir.recursive=true;
SET hive.mapred.supports.subdirectories=true;
SET hive.groupby.orderby.position.alias=true;

DROP TABLE IF EXISTS raw_logs;
CREATE EXTERNAL TABLE raw_logs (
  host STRING,
  identity STRING,
  user STRING,
  rawdatetime STRING,
  request STRING,
  status STRING,
  size STRING,
  refer STRING,
  agent STRING
  )
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.RegexSerDe'
WITH SERDEPROPERTIES (
  "input.regex" = "([^ ]*) ([^ ]*) ([^ ]*) (-|\\[[^\\]]*\\]) ([^ \"]*|\"[^\"]*\") (-|[0-9]*) (-|[0-9]*) \"([^\"]*)\" \"([^\"]*)\".*",
  "output.format.string" = "%1$s %2$s %3$s %4$s %5$s %6$s %7$s %8$s %9$s"
)
STORED AS TEXTFILE
LOCATION 's3://gu-anly502/ps05/forensicswiki/2012/';
-- LOCATION 's3://gu-anly502/ps05/forensicswiki/2012/12/';

DROP TABLE IF EXISTS agent_logs;
create temporary table agent_logs (
  date  timestamp,
  agent string,
  os    string,
  bot   boolean
);

insert overwrite table agent_logs
select 
from_unixtime(unix_timestamp(rawdatetime, "[dd/MMM/yyyy:HH:mm:ss Z]")),
agent,
if ( instr(lower(agent),"windows")>0, "windows",if ( instr(lower(agent),"mac")>0, "mac",if ( instr(lower(agent), "linux")>0, "linux",""))),
instr(lower(agent),"bot")>0
from raw_logs;

-- select * from agent_logs limit 5;

-- Section #1:
select 
os,
count(*) as num_of_hits
from agent_logs
where (os='windows' or os='mac' or os='linux')
group by os;

-- Section #2: Provide 5 agents for which the OS could not be classified that are bots
select 
agent as Bot_agent,count(*) as number_of_hits
from agent_logs 
where os='' and bot=True and length(agent)>5 and length(agent)<15 
group by agent
limit 5;

-- Section #3: Provide 5 agents for which the OS could not be classified that are not bots.
select
agent as non_Bot_agent,count(*) as number_of_hits
from agent_logs 
where os='' and bot=False and length(agent)>5 and length(agent)<15 
group by agent
limit 5;
