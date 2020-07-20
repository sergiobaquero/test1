from flask import *
import json
import os
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import pickle

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/predict',methods=["post"])
def predict():
    formvalues = request.form
    path1 = "/static/json/"
    with open(os.path.join(os.getcwd()+"/"+path1,'file.json'), 'w') as f:
        json.dump(formvalues, f)
    with open(os.path.join(os.getcwd()+"/"+path1,'file.json'), 'r') as f:
        values = json.load(f)

    df = pd.DataFrame(json_normalize(values))
    my_dict = {"B": float(df['glucose']), "C":float(df['bp']),"D":float(df['trc']), "E":float(df['insulin']), "F": float(df['bmi'])}

    model_path=os.getcwd()+"/static/model/diabetes.pkl"

    df=pd.DataFrame(data=my_dict,index=[0])

    with open(model_path,'rb') as model:
        p=pickle.load(model)
    op=p.predict(df)

    if op[0]==0:
        msg="Unsuccess"
    else:
        msg="Success"

    return render_template("index.html",msg=msg,**request.args)


if __name__ == '__main__':
    app.run()
