#!/usr/bin/env python3

""" JR's solar lab solution, cleaned up with 'black' and Pylint
    to conform to PEP8 specs."""

import datetime
import sys
import requests
from constants import constant1, constant2


def get_observer_location():

    """Returns the longitude and latitude for the location of this machine.
    Returns:
    str: latitude
    str: longitude"""
    url = "http://ip-api.com/json/"
    try:
        response = requests.get(url)
        if not response.status_code == 200:
            return None, None
    except requests.exceptions.ConnectionError:
        return None, None
    except requests.exceptions.Timeout:
        return None, None
    data = response.json()
    # NOTE: Replace with your real return values!
    return data.get("lat"), data.get("lon")


def get_sun_position(latitude, longitude, body="sun"):
    """Returns the current position of the sun in the sky at the specified location
    Parameters:
    latitude (str)
    longitude (str)
    Returns:
    float: azimuth
    float: altitude
    """
    body = body or "sun"
    url = f"https://api.astronomyapi.com/api/v2/bodies/positions/{body}"
    now = datetime.datetime.now()
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "elevation": 0,
        "from_date": now.date().isoformat(),
        "to_date": now.date().isoformat(),
        "time": now.strftime("%H:%M:%S"),
    }
    try:
        response = requests.get(
            url, auth=(constant1, constant2), params=params
        )
        if not response.status_code == 200:
            return None, None
    except requests.exceptions.ConnectionError:
        return None, None
    except requests.exceptions.Timeout:
        return None, None
    data = response.json()
    body_data = data["data"]["table"]["rows"][0]["cells"][0]
    position = body_data["position"]["horizontal"]
    alt = position["altitude"]["degrees"]
    az = position["azimuth"]["degrees"]
    return az, alt


def print_position(azimuth, altitude):
    """Prints the position of the sun in the sky using the supplied coordinates
    Parameters:
    azimuth (float)
    altitude (float)"""
    print(
        f"The Sun is currently at: " f"{altitude} deg altitude, {azimuth} deg azimuth."
    )


if __name__ == "__main__":
    latitude, longitude = get_observer_location()
    if latitude is None or longitude is None:
        print("Could not find your location by IP!")
        sys.exit(1)
    azimuth, altitude = get_sun_position(latitude, longitude)
    if azimuth is None or altitude is None:
        print("Could not get Sun position from Astronomy API")
        sys.exit(2)
    print_position(azimuth, altitude)
