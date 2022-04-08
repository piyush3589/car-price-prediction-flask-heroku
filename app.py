from flask import Flask, render_template, request
import requests
import pickle
import numpy as np
import xgboost as xgb

import sklearn
app = Flask(__name__)
#model = joblib.load(open('Final_RF_Model_train_data.pkl', 'rb'))
#pickle_in = open("Final_XGB_Model.pkl","rb")
#model=pickle.load(pickle_in)
model1 = xgb.XGBRegressor()
model1.load_model("final_xg_model.txt")

@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        Year = float(request.form['Year'])
        KMD=float(request.form['Kms_Driven'])
        FuelType=request.form['FuelType']
        Mileage = float(request.form["Mileage"])
        Transmission=request.form['Transmission']
        SellerType =request.form["SellerType"]
        Engine=float(request.form["Engine"])
        Seats=float(request.form['Seats'])
        
        if FuelType == "Diesel":
            FuelType = 0
        elif FuelType == "Petrol":
            FuelType = 1
        elif FuelType == "CNG":  
            FuelType = 2
        elif FuelType == "lPG":  
            FuelType = 3
        elif FuelType == "Electric":  
            FuelType = 4
        
        if Transmission == "Manual":
            Transmission = 0
        elif Transmission == "Automatic":
            Transmission = 1
       
        if SellerType == "Dealer":
            SellerType = 0
        elif SellerType == "Individual":
            SellerType = 1
        elif SellerType == "Trustmark Dealer":  
            SellerType = 2
        prediction=model1.predict([[Year,KMD,FuelType,Mileage,Transmission,SellerType,Engine,Seats]])
        output=round(prediction[0],4)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this car")
        else:
            return render_template('index.html',prediction_text="You Can Sell The Car at {} lakhs".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)
    #app.run(host="0.0.0.0",port="8080")