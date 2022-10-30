#!/bin/env python3

""" An application to output the position of the Sun in the sky at the current
    time, from a specific latitude and longitude.\

    Parameters:
    IP address (autodetected)
    Date / time (local system)
    Data gathered from https://astronomyapi.com/

    Returns:
    'As of <date> <time>, the Sun is at < X > degrees azimuth and < X > degrees altitude.'

    """

import datetime
import time
import json
import requests
from constants import constant1, constant2


def get_location():
    """Gathers the longitude and latitude for the location of an IP.
    Parameter:
    IP address

    Returns:
    float:  latitude
    float:  longitude

    Note:  The IP below in "target" is a local entry for accuracy.
    The URL format is based on the value required by the API.
    If this is run from a VM, it will return the location of the data center.
    """
    target = requests.get("http://ip-api.com/json/174.31.14.127?fields=lat,lon")
    target_data = json.loads(target.text)
    latitude = target_data["lat"]
    longitude = target_data["lon"]
    return latitude, longitude


get_location()


def time_params():

    """Gathers the date and time values required for position.

    Returns:
    str: today's date
    str: current time

    """

    cal_day = datetime.date.today().strftime("%Y-%m-%d")
    time_now = time.strftime("%H:%M:%S")

    return cal_day, time_now


time_params()


def get_sun_position():

    """Returns the current position of the Sun in the sky at
    the specified location.

    Parameters:
    latitude (str)
    longitude (str)
    elevation (str)
    Returns:
    float:  altitude
    float:  azimuth
    """

    loc_lat, loc_lon = get_location()
    cal_day, time_now = time_params()
    loc_elev = 526  # elevation in meters, work on elevation API in progress
    astronomy_api = "https://api.astronomyapi.com/api/v2/bodies/positions/sun"
    let_me_in = (constant1, constant2)
    values = {
        "latitude": loc_lat,
        "longitude": loc_lon,
        "elevation": loc_elev,
        "from_date": cal_day,
        "to_date": cal_day,
        "time": time_now,
    }
    response = requests.get(astronomy_api, auth=let_me_in, params=values)
    response_data = json.loads(response.content)
    position = response_data["data"]["table"]["rows"][0]["cells"][0]["position"][
        "horizontal"
    ]
    altitude = position["altitude"]["degrees"]
    azimuth = position["azimuth"]["degrees"]
    return azimuth, altitude


get_sun_position()


def print_position():

    """Prints the position of the sun in the sky using the supplied coordinates
    Parameters:
    azimuth (float)
    altitude (float)
    Returns:
    print statement
    """
    cal_day, time_now = time_params()
    azimuth, altitude = get_sun_position()
    return f"As of {cal_day} {time_now}, the Sun is at {azimuth} degrees azimuth and {altitude} degrees altitude."


print_position()

if __name__ == "__main__":
    ip_location = get_location()
    body_position = get_sun_position()
    output = print(print_position())
