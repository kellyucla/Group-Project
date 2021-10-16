#!/usr/bin/env python
# coding: utf-8

# **Education Attainment in San Diego County**
# 
# This notebook takes a look at the level of educational attainment and employment in San Deigo County by people between the ages of 25 to 64.
# 
# Kelly Banh

# In[1]:


import pandas as pd

# to read and visualize spatial data
import geopandas as gpd

# to provide basemaps 
import contextily as ctx

# to give more power to your figures (plots)
import matplotlib.pyplot as plt


# In[2]:


edu = gpd.read_file('eduemploy.geojson')


# In[3]:


edu.shape


# In[4]:


edu.head


# In[5]:


edu.plot(figsize=(10,10))


# In[6]:


# overwriting default settings
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[7]:


edu.sample()


# In[8]:


# looking at the data types
edu.info()


# In[9]:


edu.geoid.head()


# In[11]:


# check the data again
edu.head()


# In[13]:


# drop the row with index 0 (i.e. the first row)
edu = edu.drop([0])


# In[14]:


# check to see if it has been deleted
edu.head()


# In[15]:


list(edu)


# In[16]:


# columns to keep
columns_to_keep = ['geoid',
 'name',
 'B23006001',
 'B23006002',
 'B23006009',
 'B23006016',
 'B23006023',
 'B23006024',
 'B23006025',
 'B23006026',
 'B23006027',
 'B23006028',
 'B23006029',
 'geometry']


# In[17]:


# redefine edu with only columns to keep
edu = edu[columns_to_keep]


# In[18]:


# check the slimmed down gdf
edu.head()


# In[19]:


list(edu)


# In[20]:


edu.columns = ['geoid',
 'name',
 'Total',
 'Less than HS graduate',
 'HS Graduate',
 'Some College or Associates Degree',
 'Bachelors degree or Higher',
 'In Labor Force',
 'In Armed Forces',
 'Civillian',
 'Employed',
 'Unemployed',
 'Not in Labor Force',
 'geometry']


# In[21]:


edu.head()


# In[23]:


# get a random record
random_tract = edu.sample()
random_tract


# In[30]:


# example usage of iloc to get the total population of our random record
# "for the 0th record, get the value in the Total column"
random_tract.iloc[0]['Total']


# In[25]:


# print this out in plain english
print('Total population: ' + str(random_tract.iloc[0]['Total']))


# In[31]:


# Less than HS degree plus all the HS degree and higher categories
print(random_tract.iloc[0]['Less than HS graduate'] + 
      random_tract.iloc[0]['HS Graduate'] + 
      random_tract.iloc[0]['Some College or Associates Degree'] + 
      random_tract.iloc[0]['Bachelors degree or Higher']) 


# In[32]:


# access a single column like df['col_name']
edu['Total'].head()


# In[34]:


# What is the mean?
edu['Total'].mean()


# In[35]:


# What is the median?
edu['Total'].median()


# In[36]:


#  get some stats
edu['Total'].describe()


# In[37]:


# plot it as a historgram with 50 bins
edu['Total'].plot.hist(bins=50)


# In[40]:


edu_sorted = edu.sort_values(by='Total',ascending = False)


# In[41]:


# display the data, but just a few columns to keep it clean
edu_sorted[['geoid','Total']].head(10)


# In[43]:


# plot it
edu_sorted.head(10).plot()


# In[44]:


# Make it prettier
edu_sorted.head(100).plot(figsize=(10,10),column='Total',legend=True)


# In[45]:


# subset the data so that we can see the data per row... 
# in other words, this syntax is asking to "show me the values in my dataframe that match this filter
edu[edu['Total']==0]


# In[47]:


# create a new variable for census tracts with zero pop
edu_no_pop = edu[edu['Total']==0]


# In[48]:


# how many records?
print('There are ' + str(len(edu_no_pop)) + ' census tracts with no people in them')


# In[49]:


# display it
edu_no_pop[['geoid','Total']]


# In[50]:


# output columns
list(edu)


# In[52]:


# create a new column, and populate it with normalized data to get the percent of total value
edu['Percent Less than HS graduate'] = edu['Less than HS graduate']/edu['Total']*100
edu['Percent HS Graduate'] = edu['HS Graduate']/edu['Total']*100
edu['Percent Some College or Associates Degree'] = edu['Some College or Associates Degree']/edu['Total']*100
edu['Percent Bachelors degree or Higher'] = edu['Bachelors degree or Higher']/edu['Total']*100


# In[53]:


edu.sample(5)


# In[54]:


# the remaining columns
edu['Percent In Labor Force'] = edu['In Labor Force']/edu['Total']*100
edu['Percent In Armed Forces'] = edu['In Armed Forces']/edu['Total']*100
edu['Percent Civillian'] = edu['Civillian']/edu['Total']*100
edu['Percent Employed'] = edu['Employed']/edu['Total']*100
edu['Percent Unmployed'] = edu['Unemployed']/edu['Total']*100
edu['Percent Not in Labor Force'] = edu['Not in Labor Force']/edu['Total']*100


# In[55]:


edu.plot(figsize=(12,10),
                 column='Percent Less than HS graduate',
                 legend=True, 
                 scheme='NaturalBreaks')


# In[56]:


edu.plot(figsize=(12,10),
                 column='Percent Less than HS graduate',
                 legend=True, 
                 scheme='equal_interval')


# In[57]:


edu.plot(figsize=(12,10),
                 column='Percent Less than HS graduate',
                 legend=True, 
                 scheme='quantiles')


# In[58]:


edu.plot(figsize=(12,10),
                 column='Percent Some College or Associates Degree',
                 legend=True, 
                 scheme='quantiles')


# In[60]:


# create the 1x2 subplots
fig, axs = plt.subplots(1, 2, figsize=(15, 12))

# name each subplot
ax1, ax2 = axs

# percent Less than HS graduate map on the left
edu.plot(column='Percent Less than HS graduate', 
            cmap='RdYlGn_r', 
            scheme='quantiles',
            k=5, 
            edgecolor='white', 
            linewidth=0., 
            alpha=0.75, 
            ax=ax1, # this assigns the map to the subplot,
            legend=True
           )

ax1.axis("off")
ax1.set_title("Percent Less than HS graduate")

# percent Bachelors degree or higher map on the right
edu.plot(column='Percent Bachelors degree or Higher', 
            cmap='RdYlGn_r', 
            scheme='quantiles',
            k=5, 
            edgecolor='white', 
            linewidth=0., 
            alpha=0.75, 
            ax=ax2, # this assigns the map to the subplot
            legend=True
           )

ax2.axis("off")
ax2.set_title("Percent Bachelors degree or Higher")


# In[66]:


edu[edu['Percent Less than HS graduate'] >50]


# In[68]:


# reproject to Web Mercator
gdf_web_mercator = edu.to_crs(epsg=3857)


# In[71]:


# use subplots that make it easier to create multiple layered maps
fig, ax = plt.subplots(figsize=(15, 15))

# add the layer with ax=ax in the argument 
gdf_web_mercator[gdf_web_mercator['Percent Less than HS graduate'] > 50].plot(ax=ax, alpha=0.8)

# turn the axis off
ax.axis('off')

# set a title
ax.set_title('Census Tracts with more than 50% Less than High School graduate Population',fontsize=16)

# add a basemap
ctx.add_basemap(ax)


# In[ ]:




