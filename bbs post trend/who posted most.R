setwd("E:/my/Dropbox/BBS data analysis/")

a = read.table("posts-by-uid.txt")
str(a)
colnames(a) = c('uid', 'posts')

## total user: 102921
102921-36091

a$postbin = cut(a$posts, breaks = c(0,1,10,100,1000,25000))
table(a$postbin)
(0,1]          (1,10]        (10,100]     (100,1e+03]   (1e+03,1e+04] (1e+04,2.5e+04] 
11291           13976            8718            2004             100               2 

library(plyr)

tot = ddply(a,c("postbin"), summarise, sum(posts))
len = ddply(a,c("postbin"), summarise, length(posts))

aa = data.frame(bin = tot[[1]], total = tot[[2]], count = len[[2]])
aa = rbind(c("zero",0,102921-36091),aa)
rownames(aa)[1]=0

aa$bin = as.character(aa$bin)
aa$bin[is.na(aa$bin)] = "(-1,0]"
aa$bin= as.factor(aa$bin)

aa$Total = as.numeric(aa$total)/sum(as.numeric(aa$total))
aa$Count = as.numeric(aa$count)/sum(as.numeric(aa$count))

aa$CumSumTotal = cumsum(aa$Total)
aa$CumSumCount = cumsum(aa$Count)

library(reshape)
ab = melt(aa, id.vars="bin", measure.vars=c('Total',"Count"))

ggplot(data=ab, aes(factor(variable), fill=bin, y=value))+geom_bar()


hist(a$posts)
library(ggplot2)

g = ggplot(a, aes(x=posts))
g+stat_bin(breaks=c(1,10,100,1000,10000))

m = qplot(uid, posts, data=a)
bks = seq(1, 25000)

m +  scale_y_log10(breaks=bks, labels=bks)
qplot(posts, data=a, geom="histogram")+coord_trans(x = "log10")


ggplot(a, aes(x=uid, y=posts)) + geom_point(shape=19, alpha=.3)+scale_y_log10(breaks=bks, labels=bks)




MAXDAYS=2000 # change this value
b = read.table("E:/my/Dropbox/BBS data analysis/full-user-info.txt")

colnames(b) = c("uid",       
                "friends","posts","threads","views","status","adminid","groupid","credits",
                "regdate",
             "lifeduration",
                 "absentdays",
                 "dayssincelastpost",
               "regonbbsdays",
                "hoursonline")
b$dead = b$absentdays > 120
b$postbin = cut(b$posts, breaks = c(-1,0,1,10,100,1000,25000))
b$regonbbsdays[b$regonbbsdays<0 | b$regonbbsdays > MAXDAYS]=NA
b$lifeduration[b$lifeduration>MAXDAYS] = NA 
b$absentdays[b$absentdays>MAXDAYS] = NA
b$dayssincelastpost[b$dayssincelastpost>MAXDAYS] = NA
ggplot(data=b, aes(x=posts, y=lifeduration, color=views))+geom_point(shape=19, alpha=.3)+scale_x_log10(breaks=bks, labels=bks)

ggplot(data=b, aes(x=regonbbsdays, y=lifeduration, color=dead))+geom_point(shape=19, alpha=.3)

ggplot(data=b, aes(x=posts, y=lifeduration, color=absentdays))+geom_point(shape=19, alpha=.3)+scale_x_log10(breaks=bks, labels=bks)

## active users by reg date
ggplot(data=b,aes(factor(regonbbsdays), fill=dead))+geom_bar()+scale_x_discrete(breaks=c(365*(0:4),1728-120),labels=c("Start","Year1","Year2","Year3", "Year4", "cutoff"))


## posts by reg date
ggplot(data=b,aes(factor(regonbbsdays), fill=postbin))+geom_bar()+scale_x_discrete(breaks=c(365*(0:4)),labels=c("Start","Year1","Year2","Year3", "Year4"))#+ scale_fill_brewer()


## when did active users register
ggplot(data=subset(b,posts>100),aes(factor(regonbbsdays), fill=postbin))+geom_bar()+scale_x_discrete(breaks=c(365*(0:4)),labels=c("Start","Year1","Year2","Year3", "Year4"))#+ scale_fill_brewer()


## views and posts
ggplot(data=b, aes(x=views, y=posts, color=dead)) + geom_point(shape=16, size=5, alpha=.1)+scale_x_log10(breaks=bks, labels=bks)+scale_y_log10(breaks=bks, labels=bks)


library(survival)
fit = survfit(Surv(lifeduration, dead)~1, data=b)
plot(fit, xlim=c(-1,30))
ggsurv(fit)

## now, predict churn/attrition!!

