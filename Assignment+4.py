
# In[1]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# In[2]:


# This dictionary is used to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[3]:


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning is be done:

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




