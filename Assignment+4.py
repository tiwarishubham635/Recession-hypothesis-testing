
# In[1]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# In[2]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[3]:


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    towns = pd.read_fwf('university_towns.txt')
    b=[]
    a=[]
    towns=towns.T
    towns = towns.reset_index()
    towns = towns.T
    towns = towns.reset_index()
    del towns['index']
    for j in range(567):
        for k in range(len(towns[0][j])):
            if(towns[0][j][k]=='['):
                towns[0][j] = towns[0][j][:k+1]
                break
            if(towns[0][j][k]=='('):
                towns[0][j] = towns[0][j][:k]
                break
    for j in range(567):
        if(towns[0][j][-1]=='['):
                b.append({'State':towns[0][j][:-1], 'RegionName':[]})
        if(towns[0][j][-1]!='['):
                b[len(b)-1]['RegionName'].append(towns[0][j])
    for i in range(50):
        for j in b[i]['RegionName']:
            a.append({'State':b[i]['State'], 'RegionName':j})
    towndf = pd.DataFrame(a)
    towndf = towndf[['State','RegionName']]
    for i in range(len(towndf)):
        if(towndf.iloc[i]['RegionName'][-1]==' '):
            towndf.set_value(i,'RegionName',towndf.iloc[i]['RegionName'][:-1])
    return towndf
get_list_of_university_towns()


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


# In[6]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    hd = pd.read_csv('City_Zhvi_AllHomes.csv')
    hd=hd.set_index(['State','RegionName'])
    coln=0
    for col in hd.columns:
        if(coln<49):
            del hd[col]
        coln=coln+1
    hd = (hd.groupby(pd.PeriodIndex(hd.columns,freq='Q'),axis=1).mean().rename(columns=lambda c: str(c).lower()))
    hd=hd.reset_index()
    for i in range(len(hd)):
        if hd.iloc[i]['State'] in states.keys():
            hd.set_value(i,'State',states[hd.iloc[i]['State']])
    hd=hd.set_index(['State','RegionName'])
    return hd#.loc["Texas"].loc["Austin"].loc["2010q3"])
convert_housing_data_to_quarters()


# In[9]:


from scipy import stats
def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    data = convert_housing_data_to_quarters()
    for col in data.columns:
        if(col!='2008q3' and col!= '2009q2'):
            del data[col]
    utown = get_list_of_university_towns()
    #utown=utown.set_index(['State','RegionName'])
    ntown = data.reset_index()
    #df=df.set_index('State')
    #ntown=ntown.sort_index()
    r={}
    for i in range(len(utown)):
        r.update({utown.iloc[i]['State']:[]})
    for i in range(len(utown)):
        r[utown.iloc[i]['State']].append(utown.iloc[i]['RegionName'])
    x=[]
    for i in range(len(ntown)):
        if ntown.iloc[i]['State'] in r.keys():
            if ntown.iloc[i]['RegionName'] in r[ntown.iloc[i]['State']]:
                x.append(i)
                #ntown = ntown.drop(i)
    for i in x:
        ntown = ntown.drop(i)
    utown = utown.set_index(['State','RegionName'])
    #utown=utown.sort_index()
    ut = pd.merge(utown,data,how='inner',left_index=True,right_index=True)
    ut = ut.sort_index()
    nt = ntown.set_index(['State','RegionName'])
    nt = nt.sort_index()
    ut['ratio']=ut['2008q3']/ut['2009q2']
    nt['ratio']=nt['2008q3']/nt['2009q2']
    ut = ut.dropna()
    nt = nt.dropna()
    p = stats.ttest_ind(ut['ratio'],nt['ratio']).pvalue
    return (True,p,"university town")
run_ttest()


# In[ ]:




