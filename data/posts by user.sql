SELECT pid, fid, tid, first, author, authorid,date_format(from_unixtime(dateline),"%Y-%m-%d"),useip, rate,ratetimes,status,comment FROM x2.x2_forum_post;

select count(*) FROM x2.x2_forum_post;

# how many users had at least one post: #36091
SELECT authorid, count(distinct pid) as postnumber FROM x2.x2_forum_post where authorid <> 0 group by authorid order by postnumber desc limit 1000000 INTO OUTFILE 'E:/my/Dropbox/BBS data analysis/posts-by-uid.txt'; 

# users who posted once: 11291
SELECT author, authorid, count(distinct pid) as postnumber FROM x2.x2_forum_post where authorid <> 0 group by authorid having postnumber <= 10 limit 1000000;

# users who posted 11-100:8700
SELECT author, authorid, count(distinct pid) as postnumber FROM x2.x2_forum_post where authorid <> 0 group by authorid having postnumber < 100 and postnumber >10 limit 1000000;

# users who posted 100-1000:2022
SELECT author, authorid, count(distinct pid) as postnumber FROM x2.x2_forum_post where authorid <> 0 group by authorid having postnumber < 1000 and postnumber >=100 limit 1000000;

# users who posted 100-1000:100
SELECT author, authorid, count(distinct pid) as postnumber FROM x2.x2_forum_post where authorid <> 0 group by authorid having postnumber < 10000 and postnumber >=1000 limit 1000000;



SELECT author, authorid, count(distinct pid) as postnumber FROM x2.x2_forum_post where authorid <> 0 group by authorid order by postnumber desc;





SELECT count(*) as users from (SELECT author, authorid, count(distinct pid) as postnumber FROM x2.x2_forum_post where authorid <> 0 group by authorid) as posts;