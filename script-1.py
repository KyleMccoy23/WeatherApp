from flask import Flask, jsonify, render_template, request, redirect
from httpx import get
import requests, PIL.Image, io

from os import getenv
from dotenv import load_dotenv
load_dotenv()
key = getenv('API_KEY')

app = Flask(__name__)

degree = True
last_location = 'toronto'

def getWeather(location: str) -> str:
    global degree, key
    query:str = f'http://api.weatherapi.com/v1/current.json?key={key}&q={location}&aqi=no'
    response = requests.get(query).json()
    if degree == True:
        temp = response.get('current').get('temp_c')
    else:
        temp = response.get('current').get('temp_f')
    region = response.get('location').get('region')
    city = response.get('location').get('name')
    getImage(response.get('current').get('condition').get('icon'))
    if degree == True:
        return f'{temp} °C', region, city
    else:
        return f'{temp} °F', region, city

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

@app.route('/', methods=["POST", "GET"])
def index():
    last_location_tmp=''
    global content, region, city, last_location, degree
    if request.method == "POST":
        try:
            if request.is_json:
                content = request.json['City']
                degree = request.json['state']
                if degree == 'true':
                    degree = True
                else:
                    degree = False
            else:
                content = request.form['City']
            if content == '':
                content = last_location
            last_location_tmp = content
            content, region, city = getWeather(content)
            last_location = last_location_tmp
            if request.is_json:
                return jsonify({"content": content, "region": region, "city": city})
            return redirect('/')
        except:
            if request.is_json:
                degree = request.json['state']
                if degree == 'true':
                    degree = True
                else:
                    degree = False
            content, region, city = getWeather(last_location)
            if request.is_json:
                return jsonify({"content": content, "region": region, "city": city})
            return redirect('/')
    return render_template('index.html', content=content, city=city, region=region)


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