import re
from tkinter import NO
from urllib import response
from flask import Flask, jsonify, render_template, request, redirect
from httpx import get
from regex import E
import requests, PIL.Image, io

from os import getenv
from dotenv import load_dotenv
load_dotenv()
key = getenv('API_KEY')

app = Flask(__name__)

degree = True
last_location = 'toronto'

def getWeather(location: str):
    global degree, key
    query = f'http://api.weatherapi.com/v1/current.json?key={key}&q={location}&aqi=no'
    response = requests.get(query).json()

    if response.get('error'):
        raise Exception(response['error'].get('message', 'Unknown error'))

    temp_c = response['current']['temp_c']
    temp_f = response['current']['temp_f']
    region = response['location']['region']
    city = response['location']['name']

    return {'temp_c':f'{temp_c} °C', 'temp_f':f'{temp_f} °F'}, region, city


def getImage(icon: str):
        icon = icon
        iconSplit = icon.split('/')
        iconSplit[-3] = '128x128'
        icon = '/'.join(iconSplit)
        imgQuery:str = f'https:{icon}'

        img_data = requests.get(imgQuery).content
        image = PIL.Image.open(io.BytesIO(img_data))
        image.save('static/img/weather.png')

content, region, city = getWeather('Toronto')

@app.route('/', methods=["GET"])
def index():
    global content, region, city
    if degree:
        return render_template('index.html', content=content['temp_c'], city=city, region=region)
    else:
        return render_template('index.html', content=content['temp_f'], city=city, region=region)
# FIX THIS PLEASE I BEG OF YOU
@app.route('/toggle-unit', methods=["POST"])
def toggle_unit():
    global degree, content
    try:
        if request is None:
            raise Exception
        if request.is_json:
            data = request.json
            state = data.get('state')
            if state == 'true':
                degree = True
                return jsonify({'content':content['temp_c'], 'region':region, 'city':city}), 200
            else:
                degree = False
                return jsonify({'content':content['temp_f'], 'region':region, 'city':city}), 200
            
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "reason": "Not Json"}), 500

@app.route('/weather', methods=["POST"])
def fetch_weather():
    global content, region, city, last_location, degree
    try:
        if request.is_json:
            data = request.json
            location = data.get('City', last_location)
            degree = data.get('state', 'true') == 'true'
        else:
            location = request.form.get('City', last_location)

        if not location.strip():
            location = last_location

        content, region, city = getWeather(location)
        last_location = location

        return redirect('/')
    except Exception as e:
        # Handle errors and return fallback weather data
        return jsonify({"error": str(e), "content": content, "region": region, "city": city}), 500
        # return redirect('/')


@app.route('/autocomplete', methods=["GET"])
def autocomplete():
    query = request.args.get('query', '')
    geocoding_api_key = getenv('GEO_API_KEY')
    url = f"https://api.opencagedata.com/geocode/v1/json?q={query}&key={geocoding_api_key}&limit=5"
    
    response = requests.get(url).json()
    suggestions = [result.get('formatted') for result in response.get('results', [])]
    return jsonify(suggestions)


def main() -> None:
    app.run()


if __name__ == "__main__":
    main()