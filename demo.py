# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 10:04:19 2020

@author: Rajkumar
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_excel('dataset/Data_Train.xlsx')

df = df.replace({'RATING':['NEW','-']},'0')
df['RATING'] = df['RATING'].astype('float')
def datacleaning(df, special_character1=False, digit=False,
                 nalpha=False):
    df = df.drop_duplicates(keep='first')
    df = df.reset_index(drop=True)
    df_cleaned = df.copy()
    if special_character1:
        df_cleaned = df_cleaned.apply(lambda x: x.str.split(r'[^a-zA-Z.\d\s]').
                                      str[0] if(x.dtypes == object) else x)
    if digit:
        df_cleaned = df_cleaned.apply(lambda x: x.str.replace(r'\d+', '')
                                      if(x.dtypes == object) else x)
    if nalpha:
        df_cleaned = df_cleaned.apply(lambda x: x.str.replace(r'\W+', ' ')
                                      if(x.dtypes == object) else x)
    df_cleaned = df_cleaned.apply(lambda x: x.str.strip() if(x.dtypes == object)
                                  else x)
    df_cleaned['CITY'] = df_cleaned['CITY'].str.replace('New Delhi', 'Delhi')
    return df_cleaned
df = df.dropna()
df = df.fillna('')
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df['months'] = df['Timestamp'].dt.month_name()
df['day'] = df['Timestamp'].dt.day_name()
## join 
resultant = df.merge(company_df, left_on="company_id", right_on="company_id",how='outer')
# how: {‘left’, ‘right’, ‘outer’, ‘inner’}
## sortng
track = df.sort_values(by=['COST'], ascending=False).reset_index(drop=True)
track = df.sort_values(by=['COST','TITLE'], ascending=False).reset_index(drop=True)
# find district values
x = list(pd.unique(track['TITLE']))
## duplicates
df = df.drop_duplicates(keep='first')
drop = df.drop_duplicates(subset=['TITLE'], keep='first')
# find duplicates rows
duplicates = df[df.duplicated(subset=['TITLE'], keep='first')]
duplicates = df[df.duplicated()]
## cumulative sum of crows
cumsum = df['COST'].cumsum()

## groupby sum,mean, count
avg = df.groupby('TITLE').mean()
summ = df.groupby('TITLE').sum()
minn = df.groupby('TITLE').min()
count = df.groupby('TITLE').count()
count = df.groupby(['TITLE','CUISINES']).count().reset_index()
count = df['TITLE'].value_counts()

## second highest cost
second = df.sort_values(by='COST', ascending=False).iloc[1,:]
## pivot table
table = pd.pivot_table(df, index=["TITLE"], aggfunc=np.sum, fill_value=0)

# Exploratory Data Analysis ###
f, axes = plt.subplots(2, 2)
sns.boxplot(x=df['COST'], ax=axes[0, 0])
sns.boxplot(x=df['VOTES'], ax=axes[0,1])
sns.boxplot(x=df['RATING'] , ax=axes[1,0])
sns.pairplot(df,vars=['COST','RATING'], kind='scatter')
sns.countplot(y=df["CITY"])
sns.countplot(y=df["CUISINES"])
sns.lineplot(x='months',y='COST',data=df, estimator=np.median)
sns.barplot(x="COST", y="CITY", data=df, estimator=np.median)
table=pd.crosstab(df["CUISINES"], df['TITLE'])
table.plot(kind='barh',stacked=True)
