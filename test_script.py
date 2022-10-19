"""Unit tests for solar.py Astronomy API client"""
from requests import exceptions
from unittest.mock import patch
import solar

def test_get_observer_location_success():
    """Test correct values are returned during a successful API call"""
    with patch('requests.get') as mock_get:
        expected = {
            "lat": 32.765,
            "lon": 45.123,
        }
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = expected
        lat, lon = solar.get_observer_location()
        mock_get.assert_called_with("http://ip-api.com/json/")
        assert lat == expected["lat"]
        assert lon == expected["lon"]

def test_get_observer_location_server_error():
    """Test error value is returned for a HTTP Server Error (500)"""
    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 500
        lat, lon = solar.get_observer_location()
        mock_get.assert_called_with("http://ip-api.com/json/")
        assert lat is None
        assert lon is None

def test_get_observer_location_connectionerror():
    """Test error value is returned for a ConnectionError exception"""
    with patch('requests.get') as mock_get:
        # Causes Mock requests.get to raise an exception
        # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect
        mock_get.side_effect = exceptions.ConnectionError
        lat, lon = solar.get_observer_location()
        mock_get.assert_called_with("http://ip-api.com/json/")
        assert lat is None
        assert lon is None

def test_get_observer_location_timeouterror():
    """Test error value is returned for a Timeout exception"""
    with patch('requests.get') as mock_get:
        # Causes Mock requests.get to raise an exception
        # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect
        mock_get.side_effect = exceptions.Timeout
        lat, lon = solar.get_observer_location()
        mock_get.assert_called_with("http://ip-api.com/json/")
        assert lat is None
        assert lon is None

def test_get_sun_position_success():
    """Test correct values are returned during a successful API call"""
    with patch('requests.get') as mock_get:
        # Mimic the structure of the response, but only worry about the pieces
        # we actually access in our function under test.
        expected = {
            "data": {
                "table": {
                    "rows": [{
                        "cells": [{
                            "position": {
                                "horizontal": {
                                    "altitude": {
                                        "degrees": 45.123,
                                    },
                                    "azimuth": {
                                        "degrees": 32.125,
                                    },
                                },
                            },
                        }],
                    }],
                },
            },
        }
        expected_position = expected["data"]["table"]["rows"][0]["cells"][0]["position"]
        expected_az = expected_position["horizontal"]["azimuth"]["degrees"]
        expected_alt = expected_position["horizontal"]["altitude"]["degrees"]
        mock_response = mock_get.return_value
        mock_response.status_code = 200
        mock_response.json.return_value = expected
        az, alt = solar.get_sun_position(123, 456)
        assert az == expected_az
        assert alt == expected_alt

def test_get_sun_position_server_error():
    """Test error value is returned for a HTTP Server Error (500)"""
    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.status_code = 500
        az, alt = solar.get_sun_position(123, 456)
        assert az is None
        assert alt is None

def test_get_sun_position_connectionerror():
    """Test error value is returned for a ConnectionError exception"""
    with patch('requests.get') as mock_get:
        # Causes Mock requests.get to raise an exception
        # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect
        mock_get.side_effect = exceptions.ConnectionError
        az, alt = solar.get_sun_position(123, 456)
        assert az is None
        assert alt is None

def test_get_sun_position_timeout():
    """Test error value is returned for a Timeout exception"""
    with patch('requests.get') as mock_get:
        # Causes Mock requests.get to raise an exception
        # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.Mock.side_effect
        mock_get.side_effect = exceptions.Timeout
        az, alt = solar.get_sun_position(123, 456)
        assert az is None
        assert alt is None