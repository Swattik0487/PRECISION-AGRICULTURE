from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import psycopg2
import numpy as np
import csv 
import os
import pandas as pd
import requests
from datetime import datetime

app = Flask(__name__)
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
CSV_FILE = "data.csv"

CORS(app) 

DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "postgres",
    "host": "localhost",
    "port": "5432"
}

def get_data_from_db(latitude, longitude):
    """Fetch relevant data for given coordinates from PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        query = """
            SELECT Sigma0_VV, Sigma0_VH, Soil_moisture, vh_veg, Realpart_Dielectric, CC
            FROM data
            ORDER BY (latitude::double precision - %s)^2 + (longitude::double precision - %s)^2
            LIMIT 1;
        """
        cursor.execute(query, (latitude, longitude))
        data = cursor.fetchone()
        
        conn.close()
        return data if data else None

    except Exception as e:
        print("Database error:", e)
        return None

def predict_cpi(features):
    """Perform regression-based prediction for Crop Productivity Index (CPI)"""
    # Sample weights (these can be optimized based on dataset)
    weights = np.array([0.2, 0.15, 0.25, 0.1, 0.2, 0.1])
    
    # Compute weighted average as a simple regression model
    cpi = np.dot(features, weights)
    return round(cpi, 2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Receive coordinates from frontend, fetch data, and return CPI prediction"""
    try:
        data = request.get_json()
        print(data)
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))

        # Fetch data from DB
        record = get_data_from_db(latitude, longitude)
        if not record:
            return jsonify({"error": "No data found for the given location"}), 404

        # Predict Crop Productivity Index
        cpi = predict_cpi(np.array(record))
        file_exists = os.path.isfile(CSV_FILE)
    
        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Latitude", "Longitude", "CPI"])  
            
            writer.writerow([latitude, longitude, cpi])
                
        return jsonify({"crop_productivity_index": cpi})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



API_KEY = "e532bcac8a0708f76d1b7538384690f4"  
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
AQI_URL = "https://api.openweathermap.org/data/2.5/air_pollution"
@app.route("/get_weather", methods=["GET"])
def get_weather():
    city = request.args.get("city", "Kanniyakumari") 

 
    weather_params = {"q": city, "appid": API_KEY, "units": "metric"}
    weather_response = requests.get(WEATHER_URL, params=weather_params)
    
    if weather_response.status_code != 200:
        return jsonify({"error": "Weather data not found"}), 400

    weather_data = weather_response.json()
    lat, lon = weather_data["coord"]["lat"], weather_data["coord"]["lon"]

    # Get AQI Data
    aqi_params = {"lat": lat, "lon": lon, "appid": API_KEY}
    aqi_response = requests.get(AQI_URL, params=aqi_params)
    
    if aqi_response.status_code != 200:
        aqi_value = "N/A"
    else:
        aqi_data = aqi_response.json()
        aqi_value = aqi_data["list"][0]["main"]["aqi"]  

    # Format Data
    weather_info = {
        "temperature": weather_data["main"]["temp"],
        "pressure": weather_data["main"]["pressure"],
        "humidity": weather_data["main"]["humidity"],
        "aqi": aqi_value,
        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "city": weather_data["name"]
    }
    return jsonify(weather_info)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
