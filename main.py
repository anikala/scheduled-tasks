import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
MY_LAT = 48.732071
MY_LONG = -3.458700
appi_key = os.environ.get("OwV_APPI_KEY")
account_sid = os.environ.get("ACCOUNT_SID")
auth_token = os.environ.get("AUTH_TOKEN")
twilio_number = os.environ.get("TWILIO_NUM")
my_whats_up = os.environ.get("MY_WHATS_UP")

parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid": appi_key,
    "cnt": 4,
}

response = requests.get(OWM_Endpoint, params=parameters)
response.raise_for_status()
weather_data = response.json()
weather_id = weather_data["list"][0]["weather"][0]["id"]

weather_id_list = [weather_data["list"][i]["weather"][0]["id"] for i in range(4)]
will_rain = False
for code in weather_id_list:
    if code < 700:
        will_rain = True
if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)

    message = client.messages.create(
        from_=twilio_number,
        body="It's going to rain today. Remember to bring an umbrella",
        to=my_whats_up
    )
    print(message.status)
print(weather_id_list)

