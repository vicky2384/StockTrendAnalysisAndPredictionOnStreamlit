import streamlit as st
import numpy as np 
import pandas as pd
import pandas_datareader as data
import matplotlib.pyplot as plt 
from keras.models import load_model



start = '2010-01-01'
end = '2022-10-07'

st.title('STOCK TREND PREDICTION')

user_input = st.text_input('enter stock ticket' , 'AAPL')
df = data.DataReader(user_input ,'yahoo' , start ,end)


st.subheader('Data from 2010-2022')
st.write(df.describe())
#visvualization

st.subheader('closing price vs time chart with 100MA')
ma100 = df.Close.rolling(100).mean()
fig=plt.figure(figsize=(8,6))
plt.plot(ma100)
plt.plot(df.Close)
st.pyplot(fig)
 

st.subheader('closing price vs time chart with 100MA & 200MA')
ma100=df.Close.rolling(100).mean()
ma200=df.Close.rolling(200).mean()
fig=plt.figure(figsize=(8,6))
plt.plot(ma100)
plt.plot(ma200)
plt.plot(df.Close)
st.pyplot(fig)

#splitting data into training and testing

data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)]) 
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))

data_training_array = scaler.fit_transform(data_training)
#Model 

#load my model
model = load_model('keras_model.h5')

#testing part
past_100_days = data_training.tail(100)
final_df = past_100_days.append(data_testing,ignore_index=True)
input_data = scaler.fit_transform(final_df)

x_test =[]
y_test = []
 
for i in range(100, input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i,0])

x_test, y_test = np.array(x_test), np.array(y_test)    
y_predicted = model.predict(x_test)
scaler = scaler.scale_

scale_factor = 1/scaler[0]
y_predicted = y_predicted * scale_factor
y_test = y_test * scale_factor

#final Graph
st.subheader('Prediction Vs Original')
fig2 = plt.figure(figsize=(8,6))
plt.plot(y_test) 
plt.plot(y_predicted)
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot(fig2)
