from django.shortcuts import render
from django.template import RequestContext

from datetime import datetime
import json
import urllib.request

# Create your views here.
def index(request):
    if request.method == "POST":
        city = request.POST["city"]
        apiKey = "f4d6a7640f463a5c53d68ba6d2e41448"

        res = urllib.request.urlopen(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&APPID={apiKey}"
        ).read()
        json_data = json.loads(res)
        cod = str(json_data["cod"])

        if cod == "200":
            main_json_data = json_data["main"]
            data = {
                "country_code": f"{json_data['sys']['country']}",
                "coordinate": f"{json_data['coord']['lon']}, {json_data['coord']['lat']}",
                "celsiusTemp": f"{main_json_data['temp'] - 273.15:.1f} °C",
                "kelvinTemp": f"({main_json_data['temp']} K)",
                "feelsLikeCelsius": f"{main_json_data['feels_like'] - 273.15:.1f} °C",
                "feelsLikeKelvin": f"({main_json_data['feels_like']} K)",
                "pressure": f"{main_json_data['pressure']} hPa",
                "humidity": f"{main_json_data['humidity']}%",
                "visibility": f"{json_data['visibility']} m",
                "windSpeed": f"{json_data['wind']['speed']} mph",
                "sunrise": f"{datetime.fromtimestamp(json_data['sys']['sunrise'])}",
                "sunset": f"{datetime.fromtimestamp(json_data['sys']['sunset'])}",
                "description": f"{json_data['weather'][0]['main']}",
                "cityName": json_data["name"],
                "cod": cod,
            }
        elif cod == "404":
            data = {"cityName": json_data["cityName"], "cod": cod}
    else:
        city = ""
        data = {}
    return render(request, "index.html", {"city": city, "data": data})


def handler404(request, exception, template_name="404.html"):
    response = render(None, template_name)
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(None, "500.html")
    response.status_code = 500
    return response
