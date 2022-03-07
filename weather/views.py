from django.shortcuts import render

from datetime import datetime
import json
import urllib.request

# Create your views here.
def index(request):
    if request.method == "POST":
        city = request.POST["city"]
        apiKey = "cb771e45ac79a4e8e2205c0ce66ff633"

        res = urllib.request.urlopen(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={apiKey}"
        ).read()
        json_data = json.loads(res)

        main_json_data = json_data["main"]
        data = {
            "country_code": f"{json_data['sys']['country']}",
            "coordinate": f"{json_data['coord']['lon']}, {json_data['coord']['lat']}",
            "celsiusTemp": f"{main_json_data['temp'] - 273.15:.1f} °C",
            "kelvinTemp": f"({main_json_data['temp']} K)",
            "feelsLikeCelsius": f"{main_json_data['feels_like'] - 273.15:.1f} °C",
            "feelsLikeKelvin": f"({main_json_data['feels_like']} K)",
            "pressure": f"{main_json_data['pressure']} hPa",
            "humidity": f"{main_json_data['humidity']} %",
            "visibility": f"{json_data['visibility']} m",
            "windSpeed": f"{json_data['wind']['speed']} mph",
            "sunrise": f"{datetime.fromtimestamp(json_data['sys']['sunrise'])}",
            "sunset": f"{datetime.fromtimestamp(json_data['sys']['sunset'])}",
            "description": f"{json_data['weather'][0]['description']}",
        }
    else:
        city = ""
        data = {}
    return render(request, "index.html", {"city": city, "data": data})
