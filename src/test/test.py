#!/usr/bin/env python3

#Diabetes Prediction Using Support Vector Machine
import pickle
import os
import sys
import pandas as pd
import time
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
sys.path.append("./")
import parameters as params


#Test accuracy of the model
def test():

    file='./data/'+params.source_file
    dataset = pd.read_csv(file)
    X = dataset[['F','D','E','B','C']]
    Y = dataset[['I']]

    with open(params.model_name+'.pkl','rb') as mod:
        p=pickle.load(mod)

    pre=p.predict(X)
    accur=accuracy_score(Y,pre)
    print("LA PRECISION CON LOS DATOS DE TEST ES DE:")
    print (accur) #Prints the accuracy of the model
    file = open(".accuracy.txt","w")
    file.write(str(accur))
    file.close()

if __name__=='__main__':
    test()
