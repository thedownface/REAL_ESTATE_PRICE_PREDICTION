from django.db import models
import pickle
from sklearn.preprocessing import LabelEncoder

# Load the pre-trained machine learning model
with open('C:/Users/iamfa/OneDrive/Desktop/projects/SCRAP E COMM WEBSITE/model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define a function to make predictions based on user input
def predict_price(location, area, bedrooms, new_resale, gymnasium, lift_available, car_parking, maintenance, security, children_park, clubhouse, intercom, gardens, indoor_games, gas_connection, jogging_track, swimming_pool):
    # Convert input values to appropriate data types
    location = str(location)
    le = LabelEncoder()
    location= le.fit_transform(location)
    area = float(area)
    bedrooms = int(bedrooms)
    new_resale = int(new_resale)
    gymnasium = int(gymnasium)
    lift_available = int(lift_available)
    car_parking = int(car_parking)
    maintenance = float(maintenance)
    security = int(security)
    children_park = int(children_park)
    clubhouse = int(clubhouse)
    intercom = int(intercom)
    gardens = int(gardens)
    indoor_games = int(indoor_games)
    gas_connection = int(gas_connection)
    jogging_track = int(jogging_track)
    swimming_pool = int(swimming_pool)
    
    input_data = [[location, area, bedrooms, new_resale, gymnasium, lift_available, car_parking, maintenance, security, children_park, clubhouse, intercom, gardens, indoor_games, gas_connection, jogging_track, swimming_pool]]
    prediction = model.predict(input_data)
    return prediction[0]