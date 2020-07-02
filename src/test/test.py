#!/usr/bin/env python3

#Diabetes Prediction Using Support Vector Machine
import pickle
import os
import sys
import pandas as pd
import time
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
sys.path.append("./")
import parameters as params


#Test accuracy of the model
def test():

    file='./data/'+params.source_file
    dataset = pd.read_csv(file)
    X = dataset[['F','D','E','B','C']]
    Y = dataset[['I']]

    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = params.test_size, random_state = params.random_state)

    with open(params.model_name+'.pkl','rb') as mod:
        p=pickle.load(mod)

    pre=p.predict(X_test)
    accur=accuracy_score(Y-test,pre)
    print("LA PRECISION CON LOS DATOS DE TEST ES DE:")
    print (accur) #Prints the accuracy of the model
    file = open(".accuracy.txt","w")
    file.write(str(accur))
    file.close()

    print(confusion_matrix(y_test,y_pred))
    print(classification_report(y_test,y_pred))


if __name__=='__main__':
    test()
