from flask import Flask, render_template
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

""" API Request Info """

# Spotify
SPOTIPY_CLIENT_ID = "2bf475fed7634cbc937836b2336fbcfb"
SPOTIPY_CLIENT_SECRET = "229841e1ef574dbfb403b5fc2774005e"
SPOTIPY_REDIRECT_URI = "http://example.com"

SpotifyEndpointUrl = "https://api.spotify.com/v1/search"


# Create Spotipy instance for tracks search function.
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri=SPOTIPY_REDIRECT_URI))

# Open Weather
OpenWeatherMapsKey = "b77e07f479efe92156376a8b07640ced"
OpenWeatherUrl = "http://api.openweathermap.org/data/2.5/weather"

# Flask Server Setup
app = Flask(__name__)
app.config["DEBUG"] = True

"""
-> The Challenge
    Create a micro-service able to accept RESTful requests receiving as 
    parameter either city name or lat long coordinates and returns a playlist
     (only track names is fine) suggestion according to the current temperature.

-> Business rules
    If temperature (celcius) is above 30 degrees, suggest tracks for party
    
    In case temperature is between 15 and 30 degrees, suggest pop music tracks
    
    If it's a bit chilly (between 10 and 14 degrees), suggest rock music tracks
    
    Otherwise, if it's freezing outside, suggests classical music tracks
    
-> Hints
    You can make usage of OpenWeatherMaps API (https://openweathermap.org) to fetch 
    temperature data and Spotify (https://developer.spotify.com) to suggest the tracks
     as part of the playlist.

    API's:
    
    OpenWeatherMaps API (You can use this API Key: b77e07f479efe92156376a8b07640ced)
    Spotify API (You can use this Client Id: 08c1a6be652e4fdca07f1815bfd167e4)
    
    -> example query:
    http://api.openweathermap.org/data/2.5/weather?q=campinas&appid=b77e07f479efe92156376a8b07640ced
    -> example response:
    {
    "coord":{"lon":-47.0608,"lat":-22.9056},
    "weather":[{"id":800,"main":"Clear", "description":"clear sky","icon":"01d"}],
    "base":"stations",
    "main":{"temp":291.04,"feels_like":289.54,"temp_min":291.04,"temp_max":291.55,"pressure":1015,"humidity":25},
    "visibility":10000,
    "wind":{"speed":7.72,"deg":310},
    "clouds":{"all":0},
    "dt":1652815023,
    "sys":{"type":1,"id":8393,"country":"BR","sunrise":1652780101,"sunset":1652819669},
    "timezone":-10800,
    "id":3467865,
    "name":"Campinas",
    "cod":200
    }
    
    
    Project Strife's:
    
    * Fault tolerant, Responsive and Resilient.
    
    * Also, make it easy to deploy/run your service(s) locally 
    (consider using some container/vm solution for this). 
    Once done, share your code with us.

"""


# Route for Rest API Main Landing Page
@app.route("/")
def home():
    return render_template(template_name_or_list="index.html")


# Function to get the genre for the search in spotify.
def get_genre(temp_celsius):
    """
    Given a temperature in Celsius, returns the genre.
    """
    if temp_celsius > 30.0:
        return "party"
    elif 15 < temp_celsius < 30:
        return "pop"
    elif 15 > temp_celsius > 10:
        return "rock"
    else:
        return "classic"


# Routes for Request Given City or LAT/LNG Parameters

# City as a Request Param
@app.route("/playlist/c=<city>")
def playlist_by_city_climate(city):
    request_params = {
        "q": city,
        "appid": OpenWeatherMapsKey
    }
    weather_response = requests.get(url=OpenWeatherUrl, params=request_params)

    # TODO: Re-route to error page or api command info
    if weather_response.status_code != 200:
        return render_template(template_name_or_list="index.html")

    weather_content = weather_response.json()

    t_celsius = round(weather_content["main"]["temp"] - 273.15, 2)
    genre = get_genre(t_celsius)

    search_result = sp.search(q=f'genre: {genre}')
    song_list = []

    for item in search_result['tracks']['items']:
        if item['name'] not in song_list:
            song_list.append(item['name'])

    return render_template(template_name_or_list="playlist.html", temp=t_celsius, location=city.title(),
                           genre=genre.title(), songs=song_list)


# Latitude and Longitude as a Request Param
@app.route("/playlist/lat=<lat>&lon=<lon>")
def playlist_by_lat_lon_climate(lat, lon):
    request_params = {
        "lat": lat,
        "lon": lon,
        "appid": OpenWeatherMapsKey
    }
    weather_response = requests.get(url=OpenWeatherUrl, params=request_params)

    # TODO: Re-route to error page or api command info
    if weather_response.status_code != 200:
        return render_template(template_name_or_list="index.html")

    weather_content = weather_response.json()

    t_celsius = round(weather_content["main"]["temp"] - 273.15, 2)
    genre = get_genre(t_celsius)

    search_result = sp.search(q=f'genre: {genre}')
    song_list = []

    for item in search_result['tracks']['items']:
        if item['name'] not in song_list:
            song_list.append(item['name'])

    return render_template(template_name_or_list="playlist.html", temp=t_celsius, location=f'{lat}ºN {lon}ºL',
                           genre=genre.title(), songs=song_list)


if __name__ == "__main__":
    app.run()
