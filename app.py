from flask import Flask, render_template
from dotenv import load_dotenv
import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

server_host = "http://127.0.0.1:5000"


# Configuration function for the app
def server_setup():
    # Configure environment variables
    load_dotenv()

    # Create Spotipy instance for tracks search function.
    return spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'),
                                                     client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                                                     redirect_uri=server_host))


# API Endpoints
OpenWeatherUrl = "http://api.openweathermap.org/data/2.5/weather"
SpotifyEndpointUrl = "https://api.spotify.com/v1/search"

# Flask Server Setup
app = Flask(__name__)
app.config["DEBUG"] = True


# Route for Rest API Main Landing Page
@app.route("/")
@app.route('/index.html')
def home():
    return render_template(template_name_or_list="index.html", error_message="")


# Function to get the genre for the search in spotify.
def get_genre(temp_celsius):
    """
    Given a temperature in Celsius, returns the genre.
    """
    if temp_celsius > 30.0:
        return "party"
    elif 15 < temp_celsius < 30:
        return "pop"
    elif 10 < temp_celsius < 15:
        return "rock"
    else:
        return "classical music"


# Routes for Request Given City or LAT/LNG Parameters

# City as a Request Param
@app.route("/playlist/c=<city>")
def playlist_by_city_climate(city):
    request_params = {
        "q": city,
        "appid": os.getenv('OpenWeatherMapsKey')
    }
    weather_response = requests.get(url=OpenWeatherUrl, params=request_params)

    # If the response fails, redirect the user to the main page
    # containing api request info

    if weather_response.status_code != 200:
        return render_template(template_name_or_list="index.html", error_message="City not Found!")

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
        "appid": os.getenv('OpenWeatherMapsKey')
    }
    weather_response = requests.get(url=OpenWeatherUrl, params=request_params)

    # If the response fails, redirect the user to the main page
    # containing api request info

    if weather_response.status_code != 200:
        return render_template(template_name_or_list="index.html", error_message="Coordinates not Found!")

    weather_content = weather_response.json()

    t_celsius = round(weather_content["main"]["temp"] - 273.15, 2)
    genre = get_genre(t_celsius)

    search_result = sp.search(q=f'genre: {genre}')
    song_list = []

    for item in search_result['tracks']['items']:
        if item['name'] not in song_list:
            song_list.append(item['name'])

    return render_template(template_name_or_list="playlist.html", temp=t_celsius, location=f'{lat}??N {lon}??L',
                           genre=genre.title(), songs=song_list)


if __name__ == "__main__":
    sp = server_setup()
    app.run()
