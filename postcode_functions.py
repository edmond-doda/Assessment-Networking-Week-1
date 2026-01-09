"""Functions that interact with the Postcode API."""

import requests as req
import os
import json

CACHE_FILE = "./postcode_cache.json"

def load_cache() -> dict:
    """Loads the cache from a file and converts it from JSON to a dictionary."""
    # This function is used in Task 3, you can ignore it for now.
    ...


def save_cache(cache: dict):
    """Saves the cache to a file as JSON"""
    # This function is used in Task 3, you can ignore it for now.
    ...



def validate_postcode(postcode: str) -> bool:
    pass


def get_postcode_for_location(lat: float, long: float) -> str:
    pass


def get_postcode_completions(postcode_start: str) -> list[str]:
    pass


def get_postcodes_details(postcodes: list[str]) -> dict:
    pass
