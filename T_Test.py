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
