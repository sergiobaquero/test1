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

#For training
def train():
    file='./data/'+params.source_file
    dataset = pd.read_csv(file)
    X = dataset[['F','D','E','B','C']]
    Y = dataset[['I']]
    
    #train test split
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size = params.test_size, random_state = params.random_state)
    
    from sklearn.svm import SVC
    model = SVC(kernel='linear')
    svc=model.fit(X_train,Y_train)
    
    #Save Model As Pickle File
    with open(params.model_name+'.pkl','wb') as m:
        pickle.dump(svc,m)
    test(X_test,Y_test)

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
    print("LA PRECISION CON LOS DATOS DE TESTTTTTTTTTT ES DE:")
    print (accur) #Prints the accuracy of the model
    file = open(".accuracy.txt","w") 
    file.write(str(accur)) 
    file.close() 


def find_data_file(filename):
    if getattr(sys, "frozen", False):
        # The application is frozen.
        datadir = os.path.dirname(sys.executable)
    else:
        # The application is not frozen.
        datadir = os.path.dirname(__file__)

    return os.path.join(datadir, filename)


def check_input(data) ->int :
    df=pd.DataFrame(data=data,index=[0])
    with open(find_data_file(params.model_name+'.pkl'),'rb') as model:
        p=pickle.load(model)
    op=p.predict(df)
    return op[0]
if __name__=='__main__':
    test()    
