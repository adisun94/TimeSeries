import unittest
import pandas as pd
import numpy as np
import os
import warnings
with warnings.catch_warnings():
    warnings.simplefilter(action='ignore', category=FutureWarning)

def TS_imputation(selected_pollutant,selected_state):

    def time_window(poll,stat):

        years=os.listdir(f'c:\\Users\\adity\\Documents\\TimeSeries/DataAQ/{selected_pollutant}-{selected_state}')
        years=[int(y.split('-')[-1]) for y in years]
        years.sort()

        return years
    
    def collect_format_data(y,poll,stat):

        d=pd.DataFrame({})
        for i in y:
            if len(d)==0:
                d=pd.read_csv(f'c:\\Users\\adity\\Documents\\TimeSeries/DataAQ/{selected_pollutant}-{selected_state}/{selected_pollutant}-{selected_state}-{i}')
            else:
                d=pd.concat([d,pd.read_csv(f'c:\\Users\\adity\\Documents\\TimeSeries/DataAQ/{selected_pollutant}-{selected_state}/{selected_pollutant}-{selected_state}-{i}')],axis=0)

        d['Date']=pd.to_datetime(d['Date'])

        return d

    def select_site(d):

        site_name=d['Site Name'].value_counts().index[0]
        site_count=d['Site Name'].value_counts()[0]

        d=d[d['Site Name']==site_name]

        return d

    def drop_unique_groupby(d):

        d=d.loc[:,d.nunique()>1]
        d=d.reset_index(drop=True)

        d=d.groupby([d['Date']]).mean()

        return d

    def interpolate_AQI(d):

        d=d[['DAILY_AQI_VALUE']]

        idx = pd.date_range(min(d.index),max(d.index))
        d=d.reindex(idx,fill_value=np.nan)
        d['DAILY_AQI_VALUE']= d['DAILY_AQI_VALUE'].interpolate(option='spline')

        return d

    years=time_window(selected_pollutant,selected_state)
    d=collect_format_data(years,selected_pollutant,selected_state)
    d=select_site(d)
    d=drop_unique_groupby(d)
    d=interpolate_AQI(d)

    return d

class TestAQIimputation(unittest.TestCase):
    
    def test_interpolate_AQI(self):
        
        actual = TS_imputation('CO','Florida')
        expected = np.loadtxt('CO_Florida.txt')
    
        self.assertCountEqual(np.array(actual), np.array(expected))