import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
import geopandas as gpd

plt.rcParams.update({'figure.max_open_warning': 0})
st.set_option('deprecation.showPyplotGlobalUse', False)

st.title("Chicago Rideshare App Demand Prediction Per Day")
st.write("Created by HoJoon Kim (cescud@umich.edu)")
st.write("and Daiwei Zhang (daiweizh@umich.edu)")

# set the filepath and load
fp = 'geo_export_932ddab5-73ca-4da9-88b4-a10b650fc3bf.shp'
#reading the file stored in variable fp
map_df = gpd.read_file(fp)

sample = map_df.drop(['area', 'area_num_1', 'comarea', 'comarea_id'], axis = 1)
sample2 = map_df[['area_numbe','community']]
sample['area_numbe'] = sample['area_numbe'].astype('float64')
sample2['area_numbe'] = sample2['area_numbe'].astype('float64')

df = pd.DataFrame([1,2,3,4,5,6,7,8,9,10,11,12],columns=['Month'])
df2 = pd.DataFrame([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31],columns=['Day'])
df3 = pd.DataFrame([i for i in range(1,77)],columns=['Community'])
df4 = pd.DataFrame(['Monday', 
                                                    'Tuesday', 'Wednesday', 'Thursday',
                                                    'Friday', 'Saturday', 'Sunday'], columns=['DayOfWeek'])
df5 = pd.DataFrame([True,False], columns=['Covid'])
st.write("Make the following selection to see the ride predictions for the day")
option = st.selectbox(
    'Please select a month',
     df['Month'])

'You selected: ', option


option2 = st.selectbox(
    'Please select day of the month',
     df2['Day'])

'You selected: ', option2



option4 = st.selectbox(
    'Please select day of the week',
     df4['DayOfWeek'])

'You selected: ', option4

option5 = st.selectbox(
    'Are COVID Restrictions in place?',
     df5['Covid'])

'You selected: ', option5

def inference(X, scaler, model, feat_cols):
    
    features = pd.DataFrame(X, columns = feat_cols)
    features_scaled = scaler.transform(features)
    result = model.predict(features_scaled)
    features['Frequency'] = result
    return features

hour_to_filter = st.sidebar.slider('Hour of Day', 0, 24)  # min: 0, max: 24

# Month, Day, DayofWeek

def convert_dayofweek(dayofweek):
    if dayofweek == 'Monday':
        dayofweek_converted = 0
    elif dayofweek == 'Tuesday':
        dayofweek_converted = 1
    elif dayofweek == 'Wednesday':
        dayofweek_converted = 2
    elif dayofweek == 'Thursday':
        dayofweek_converted = 3
    elif dayofweek == 'Friday':
        dayofweek_converted = 4
    elif dayofweek == 'Saturday':
        dayofweek_converted = 5
    elif dayofweek == 'Sunday':
        dayofweek_converted = 6
    return dayofweek_converted

option4 = convert_dayofweek(option4)

row = [option,option2,option4]    


new_list2 = []
for hour in range(24):
    for i in range(77):
        tem = []
        tem.append(i)
        tem += row
        tem.insert(3,hour)
        new_list2.append(tem)

feat_cols = ['Pickup Community Area','month','day','hour','dayofweek']

if option5:
    flie_name='covid_model.sav'
    scaler = pickle.load(open('covid_scaler.sav','rb'))
    model = pickle.load(open(flie_name,'rb'))
    result = inference(new_list2,scaler, model, feat_cols)
else:
    flie_name='normal_model.sav'
    scaler = pickle.load(open('normal_scaler.sav','rb'))                     
    model = pickle.load(open(flie_name,'rb'))
    result = inference(new_list2,scaler, model, feat_cols)

data_list = []
for i in range(24):
    data_list.append(result[result['hour']==i][['Pickup Community Area','Frequency']])

new_l = []

for i in data_list:
    e = i.rename({'Pickup Community Area':'area_numbe', 'Frequency':'Counts of Rides'}, axis = 1)
    new_l.append(e)

data_list = new_l

new_l_2 = []
new_l_3 = []
for i in data_list:

    new_l_2.append(pd.merge(sample, i, on = 'area_numbe', how = 'outer')) 
    i['Counts of Rides'] = i['Counts of Rides'].apply(lambda x:np.array(10 ** x))
    new_l_3.append(pd.merge(sample2, i, on = 'area_numbe', how = 'outer')) 




if hour_to_filter<=23:
    st.text('Hour '+str(hour_to_filter+1)+ ' Ride Predicions')
    st.dataframe(new_l_3[hour_to_filter])
    fig = plt.figure(figsize=(4, 4))

    new_l_2[hour_to_filter].plot(column='Counts of Rides', cmap='BuGn', linewidth=0.8, edgecolor='0.8')
    plt.title('Hour '+str(hour_to_filter+1)+ ' Frequency')

    st.pyplot()    
else:
   st.header('You unlocked: Display All')    
   for i in range(24):
    st.write('Hour '+str(i+1)+ ' Ride Predicions')
    st.dataframe(new_l_3[i])
    fig = plt.figure(figsize=(4, 4))

    new_l_2[i].plot(column='Counts of Rides', cmap='BuGn', linewidth=0.8, edgecolor='0.8')
    plt.title('Hour '+str(i+1)+ ' Frequency')

    st.pyplot()  

