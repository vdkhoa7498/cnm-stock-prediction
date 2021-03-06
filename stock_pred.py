# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Jim_bfOa5EIdeMXF0snQn1bpRTQCXIyW
"""

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# %matplotlib inline
from matplotlib.pylab import rcParams
rcParams['figure.figsize']=20,10

from sklearn.preprocessing import MinMaxScaler
from datetime import datetime,date,timedelta
from keras.models import Sequential
from keras.layers.wrappers import Bidirectional
from keras.layers import Dense, Lambda, dot, Activation, concatenate, Embedding, LSTM, SimpleRNN, Dropout



df=pd.read_csv("stock_data.csv")
df.head()

df = df.sort_values(by='Date')

df["Date"]=pd.to_datetime(df.Date,format="%Y-%m-%d")
df.index=df['Date']

plt.figure(figsize=(16,8))
plt.plot(df[["Close"]],label='Close Price history')

data=df.sort_index(ascending=True,axis=0)
new_dataset=pd.DataFrame(index=range(0,len(df)),columns=['Date','Close'])

for i in range(0,len(data)):
    new_dataset["Date"][i]=data['Date'][i]
    new_dataset["Close"][i]=data["Close"][i]

percent_train = 80
percent_valid = 100 - percent_train
cout_percent_train = int(len(new_dataset)/100*percent_train)

scaler=MinMaxScaler(feature_range=(0,1))
final_dataset=new_dataset.values

train_data=final_dataset[0:cout_percent_train,:]
valid_data=final_dataset[cout_percent_train:,:]

new_dataset.index=new_dataset.Date
new_dataset.drop("Date",axis=1,inplace=True)
scaler=MinMaxScaler(feature_range=(0,1))

scaled_data=scaler.fit_transform(new_dataset)

x_train_data,y_train_data=[],[]

for i in range(60,len(train_data)):
    x_train_data.append(scaled_data[i-60:i,0])
    y_train_data.append(scaled_data[i,0])
    
x_train_data,y_train_data=np.array(x_train_data),np.array(y_train_data)

x_train_data=np.reshape(x_train_data,(x_train_data.shape[0],x_train_data.shape[1],1))


rnn_model=Sequential()
rnn_model.add(SimpleRNN(units=50,return_sequences=True,input_shape=(x_train_data.shape[1],1)))
rnn_model.add(SimpleRNN(units=50))
rnn_model.add(Dense(1))

rnn_model.compile(loss='mean_squared_error',optimizer='adam', metrics=['acc'])
rnn_model.summary()

rnn_model.fit(x_train_data,y_train_data,epochs=2,batch_size=1,verbose=2)

rnn_model.save("model_RNN.h5")



lstm_model=Sequential()
lstm_model.add(LSTM(units=50,return_sequences=True,input_shape=(x_train_data.shape[1],1)))
lstm_model.add(LSTM(units=50))
lstm_model.add(Dense(1))

lstm_model.compile(loss='mean_squared_error',optimizer='adam', metrics=['acc'])
lstm_model.summary()

lstm_model.fit(x_train_data,y_train_data,epochs=2,batch_size=10,verbose=2)

lstm_model.save("model_LSTM.h5")

inputs_data=new_dataset[len(new_dataset)-len(valid_data)-60:].values
inputs_data=inputs_data.reshape(-1,1)
inputs_data=scaler.transform(inputs_data)

train_data=new_dataset[:cout_percent_train]
valid_data=new_dataset[cout_percent_train:]
valid_data_=new_dataset[cout_percent_train:]

valid_data['Predictions']=predicted_closing_price
valid_data_['Predictions']=predicted_closing_price_
plt.plot(train_data["Close"])
plt.plot(valid_data[['Close',"Predictions"]])
plt.plot(valid_data_[['Close',"Predictions"]])

plt.plot(valid_data_[['Close',"Predictions"]]) #RNN

plt.plot(valid_data[['Close',"Predictions"]]) #LSTM