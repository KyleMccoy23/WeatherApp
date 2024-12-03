from flask_session import Session
from flask import Flask, jsonify, render_template, request, redirect
import requests, PIL.Image, io

from flask import session

from os import getenv
from dotenv import load_dotenv
load_dotenv()
key = getenv('API_KEY')

app = Flask(__name__)

SK = getenv('SK')
app.secret_key = SK
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

degree = True
last_location = 'toronto'

def getWeather(location: str):
    global degree, key
    query = f'http://api.weatherapi.com/v1/current.json?key={key}&q={location}&aqi=no'
    response = requests.get(query).json()

    # if response.get('error'):
    #     raise Exception(response['error'].get('message', 'Unknown error'))

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

@app.route('/initialize-session', methods=["POST"])
def initialize_session():
    tab_id = request.get_json().get("tabId")

    if not tab_id:
        return jsonify({"error": "Tab ID missing"}), 400

    if "sessions" not in session:
        session["sessions"] = {}  # Initialize a dictionary for tab-specific sessions

    if tab_id not in session["sessions"]:
        session["sessions"][tab_id] = {
            "degree": 'true',  # Default to Celsius
            "last_location": "Toronto",  # Default location
            "data": {'content':content, 'region':region, 'city':city},
        }
    return jsonify({"success": True, 'tabId': tab_id}), 200

@app.route('/', methods=['POST', 'GET'])
def index():
    global content, region, city
    if degree:
        return render_template('index.html', content=content['temp_c'], city=city, region=region)
    else:
        return render_template('index.html', content=content['temp_f'], city=city, region=region)
    
@app.route('/toggle-unit', methods=["POST"])
def toggle_unit():
    data = request.get_json()
    tab_id = request.headers.get("tabId")

    if tab_id not in session["sessions"].keys():
        return jsonify({"error": "Invalid session"}), 400

    tab_session = session["sessions"][tab_id]
    state = data.get("state")
    tab_session["degree"] = state
    if state == 'true':
        return jsonify({"success": True, 'content':tab_session["data"]['content']['temp_c'], 'region':tab_session["data"]['region'], 'city':tab_session["data"]['city']})
    else:
        return jsonify({"success": True, 'content':tab_session["data"]['content']['temp_f'], 'region':tab_session["data"]['region'], 'city':tab_session["data"]['city']})

@app.route('/weather', methods=["GET"])
def fetch_weather():
    data = request.get_json()
    tab_id = request.headers.get("Tab-Id")

    if not tab_id or "sessions" not in session or tab_id not in session["sessions"]:
        return jsonify({"error": "Invalid session"}), 400

    tab_session = session["sessions"][tab_id]
    location = data.get("City", tab_session["last_location"])
    tab_session["last_location"] = location

    # Example weather data (replace with actual API call)
    content = f"Weather in {location}: 20°C"
    tab_session["content"] = content  # Save content in session

    return jsonify({"content": content, "tab_id": tab_id})

@app.route('/debug-session', methods=["GET"])
def debug_session():
    return jsonify({"sessions": session.get("sessions", {})})


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