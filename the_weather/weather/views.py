import requests
from django.shortcuts import render
from django.forms.utils import ErrorList
from .forms import CityForm
from .models import City


# Create your views here.
def index(request):
    
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
    api = 'Your Api Key from openweathermap'

    if request.method == 'POST':
        form = CityForm(request.POST)
        response = requests.get(url.format(request.POST.get('name'))).json()
        if len(response) > 2:
            form.save()
        else:
            form.add_error(None, "Can't find out such a city")

    form = CityForm()
    cities = City.objects.all()
    weather_data = []

    for city in cities:
        response = requests.get(url.format(city)).json()
        city_temperature = response['main']['temp']
        city_description = response['weather'][0]['description'][:1] + r['weather'][0]['description'][1:]
        city_icon = response['weather'][0]['icon']
        
        city_weather = {
            'city': city.name,
            'temperature': city_temperature,
            'description': city_description,
            'icon': city_icon,
        }

        weather_data.append(city_weather)

    context = {'weather_data': weather_data, 'form': form}
    return render(request, 'weather/weather.html', context)
