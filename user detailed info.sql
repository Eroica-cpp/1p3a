#total number
SELECT count(*) FROM x2.x2_common_member limit 150000;

select GROUP_CONCAT(CONCAT("'",COLUMN_NAME,"'"))
from INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'my_table'
AND TABLE_SCHEMA = 'my_schema'
order BY ORDINAL_POSITION;
# user info
select b.uid,friends,posts,threads,views,status,adminid,groupid,credits,
		date_format(from_unixtime(regdate),"%Y-%m-%d") AS regdate,
		timestampdiff(day, from_unixtime(regdate), from_unixtime(a.lastvisit)) as lifeduration,
		timestampdiff(day, from_unixtime(a.lastvisit), now()) as absentdays,
		if(posts>0, timestampdiff(day, from_unixtime(a.lastpost), now()), -1) as dayssincelastpost,
		#timestampdiff(day, a.lastactivity, now()) as dayssincelastactivity,
		timestampdiff(day, '2009-05-15' , from_unixtime(regdate) ) as regonbbsdays,
		oltime as hoursonline
from
(select crds.*, r.status, avatarstatus,adminid, groupid, regdate,credits from 
        (SELECT uid,status,avatarstatus,adminid, groupid, regdate, credits  FROM x2.x2_common_member) as r 
	    join (SELECT * FROM x2.x2_common_member_count) as crds on r.uid = crds.uid ) 
 as b
   join (SELECT uid,lastvisit,lastactivity,lastpost,favtimes,sharetimes FROM x2.x2_common_member_status) as a on a.uid = b.uid
limit 150000 
INTO OUTFILE 'E:/my/Dropbox/BBS data analysis/full-user-info.txt' 
;
