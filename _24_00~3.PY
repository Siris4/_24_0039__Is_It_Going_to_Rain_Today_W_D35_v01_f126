# environment variable master with named keys

# importing necessary libraries
import requests, os
from twilio.rest import Client
import smtplib

# set up environment variables and print their status
API_KEY = os.environ.get('API_KEY', 'API key not found')
print(f"The API_KEY is: {API_KEY}\n")

TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID', 'Twilio Account SID not found')
print(f"The TWILIO_ACCOUNT_SID is: {TWILIO_ACCOUNT_SID}\n")

TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN', 'Twilio Auth Token not found')
print(f"The TWILIO_AUTH_TOKEN is: {TWILIO_AUTH_TOKEN}\n")

SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'Sender email not found')
print(f"The SENDER_EMAIL is: {SENDER_EMAIL}\n")

SENDER_APP_PASSWORD = os.environ.get('SENDER_APP_PASSWORD', 'Sender app password not found')
print(f"The SENDER_APP_PASSWORD is: {SENDER_APP_PASSWORD}\n")

RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL', 'Receiver email not found')
print(f"The RECEIVER_EMAIL is: {RECEIVER_EMAIL}\n")

# ------------------ START OF WEATHER VARIABLE SETUP ------------------------ #
API_Weather_URL_Endpoint = "https://api.openweathermap.org/data/2.5/forecast"
lat = 31.332939  # lat for Lufkin, TX
lon = -94.727882  # lon for Lufkin, TX

weather_params = {
    "lat": lat,
    "lon": lon,
    "appid": API_KEY,
    "cnt": 4,
}

response = requests.get(url=API_Weather_URL_Endpoint, params=weather_params)
data = response.json()
print(f"The JSON data is: {data}")
print(f"The status code (response code - for calling this API) is: {data['cod']}")
response.raise_for_status()

# checking weather conditions
will_rain = False
for hour_data in data["list"]:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 600:
        will_rain = True

if will_rain:
    print("Bring an umbrella!")

    # email notification setup
    subject = "Subject: Your 12 Hour heads up of precipitation!!!\n\n"
    body = "It's going to rain within 12 hours here. Bring an umbrella!"

    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=SENDER_EMAIL, password=SENDER_APP_PASSWORD)
        connection.sendmail(
            from_addr=SENDER_EMAIL,
            to_addrs=RECEIVER_EMAIL,
            msg=f"{subject}{body}"
        )
