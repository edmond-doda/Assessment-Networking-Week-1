"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"
URL = 'https://api.postcodes.io/postcodes'


def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary.
    Creates empty dictionary if file doesn't exist"""
    try:
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)
            return cache
    except Exception:
        return {}


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    with open(CACHE_FILE, 'w') as f:
        json.dump(cache, f, indent=2)


def validate_postcode(postcode: str) -> bool:
    """Validates whether a postcode exists, and returns True if it does."""
    validates_string(postcode)
    formatted_postcode = postcode.upper().strip()

    cache = load_cache()
    if formatted_postcode in cache and "valid" in cache[formatted_postcode]:
        return cache[formatted_postcode]["valid"]

    response = req.get(f'{URL}/{formatted_postcode}/validate')
    status_code_exceptions(response.status_code)
    data = response.json()

    cache[formatted_postcode] = {
        'valid': data['result'],
        'completions': formatted_postcode
    }
    save_cache(cache)

    return data['result']


def get_postcode_for_location(lat: float, long: float) -> str:
    """Returns the postcode given the longitude and latitude values"""
    validates_float(lat)
    validates_float(long)
    response = req.get(f'{URL}?lon={long}&lat={lat}')
    status_code_exceptions(response.status_code)

    data = response.json()

    if data['result'] is None:
        raise ValueError('No relevant postcode found.')

    postcode = data['result'][0]['postcode']
    return postcode


def get_postcode_completions(postcode_start: str) -> list[str]:
    """Returns a list of all the possible postcodes using the start of some postcode"""
    validates_string(postcode_start)
    formatted_postcode_start = postcode_start.upper().strip()

    cache = load_cache()
    if formatted_postcode_start in cache:
        return cache[formatted_postcode_start]['completions']

    response = req.get(
        f'{URL}/{formatted_postcode_start}/autocomplete?limit=5')
    status_code_exceptions(response.status_code)
    postcodes = response.json()['result']

    cache[formatted_postcode_start] = {
        'valid': False,
        'completions': postcodes
    }
    save_cache(cache)

    return postcodes


# was -> dict but test looks for values with indexes so must be -> list
def get_postcodes_details(postcodes: list[str]) -> list:
    """Returns detailed information for multiple postcodes using a bulk lookup."""
    validates_list_of_strings(postcodes)

    response = req.post(f'{URL}', json={"postcodes": postcodes})
    status_code_exceptions(response.status_code)
    data = response.json()
    return data['result']


def validates_string(text: str) -> str:
    if not type(text) == str:
        raise TypeError('Function expects a string.')
    return text


def validates_float(number: float) -> float:
    if not type(number) == float:
        raise TypeError('Function expects two floats.')
    return number


def status_code_exceptions(status_code: int) -> None:
    if status_code >= 500:
        raise req.RequestException('Unable to access API.')


def validates_list_of_strings(list_of_strings: list[str]) -> None:
    if not isinstance(list_of_strings, list):
        raise TypeError('Function expects a list of strings.')

    for item in list_of_strings:
        if not isinstance(item, str):
            raise TypeError('Function expects a list of strings.')


if __name__ == '__main__':
    print(validate_postcode('rm6 5et'))
    print(get_postcode_for_location(51.562533, 0.130226))
