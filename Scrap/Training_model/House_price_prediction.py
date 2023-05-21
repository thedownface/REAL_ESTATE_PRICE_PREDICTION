import pickle as pkl
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import numpy as np
from sklearn.ensemble import RandomForestRegressor
import pandas as pd
from sklearn.metrics import r2_score, mean_squared_error
rfc = RandomForestRegressor()

data = pd.read_csv('C:/Users/iamfa/OneDrive/Desktop/projects/SCRAP E COMM WEBSITE/Scrap/Training_model/Bangalore_data.csv')

le = LabelEncoder()
data['Location'] = le.fit_transform(data['Location'])
data['Price'] = np.log(data['Price'])

x = data.drop(['id','Price'],axis=1)
y = data['Price']

q1 = x['Area'].quantile(0.25)
q3 = x['Area'].quantile(0.75)

iqr = q3-q1

u = q3 + 1.5*iqr
l = q1 - 1.5*iqr

out1 = x[x['Area'] < l].values
out2 = x[x['Area'] > u].values

x['Area'].replace(out1,l,inplace = True)
x['Area'].replace(out2,u,inplace = True)

# Price
q1 = y.quantile(0.25)
q3 = y.quantile(0.75)

iqr = q3-q1

u = q3 + 1.5*iqr
l = q1 - 1.5*iqr

out1 = y[y < l].values
out2 = y[y > u].values

y.replace(out1,l,inplace = True)
y.replace(out2,u,inplace = True)


x_train, x_test, y_train, y_test=train_test_split(x, y, random_state=0, train_size=0.3)

rfc.fit(x_train,y_train)
y_pred = rfc.predict(x_test)

print(r2_score(y_test,y_pred))

pkl.dump(rfc, open('model.pkl','wb'))