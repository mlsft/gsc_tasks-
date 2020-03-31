# -*- coding: utf-8 -*-
"""Keras_inference.ipynb"""

#!pip install keras==2.1.5 --no-deps

import numpy as np
import pandas as pd
import h5py
#import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
#from keras.utils import np_utils
from keras.models import load_model,model_from_json
#from sklearn.model_selection import train_test_split
from keras import optimizers
from numpy import savetxt
from sklearn.utils import shuffle
print("Importing completed.")

#Enter the batch size you want to evaluate on
batch_size=input("Enter the batch size(max 1000): ")

batch_start_idx=0
batch_end_idx=int(batch_size)

filename='SingleElectronPt50_IMGCROPS_n249k_RHv1_inference.hdf5'
data1 = h5py.File(filename, 'r')
Y1=data1['y']
X1=data1['X']

filename='SinglePhotonPt50_IMGCROPS_n249k_RHv1_inference.hdf5'
data0 = h5py.File(filename, 'r')
Y0=data0['y']
X0=data0['X']
print("Data loading completed.")

X_final=np.concatenate((X0[:],X1[:]),axis=0)
Y_final=np.concatenate((Y0[:],Y1[:]),axis=0)

X_final=(X_final[:,:,:,0].reshape((X_final.shape[0],X_final.shape[1],X_final.shape[2],1)))

X_final, Y_final = shuffle(X_final, Y_final)

data1.close()
data0.close()
print("Data preparation completed.")

#model1=load_model('model1.hdf5')

#model1.save('model1.hdf5')

# load json and create model
json_file = open('model1.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model1 = model_from_json(loaded_model_json)
# load weights into new model
model1.load_weights("model1.hdf5")
print("Loaded model from disk")

adam=optimizers.adam(lr=0.001)
model1.compile(loss = 'binary_crossentropy', optimizer=adam,metrics = [ 'accuracy','mae','mse'])
print("Model compiled successfully")

target=model1.predict(X_final[batch_start_idx:batch_end_idx])
target[target<0.5]=0
target[target>0.5]=1
true_values=Y_final[batch_start_idx:batch_end_idx]
target=target.reshape(true_values.shape)

metrics=model1.evaluate(X_final[batch_start_idx:batch_end_idx,:,:,:],true_values.reshape((true_values.shape[0],1)),verbose=1)
print(model1.metrics_names[0]+": "+str(metrics[0])+"\n"+model1.metrics_names[1]+": "+str(metrics[1])+"\n"+model1.metrics_names[2]+": "+str(metrics[2])+"\n"+str(model1.metrics_names[3])+": "+str(metrics[3]))

savetxt('output.csv',target,delimiter=',')
savetxt('ground_truth.csv',true_values,delimiter=',')

print("The outputs have been saved in file named output.csv corresponding to the respective indices. The first 20 values of output are:\n"+str(target[:20]))

print("The first 20 values of true values are:\n"+str(true_values[:20]))

