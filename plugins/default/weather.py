import requests, json
import plugins.default.config as config
from core.command_factory import command_factory
from core.notification_factory import notification_factory

from datetime import datetime, timedelta
from pytz import timezone

def get_weather(city):
    base_url = "http://api.openweathermap.org/data/2.5/forecast?"
    complete_url = base_url + "q=" + city + "&appid=" + config.api_key

    response = requests.get(complete_url)
    response_json = response.json()

    # "404", means city is found otherwise, city is not found
    if int(response_json["cod"]) < 300:
        data_dict = response_json["list"][0]
        quant_data = data_dict["main"]

        k_to_c = 273.15

        current_temperature = int(quant_data["temp"]) - k_to_c
        feels_like = int(quant_data["feels_like"]) - k_to_c
        current_humidity = quant_data["humidity"]
        min = 999999999
        max = 0
        for i in range(0, 7):
            c_dict = response_json["list"][0]
            c_quant_data = c_dict["main"]
            c_min = int(c_quant_data["temp_min"]) - k_to_c
            c_max = int(c_quant_data["temp_max"]) - k_to_c
            max = c_max if c_max > max else max
            min = c_min if c_min < min else min

        qual_data = data_dict["weather"]
        weather_description = qual_data[0]["description"]

        sun_data = response_json["city"]
        sunrise = sun_data['sunrise']
        sunset = sun_data['sunset']
        t_sunrise = datetime.utcfromtimestamp(int(sunrise))
        t_sunset = datetime.utcfromtimestamp(int(sunset))
        tz = timezone(config.default_timezone)
        t_sunrise = tz.fromutc(t_sunrise).strftime("%I:%M %p")
        t_sunset = tz.fromutc(t_sunset).strftime("%I:%M %p")

        res_city = sun_data["name"]
        res_country = sun_data['country']

        rep_time = tz.fromutc(datetime.now()).strftime("%A %B %d, %Y\nGenerated %I:%M %p")

        title = ":sun: Weather Report :snowflake: \n" + res_city + ", " + res_country + "\n"
        def temp_format(t):
            return str("{:.1f}".format(t)) + "°C"

        body = (str(rep_time) + '\n\nCurrent Conditions:\n' + str(weather_description) +
               "\n\nCurrent Temp: " + temp_format(current_temperature) +
               "\n\nFeels Like: " + temp_format(feels_like) +
               "\nHumidity: " + str(current_humidity) +
               "\n12h Low: " + temp_format(min) + #add day hi/low
               "\n12h High: " + temp_format(max) +
               "\n\nSunrise: " + str(t_sunrise) +
               "\nSunset: " + str(t_sunset) +
               "\n\nUse !weather to get the current weather any time.")

        return title + body

    else:
        return "Unable to get weather for city '" + city + "'."

def get_weather_default():
    return get_weather(config.default_city)

@notification_factory(
    first_run=datetime(2021, 8, 4, hour=7, minute=0, second=1),
    delta=timedelta(hours=12),
    toggle_command='toggleweather'
)
def weather_notification():
    return get_weather_default()

@command_factory(help_desc="Get the current weather.")
def weather(msg):
    if msg.body == '':
        return get_weather_default()
    return get_weather(msg.body)
