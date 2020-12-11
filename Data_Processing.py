import numpy as np
import pandas as pd
import os


#datasets = ['2019_01.csv', '2019_02.csv', '2019_03.csv', '2019_04.csv', '2019_05.csv', '2019_06.csv',
#            '2019_07.csv', '2019_08.csv', '2019_09.csv', '2019_10.csv', '2019_11.csv', '2019_12.csv']

#datasets = ['2018_11.csv', '2018_12.csv']
#datasets = ['2020_01.csv', '2020_02.csv'] 

#datasets = ['2020_03.csv', '2020_04.csv']
datasets = ['2020_05.csv']

for data in datasets:
    df = pd.read_csv(data, parse_dates=['Trip Start Timestamp'], usecols =['Trip Start Timestamp', 'Pickup Community Area'])
    time_feature_df =df.copy()
    time_feature_df['month'] = time_feature_df['Trip Start Timestamp'].dt.month
    time_feature_df['day'] = time_feature_df['Trip Start Timestamp'].dt.day
    time_feature_df['hour'] = time_feature_df['Trip Start Timestamp'].dt.hour
    time_feature_df['dayofweek'] = time_feature_df['Trip Start Timestamp'].dt.dayofweek
    time_feature_df = time_feature_df.drop('Trip Start Timestamp', axis = 1)
    hdr = False  if os.path.isfile('test_data_2020_05_dayofweek.csv') else True
    time_feature_df.to_csv('test_data_2020_05_dayofweek.csv', mode = 'a', header=hdr)




