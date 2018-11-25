#!/usr/bin/env python
# coding: utf-8

# # CA4 - Ciaran Dunne - 10393193 

# Import each of the libaries that will be used

# In[222]:


import pandas as pd


# In[223]:


import numpy as np


# In[224]:


import matplotlib.pyplot as plt


# In[225]:


import seaborn as sns


# # Step 1 - Gather the Data

# Import the file to be used and check it

# In[226]:


csv_file = 'changes.csv'
changes = pd.read_csv(csv_file, usecols = [0, 1, 2, 3, 4, 5])


# # Step 2 - Prepare the Data

# In[227]:


changes['author'].value_counts()


# One of the "users" is unreadable - so change that to "UNKNOWN" for ease of use

# In[228]:


changes = changes.replace(to_replace=r'/OU=Domain Control Validated/CN=svn.company.net', value='UNKNOWN', regex=True)


# In[229]:


#changes[['revision','author']]


# Split out dates for year, month and day to support analysis (mainly for month)

# In[230]:


# new data frame with split value columns 
newdate = changes["date"].str.split("-", n = 3, expand = True) 
  
# making seperate column for year 
changes["year"]= newdate[0] 
  
# making seperate column for month
changes["month"]= newdate[1] 
  
# making seperate column for day 
changes["day"]= newdate[2] 

# df display 
#changes


# Split out time for hour, minute and second to support analysis (mainly for hour of the day)

# In[231]:


# new data frame with split value columns 
newtime = changes["time"].str.split(":", n = 3, expand = True) 
  
# making seperate column for year 
changes["hour"]= newtime[0] 
  
# making seperate column for month
changes["minute"]= newtime[1] 
  
# making seperate column for day 
changes["second"]= newtime[2] 

# df display 
#changes


# In[232]:


#changes.to_csv("TableauFile", sep='\t')


# Identify the day of the week that commits were made - to see if anyone was working weekends. 

# In[233]:


changes['NewDate'] = pd.to_datetime(changes['date'], format='%Y-%m-%d %H:%M:%S')


# In[234]:


changes['weekday'] = changes['NewDate'].dt.weekday_name


# In[235]:


changes.dtypes


# In[236]:


changes[['hour', 'minute', 'second']] = changes[['hour', 'minute', 'second']].apply(pd.to_numeric)


# Check how the table is looking

# In[237]:


changes


# # Step 3 - Get Insights

# 1. Check the mean number of lines per comment across all authors 

# In[238]:


changes['number_of_lines'].mean()


#  

# 2. Identify the total number of revisions made by each author during the period in question, and represent it graphically:
#  - Bar chart
#  - Pie Chart

# In[239]:


rev_auth = changes['author'].value_counts()


# In[240]:


rev_auth.plot(kind = 'bar', title = 'Number of Revisions by Author', rot = 45, ).set(xlabel = 'Authors', ylabel = 'No. of Revisions')


# In[241]:


rev_auth.plot(kind = 'pie', figsize=(6, 6), title = 'Number of Revisions by Author', rot = 45, ).set(xlabel = '', ylabel = '', )


#  

# 3. Identify the number of revisions made each month to understand peak and tough activity, and represent it graphically:
#  - Bar chart
#  - Pie Chart
#  - Line Graph

# In[242]:


rev_month = changes.groupby(["month"]).count()["revision"]
rev_month


# In[243]:


rev_month.plot(kind = 'bar', title = 'Number of Revisions by Month', rot = 45, ).set(xlabel = 'Month', ylabel = 'No. of Revisions')


# In[244]:


rev_month.plot(kind = 'pie', figsize=(6, 6), title = 'Number of Revisions by Month', rot = 45, ).set(xlabel = 'Month', ylabel = 'No. of Revisions')


# In[245]:


rev_month.plot(table=True, figsize=(6, 6), yticks=(np.arange(0, 140, step=10)))


#  

# 4. Identify the hour of the day that commits are made and represent it graphically 
#  - Line Graph
#  - Scatter Plot

# In[246]:


rev_time = changes.groupby(["hour"]).count()["revision"]
rev_time


# In[247]:


rev_time.plot(table=True, figsize=(6, 6), yticks=(np.arange(0, 140, step=10)))


# In[248]:


rev_time = changes.groupby(["author", "hour"]).count()["revision"]
rev_time


# In[249]:


# construct plot
# https://www.datacamp.com/community/tutorials/seaborn-python-tutorial
f, ax = plt.subplots(figsize = (20, 10))
sns.swarmplot(x="author", y="hour", data=changes, ax=ax)

# Show plot
plt.show()


#  

# 5. Identify the activity by day of the week to see if there was any activity over weekends.
#  - Pie Chart

# In[250]:


rev_day = changes.groupby(["weekday"]).count()["revision"]
rev_day


# In[251]:


rev_day.plot(kind = 'pie', title = 'Revisions by Day of the Week', rot = 45, ).set(xlabel = '', ylabel = '')


#  

# 6. Identify activity outside of typical working hours (ie. 9am - 6pm) and represent graphically
#  - Bar Chart

# In[252]:


changes['author'][changes['time'] > '17:30:00'].count()


# In[253]:


afterSix = changes[changes['hour']>=18]


# In[254]:


afterSix = afterSix.groupby(["author"]).count()["revision"]
afterSix


# In[255]:


afterSix.plot(kind = 'bar', title = 'Commits after 6pm', rot = 45, ).set(xlabel = 'Authors', ylabel = 'Total Commits')


# In[256]:


beforeNine = changes[changes['hour']<=8]


# In[257]:


beforeNine = beforeNine.groupby(["author"]).count()["revision"]
beforeNine


# In[258]:


beforeNine.plot(kind = 'bar', title = 'Commits before 9am', rot = 45, ).set(xlabel = 'Authors', ylabel = 'Total Commits')


# # Summary of Analysis

# As part of the analysis we looked at the data from 6 different perspectives
# 
# 1. Comment detail per commit (averages)
# 2. Total commit volumes per author 
# 3. Number of revisions made per month to understand peak and tough activity
# 4. Timing of commits (hour of the day)
# 5. Activity by day of the week 
# 6. Activity outside of typical working hours (ie. 9am - 6pm)
# 

# # Statistical Pieces of "Interestingness"

# 1. The team don't do much work outside of typical working hours 
#  - There were no commits made on weekends.
#  - There were a total of 26 commits outside of standard working hours over the 5 months (18 before 9am,  and 8 after 5.30pm) - which is quite low. 
# 
# 
# 2. Team member commits are not consistent  
#  - There are some team members who are doing considerably more commits that the rest of the team.
#  - Thomas and Jimmy make the vast majority of commits when compared to other team members. 
# 
# 
# 3. There are some peaks and troughs in terms of commit activity
#  - The vast majority of commits are made in the middle of the day at around 2pm. If there are operational constraints, the team could looks to distribute commits more over the course of the day. 
#  - There is an even enough spread of commits over the days of the week, but in terms of months, each month had relatively consistant levels of activity, however, September had less than half the volume of commits as other months. This might be worth looking into if it is already not understood. 
# 
# 
