# In[4]:


gdp = pd.read_excel('gdplev.xls',index_col=4, skiprows=219)
del gdp['Unnamed: 0']
del gdp['Unnamed: 1']
del gdp['Unnamed: 2']
del gdp['Unnamed: 3']
del gdp['Unnamed: 7']
gdp = gdp.reset_index()
gdp = gdp.T
gdp = gdp.reset_index()
gdp = gdp.T
del gdp[1]
gdp = gdp.T
del gdp['index']
gdp = gdp.T
for col in gdp.columns:
    if(col==0):
        gdp.rename(columns={col:'Quarter'},inplace=True)
    if(col==2):
        gdp.rename(columns={col:'GDP'},inplace=True)
gdp['GDP'] = np.float64(gdp['GDP'])

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    a = 'abc'
    for i in range(2,len(gdp)):
        if(gdp['GDP'][i]<gdp['GDP'][i-1] and gdp['GDP'][i-1]<gdp['GDP'][i-2]):
            a = gdp['Quarter'][i-1]
            break
    return a
get_recession_start()


# In[5]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    a = []
    for i in range(37,len(gdp)):
        if(gdp['GDP'][i]>gdp['GDP'][i-1] and gdp['GDP'][i-1]>gdp['GDP'][i-2]):
            a = gdp['Quarter'][i]
            break
    return a
get_recession_end()


# In[41]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    a = []
    m = gdp['GDP'][35]
    for i in range(35,40):
        if(m>gdp['GDP'][i]):
            m = gdp['GDP'][i]
            a = gdp['Quarter'][i]
    return a
get_recession_bottom()

