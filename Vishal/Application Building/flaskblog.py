from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from tensorflow import keras
import joblib
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pandas as pd

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


posts = []

#link model here and make prediction
def getPrediction(prices):
    look_back=10
    sc = MinMaxScaler(feature_range=(0,1))
    regressor = keras.models.load_model('regressor.h5') 
    user_data=pd.DataFrame(prices,columns=['Prices'])
    sc_lst=sc.fit_transform(np.float64(user_data))
    sc_lst=np.array(sc_lst)
    sc_new=[]
    for i in range(len(sc_lst)-look_back+1):
        a=sc_lst[i:(i+look_back)]
        sc_new.append(a)
    X_pred_values=np.array(sc_new)
    X_pred_values=np.reshape(X_pred_values,(X_pred_values.shape[0], 10, 1))
    Y_pred_values=regressor.predict(X_pred_values)
    Y_pred_values=sc.inverse_transform(Y_pred_values)
    return Y_pred_values[0][0]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/predict", methods=['POST'])
def predict():
    data = request.get_json()
    prices =[float(i) for i in data["prices"]]
    print(prices)
    print(getPrediction(prices))
    return str(getPrediction(prices))

if __name__ == '__main__':
    app.run(debug=True)