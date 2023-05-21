import pickle as pkl
from django.shortcuts import render
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

rfc = pkl.load(open('C:/Users/iamfa/OneDrive/Desktop/projects/SCRAP E COMM WEBSITE/model.pkl', 'rb'))

def predict(request):
    if request.method == 'POST':
        data = pd.read_csv('C:/Users/iamfa/OneDrive/Desktop/projects\SCRAP E COMM WEBSITE/Scrap/Training_model/Bangalore_data.csv')
        le = LabelEncoder()
        data['Location'] = le.fit_transform(data['Location'])
        x = data.drop(['id','Price'],axis=1)
        q1 = x['Area'].quantile(0.25)
        q3 = x['Area'].quantile(0.75)
        iqr = q3-q1
        u = q3 + 1.5*iqr
        l = q1 - 1.5*iqr
        out1 = x[x['Area'] < l].values
        out2 = x[x['Area'] > u].values
        x['Area'].replace(out1,l,inplace = True)
        x['Area'].replace(out2,u,inplace = True)
        location = le.transform([request.POST.get('location')])[0]
        area = float(request.POST.get('area'))
        bedrooms = int(request.POST.get('bedrooms'))
        new = 1 if request.POST.get('new') == 'on' else 0
        gym = 1 if request.POST.get('gym') == 'on' else 0
        lift = 1 if request.POST.get('lift') == 'on' else 0
        car = 1 if request.POST.get('car') == 'on' else 0
        maintainance = 1 if request.POST.get('maintainance') == 'on' else 0
        security= 1 if request.POST.get('security') == 'on' else 0
        children = 1 if request.POST.get('children') == 'on' else 0
        club = 1 if request.POST.get('club') == 'on' else 0
        intercom = 1 if request.POST.get('intercom') == 'on' else 0
        landscape= 1 if request.POST.get('landscape') == 'on' else 0
        indoor = 1 if request.POST.get('indoor') == 'on' else 0
        gas= 1 if request.POST.get('gas') == 'on' else 0
        jogging = 1 if request.POST.get('jogging') == 'on' else 0
        swimming = 1 if request.POST.get('swimming') == 'on' else 0
        input = pd.DataFrame([[area, location, bedrooms, new, gym,lift, car,maintainance,security ,children,club,intercom,landscape,indoor,gas,jogging,swimming]], columns=['Area','Location','No. of Bedrooms','New/Resale','Gymnasium','Lift Available','Car Parking','Maintenance Staff','24x7 Security',"Children's Play Area",'Clubhouse','Intercom','Landscaped Gardens','Indoor Games','Gas Connection','Jogging Track','Swimming Pool'])
        pred = rfc.predict(input)[0]*1e6
        print(pred)
        return render(request, 'model/result.html', {'prediction': pred})
    return render(request, 'model/predict.html')
