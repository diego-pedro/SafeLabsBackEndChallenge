from flask import Flask
import requests

# API Request Info
SpotifyAPIClientId = "08c1a6be652e4fdca07f1815bfd167e4"
OpenWeatherMapsKey = "b77e07f479efe92156376a8b07640ced"


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

# TODO 1: Route for Rest API Main Landing Page
# TODO 2: Route for Request Given City or LAT/LNG Parameters
# TODO 3: Use Returned Weather (Temperature converted to Celsius) Response to Identify Song Genre
# View the conditions above
# TODO 4: Send Request to Spotify and Return List of Track Names in that Genre
