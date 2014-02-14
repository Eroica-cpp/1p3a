Analyzing 1point3acres Data
=================

By hacking on data we are familiar with and solving problems we are curious about, we hope to hone our skills as data scientists.


Background
----------------
[一亩三分地论坛](http://www.1point3acres.com/bbs) is a forum for Chinese students, scholars and young professional overseas. Its main users are graduate school applicants, undergraduate and graduate students studying in North America, and young professionals, mostly in high tech fields. Majority of its users are between 18 and 25 years old, highly educated and either have or are working on an advanced degree. 


Data
----------
The Forum for 1point3acres.com was founded on 2009/05/15. Posting behaviors from its **100,000+ users** in **over 1 million posts** have been recorded in the database since then. 

While this is not a huge amount of data, it provides a good starting point for some interesting analysis. 

\ data folder: hopefully file names are self explanatory

Where did the data come from:
Discuz database:Full data schema is explained [here](http://faq.comsenz.com/library/database/x25/x25_index.htm).
It's not an exact match of the current version of discuz we have, but should be OK as a starting point. 

SQL queries were also included for completeness. 

Data is intentionally stripped to any obvious user information like full user name, ip etc. Please respect other's and try not to use the data for anything other than education purposes. 

Analysis
-----------
Minimal data cleaning is needed.
Feel free to analyze the data for any questions that interest you. All we ask is that you share the results as well as the methods/code. 

Data science, describe, predict and prescribe. 

We encourage reproducible research. Our tools include R (knitr, Rmd, etc), Python (iPython Notebook etc), etc.

### Story telling with Data ####
#####Attrition of users:#### 
When a user fails to visit the forum since at least 120 days ago, we consider the user "lost" forever. 

1. What is the attrition pattern of the whole forum over time? 
2. What's the typical duration of a user on the forum? 
3. Based on past behavior of user interaction with posts and other users, can we predict upcoming attrition and intervene?

Time to event (survival) data analysis may be used.

##### Time trend of user activity: 
1. Over the past four years the forum has seen some growth over time. 
2. The growth has strong seasonality effect due to the nature of discussions commonly associated with this forum, namely, graduate school applications. During the "peak" months of Feb, March, April the forum usually sees a drastic increase in new users registered, page views and new posts. On the other hand May, June and July are the troughs. 
3. In addition, similar to most websites, there's a strong weekend/weekday effect. 
4. The day/night effect can be more complicated. By analyzing ip address of visitors, we can see the shift in user population. Users come from two main areas, China, and North America. With timezones approximately half a day apart, this dilutes the usual day/night effect. An analysis of the user geo-location over time can also shed some light on the growth in popularity of the forum.
5. Posts follow a high skewed distribution, where a small fraction of user accounted for a vast majority of activities on the forum. 

Even though longitudinal study can not be used to make causal inference, it may serve as an indicator of overall health of the forum. (Times series analysis)

##### Interaction between users
Social Network analysis.

##### Topics of interest and shift over time
Text Analytics. Sentiment Analysis.
##### Data driven app devlopment
1. What's my key words on the forum?
2. What are my progress/accomplishment charts on MOOCs?
3. ?

##### 飞跃? Geographical Shift of Users
Due to the nature of the forum, many users tend to start visiting the site when they start preparing for going abroad, and may continue to visit after landing overseas. By Comparing registering IP and IP on subsequent visits, we can track the movement of users. Too fine grained information seems too much to reveal on the individual user level, as an aggregate we may still examine the overall pattern of "moving overseas" of our users. 

##### Machine Learning Prediction Model for Graduate School Admission
Why the current available data can not give an accurate prediction


Us, the Analyzers
------------
We are users of the forum, interested in finding insights from data. In our daily lives we are (aspiring) statisticians, data scientists, and coders. 

References
---------------
1. [Modeling Techniques in Preditive Analytics](http://www.ftpress.com/promotions/modeling-techniques-in-predictive-analytics-139480)
2. Forecast with R
3. 