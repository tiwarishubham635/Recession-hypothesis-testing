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
