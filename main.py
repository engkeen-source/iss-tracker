from datetime import datetime
import requests
import smtplib
import time

# API Endpoint
API_ENDPOINT = 'https://api.sunrise-sunset.org/json'

# Singapore
MY_LAT = 1.352083
MY_LONG = 103.819839

# Email
MY_EMAIL = "pythontest684@gmail.com"
MY_PASSWORD = 'xxx'


def is_iss_overhead():
    # Get current sunset and sunrise position
    iss_response = requests.get(url=API_ENDPOINT)
    iss_response.raise_for_status()
    iss_data = iss_response.json()

    iss_latitude = float(iss_data['iss_position']['latitude'])
    iss_longitude = float(iss_data['iss_position']['longitude'])

    return MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5


def is_night():
    parameters = {
        'lat': MY_LAT,
        'lng': MY_LONG,
        'formatted': 1
    }

    response = requests.get(url=API_ENDPOINT, params=parameters)
    response.raise_for_status()

    # All times are in UTC and summer adjustments are not included in the returned data.
    data = response.json()
    sunrise = data['results']['sunrise']  # example 2023-09-26T22:51:37+00:00
    sunset = data['results']['sunset']

    sunrise_hour = sunrise.split('T')[1].split(':')[0]
    sunset_hour = sunset.split('T')[1].split(':')[0]

    time_now = datetime.now()

    return time_now >= sunset_hour or time_now <= sunrise_hour


while True:
    time.sleep(60)
    if is_iss_overhead() and is_night():
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=f"Subject:Look Up\n\nISS is above you in the sky."
            )

