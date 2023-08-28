#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# In[2]:


isp_data = pd.read_csv('../files/isp_data.csv')


# In[4]:


isp_data


# In[17]:


monthly_payments = isp_data.groupby(['ISP','year', 'month'])['amount'].sum().reset_index()

monthly_payments = pd.DataFrame(monthly_payments)

monthly_payments


# In[24]:


# Create a custom date column in the format 'YYYY-Month'
df['date'] = df['year'].astype(str) + '-' + df['month'].apply(lambda x: calendar.month_name[x])

# Create a bar plot using Seaborn
plt.figure(figsize=(12, 6))
sns.set_style("whitegrid")
sns.barplot(data=df, x="date", y="amount", hue="ISP", ci=None)

# Rotate X-axis labels for better readability
plt.xticks(rotation=45, ha="right")

# Set plot labels and title
plt.xlabel("Year-Month")
plt.ylabel("Amount")
plt.title("Monthly Expenditure on Internet Services by ISP")

# Show the plot
plt.savefig('plot.png')


# In[ ]:





# In[ ]:




