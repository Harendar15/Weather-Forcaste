from django.shortcuts import render
from django.contrib import messages
import requests
import datetime


def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'indore'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=bea54cf8d2d6384d1c060a5d9e60de0c'
    PARAMS = {'units': 'metric'}

    API_KEY = 'AIzaSyBG8ItY98ZMScsGPNe1dFAlTIktl'  # Add your API key here
    SEARCH_ENGINE_ID = '037ec29fbbee6417d'  # Add your search engine ID here

    query = city + " 1920x1080"
    page = 1
    start = (page - 1) * 10 + 1
    searchType = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&start={start}&searchType={searchType}&imgSize=xlarge"

    try:
        data = requests.get(city_url).json()
        search_items = data.get("items")
        image_url = "https://images.pexels.com/photos/3008509/pexels-photo-3008509.jpeg?auto=compress&cs=tinysrgb&w=1600%27"  # fallback image

        if search_items and len(search_items) > 1:
            image_url = search_items[1].get('link', image_url)

        # Get weather data
        weather_data = requests.get(url, params=PARAMS).json()
        description = weather_data['weather'][0]['description']
        icon = weather_data['weather'][0]['icon']
        temp = weather_data['main']['temp']
        day = datetime.date.today()

        return render(request, 'weatherapp/index.html', {
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'city': city,
            'exception_occurred': False,
            'image_url': image_url
        })

    except KeyError:
        error_msg = weather_data.get('message', 'City information is not available to Weather API')
        messages.error(request, f"Error: {error_msg}")

    # If an error occurs, provide default values
    day = datetime.date.today()
    return render(request, 'weatherapp/index.html', {
        'description': 'clear sky',
        'icon': '01d',
        'temp': 25,
        'day': day,
        'city': 'indore',
        'exception_occurred': True,
        'image_url': image_url
    })
