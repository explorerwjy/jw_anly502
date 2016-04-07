-- Set up config options based on documentation

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

DROP TABLE IF EXISTS bot_logs;
create temporary table bot_logs (
  date  timestamp,
  size  bigint,
  agent string,
  bot   boolean
);

insert overwrite table bot_logs
  select from_unixtime(unix_timestamp(rawdatetime, "[dd/MMM/yyyy:HH:mm:ss Z]")),
         int(size),
         agent,
         instr(lower(agent),"bot")>0
  from raw_logs;

--select * from bot_logs where bot limit 3;
--select * from bot_logs where not bot limit 3;

create temporary table bot_stats (
  yearmonth string,
  count bigint,
  botcount bigint,
  nonbotcount bigint,
  size bigint,
  botsize bigint,
  nonbotsize bigint
);

insert overwrite table bot_stats
select 
substr(date,1,10),
	count(*),
	sum(IF(bot,1,0)),
	sum(IF(bot,0,1)),
	sum(size),
	sum(IF(bot,size,0)),
	sum(IF(bot,0,size))
	from bot_logs
	group by substr(date,1,10);

-- select yearmonth,botcount,nonbotcount from bot_stats order by yearmonth;
select yearmonth,count,botcount,nonbotcount,size,botsize,nonbotsize from bot_stats order by yearmonth;
